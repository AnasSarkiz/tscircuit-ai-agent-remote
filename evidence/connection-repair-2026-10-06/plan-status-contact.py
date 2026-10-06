"""Retire an obstructing duplicate top escape; retain its real inner connection."""
import json,runpy,math
from pathlib import Path
from shapely.geometry import Polygon
h=runpy.run_path('scripts/routing/plan-power-copper.py');b=runpy.run_path('scripts/routing/plan-connection-bridges.py');directory=Path('evidence/connection-repair-2026-10-06');c=json.loads((directory/'relocated-native/circuit.json').read_text());amp=json.loads((directory/'amplifier-proposal.json').read_text());sources={r['source_trace_id']:r for r in c if r['type']=='source_trace'}
trace=next(r for r in c if r['type']=='pcb_trace' and sources[r['source_trace_id']].get('name')=='MANUAL_INNER_ESCAPE_38_0');vias=[r for r in c if r['type']=='pcb_via' and r.get('pcb_trace_id')==trace['pcb_trace_id']];assert len(vias)==1
retired={trace['pcb_trace_id']:{'top':None,'bottom':None},**{r['original_pcb_trace_id']:{'top':None} for r in amp['retired_replay_connections']}}
p=h['Planner'](c,{'relocated_trace_layers':retired,'retired_feature_ids':{vias[0]['pcb_via_id']}});p.set_grid(.05);p.via_copper_clearance=.27;p.reserve_proposals(amp);nets={r['name']:r for r in c if r['type']=='source_net'}
for region in amp['pours']:p.copper.append((p.root(nets[region['net']]['source_net_id']),region['layer'],Polygon([(xy['x'],xy['y']) for xy in region['outline']])))
net='CHARGE_STATUS_N';root=p.root(nets[net]['source_net_id']);relocation=next(r for r in json.load(open('src/board/inner-signal-copper.json'))['paths'] if r['original_path_index']==38);target=relocation['regions'][0]['path_mm'][0];layer=relocation['regions'][0]['layer'];existing=[r for r in c if r['type']=='pcb_via' and r['pcb_via_id']!=vias[0]['pcb_via_id'] and p.via_root(r)==root]
result={'classification':'authored native bridge from retained charger-status via to intact inner route','paths':[],'pours':[],'vias':[],'unresolved':[],'retired_inner_escapes':[{'source_name':'MANUAL_INNER_ESCAPE_38_0','original_path_index':38,'escape_index':0,'original_pcb_trace_id':trace['pcb_trace_id'],'retired_via_id':vias[0]['pcb_via_id']}],'repaired_islands':[]}
for via in sorted(existing,key=lambda r:math.dist((r['x'],r['y']),target)):
 obstacles=h['inner_obstacles'](p,{'root':root,'width':.202,'new_vias':[(r['x'],r['y']) for r in existing],'layer':layer,'copper_clearance_mm':.27});route=p.grid_route(((via['x'],via['y']),target,obstacles))
 if route:
  result['pours']=b['region_records'](net,{'parts':[(layer,route)],'width':.2});break
else:result['unresolved'].append({'net':net,'reason':'No inner bridge to retained real status via'})
(directory/'status-contact-proposal.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='pours'}));raise SystemExit(1 if result['unresolved'] else 0)
