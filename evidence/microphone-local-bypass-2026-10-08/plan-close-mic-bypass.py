import gzip,json,runpy,math
from pathlib import Path
from shapely.affinity import rotate,translate
from shapely.geometry import Point,LineString,Polygon
root=Path('/workspace/tscircuit-ai-agent-remote');out=root/'evidence/microphone-local-bypass-2026-10-08';circuit=json.loads(gzip.decompress((out/'before/circuit.json.gz').read_bytes()));helpers=runpy.run_path(str(root/'scripts/routing/plan-manual-signals.py'));power=runpy.run_path(str(root/'scripts/routing/plan-power-copper.py'));bridges=runpy.run_path(str(root/'scripts/routing/plan-connection-bridges.py'))
sources={r['source_trace_id']:r for r in circuit if r['type']=='source_trace'}
retired_traces={r['pcb_trace_id'] for r in circuit if r['type']=='pcb_trace' and sources[r['source_trace_id']].get('name') in ['MANUAL_VMIC_109','MANUAL_GND_217','CONNECTION_ESCAPE_VMIC_17','CONNECTION_ESCAPE_MIC_WS_20']}
retired_vias={r['pcb_via_id'] for r in circuit if r['type']=='pcb_via' and r.get('pcb_trace_id') in retired_traces}
planner=helpers['ManualSignalPlanner'](circuit,{'retired_feature_ids':list(retired_vias),'relocated_trace_layers':{t:{'top':None} for t in retired_traces}})
source_components={r['source_component_id']:r['name'] for r in circuit if r['type']=='source_component'};component_names={r['pcb_component_id']:source_components.get(r['source_component_id']) for r in circuit if r['type']=='pcb_component'}
poses={'C81':{'old':(4,-19.25),'new':(17.05,-28.1),'angle':180},'R93':{'old':(16.75,-28.25),'new':(16.5,-31.42),'angle':0}}
def transform_shape(shape,pose):
 return translate(rotate(shape,pose['angle'],origin=pose['old']),xoff=pose['new'][0]-pose['old'][0],yoff=pose['new'][1]-pose['old'][1])
planner.pads=[(r,transform_shape(shape,poses[component_names[r['pcb_component_id']]]) if component_names[r['pcb_component_id']] in poses else shape) for r,shape in planner.pads]
for p in planner.ports.values():
 name=component_names.get(p.get('pcb_component_id'))
 if name in poses:
  transformed=transform_shape(Point(p['x'],p['y']),poses[name]);p['x'],p['y']=transformed.x,transformed.y
nets={r['name']:r for r in circuit if r['type']=='source_net'};vmic=planner.root(nets['VMIC']['source_net_id']);gnd=planner.root(nets['GND']['source_net_id']);ws=planner.root(nets['MIC_WS']['source_net_id']);violations=[];measurements=[]
for r,shape in planner.pads:
 if component_names[r['pcb_component_id']] not in poses:continue
 p=planner.ports[r['pcb_port_id']];own=planner.root(p['source_port_id'])
 for other,other_shape in planner.pads:
  other_port=planner.ports.get(other.get('pcb_port_id'));other_root=planner.root(other_port['source_port_id']) if other_port else None
  if other_root!=own and shape.distance(other_shape)<.1-1e-6:violations.append(['pad-pad',r['pcb_smtpad_id'],other['pcb_smtpad_id'],shape.distance(other_shape)])
 for hole in planner.holes:
  if shape.distance(hole)<.2-1e-6:violations.append(['pad-drill',r['pcb_smtpad_id'],shape.distance(hole)])
 for other_root,layer,other_shape in planner.copper:
  if layer=='top' and other_root!=own and shape.distance(other_shape)<.2-1e-6:violations.append(['pad-copper',r['pcb_smtpad_id'],shape.distance(other_shape)])
 for _,keepout in planner.keepouts:
  if shape.intersects(keepout):violations.append(['pad-keepout',r['pcb_smtpad_id']])
 measurements.append({'part':component_names[r['pcb_component_id']],'pad':r['port_hints'],'bounds_mm':list(shape.bounds)})
segments=[('bypass-supply',vmic,.3,[(17.750024,-28.1),(19.1928144,-28.099951)]),('bypass-ground',gnd,.3,[(16.349976,-28.1),(15.75,-28.1)]),('R93-WS',ws,.2,[(17.25335,-31.42),(18.5,-31.42),(18.499994,-30.300049)])]
for name,own,width,points in segments:
 line=LineString(points)
 if line.intersects(planner.obstacles(own,'top',width)):violations.append(['trace-obstacle',name])
 planner.copper.append((own,'top',line.buffer(width/2)))
 measurements.append({'route':name,'path_mm':points,'width_mm':width,'length_mm':line.length,'layer':'top'})
origin=(15.74665,-31.42);via=(19.35,-27.35);spec={'root':vmic,'via_outer_mm':.45,'via_hole_mm':.3}
if Point(via).intersects(power['via_obstacles'](planner,spec)):violations.append(['retained-via-obstacle',via])
bridges['reserve_via'](planner,{'root':vmic,'position':via})
planner.set_grid(.01,bounds=(12.,-32.,20.5,-26.5))
obstacles=planner.obstacles(vmic,'top',.3)
points=planner.grid_route((origin,via,obstacles))
regions=[]
if not points:violations.append(['R93-supply','no top route to retained via'])
else:measurements.append({'route':'R93-supply-escape','path_mm':points,'length_mm':LineString(points).length,'width_mm':.3,'layer':'top','through_via_mm':via})
courtyards=[]
for r in circuit:
 if r['type']=='pcb_courtyard_outline':
  shape=Polygon([(p['x'],p['y']) for p in r['outline']]);name=component_names.get(r['pcb_component_id']);shape=transform_shape(shape,poses[name]) if name in poses else shape;courtyards.append((name,shape))
for name,shape in courtyards:
 if name not in poses:continue
 for other,other_shape in courtyards:
  if other!=name and shape.intersection(other_shape).area>1e-9:violations.append(['courtyard',name,other])
 for _,keepout in planner.keepouts:
  if shape.intersection(keepout).area>1e-9:violations.append(['courtyard-keepout',name])
receipt={'classification':'prospective rigid transforms of genuine footprints; actual native regeneration and full audits still required','poses':poses,'retired_trace_ids':sorted(retired_traces),'retired_via_ids':sorted(retired_vias),'measurements':measurements,'regions':regions,'violations':violations,'ready_for_native_trial':not violations,'minimum_possible_capacitor_pad_centre_distance_mm':1.3800592,'basis':'Untouched U5 VDD is 0.7300600 mm inside its nearest courtyard boundary; C81 supply-pad centre is at least 0.6499992 mm inside its own courtyard at any rotation. Nonoverlapping courtyards therefore cannot meet the inferred 1.0 mm maximum. New declared 2.0 mm target retains a finite bound above that physical lower bound; actual proposed top route is 1.4427904 mm.'}
(out/'close-bypass-proposal-4.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k not in ['regions','poses','measurements']},indent=2));raise SystemExit(bool(violations))
