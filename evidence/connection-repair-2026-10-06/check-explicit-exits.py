import json,runpy
from pathlib import Path
from shapely.geometry import Point,LineString
h=runpy.run_path('scripts/routing/plan-power-copper.py');d=Path('evidence/connection-repair-2026-10-06');c=json.loads((d/'usb-ground-power-speaker-native/circuit.json').read_text());r=json.loads((d/'control-corridors-proposal.json').read_text());changes={q['original_pcb_trace_id']:{l:None for l in ('top','bottom','inner1','inner2')} for q in r['retired_inner_escapes']};p=h['Planner'](c,{'relocated_trace_layers':changes,'retired_feature_ids':{q['retired_via_id'] for q in r['retired_inner_escapes']}});p.set_grid(.05);p.set_copper_reserve(.0001);p.via_copper_clearance=.27;nets={q['name']:q for q in c if q['type']=='source_net'};out=[]
for net,selector,positions,width in [('USB_CC1','.J1 > .pin6',[(-1.249934,-27.5),(-1.249934,-27.8),(-1.45,-27.3),(-1.249934,-28)],.2),('USB_DP','.J1 > .pin10',[(.750062,-24.),(.9,-24),(.75,-23.9)],.2979),('USB_DN','.J1 > .pin7',[(-1.1,-23.45),(-.750062,-23.4)],.2979),('VBUS','.C1 > .pin1',[(-10.95,-25.3),(-10.9,-25.3),(-11,-25.35),(-11,-25.25)],.3)]:
 root=p.root(nets[net]['source_net_id']);port=next(q for q in p.ports.values() if p.port_name(q)==selector);origin=(port['x'],port['y']);top=p.obstacles(root,'top',width);via=h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3})
 for xy in positions:out.append({'net':net,'port':selector,'xy':xy,'direct_escape_blocked':LineString([origin,xy]).intersects(top),'via_blocked':Point(xy).intersects(via)})
(d/'explicit-exit-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
