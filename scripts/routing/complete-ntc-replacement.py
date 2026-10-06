"""Complete a coherent USB proposal by routing its displaced NTC connection.

Try the actual native pad escapes and plated terminal on eligible layers. Keep
the original cache and input native JSON immutable; never accept a partial net.
"""
import argparse,json,runpy
from pathlib import Path
from shapely.geometry import Point,LineString,Polygon
b=runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')));h=b['helpers']


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('native');ap.add_argument('proposal');ap.add_argument('output');ap.add_argument('--reserve-proposals',action='append',default=[]);args=ap.parse_args()
    c=json.loads(Path(args.native).read_text());plan=json.loads(Path(args.proposal).read_text());extra=[json.loads(Path(f).read_text()) for f in args.reserve_proposals]
    if not plan['unresolved'] or any(r['net']!='PACK_NTC' for r in plan['unresolved']):raise ValueError('Only the single remaining NTC net may be completed here')
    manual=json.loads(Path('src/board/manual-signal-paths.json').read_text())['paths'];sources={r['source_trace_id']:r for r in c if r['type']=='source_trace'}
    names={f"MANUAL_{manual[i]['net']}_{i}" for d in extra for i in d.get('retired_manual_path_indices',[])}
    retired={r['pcb_trace_id']:{layer:None for layer in ('top','inner1','inner2','bottom')} for r in c if r['type']=='pcb_trace' and sources[r['source_trace_id']].get('name') in names}
    for r in plan['retired_replay_connections']:retired[r['original_pcb_trace_id']]={layer:None for layer in ('top','inner1','inner2','bottom')}
    p=h['Planner'](c,{'relocated_trace_layers':retired,'retired_feature_ids':set(plan['retired_native_vias'])});p.set_grid(.05);p.set_copper_reserve(.0001);p.via_copper_clearance=.27
    nets={r['name']:r for r in c if r['type']=='source_net'};net=nets['PACK_NTC'];root=p.root(net['source_net_id']);ports={p.port_name(q):q for q in p.ports.values() if p.source_ports[q['source_port_id']].get('source_component_id') in p.source_components}
    result={**plan,'paths':[r for r in plan['paths'] if r['net']!='PACK_NTC'],'unresolved':[],'ntc_completion_input':args.proposal};base_plans=[result,*extra]
    for d in base_plans:
        p.reserve_proposals(d)
        for r in d['pours']:p.copper.append((p.root(nets[r['net']]['source_net_id']),r['layer'],Polygon([(q['x'],q['y']) for q in r['outline']])))
    base=list(p.copper),list(p.holes),dict(p.plated_hole_roots)
    trace=next(r for r in c if r.get('pcb_trace_id')=='saved_phase_null_21_0');indices=[i for i,q in enumerate(trace['route']) if q['route_type']=='via'];original=[]
    if len(indices)!=2:raise ValueError('Original NTC phase must contain two real top escapes')
    for port_id,points in [(trace['route'][0]['start_pcb_port_id'],trace['route'][:indices[0]+1]),(trace['route'][-1]['end_pcb_port_id'],list(reversed(trace['route'][indices[-1]:])))]:
        positions=[]
        for q in points:
            xy=(q['x'],q['y'])
            if not positions or xy!=positions[-1]:positions.append(xy)
        original.append({'selector':p.port_name(p.ports[port_id]),'positions':positions})
    source_chip=next(r for r in plan['paths'] if r['net']=='PACK_NTC' and r['from']=='.U16 > .pin1')
    variants=[('new-chip-to-plated-terminal',[{'selector':source_chip['from'],'positions':source_chip['global_path_mm']}],(22.,25.)),('original-chip-to-plated-terminal',[original[0]],(22.,25.)),('original-pad-escapes',original,None)]
    failures=[]
    for name,escapes,target in variants:
      for layers in [('bottom','inner1'),('bottom','inner2'),('inner1','inner2')]:
        p.copper,p.holes,p.plated_hole_roots=list(base[0]),list(base[1]),dict(base[2]);paths=[];endpoints=[];legal=True
        for r in escapes:
            points=r['positions'];position=points[-1]
            if Point(position).intersects(h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3})) or LineString(points).intersects(p.obstacles(root,'top',.2)):legal=False;break
            paths.append(h['escape_record'](p,{'root':root,'net':net,'port':ports[r['selector']],'width':.2,'positions':points,'via_outer_mm':.45,'via_hole_mm':.3}));endpoints.append(position)
        if not legal:failures.append({'variant':name,'layers':layers,'reason':'Retained escape conflicts with repaired copper'});continue
        if target is not None:
            port=ports['.J3 > .pin2']
            if (port['x'],port['y'])!=target or not any(r['type']=='pcb_plated_hole' and r.get('pcb_port_id')==port['pcb_port_id'] and {'top','inner1','inner2','bottom'}<=set(r['layers']) for r in c):raise ValueError('Expected genuine numbered plated NTC terminal')
            endpoints.append(target)
        route=h['wide_multilayer_route'](p,{'root':root,'first':endpoints[0],'last':endpoints[1],'width':.202,'new_vias':endpoints,'layers':layers,'via_outer_mm':.45,'via_hole_mm':.3,'copper_clearance_mm':.27,'multi_anchor':True})
        print(json.dumps({'ntc_variant':name,'layers':layers,'routed':bool(route)}),flush=True)
        if not route:failures.append({'variant':name,'layers':layers,'reason':'No complete physical corridor'});continue
        parts,vias=route;result['paths'].extend(paths);result['pours'].extend(b['region_records']('PACK_NTC',{'parts':parts,'width':.2}));result['vias'].extend({'net':'PACK_NTC','x':xy[0],'y':xy[1],'hole_mm':.3,'outer_mm':.45} for xy in vias);result['ntc_variant']=name;result['failed_ntc_candidates']=failures
        result['retired_authored_regions']=[identifier for identifier in result['retired_native_vias'] if identifier.startswith('pcb_copper_pour_')]
        result['retired_native_vias']=[identifier for identifier in result['retired_native_vias'] if identifier.startswith('pcb_via_')]
        Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'complete':True,'variant':name,'layers':layers}));return 0
    result['unresolved']=[{'net':'PACK_NTC','reason':'All recorded complete-route candidates failed','candidates':failures}];Path(args.output).write_text(json.dumps(result,indent=2)+'\n');return 1


if __name__=='__main__':raise SystemExit(main())
