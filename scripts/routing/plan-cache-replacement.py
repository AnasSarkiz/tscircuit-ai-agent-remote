"""Replace a complete verified MCU audio-DIN replay with authored inner copper.

Retain its measured pad escapes, original files and numbered terminals. This
proposal is never a solver cache and requires native DRC/continuity/width checks.
"""
import argparse
import hashlib
import json
import runpy
from pathlib import Path
from shapely.geometry import Polygon

b=runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')))
h=b['helpers']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('native');parser.add_argument('audit');parser.add_argument('output')
    parser.add_argument('--reserve-proposals',action='append',default=[])
    args=parser.parse_args();c=json.loads(Path(args.native).read_text());physical=json.loads(Path(args.audit).read_text())
    trace=next(r for r in c if r.get('pcb_trace_id')=='saved_phase_null_19_0')
    if any(r['route_type']=='wire' and r['width']!=.2 for r in trace['route']):raise ValueError('Unexpected retained signal width')
    cache=json.loads(Path('routes/a7/mcu-amplifier-din.json').read_text())
    if len(cache)!=1:raise ValueError('Only a complete single-connection phase may be replaced')
    plans=[json.loads(Path(path).read_text()) for path in args.reserve_proposals]
    manual=json.loads(Path('src/board/manual-signal-paths.json').read_text())['paths']
    sources={r['source_trace_id']:r for r in c if r['type']=='source_trace'}
    names={f"MANUAL_{manual[i]['net']}_{i}" for plan in plans for i in plan.get('retired_manual_path_indices',[])}
    retired={r['pcb_trace_id']:{layer:None for layer in ('top','bottom','inner1','inner2')}
             for r in c if r['type']=='pcb_trace' and sources[r['source_trace_id']].get('name') in names}
    if len(retired)!=len(names):raise ValueError('Every reserved retirement must exist in native copper')
    retired[trace['pcb_trace_id']]={layer:None for layer in ('top','bottom','inner1','inner2')}
    retired_vias={r['pcb_via_id'] for r in c if r['type']=='pcb_via' and r.get('pcb_trace_id')==trace['pcb_trace_id']}
    p=h['Planner'](c,{'relocated_trace_layers':retired,'retired_feature_ids':retired_vias});p.set_grid(.05);p.via_copper_clearance=.27
    nets={r['name']:r for r in c if r['type']=='source_net'};net=nets['MCU_AUDIO_DIN'];root=p.root(net['source_net_id'])
    for plan in plans:
        p.reserve_proposals(plan)
        for region in plan.get('pours',[]):p.copper.append((p.root(nets[region['net']]['source_net_id']),region['layer'],Polygon([(q['x'],q['y']) for q in region['outline']])))
    starts=[i for i,r in enumerate(trace['route']) if r['route_type']=='via']
    if len(starts)<2:raise ValueError('Preservation requires two existing pad escapes')
    paths=[];positions=[]
    for record,points in [(trace['route'][0],trace['route'][:starts[0]+1]),
                          (trace['route'][-1],list(reversed(trace['route'][starts[-1]:])) )]:
        port_id=record.get('start_pcb_port_id') or record.get('end_pcb_port_id');port=p.ports[port_id]
        if p.root(port['source_port_id'])!=root:raise ValueError('Unexpected named-net endpoint')
        if any(r['route_type']=='wire' and r['layer']!='top' for r in points):raise ValueError('Original pad escape must be on top')
        xy=[]
        for point in points:
            current=(point['x'],point['y'])
            if not xy or current!=xy[-1]:xy.append(current)
        paths.append(h['escape_record'](p,{'port':port,'net':net,'root':root,'positions':xy,'width':.2,'via_outer_mm':.45,'via_hole_mm':.3}))
        positions.append(xy[-1])
    if [r['from'] for r in paths]!=['.U1 > .pin7','.R65 > .pin1']:raise ValueError('Unexpected MCU audio-DIN numbered terminals')
    result={'classification':'authored complete net replacement retaining measured native pad escapes; native qualification required',
        'source_native_sha256':hashlib.sha256(Path(args.native).read_bytes()).hexdigest(),
        'paths':paths,'pours':[],'vias':[],'unresolved':[],
        'retired_replay_connections':[{'phase_index':19,'connection':cache[0]['connection'],'original_pcb_trace_id':trace['pcb_trace_id']}],
        'retired_native_vias':sorted(retired_vias)}
    route=h['wide_multilayer_route'](p,{'root':root,'first':positions[0],'last':positions[1],
        'width':.202,'new_vias':positions,'layers':('inner2','inner1'),'via_outer_mm':.45,'via_hole_mm':.3,'copper_clearance_mm':.27})
    if route:
        parts,vias=route;result['pours']=b['region_records']('MCU_AUDIO_DIN',{'parts':parts,'width':.2})
        result['vias']=[{'net':'MCU_AUDIO_DIN','x':x,'y':y,'hole_mm':.3,'outer_mm':.45} for x,y in vias]
    else:result['unresolved'].append({'net':'MCU_AUDIO_DIN','reason':'No complete width-preserving inner route between retained escapes'})
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'complete':not result['unresolved'],'paths':len(paths),'regions':len(result['pours']),'vias':len(result['vias'])}))
    return 1 if result['unresolved'] else 0


if __name__=='__main__':raise SystemExit(main())
