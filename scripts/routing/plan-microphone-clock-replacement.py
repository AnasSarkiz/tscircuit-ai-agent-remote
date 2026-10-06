"""Replace the U4 clock escape while preserving its numbered pad and old corridor.

The existing clock crosses the microphone ground-port neighbourhood. Releasing
that top route may restore native ground-plane recognition; only a fresh native
build can establish this. Original geometry and supplier definitions are intact.
"""
import json,runpy,sys
from pathlib import Path
h=runpy.run_path(str(Path(__file__).with_name('plan-power-copper.py')))
b=runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')))
c=json.loads(Path(sys.argv[1]).read_text());sources={r['source_trace_id']:r for r in c if r['type']=='source_trace'}
trace=next(r for r in c if r['type']=='pcb_trace' and sources[r['source_trace_id']].get('name')=='MANUAL_INNER_ESCAPE_246_0')
via=next(r for r in c if r['type']=='pcb_via' and r.get('pcb_trace_id')==trace['pcb_trace_id'])
p=h['Planner'](c,{'relocated_trace_layers':{trace['pcb_trace_id']:{'top':None}}});p.set_grid(.05);p.via_copper_clearance=.27
port=p.ports[trace['route'][0]['start_pcb_port_id']];root=p.root(port['source_port_id']);net=next(r for r in c if r['type']=='source_net' and p.root(r['source_net_id'])==root);target=(via['x'],via['y'])
result={'classification':'Complete authored U4 clock replacement; native ground recognition and preservation must be verified',
        'paths':[],'pours':[],'vias':[],'unresolved':[],'retired_inner_escapes':[]}
found=h['pad_escape'](p,{'root':root,'net':net,'width':.2,'origin':(port['x'],port['y']),
    'new_vias':[target],'via_outer_mm':.45,'via_hole_mm':.3,'distribution_layers':('inner1','inner2'),
    'distribution_width_mm':.202,'copper_clearance_mm':.27,'connected_targets':[target]})
if not found:result['unresolved'].append('No complete replacement clock escape')
else:
    xy,positions=found
    path=h['escape_record'](p,{'root':root,'net':net,'port':port,'positions':positions,'width':.2,'via_outer_mm':.45,'via_hole_mm':.3})
    route=h['wide_multilayer_route'](p,{'root':root,'first':xy,'last':target,'width':.202,
        'new_vias':[xy,target],'layers':('inner1','inner2'),'via_outer_mm':.45,'via_hole_mm':.3,
        'copper_clearance_mm':.27,'multi_anchor':True})
    if not route:result['unresolved'].append('Replacement clock corridor incomplete')
    else:
        parts,vias=route;result['paths']=[path];result['pours']=b['region_records'](net['name'],{'parts':parts,'width':.2})
        result['vias']=[{'net':net['name'],'x':pos[0],'y':pos[1],'hole_mm':.3,'outer_mm':.45} for pos in [target]+vias]
        result['retired_inner_escapes']=[{'source_name':'MANUAL_INNER_ESCAPE_246_0','original_path_index':246,'escape_index':0,
            'original_pcb_trace_id':trace['pcb_trace_id'],'retired_via_id':via['pcb_via_id']}]
Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'complete':not result['unresolved'],'new_escape':result['paths'],'regions':len(result['pours']),'unresolved':result['unresolved']}))
raise SystemExit(1 if result['unresolved'] else 0)
