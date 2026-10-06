import json,runpy
from pathlib import Path
from shapely.geometry import Polygon,Point
b=runpy.run_path('scripts/routing/plan-connection-bridges.py');h=b['helpers'];d=Path('evidence/connection-repair-2026-10-06');c=json.loads((d/'power-control-manual-native/circuit.json').read_text());plans=[json.loads((d/name).read_text()) for name in ['ground-speaker-relocation-proposal.json','independent-ground-proposal.json','outer-after-corridors-fixed-proposal.json']];manual=json.load(open('src/board/manual-signal-paths.json'))['paths'];sources={r['source_trace_id']:r for r in c if r['type']=='source_trace'};names={f"MANUAL_{manual[i]['net']}_{i}" for plan in plans for i in plan.get('retired_manual_path_indices',[])};retired={r['pcb_trace_id']:{layer:None for layer in ('top','bottom','inner1','inner2')} for r in c if r['type']=='pcb_trace' and sources[r['source_trace_id']].get('name') in names};p=h['Planner'](c,{'relocated_trace_layers':retired});p.set_grid(.05);p.via_copper_clearance=.27;nets={r['name']:r for r in c if r['type']=='source_net'};net_names={p.root(r['source_net_id']):name for name,r in nets.items()}
for plan in plans:
 p.reserve_proposals(plan)
 for r in plan['pours']:p.copper.append((p.root(nets[r['net']]['source_net_id']),r['layer'],Polygon([(q['x'],q['y']) for q in r['outline']])))
out=[]
for net,xy in [('SPEAKER_P',(-16,6.5)),('SPEAKER_N',(-16.5,6.5)),('VBUS',(-11,-25.3)),('VBUS',(-13,-24.5))]:
 root=p.root(nets[net]['source_net_id']);point=Point(xy);near=[{'net':net_names.get(other,other),'layer':layer,'distance_mm':round(shape.distance(point),6),'bounds':[round(v,5) for v in shape.bounds]} for other,layer,shape in p.copper if other!=root and shape.distance(point)<1.2];near.sort(key=lambda r:r['distance_mm']);record={'net':net,'candidate_mm':xy,'via_blocked':point.intersects(h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3})),'nearest_foreign_copper':near[:16]};out.append(record);print(json.dumps(record),flush=True)
(d/'remaining-fanout-diagnosis.json').write_text(json.dumps(out,indent=2)+'\n')
