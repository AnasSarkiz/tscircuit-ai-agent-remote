import json,runpy
from pathlib import Path
from shapely.geometry import Point,LineString
h=runpy.run_path('scripts/routing/plan-power-copper.py');c=json.load(open('evidence/connection-repair-2026-10-06/usb-ground-power-speaker-native/circuit.json'));p=h['Planner'](c);p.set_grid(.05);p.set_copper_reserve(.0001);p.via_copper_clearance=.27
nets={r['name']:r for r in c if r['type']=='source_net'};root_names={p.root(r['source_net_id']):name for name,r in nets.items()};out=[]
for net,selector,targets,width in [('USB_DN','.J1 > .pin9',[(.249936,-26.85),(-.750062,-26.85)],.2979),('LCD_SDA','.U14 > .pin14',[(9.975,11.8),(9.975,12.5)],.2),('LCD_SCLK','.U14 > .pin15',[(9.325,11.8),(9.325,12.5)],.2),('VBUS','.C1 > .pin1',[(-11,-25.3)],.3)]:
 port=next(r for r in p.ports.values() if p.port_name(r)==selector);origin=(port['x'],port['y']);root=p.root(nets[net]['source_net_id']);o=p.obstacles(root,'top',width);v=h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3});item={'net':net,'port':selector,'origin_mm':origin,'origin_blocked':Point(origin).intersects(o),'candidates':[]}
 for xy in targets:
  item['candidates'].append({'xy':xy,'straight_escape_blocked':LineString([origin,xy]).intersects(o),'via_blocked':Point(xy).intersects(v),'foreign_copper':sorted([{'net':root_names.get(other,other),'layer':layer,'distance':round(shape.distance(Point(xy)),6),'bounds':[round(z,5) for z in shape.bounds]} for other,layer,shape in p.copper if other!=root and shape.distance(Point(xy))<1],key=lambda r:r['distance'])[:8]})
 out.append(item)
Path('evidence/connection-repair-2026-10-06/tight-pad-exit-diagnosis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
