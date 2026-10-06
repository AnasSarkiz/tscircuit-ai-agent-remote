"""Reserve genuine USB pad exits before replacing interfering control routes.

Replace complete charger-current/NTC replay phases and two authored .3 mm
regions. Keep all original numbered terminals, footprints and source widths.
No deferred J3 outer or J7 contact is assigned. Native qualification required.
"""
import argparse,json,math,runpy
from pathlib import Path
from shapely.geometry import Point,LineString,Polygon
from shapely.ops import substring
b=runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')));h=b['helpers']


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('native');ap.add_argument('output');ap.add_argument('--reserve-proposals',action='append',default=[]);ap.add_argument('--retain-ntc-escapes',action='store_true');args=ap.parse_args()
    c=json.loads(Path(args.native).read_text());nets={r['name']:r for r in c if r['type']=='source_net'};probe=h['Planner'](c)
    caches=[(3,'CHARGER_ILIM','routes/a5/charger-current-limit.json'),(21,'PACK_NTC','routes/a7/charger-ntc.json')]
    retired={};features=set();replay=[];terminal_pairs=[];retained_ntc_escapes=[]
    for phase,net,file in caches:
        cache=json.loads(Path(file).read_text())
        if len(cache)!=1:raise ValueError('Only complete verified single-connection phases can be retired')
        trace=next(r for r in c if r.get('pcb_trace_id')==f'saved_phase_null_{phase}_0')
        if any(r['route_type']=='wire' and r['width']!=.2 for r in trace['route']):raise ValueError('Unexpected old control width')
        retired[trace['pcb_trace_id']]={layer:None for layer in ('top','inner1','inner2','bottom')};features.update(r['pcb_via_id'] for r in c if r['type']=='pcb_via' and r.get('pcb_trace_id')==trace['pcb_trace_id'])
        terminal_pairs.append((net,probe.port_name(probe.ports[trace['route'][0]['start_pcb_port_id']]),probe.port_name(probe.ports[trace['route'][-1]['end_pcb_port_id']]),.2))
        replay.append({'phase_index':phase,'connection':cache[0]['connection'],'original_pcb_trace_id':trace['pcb_trace_id']})
        if net=='PACK_NTC':
            via_indices=[i for i,q in enumerate(trace['route']) if q['route_type']=='via']
            if len(via_indices)!=2:raise ValueError('Expected two real NTC pad escapes')
            for port_id,points in [(trace['route'][0]['start_pcb_port_id'],trace['route'][:via_indices[0]+1]),(trace['route'][-1]['end_pcb_port_id'],list(reversed(trace['route'][via_indices[-1]:])))]:
                if any(q['route_type']=='wire' and q['layer']!='top' for q in points):raise ValueError('Retained NTC escape must be top copper')
                positions=[]
                for q in points:
                    xy=(q['x'],q['y'])
                    if not positions or xy!=positions[-1]:positions.append(xy)
                retained_ntc_escapes.append((probe.port_name(probe.ports[port_id]),positions))
    power=json.loads(Path('src/board/manual-power-copper.json').read_text())['pours'];region_replacements=[]
    for index,net in [(101,'MCU_MIC_WS'),(118,'VMIC')]:
        source=power[index]
        if source['net']!=net or source['nominal_width_mm']!=.3:raise ValueError('Unexpected authored control region')
        shape=Polygon([(q['x'],q['y']) for q in source['outline']]);matches=[]
        for r in c:
            if r['type']=='pcb_copper_pour' and r['source_net_id']==nets[net]['source_net_id'] and r['layer']==source['layer']:
                brep=r['brep_shape'];actual=Polygon([(q['x'],q['y']) for q in brep['outer_ring']['vertices']], [[(q['x'],q['y']) for q in ring['vertices']] for ring in brep['inner_rings']]);matches.append((shape.intersection(actual).area,r['pcb_copper_pour_id']))
        area,identifier=max(matches)
        if area<shape.area*.8:raise ValueError('Cannot identify complete real region for replacement')
        features.add(identifier);region_replacements.append({'source':'src/board/manual-power-copper.json','index':index,'net':net,'native_feature_id':identifier,'original_nominal_width_mm':.3,'first':source['path_mm'][0],'last':source['path_mm'][-1]})
    del probe
    p=h['Planner'](c,{'relocated_trace_layers':retired,'retired_feature_ids':features});p.set_grid(.05);p.set_copper_reserve(.0001);p.via_copper_clearance=.27
    ports={p.port_name(q):q for q in p.ports.values() if p.source_ports[q['source_port_id']].get('source_component_id') in p.source_components}
    for file in args.reserve_proposals:
        plan=json.loads(Path(file).read_text());p.reserve_proposals(plan)
        for r in plan['pours']:p.copper.append((p.root(nets[r['net']]['source_net_id']),r['layer'],Polygon([(q['x'],q['y']) for q in r['outline']])))
    result={'classification':'authored USB repair and complete interfering-control replacement; fresh native qualification required','paths':[],'pours':[],'vias':[],'unresolved':[],'retired_replay_connections':replay,'retired_native_vias':sorted(features),'retired_authored_source_regions':region_replacements,'source_native':args.native}
    # Preserve most of the existing .3 mm clock strip as an obstacle. Only its
    # short USB-via neighbourhood changes, so the new USB trunk cannot occupy
    # the clock's already connected long corridor.
    ws=next(r for r in region_replacements if r['net']=='MCU_MIC_WS');line=LineString(power[ws['index']]['path_mm']);distance=line.project(Point(.25,-27));before=max(0,distance-2);after=min(line.length,distance+2)
    retained=[list(substring(line,0,before).coords),list(substring(line,after,line.length).coords)]
    ws['replacement_first']=retained[0][-1];ws['replacement_last']=retained[1][0]
    for points in retained:
        regions=b['region_records']('MCU_MIC_WS',{'parts':[('inner1',points)],'width':.3});result['pours'].extend(regions)
        for r in regions:p.copper.append((p.root(nets['MCU_MIC_WS']['source_net_id']),'inner1',Polygon([(q['x'],q['y']) for q in r['outline']])))
    def escape(net,selector,width,position=None,targets=()):
        root=p.root(nets[net]['source_net_id']);port=ports[selector];origin=(port['x'],port['y'])
        # A genuine plated connector terminal already reaches every layer.
        # Join its annulus directly rather than searching for another ordinary
        # via beside the large pad. Verify the native plated-hole record.
        if position is None and any(q['type']=='pcb_plated_hole' and q.get('pcb_port_id')==port['pcb_port_id'] and {'top','inner1','inner2','bottom'}<=set(q['layers']) for q in c):return origin
        if position is None:
            layers=('inner2','bottom') if net=='USB_DN' else ('inner2','inner1')
            found=h['pad_escape'](p,{'root':root,'net':nets[net],'origin':origin,'width':width,'new_vias':list(targets),'via_outer_mm':.45,'via_hole_mm':.3,'distribution_layers':layers,'distribution_width_mm':width+.002,'copper_clearance_mm':.27,'connected_targets':list(targets)})
            if not found:return None
            position,points=found
        else:
            if Point(position).intersects(h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3})):return None
            p.set_grid(.01,(-2.5,-28.5,1.5,-22));points=p.grid_route((origin,position,p.obstacles(root,'top',width)));p.set_grid(.05)
            if not points:return None
        result['paths'].append(h['escape_record'](p,{'root':root,'net':nets[net],'port':port,'width':width,'positions':points,'via_outer_mm':.45,'via_hole_mm':.3}));return position
    def connect(net,first,last,width,**routing):
        root=p.root(nets[net]['source_net_id']);route=h['wide_multilayer_route'](p,{'root':root,'first':first,'last':last,'width':width+.002,'new_vias':[first,last],'layers':('inner2','inner1'),'via_outer_mm':.45,'via_hole_mm':.3,'copper_clearance_mm':.27,'multi_anchor':True,**routing})
        if not route:return False
        parts,vias=route;regions=b['region_records'](net,{'parts':parts,'width':width});result['pours'].extend(regions)
        for r in regions:p.copper.append((root,r['layer'],Polygon([(q['x'],q['y']) for q in r['outline']])))
        for xy in vias:b['reserve_via'](p,{'root':root,'position':xy});result['vias'].append({'net':net,'x':xy[0],'y':xy[1],'hole_mm':.3,'outer_mm':.45})
        return True
    endpoints=[]
    for selector,xy in [('.J1 > .pin7',(-.95,-24.6)),('.J1 > .pin9',(.25,-27.)) ,('.D2 > .pin2',None),('.R32 > .pin1',None)]:
        position=escape('USB_DN',selector,.2979,xy,endpoints)
        print(json.dumps({'escape':selector,'position':position}),flush=True)
        if position is None:result['unresolved'].append({'net':'USB_DN','port':selector,'reason':'No ordinary through-via escape'});break
        endpoints.append(position)
    if len(endpoints)==4:
        connected=[endpoints[0]];remaining=endpoints[1:]
        while remaining:
            _,first,last=min((math.dist(first,last),first,last) for first in connected for last in remaining)
            if not connect('USB_DN',first,last,.2979,layers=('inner2','bottom')):result['unresolved'].append({'net':'USB_DN','reason':'No complete inner/outer corridor','first':first,'last':last});break
            connected.append(last);remaining.remove(last)
    if not result['unresolved']:
        for net,first,last,width in terminal_pairs:
            if net=='PACK_NTC' and args.retain_ntc_escapes:
                positions=[];root=p.root(nets[net]['source_net_id'])
                for selector,points in retained_ntc_escapes:
                    result['paths'].append(h['escape_record'](p,{'root':root,'net':nets[net],'port':ports[selector],'width':width,'positions':points,'via_outer_mm':.45,'via_hole_mm':.3}));positions.append(points[-1])
                a,z=positions;extra={'layers':('inner2','inner1')}
            else:a=escape(net,first,width);z=escape(net,last,width,targets=[a] if a is not None else []);extra={}
            if a is None or z is None or not connect(net,a,z,width,**extra):result['unresolved'].append({'net':net,'reason':'Incomplete full-net control replacement'})
        for r in region_replacements:
            extra={'first_layer':'inner1','last_layer':'inner1'} if r['net']=='MCU_MIC_WS' else {}
            if not connect(r['net'],r.get('replacement_first',r['first']),r.get('replacement_last',r['last']),r['original_nominal_width_mm'],**extra):result['unresolved'].append({'net':r['net'],'reason':'Incomplete width-preserving authored region replacement'})
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'complete':not result['unresolved'],'unresolved':result['unresolved'],'regions':len(result['pours'])}));return 1 if result['unresolved'] else 0


if __name__=='__main__':raise SystemExit(main())
