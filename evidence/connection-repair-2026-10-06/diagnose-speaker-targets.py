import json,runpy
from pathlib import Path
from shapely.geometry import Polygon,Point
b=runpy.run_path('scripts/routing/plan-connection-bridges.py');h=b['helpers'];d=Path('evidence/connection-repair-2026-10-06');c=json.loads((d/'power-control-manual-native/circuit.json').read_text());plans=[json.loads((d/name).read_text()) for name in ['ground-speaker-relocation-proposal.json','independent-ground-proposal.json','outer-after-corridors-fixed-proposal.json']];manual=json.load(open('src/board/manual-signal-paths.json'))['paths'];sources={r['source_trace_id']:r for r in c if r['type']=='source_trace'};names={f"MANUAL_{manual[i]['net']}_{i}" for plan in plans for i in plan.get('retired_manual_path_indices',[])};retired={r['pcb_trace_id']:{layer:None for layer in ('top','bottom','inner1','inner2')} for r in c if r['type']=='pcb_trace' and sources[r['source_trace_id']].get('name') in names};p=h['Planner'](c,{'relocated_trace_layers':retired});p.set_grid(.05);p.via_copper_clearance=.27;nets={r['name']:r for r in c if r['type']=='source_net'};net_names={p.root(r['source_net_id']):name for name,r in nets.items()}
for plan in plans:
 p.reserve_proposals(plan)
 for r in plan['pours']:p.copper.append((p.root(nets[r['net']]['source_net_id']),r['layer'],Polygon([(q['x'],q['y']) for q in r['outline']])))

out=[]
for name,xy,terminal in [('SPEAKER_P',(-16,6.5),(21.02500195,8)),('SPEAKER_N',(-16.5,6.5),(23.02499795,8))]:
 root=p.root(nets[name]['source_net_id']);width=.277;obstacles=[h['inner_obstacles'](p,{'root':root,'width':width,'layer':layer,'new_vias':[terminal],'copper_clearance_mm':.27}) for layer in ('bottom','top')];data=[p.grid_data(obstacle) for obstacle in obstacles];targets=[]
 for layer,obstacle in enumerate(obstacles):
  anchor=p.grid_anchor((terminal,),(data[layer][0],obstacle))[0]
  if anchor:targets.append((layer,*anchor[0]))
 result={'net':name,'terminal':terminal,'terminal_blocked':[Point(terminal).intersects(o) for o in obstacles],'targets':targets,'via_candidate':xy,'candidate_blocked':[Point(xy).intersects(o) for o in obstacles]}
 if targets:result['candidate_reaches_connector']=h['via_exit_reachable'](p,{'grid_data':data,'obstacles':obstacles,'targets':targets,'via_blocked':p.grid_data(h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3}))[0],'target':xy})
 result['near_connector_copper']=[{'net':net_names.get(other,other),'layer':layer,'distance_mm':round(shape.distance(Point(terminal)),6),'bounds':[round(v,5) for v in shape.bounds]} for other,layer,shape in p.copper if other!=root and shape.distance(Point(terminal))<1.5]
 out.append(result);print(json.dumps(result),flush=True)
(d/'speaker-target-diagnosis.json').write_text(json.dumps(out,indent=2)+'\n')
