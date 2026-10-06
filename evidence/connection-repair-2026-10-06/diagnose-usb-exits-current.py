import json,runpy
from pathlib import Path
from shapely.geometry import Point,LineString
h=runpy.run_path('scripts/routing/plan-power-copper.py');d=Path('evidence/connection-repair-2026-10-06');c=json.loads((d/'control-corridors-cap-native/circuit.json').read_text());p=h['Planner'](c);p.set_copper_reserve(.0001);p.via_copper_clearance=.27;p.set_grid(.01,(-2.5,-28.5,1.5,-22));nets={r['name']:r for r in c if r['type']=='source_net'};root=p.root(nets['USB_DN']['source_net_id']);names={p.root(r['source_net_id']):n for n,r in nets.items()};v=h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3});top=p.obstacles(root,'top',.2979);out=[]
for selector,positions in [('.J1 > .pin7',[(-.95,-24.6),(-.95,-24.75),(-1,-24.75),(-.9,-24.7),(-.75,-27.2)]),('.J1 > .pin9',[(.25,-27),(.25,-27.2),(.25,-27.5),(.25,-27.7),(.3,-27.9)]),('.D2 > .pin2',[(-.25,-21.6),(-1.05,-22.5)])]:
 port=next(r for r in p.ports.values() if p.port_name(r)==selector);origin=(port['x'],port['y'])
 for xy in positions:
  route=p.grid_route((origin,xy,top))
  near=[{'net':names.get(other,other),'layer':layer,'distance_mm':shape.distance(Point(xy)),'bounds':shape.bounds} for other,layer,shape in p.copper if other!=root and shape.distance(Point(xy))<.55]
  out.append({'port':selector,'position':xy,'origin_blocked':Point(origin).intersects(top),'via_blocked':Point(xy).intersects(v),'top_route':route,'near_foreign_copper':near})
(d/'current-usb-exit-diagnosis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps([{k:v for k,v in q.items() if k!='near_foreign_copper'} for q in out]))
