import runpy,json,math
from pathlib import Path
from shapely.geometry import Point
h=runpy.run_path('scripts/routing/plan-power-copper.py')
c=json.load(open('dist/index/circuit.json'));nets={r['name']:r for r in c if r['type']=='source_net'}
target={'VBUS','PACK_BAT','VSYS','V3V3','VMOTOR','HAPTIC_N'}
retired={r['pcb_copper_pour_id'] for r in c if r['type']=='pcb_copper_pour' and r['source_net_id'] in {nets[n]['source_net_id'] for n in target}}
p=h['Planner'](c,retired)
result=[]
for failure in json.load(open('evidence/six-point-board-review-2026-10-06/outer-power-proposal.json'))['unresolved'][:5]:
 root=p.root(nets[failure['net']]['source_net_id']);width=failure['nominal_width_mm']+.002
 for q in failure['terminals_mm']:
  for layer in ('top','bottom'):
   a=[]
   for r,shape in p.pads:
    port=p.ports.get(r.get('pcb_port_id'))
    if layer in r.get('layers',[r.get('layer')]) and (not port or p.root(port['source_port_id'])!=root) and Point(q).intersects(shape.buffer(.27+width/2)):
     a.append({'pad':r.get('pcb_smtpad_id',r.get('pcb_plated_hole_id')),'gap':shape.distance(Point(q))})
   for other_root,other_layer,shape in p.copper:
    if other_root!=root and layer==other_layer and Point(q).intersects(shape.buffer(.27+width/2)):a.append({'foreign_copper_root':other_root,'gap':shape.distance(Point(q))})
   for shape in p.holes:
    if p.plated_hole_roots.get(shape.wkb)!=root and Point(q).intersects(shape.buffer(.26+width/2)):a.append({'drill_root':p.plated_hole_roots.get(shape.wkb),'gap':shape.distance(Point(q))})
   result.append({'net':failure['net'],'point':q,'layer':layer,'blocking_features':a})
Path('evidence/six-point-board-review-2026-10-06/outer-endpoint-diagnosis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
