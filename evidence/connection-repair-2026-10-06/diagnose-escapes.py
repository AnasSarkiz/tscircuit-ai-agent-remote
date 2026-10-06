import json,runpy
from pathlib import Path
from shapely.geometry import Point
h=runpy.run_path('scripts/routing/plan-power-copper.py');c=json.load(open('evidence/connection-repair-2026-10-06/trial-native/circuit.json'));p=h['Planner'](c);p.set_grid(.05)
nets={r['name']:r for r in c if r['type']=='source_net'}
results=[]
for selector,net in [('.U3 > .pin4','AMP_SD_MODE'),('.R63 > .pin1','AUDIO_ENABLE_SUPPLY'),('.U24 > .pin5','VMIC'),('.R93 > .pin1','VMIC'),('.U5 > .pin2','VMIC'),('.U5 > .pin5','VMIC'),('.R93 > .pin2','MIC_WS'),('.U5 > .pin4','MIC_BCLK'),('.U14 > .pin15','LCD_SCLK'),('.U14 > .pin14','LCD_SDA'),('.C2 > .pin2','GND')]:
 port=next(r for r in p.ports.values() if p.source_ports[r['source_port_id']].get('source_component_id') in p.source_components and p.port_name(r)==selector)
 root=p.root(nets[net]['source_net_id']);width=nets[net].get('trace_width') or .2;origin=(port['x'],port['y']);top=p.obstacles(root,'top',width);via=h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3});escapes=p.grid_escape(origin,(top,via))
 blockers=[]
 for other,layer,shape in p.copper:
  if other!=root and layer=='top' and shape.distance(Point(origin)) < width/2+.22: blockers.append({'root':other,'gap':shape.distance(Point(origin))})
 record={'port':selector,'net':net,'width':width,'origin_blocked':top.intersects(Point(origin)),'escapes':len(escapes),'first_escapes':escapes[:2],'near_foreign_copper':blockers}
 results.append(record);print(json.dumps(record),flush=True)
Path('evidence/connection-repair-2026-10-06/escape-diagnosis.json').write_text(json.dumps(results,indent=2)+'\n')
