"""Reserve both verified amplifier escapes before routing outer speaker trunks.

Authored native geometry only. Every proposed neck remains explicitly measured
and requires native continuity, clearance and current/stackup qualification.
"""
import argparse,json,math,runpy
from pathlib import Path
from shapely.geometry import LineString,Point,Polygon
outer=runpy.run_path(str(Path(__file__).with_name('plan-outer-connections.py')))
b=outer['bridges'];h=outer['helpers']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('native');parser.add_argument('output')
    parser.add_argument('--reserve-proposals',action='append',default=[])
    parser.add_argument('--prefer-layer',choices=('top','bottom'),default='bottom')
    parser.add_argument('--via-reserve-mm',type=float,choices=(.21,.27),default=.27,help='Planning reserve only; actual native clearance and every retained strip width must still pass')
    parser.add_argument('--neck-width-mm',type=float,choices=(.2,.275),default=.275,help='Explicit minimum-width escape sections, still bounded to5mm total and requiring load qualification')
    parser.add_argument('--nominal-trunk-mm',type=float,choices=(.3,.6),default=.6,help='Measured layout candidate width; manufacturer/load qualification remains required')
    parser.add_argument('--output-order',choices=('positive-first','negative-first'),default='positive-first')
    parser.add_argument('--replace-existing-speakers',action='store_true',help='Replace actual authored speaker traces/regions/vias, retaining the numbered pads and immutable old native input')
    args=parser.parse_args();c=json.loads(Path(args.native).read_text());plans=[json.loads(Path(f).read_text()) for f in args.reserve_proposals]
    manual=json.loads(Path('src/board/manual-signal-paths.json').read_text())['paths'];sources={r['source_trace_id']:r for r in c if r['type']=='source_trace'}
    names={f"MANUAL_{manual[i]['net']}_{i}" for d in plans for i in d.get('retired_manual_path_indices',[])}
    retired={r['pcb_trace_id']:{layer:None for layer in ('top','bottom','inner1','inner2')} for r in c if r['type']=='pcb_trace' and sources[r['source_trace_id']].get('name') in names}
    if len(retired)!=len(names):raise ValueError('Every retirement must identify actual native copper')
    for d in plans:
        for r in d.get('retired_replay_connections',[]):retired[r['original_pcb_trace_id']]={layer:None for layer in ('top','bottom','inner1','inner2')}
    vias={v for d in plans for key in ('retired_native_vias','retired_authored_vias','retired_authored_regions') for v in d.get(key,[])}
    if args.replace_existing_speakers:
        probe=h['Planner'](c)
        roots={probe.root(r['source_net_id']) for r in c if r['type']=='source_net' and r['name'] in ('SPEAKER_P','SPEAKER_N')}
        for record in c:
            if record['type']=='pcb_trace':
                source=sources[record['source_trace_id']]
                terminals=source.get('connected_source_port_ids',[])+source.get('connected_source_net_ids',[])
                if terminals and probe.root(terminals[0]) in roots:
                    retired[record['pcb_trace_id']]={layer:None for layer in ('top','bottom','inner1','inner2')}
            elif record['type']=='pcb_via' and probe.via_root(record) in roots:vias.add(record['pcb_via_id'])
            elif record['type']=='pcb_copper_pour' and probe.root(record['source_net_id']) in roots:vias.add(record['pcb_copper_pour_id'])
        del probe
    p=h['Planner'](c,{'relocated_trace_layers':retired,'retired_feature_ids':vias});p.set_grid(.05);p.via_copper_clearance=args.via_reserve_mm
    nets={r['name']:r for r in c if r['type']=='source_net'}
    for d in plans:
        p.reserve_proposals(d)
        for region in d.get('pours',[]):p.copper.append((p.root(nets[region['net']]['source_net_id']),region['layer'],Polygon([(q['x'],q['y']) for q in region['outline']])))
    result={'classification':'authored simultaneous speaker escapes and outer trunks; native/load qualification required','paths':[],'pours':[],'vias':[],'pad_necks':[],'unresolved':[],'candidate_trunk_width_mm':args.nominal_trunk_mm,'candidate_neck_width_mm':args.neck_width_mm,'planning_via_reserve_mm':args.via_reserve_mm,'existing_net_nominal_width_mm':.6,'width_qualification':'Planning does not change the existing .6mm nominal requirement or grant manufacturing/current approval; every retained native strip width must pass'}
    escapes=[]
    for name,selector,delta in [('SPEAKER_P','.U3 > .pin9',(.4,.69282)),('SPEAKER_N','.U3 > .pin10',(0,.8))]:
        port=next(r for r in p.ports.values() if p.port_name(r)==selector);origin=(port['x'],port['y']);xy=(round(origin[0]+delta[0],6),round(origin[1]+delta[1],6));net=nets[name];root=p.root(net['source_net_id'])
        if LineString([origin,xy]).intersects(p.obstacles(root,'top',args.neck_width_mm)) or Point(xy).intersects(h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3})):
            raise ValueError(f'Paired escape fails geometric requirements: {selector}')
        path=h['escape_record'](p,{'root':root,'net':net,'port':port,'positions':[origin,xy],'width':args.neck_width_mm,'via_outer_mm':.45,'via_hole_mm':.3});result['paths'].append(path);escapes.append((name,selector,xy,path['top_length_mm']))
    for name,selector,start,escape_length in (list(reversed(escapes)) if args.output_order=='negative-first' else escapes):
        root=p.root(nets[name]['source_net_id']);end_selector='.J4 > .pin1' if name=='SPEAKER_P' else '.J4 > .pin2';port=next(r for r in p.ports.values() if p.port_name(r)==end_selector);target=(port['x'],port['y'])
        route=h['wide_multilayer_route'](p,{'root':root,'first':start,'last':target,'width':args.neck_width_mm+.002,'preferred_width_mm':args.nominal_trunk_mm+.002,'new_vias':[start,target],'layers':(args.prefer_layer,'top' if args.prefer_layer=='bottom' else 'bottom'),'via_outer_mm':.45,'via_hole_mm':.3,'copper_clearance_mm':.27,'multi_anchor':True})
        if not route:result['unresolved'].append({'net':name,'reason':'No complete outer trunk after reserving both escapes'});continue
        parts,new_vias=route;regions,narrow=outer['adaptive_regions'](p,{'root':root,'net':name,'parts':parts,'nominal_width':args.nominal_trunk_mm,'neck_width':args.neck_width_mm,'new_vias':[start,target]+new_vias})
        if narrow+escape_length>5:result['unresolved'].append({'net':name,'reason':'Narrow sections exceed authoring limit','total_narrow_length_mm':narrow+escape_length});continue
        result['pours'].extend(regions)
        for region in regions:p.copper.append((root,region['layer'],Polygon([(q['x'],q['y']) for q in region['outline']])))
        for xy in new_vias:b['reserve_via'](p,{'root':root,'position':xy});result['vias'].append({'net':name,'x':xy[0],'y':xy[1],'hole_mm':.3,'outer_mm':.45})
        result['pad_necks'].append({'net':name,'terminal':selector,'width_mm':args.neck_width_mm,'length_mm':escape_length,'outer_distribution_neck_length_mm':narrow,'total_narrow_length_mm':narrow+escape_length,'nominal_trunk_width_mm':args.nominal_trunk_mm,'layer':'top','status':'Measured proposal; current/stackup qualification pending'})
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'complete':not result['unresolved'],'regions':len(result['pours']),'unresolved':result['unresolved']}))
    return 1 if result['unresolved'] else 0

if __name__=='__main__':raise SystemExit(main())
