import json,runpy,hashlib
from pathlib import Path
from shapely.affinity import translate
from shapely.geometry import Point,LineString,box
root=Path('/workspace/tscircuit-ai-agent-remote');native=root/'dist/index/circuit.json';circuit=json.loads(native.read_text());out=root/'evidence/microphone-local-bypass-2026-10-08'
helpers=runpy.run_path(str(root/'scripts/routing/plan-manual-signals.py'));planner=helpers['ManualSignalPlanner'](circuit)
source_id=next(r['source_component_id'] for r in circuit if r['type']=='source_component' and r['name']=='C81');component_id=next(r['pcb_component_id'] for r in circuit if r['type']=='pcb_component' and r['source_component_id']==source_id)
ports={r['name']:r for r in circuit if r['type']=='source_port' and r.get('source_component_id')==source_id}
new_pose=(21.,-26.8);dx,dy=17.,-7.55
supply=[(20.299976,-26.8),(19.5,-26.8),(19.1928144,-28.099951)];ground=[(21.700024,-26.8),(21.727201,-27.628501)]
violations=[];measurements=[]
for r,shape in planner.pads:
 if r['pcb_component_id']!=component_id:continue
 shape=translate(shape,xoff=dx,yoff=dy);port=planner.ports[r['pcb_port_id']];own_root=planner.root(port['source_port_id'])
 for other,other_shape in planner.pads:
  if other['pcb_component_id']==component_id:continue
  other_port=planner.ports.get(other.get('pcb_port_id'));other_root=planner.root(other_port['source_port_id']) if other_port else None
  if other_root!=own_root and shape.distance(other_shape)<.2-1e-6:violations.append(['pad',r['port_hints'],other['pcb_smtpad_id'],shape.distance(other_shape)])
 for hole in planner.holes:
  if shape.distance(hole)<.2-1e-6:violations.append(['drill',r['port_hints'],shape.distance(hole)])
 for other_root,layer,other_shape in planner.copper:
  if layer=='top' and other_root!=own_root and shape.distance(other_shape)<.2-1e-6:violations.append(['pad-copper',r['port_hints'],shape.distance(other_shape)])
 for _,keepout in planner.keepouts:
  if shape.distance(keepout)<.2-1e-6:violations.append(['keepout',r['port_hints'],shape.distance(keepout)])
 measurements.append({'pad':r['port_hints'],'new_bounds_mm':list(shape.bounds),'minimum_drill_gap_mm':min(shape.distance(hole) for hole in planner.holes)})
for name,points,port in [('supply',supply,ports['pin1']),('ground',ground,ports['pin2'])]:
 line=LineString(points);obstacles=planner.obstacles(planner.root(port['source_port_id']),'top',.3)
 if line.intersects(obstacles):violations.append(['wire',name,'intersects reserved copper/drill/keepout'])
 measurements.append({'route':name,'path_mm':points,'width_mm':.3,'layer':'top','length_mm':line.length,'new_vias':0})
body=box(19.8999768,-27.2499991,22.1000232,-26.3500009)
for r in circuit:
 if r['type']=='pcb_component' and r['pcb_component_id']!=component_id and r.get('obstructs_within_bounds',True):
  p=r['center'];shape=box(p['x']-r['width']/2,p['y']-r['height']/2,p['x']+r['width']/2,p['y']+r['height']/2)
  if body.intersects(shape):violations.append(['body',r['pcb_component_id']])
receipt={'source_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'classification':'prospective actual-footprint geometry; not native regeneration or DRC acceptance','purchased_moves':['C81'],'new_pose_mm':new_pose,'ccw_rotation_degrees':0,'measurements':measurements,'violations':violations,'ready_for_native_trial':not violations}
(out/'placement-route-proposal.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2));raise SystemExit(bool(violations))
