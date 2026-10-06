"""Identify actual copper obstructing a second speaker route; no accepted changes.

Temporary whole-net retirements are diagnostic planning inputs only. All native
source bytes are retained; a moved net must be fully replaced before acceptance.
"""
import json,runpy,sys,hashlib
from pathlib import Path
h=runpy.run_path('scripts/routing/plan-power-copper.py')
c=json.loads(Path(sys.argv[1]).read_text());probe=h['Planner'](c)
roots={r['name']:probe.root(r['source_net_id']) for r in c if r['type']=='source_net'}
sources={r['source_trace_id']:r for r in c if r['type']=='source_trace'}
output={'classification':'Unbuilt blocker diagnosis; temporarily omitted foreign copper is not a board repair or passing route','native_sha256':hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest(),'trials':[]}
for name in ('VSYS','V3V3','GND'):
 retired={};features=[]
 for r in c:
  if r['type']=='pcb_trace':
   s=sources[r['source_trace_id']];ids=s.get('connected_source_port_ids',[])+s.get('connected_source_net_ids',[])
   if ids and probe.root(ids[0])==roots[name]:retired[r['pcb_trace_id']]={layer:None for layer in ('top','bottom','inner1','inner2')}
  elif r['type']=='pcb_via' and probe.via_root(r)==roots[name]:features.append(r['pcb_via_id'])
  elif r['type']=='pcb_copper_pour' and probe.root(r['source_net_id'])==roots[name]:features.append(r['pcb_copper_pour_id'])
 p=h['Planner'](c,{'relocated_trace_layers':retired,'retired_feature_ids':features});p.set_grid(.05);p.via_copper_clearance=.27
 net=next(r for r in c if r['type']=='source_net' and r['name']=='SPEAKER_N');root=p.root(net['source_net_id']);port=next(r for r in p.ports.values() if p.port_name(r)=='.U3 > .pin10');target=next((r['x'],r['y']) for r in p.ports.values() if p.port_name(r)=='.J4 > .pin2')
 spec={'root':root,'net':net,'width':.275,'origin':(port['x'],port['y']),'new_vias':[target],'via_outer_mm':.45,'via_hole_mm':.3,'distribution_layers':('bottom','top'),'distribution_width_mm':.6,'routing_geometry':'native_wire','connected_targets':[target]}
 escape=h['pad_escape'](p,spec);trial={'temporarily_retired_net':name,'retired_trace_ids':list(retired),'retired_feature_ids':features,'has_full_width_corridor':bool(escape),'accepted':False}
 if escape:
  xy,positions=escape;trial['escape_mm']=positions
  h['escape_record'](p,{**spec,'port':port,'positions':positions})
  route=h['wide_multilayer_route'](p,{**spec,'width':.6,'first':xy,'last':target,'new_vias':[xy,target],'layers':('bottom','top'),'multi_anchor':True})
  trial['has_complete_nominal_trunk']=bool(route)
  if route:trial['trunk_parts']=route[0];trial['trunk_vias']=route[1]
 output['trials'].append(trial);Path(sys.argv[2]).write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in trial.items() if k not in ('retired_trace_ids','retired_feature_ids','trunk_parts','trunk_vias')}),flush=True)
