import json,runpy,numpy as np
from pathlib import Path
from shapely import contains_xy
from shapely.geometry import Point
h=runpy.run_path('scripts/routing/plan-power-copper.py');c=json.load(open('evidence/connection-repair-2026-10-06/trial-native/circuit.json'));p=h['Planner'](c);p.set_grid(.05);nets={r['name']:r for r in c if r['type']=='source_net'};names={p.root(r['source_net_id']):r['name'] for r in nets.values()};results=[]
for selector,net in [('.U3 > .pin4','AMP_SD_MODE'),('.U24 > .pin5','VMIC'),('.R93 > .pin1','VMIC'),('.U5 > .pin2','VMIC'),('.U5 > .pin5','VMIC'),('.R93 > .pin2','MIC_WS'),('.U5 > .pin4','MIC_BCLK'),('.C2 > .pin2','GND')]:
 port=next(r for r in p.ports.values() if p.source_ports[r['source_port_id']].get('source_component_id') in p.source_components and p.port_name(r)==selector);root=p.root(nets[net]['source_net_id']);width=nets[net].get('trace_width') or .2;origin=(port['x'],port['y']);top=p.obstacles(root,'top',width);blocked,labels=p.grid_data(top);anchor=p.grid_anchor((origin,),(blocked,top))[0];result={'port':selector,'net':net,'anchor_available':bool(anchor)}
 if anchor:
  cells=labels==labels[anchor[0]];via=h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3});legal=cells&~contains_xy(via,p.grid_x,p.grid_y);ys,xs=np.where(cells);result['reachable_cells']=len(ys);result['reachable_bounds']=[float(p.x_coordinates[xs.min()]),float(p.y_coordinates[ys.min()]),float(p.x_coordinates[xs.max()]),float(p.y_coordinates[ys.max()])];ys,xs=np.where(legal);result['legal_full_span_via_cells']=len(ys)
  if len(ys):
   distances=np.hypot(p.x_coordinates[xs]-origin[0],p.y_coordinates[ys]-origin[1]);idx=np.argmin(distances);result['nearest_via']=[float(p.x_coordinates[xs[idx]]),float(p.y_coordinates[ys[idx]])];result['nearest_distance']=float(distances[idx])
 result['near_top_foreign_nets']=sorted({names.get(other,other) for other,layer,shape in p.copper if other!=root and layer=='top' and shape.distance(Point(origin))<2})
 results.append(result);print(json.dumps(result),flush=True)
Path('evidence/connection-repair-2026-10-06/corridor-diagnosis.json').write_text(json.dumps(results,indent=2)+'\n')
