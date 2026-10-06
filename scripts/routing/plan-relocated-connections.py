"""Replace selected authored top routes to free trapped verified pad escapes."""
import argparse
import hashlib
import json
import math
import runpy
from pathlib import Path
from shapely.geometry import Polygon

bridges=runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')))
helpers=bridges['helpers']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit_json');parser.add_argument('copper_audit');parser.add_argument('output_json');parser.add_argument('indices',nargs='*',type=int)
    parser.add_argument('--replace-amplifier-din',action='store_true',help='Replace the verified saved AMP_DIN top detour with authored native copper')
    parser.add_argument('--reserve-proposals',help='Reserve already authored pending copper before this proposal')
    parser.add_argument('--relocation-only',action='store_true',help='Only replace the selected paths; keep unrelated repair attempts out of the proposal')
    args=parser.parse_args();circuit=json.loads(Path(args.circuit_json).read_text());physical=json.loads(Path(args.copper_audit).read_text());manual=json.loads(Path('src/board/manual-signal-paths.json').read_text())['paths']
    selected=[dict(manual[index]) for index in args.indices]
    # Net-directed branches must be joined to an existing numbered terminal,
    # rather than manufacturing an endpoint at an arbitrary free coordinate.
    for path in selected:
        if path['to'] == 'net.MIC_INPUT':
            path['to'] = '.U23 > .pin1'
    if any(path['width']>.3 or path['net'] in {'VBUS','VSYS','SPEAKER_N','SPEAKER_P','PACK_BAT','V3V3','VMOTOR','HAPTIC_N'} for path in selected):
        raise ValueError('Only existing low-current authored signals can be relocated')
    names={f"MANUAL_{manual[index]['net']}_{index}" for index in args.indices}
    sources={r['source_trace_id']:r for r in circuit if r['type']=='source_trace'}
    retired={r['pcb_trace_id']:{'top':None,'bottom':None,'inner1':None,'inner2':None} for r in circuit if r['type']=='pcb_trace' and sources[r['source_trace_id']].get('name') in names}
    if len(retired)!=len(names):raise ValueError('Every selected source path needs a real native trace')
    retired_replay=[]
    retained_paths=[]
    if args.replace_amplifier_din:
        detour=next(r for r in circuit if r['type']=='pcb_trace' and r['pcb_trace_id']=='saved_phase_null_5_1')
        if any(p['route_type']!='wire' or p['layer']!='top' or p['width']!=.2 for p in detour['route']):
            raise ValueError('The original AMP_DIN detour geometry has changed')
        source_ports={r['source_port_id']:r for r in circuit if r['type']=='source_port'}
        components={r['source_component_id']:r for r in circuit if r['type']=='source_component'}
        ports={r['pcb_port_id']:r for r in circuit if r['type']=='pcb_port'}
        terminals=[]
        for identifier in (detour['route'][0]['start_pcb_port_id'],detour['route'][-1]['end_pcb_port_id']):
            source=source_ports[ports[identifier]['source_port_id']]
            terminals.append(f".{components[source['source_component_id']]['name']} > .pin{source['pin_number']}")
        if terminals!=['.R68 > .pin1','.U3 > .pin1']:raise ValueError('Unexpected amplifier detour terminals')
        selected.append({'net':'AMP_DIN','from':terminals[0],'to':terminals[1],'width':.2})
        retired[detour['pcb_trace_id']]={'top':None}
        retired_replay.append({'phase_index':5,'connection':'.R68 > port.pin1','original_pcb_trace_id':detour['pcb_trace_id']})
        retained=next(r for r in circuit if r.get('pcb_trace_id')=='saved_phase_null_5_0')
        if any(p['route_type']!='wire' or p['layer']!='top' or p['width']!=.2 for p in retained['route']):
            raise ValueError('Unexpected geometry for the retained amplifier branch')
        first=ports[retained['route'][0]['start_pcb_port_id']]
        last=ports[retained['route'][-1]['end_pcb_port_id']]
        labels=[]
        for port in (first,last):
            source=source_ports[port['source_port_id']]
            labels.append(f".{components[source['source_component_id']]['name']} > .pin{source['pin_number']}")
        if labels!=['.R65 > .pin2','.R68 > .pin1']:
            raise ValueError('Unexpected retained amplifier terminals')
        component=next(r for r in circuit if r.get('pcb_component_id')==first['pcb_component_id'] and r['type']=='pcb_component')
        angle=math.radians(-component['rotation']);local=[]
        for point in retained['route'][1:]:
            dx=point['x']-component['display_offset_x'];dy=point['y']-component['display_offset_y']
            local.append({'x':round(dx*math.cos(angle)-dy*math.sin(angle),9),
                          'y':round(dx*math.sin(angle)+dy*math.cos(angle),9)})
        retained_paths.append({'net':'AMP_DIN','from':labels[0],'to':labels[1],'width':.2,'pcbPath':local,
            'global_path_mm':[[p['x'],p['y']] for p in retained['route']],
            'segment_layers':['top']*len(retained['route']),
            'classification':'authored native retention of the original R65-to-R68 geometry; migrate the complete net out of phase5',
            'retained_from_native_sha256':hashlib.sha256(Path(args.circuit_json).read_bytes()).hexdigest(),
            'original_pcb_trace_id':retained['pcb_trace_id']})
        retired_replay.append({'phase_index':5,'connection':'.R65 > port.pin2','original_pcb_trace_id':retained['pcb_trace_id']})
    if not selected:raise ValueError('Select actual native routes for replacement')
    nets={r['name']:r for r in circuit if r['type']=='source_net'}
    reserved=json.loads(Path(args.reserve_proposals).read_text()) if args.reserve_proposals else None
    if reserved:
        retired.update({r['original_pcb_trace_id']:{'top':None} for r in reserved.get('retired_replay_connections',[])})
    planner=helpers['Planner'](circuit,{'relocated_trace_layers':retired});planner.set_grid(.05);planner.via_copper_clearance=.27
    if reserved:
        planner.reserve_proposals(reserved)
        for record in reserved['pours']:
            planner.copper.append((planner.root(nets[record['net']]['source_net_id']),record['layer'],Polygon([(p['x'],p['y']) for p in record['outline']])))
    selectors={planner.port_name(port):port for port in planner.ports.values() if planner.source_ports[port['source_port_id']].get('source_component_id') in planner.source_components}
    result={'classification':'authored native signal relocation plus verified connection repairs; replay required','paths':retained_paths,'pours':[],'vias':[],'unresolved':[],'retired_manual_path_indices':args.indices,'retired_replay_connections':retired_replay,'repaired_islands':[]}
    for name in dict.fromkeys(path['net'] for path in selected):
        root=planner.root(nets[name]['source_net_id']);terminals=list(dict.fromkeys(selector for path in selected if path['net']==name for selector in (path['from'],path['to'])))
        if any(selector not in selectors for selector in terminals):raise ValueError('Relocation needs numbered source terminals')
        ports=[selectors[selector] for selector in terminals]
        targets=[]
        existing_main_ports={'MIC_WS':'.R95 > .pin1','CHARGE_STATUS_N':'.U16 > .pin9'}
        if name in existing_main_ports:
            main_selector=existing_main_ports[name]
            existing=bridges['island_vias'](planner,{'root':root,'physical':physical,'group':physical['physical_port_groups'][selectors[main_selector]['pcb_port_id']][0]})
            targets.extend(existing);ports=[port for port in ports if planner.port_name(port)!=main_selector]
        if not targets:
            seed=bridges['main_escape'](planner,{'net':nets[name],'root':root,'physical':physical,
                'group':'retired','ports':ports[:1],'existing_targets':set()})
            if not seed:
                result['unresolved'].append({'net':name,'reason':'No main escape after retirement'});continue
            result['paths'].extend(seed['paths']);result['vias'].extend(seed['vias']);targets=[seed['position']];ports=ports[1:]
        for port in ports:
            repaired=bridges['repair_island'](planner,{'net':nets[name],'root':root,'physical':physical,'group':'replaced-top-trace','ports':[port],'targets':targets})
            if repaired:
                for kind in ('paths','pours','vias'):result[kind].extend(repaired[kind])
                targets.append(repaired['connected_start'])
            else:result['unresolved'].append({'net':name,'port':planner.port_name(port),'reason':'No replacement connection'})
            print(json.dumps({'relocating':name,'port':planner.port_name(port),'routed':bool(repaired)}),flush=True)
            Path(args.output_json).write_text(json.dumps(result,indent=2)+'\n')
    result['relocation_complete']=not result['unresolved']
    if args.relocation_only:
        Path(args.output_json).write_text(json.dumps(result,indent=2)+'\n')
        return 0 if result['relocation_complete'] else 1
    # Plan the formerly trapped pads against the fully reserved replacements.
    for name,labels in [('AMP_SD_MODE',['.U3 > .pin4']),('AUDIO_ENABLE_SUPPLY',['.R63 > .pin1']),('VMIC',['.U24 > .pin5','.R93 > .pin1','.U5 > .pin2','.U5 > .pin5']),('MIC_WS',['.R93 > .pin2']),('MIC_BCLK',['.U5 > .pin4'])]:
        root=planner.root(nets[name]['source_net_id']);groups={}
        for port in planner.ports.values():
            if planner.root(port['source_port_id'])==root and planner.source_ports[port['source_port_id']].get('source_component_id') in planner.source_components:
                group=physical['physical_port_groups'][port['pcb_port_id']]
                if len(group)==1:groups.setdefault(group[0],[]).append(port)
        main_group=max(groups,key=lambda group:len(groups[group]));targets=bridges['island_vias'](planner,{'root':root,'group':main_group,'physical':physical})
        if name=='MIC_WS':targets.extend([(r['x'],r['y']) for r in result['vias'] if r['net']==name]);targets.extend([path['global_path_mm'][-1] for path in result['paths'] if path['net']==name and path['pcbPath'][-1].get('via')])
        seed=None
        if not targets:
            seed=bridges['main_escape'](planner,{'net':nets[name],'root':root,'physical':physical,'group':main_group,'ports':groups[main_group]})
            if seed:targets=[seed['position']]
        for selector in labels:
            port=selectors[selector];group=physical['physical_port_groups'][port['pcb_port_id']][0]
            if group==main_group:continue
            repaired=bridges['repair_island'](planner,{'net':nets[name],'root':root,'physical':physical,'group':group,'ports':[port],'targets':targets})
            if repaired:
                if seed:
                    result['paths'].extend(seed['paths']);result['vias'].extend(seed['vias']);seed=None
                for kind in ('paths','pours','vias'):result[kind].extend(repaired[kind])
                targets.append(repaired['connected_start']);result['repaired_islands'].append({'net':name,'ports':[selector]})
            else:result['unresolved'].append({'net':name,'port':selector,'reason':'No qualified route after moving enclosing top signals'})
            print(json.dumps({'net':name,'port':selector,'routed':bool(repaired)}),flush=True)
            Path(args.output_json).write_text(json.dumps(result,indent=2)+'\n')
    return 1 if result['unresolved'] else 0

if __name__=='__main__':raise SystemExit(main())
