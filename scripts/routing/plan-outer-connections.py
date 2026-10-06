"""Join verified power/speaker islands with outer-layer trunks and pad necks.

Neck widths and lengths are retained explicitly for load/stackup qualification.
This is authored geometry, not a solver cache or fabrication approval.
"""
import argparse
import json
import math
import runpy
from pathlib import Path
from shapely.geometry import LineString, Polygon

bridges=runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')))
helpers=bridges['helpers']


def adaptive_regions(planner, specification):
    """Keep the nominal width wherever legal; measure every narrower section."""
    regions=[];narrow_length=0
    for layer,points in specification['parts']:
        obstacle=helpers['inner_obstacles'](planner,{'root':specification['root'],
            'width':specification['nominal_width']+.002,'layer':layer,
            'new_vias':specification['new_vias'],'copper_clearance_mm':.27})
        samples=[points[0]]
        for first,last in zip(points,points[1:]):
            count=max(1,math.ceil(math.dist(first,last)/.1))
            samples.extend((first[0]+(last[0]-first[0])*i/count,
                            first[1]+(last[1]-first[1])*i/count) for i in range(1,count+1))
        run=[];run_width=None
        for first,last in zip(samples,samples[1:]):
            width=specification['neck_width'] if LineString([first,last]).intersects(obstacle) else specification['nominal_width']
            if width==specification['neck_width']:narrow_length+=math.dist(first,last)
            if width!=run_width and run:
                line=LineString(run).simplify(.000001)
                regions.extend(bridges['region_records'](specification['net'],{'parts':[(layer,list(line.coords))],'width':run_width}))
                run=[first]
            if not run:run=[first]
            run.append(last);run_width=width
        if run:
            line=LineString(run).simplify(.000001)
            regions.extend(bridges['region_records'](specification['net'],{'parts':[(layer,list(line.coords))],'width':run_width}))
    return regions,narrow_length


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit_json');parser.add_argument('copper_audit');parser.add_argument('output_json')
    parser.add_argument('--reserve-proposals',required=True,action='append')
    parser.add_argument('--ports',nargs='+',help='Only plan these actual numbered pad selectors')
    parser.add_argument('--short-outer-necks',action='store_true',help='Allow measured narrow outer-layer sections, keeping total neck length at most5mm; current qualification remains required')
    args=parser.parse_args();circuit=json.loads(Path(args.circuit_json).read_text());physical=json.loads(Path(args.copper_audit).read_text());reserved={'paths':[],'pours':[],'vias':[],'retired_replay_connections':[],'retired_inner_escapes':[],'retired_manual_path_indices':[],'retired_native_vias':[]}
    for filename in args.reserve_proposals:
        proposal=json.loads(Path(filename).read_text())
        for key in reserved:reserved[key].extend(proposal.get(key,[]))
    retired={r['original_pcb_trace_id']:{layer:None for layer in ('top','bottom','inner1','inner2')} for r in reserved.get('retired_replay_connections',[])}
    retired.update({r['original_pcb_trace_id']:{'top':None,'bottom':None} for r in reserved['retired_inner_escapes']})
    manual=json.loads(Path('src/board/manual-signal-paths.json').read_text())['paths']
    names={f"MANUAL_{manual[index]['net']}_{index}" for index in reserved['retired_manual_path_indices']}
    sources={r['source_trace_id']:r for r in circuit if r['type']=='source_trace'}
    selected={r['pcb_trace_id']:{layer:None for layer in ('top','bottom','inner1','inner2')}
              for r in circuit if r['type']=='pcb_trace' and sources[r['source_trace_id']].get('name') in names}
    if len(selected)!=len(names):raise ValueError('Reserved retirements must identify real native paths')
    retired.update(selected)
    planner=helpers['Planner'](circuit,{'relocated_trace_layers':retired,'retired_feature_ids':{r['retired_via_id'] for r in reserved['retired_inner_escapes']}|set(reserved['retired_native_vias'])});planner.set_grid(.05);planner.via_copper_clearance=.27
    # These pending proposals were authored for this board's measured .30/.45
    # through vias; do not reserve the legacy .70mm pad around their escapes.
    planner.reserve_proposals({**reserved,'paths':[{**path,'via_outer_mm':.45,'via_hole_mm':.3} for path in reserved['paths']]})
    nets={r['name']:r for r in circuit if r['type']=='source_net'}
    for record in reserved['pours']:planner.copper.append((planner.root(nets[record['net']]['source_net_id']),record['layer'],Polygon([(p['x'],p['y']) for p in record['outline']])))
    result={'classification':'authored outer-layer connection proposals; native geometry and pad-neck load qualification required','paths':[],'pours':[],'vias':[],'pad_necks':[],'unresolved':[],'repaired_islands':[],'rejected_narrow_routes':[]}
    allowed={'VBUS':{'.J1 > .pin16','.U16 > .pin13','.C1 > .pin1'},'VSYS':{'.U16 > .pin10','.U16 > .pin11','.R62 > .pin1','.U3 > .pin2'},'SPEAKER_P':{'.U3 > .pin9'},'SPEAKER_N':{'.U3 > .pin10'}}
    for name,selectors in allowed.items():
        net=nets[name];root=planner.root(net['source_net_id']);groups={}
        for port in planner.ports.values():
            if planner.root(port['source_port_id'])==root and planner.source_ports[port['source_port_id']].get('source_component_id') in planner.source_components:
                group=physical['physical_port_groups'][port['pcb_port_id']]
                if len(group)==1:groups.setdefault(group[0],[]).append(port)
        plated={r.get('pcb_port_id') for r in circuit if r['type']=='pcb_plated_hole'}
        main_group=max(groups,key=lambda group:(any(p['pcb_port_id'] in plated for p in groups[group]),len(groups[group])))
        targets=bridges['island_vias'](planner,{'root':root,'physical':physical,'group':main_group})
        targets.extend((p['x'],p['y']) for p in groups[main_group] if p['pcb_port_id'] in plated)
        if not targets:
            result['unresolved'].append({'net':name,'reason':'No actual outer-layer main-island target'});continue
        for group,ports in groups.items():
            if group==main_group:continue
            for port in ports:
                selector=planner.port_name(port)
                if selector not in selectors:continue
                if args.ports and selector not in args.ports:continue
                control_branch=selector in {'.R62 > .pin1','.U3 > .pin2'}
                width=.3 if control_branch else net['trace_width']
                neck_width=.275 if not control_branch and selector.startswith(('.U16 >','.U3 >')) else .2979 if selector=='.J1 > .pin16' else .3 if selector=='.C1 > .pin1' else width
                saved=list(planner.copper),list(planner.holes),dict(planner.plated_hole_roots)
                reserve=round(planner.copper_clearance-.2,4)
                if selector=='.J1 > .pin16':
                    # Exact .5mm USB pin pitch admits a .2979mm pad neck with
                    # the unchanged .20mm clearance. The extra reserve is .1um;
                    # native geometry still has to pass the independent audit.
                    planner.set_copper_reserve(.0001)
                found=helpers['pad_escape'](planner,{'root':root,'net':net,'width':neck_width,'origin':(port['x'],port['y']),
                    'new_vias':targets,'via_outer_mm':.45,'via_hole_mm':.3,'distribution_layers':('bottom','top'),
                    'distribution_width_mm':(neck_width if args.short_outer_necks else width)+.002,'copper_clearance_mm':.27,'connected_targets':targets})
                planner.set_copper_reserve(reserve)
                connected=False
                if found:
                    start,positions=found;length=sum(math.dist(a,b) for a,b in zip(positions,positions[1:]))
                    if neck_width==width or length<=5:
                        escape=helpers['escape_record'](planner,{'root':root,'net':net,'port':port,'width':neck_width,
                            'positions':positions,'via_outer_mm':.45,'via_hole_mm':.3})
                        for target in sorted(targets,key=lambda t:math.dist(t,start))[:20]:
                            route=helpers['wide_multilayer_route'](planner,{'first':start,'last':target,'root':root,
                                'width':(neck_width if args.short_outer_necks else width)+.002,'new_vias':targets+[start],'layers':('bottom','top'),
                                'via_outer_mm':.45,'via_hole_mm':.3,'copper_clearance_mm':.27,
                                **({'preferred_width_mm':width+.002} if args.short_outer_necks else {})})
                            if not route:continue
                            parts,vias=route;narrow_length=0
                            if args.short_outer_necks and neck_width<width:
                                regions,narrow_length=adaptive_regions(planner,{'root':root,'net':name,'parts':parts,
                                    'nominal_width':width,'neck_width':neck_width,'new_vias':targets+[start]+vias})
                                if length+narrow_length>5:
                                    result['rejected_narrow_routes'].append({'terminal':selector,'total_narrow_length_mm':length+narrow_length})
                                    continue
                            else:regions=bridges['region_records'](name,{'parts':parts,'width':width})
                            if control_branch:
                                for region in regions:region['branch_terminal']=selector
                            for region in regions:planner.copper.append((root,region['layer'],Polygon([(p['x'],p['y']) for p in region['outline']])))
                            for xy in vias:bridges['reserve_via'](planner,{'root':root,'position':xy})
                            result['paths'].append(escape);result['pours'].extend(regions);result['vias'].extend({'net':name,'x':xy[0],'y':xy[1],'hole_mm':.3,'outer_mm':.45} for xy in vias)
                            result['pad_necks'].append({'net':name,'terminal':selector,'width_mm':neck_width,'length_mm':length,
                                'outer_distribution_neck_length_mm':narrow_length,
                                'total_narrow_length_mm':length+narrow_length,
                                'nominal_trunk_width_mm':width,'layer':'top','status':'Measured layout proposal; current/stackup/thermal qualification pending'})
                            targets.append(start);result['repaired_islands'].append({'net':name,'ports':[selector]});connected=True;break
                if not connected:
                    planner.copper,planner.holes,planner.plated_hole_roots=saved
                    result['unresolved'].append({'net':name,'port':selector,'reason':'No outer trunk with a legal full-span via and at most5mm package neck; current qualification remains required'})
                print(json.dumps({'net':name,'port':selector,'routed':connected,'escape_found':bool(found),
                    'escape_length_mm':length if found else None}),flush=True)
                Path(args.output_json).write_text(json.dumps(result,indent=2)+'\n')
    return 1 if result['unresolved'] else 0

if __name__=='__main__':raise SystemExit(main())
