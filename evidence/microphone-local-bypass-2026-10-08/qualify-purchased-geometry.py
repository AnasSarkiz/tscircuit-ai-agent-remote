"""Verify genuine purchased geometry: only C81/R93 rigid poses may change.
No generated records are edited; inverse transforms are comparison-only.
"""
import argparse,gzip,hashlib,json,copy,math
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('after_native');parser.add_argument('output');args=parser.parse_args()
folder=Path(__file__).resolve().parent;root=folder.parents[1]
before_payload=gzip.decompress((folder/'before/circuit.json.gz').read_bytes())
after_payload=Path(args.after_native).read_bytes()

def quantize(value):
 if isinstance(value,float):
  rounded=round(value,9)
  return int(rounded) if rounded==int(rounded) else rounded
 if isinstance(value,list):return [quantize(v) for v in value]
 if isinstance(value,dict):return {k:quantize(v) for k,v in value.items()}
 return value

def undo_moves(payload):
 circuit=json.loads(payload)
 names={r['source_component_id']:r['name'] for r in circuit if r['type']=='source_component'}
 components={r['pcb_component_id']:names.get(r['source_component_id']) for r in circuit if r['type']=='pcb_component'}
 moves={'C81':((4,-19.25),(17.05,-28.1),180),'R93':((16.75,-28.25),(16.5,-31.42),0)}
 def inverse(point,old,new,rotation):
  x,y=point['x']-new[0],point['y']-new[1];rad=math.radians(-rotation)
  return {**point,'x':old[0]+x*math.cos(rad)-y*math.sin(rad),'y':old[1]+x*math.sin(rad)+y*math.cos(rad)}
 poses={}
 for r in circuit:
  name=components.get(r.get('pcb_component_id'))
  if name not in moves:continue
  old,new,rotation=moves[name]
  if r['type']=='pcb_component':
   poses[name]={'center':r['center'],'rotation':r['rotation'],'layer':r['layer']}
   assert math.dist((r['center']['x'],r['center']['y']),new)<1e-9 and r['rotation']==rotation and r['layer']=='top'
   r['center']=inverse(r['center'],old,new,rotation);r['display_offset_x']=old[0];r['display_offset_y']=old[1];r['rotation']-=rotation
  elif r['type'] in ('pcb_smtpad','pcb_plated_hole','pcb_solder_paste','pcb_keepout') or r['type'].startswith('pcb_courtyard_'):
   if 'x' in r and 'y' in r:r.update(inverse(r,old,new,rotation))
   if 'center' in r:r['center']=inverse(r['center'],old,new,rotation)
   if 'points' in r:r['points']=[inverse(p,old,new,rotation) for p in r['points']]
   if 'outline' in r:r['outline']=[inverse(p,old,new,rotation) for p in r['outline']]
   # A 180-degree rotation preserves these rectangular pad axes.
   for key in ('ccw_rotation','rect_ccw_rotation'):
    if key in r:r[key]=(r[key]-rotation)%180
  elif r['type']=='cad_component':
   r['position']=inverse(r['position'],old,new,rotation);r['rotation']['z']-=rotation
 return json.dumps(circuit).encode(),poses
def purchased_geometry(payload):
 circuit=json.loads(payload)
 sources={r['source_component_id']:r for r in circuit if r['type']=='source_component' and r.get('supplier_part_numbers',{}).get('jlcpcb')}
 ports={r['source_port_id']:r for r in circuit if r['type']=='source_port' and r.get('source_component_id') in sources}
 components={r['pcb_component_id']:r for r in circuit if r['type']=='pcb_component' and r.get('source_component_id') in sources}
 pcb_ports={r['pcb_port_id']:r for r in circuit if r['type']=='pcb_port' and r.get('source_port_id') in ports}
 identifiers={identifier:sources[identifier]['name'] for identifier in sources}
 identifiers.update({identifier:sources[port['source_component_id']]['name']+'.'+str(port.get('pin_number',port['name'])) for identifier,port in ports.items()})
 identifiers.update({identifier:identifiers[r['source_component_id']] for identifier,r in components.items()})
 identifiers.update({identifier:identifiers[r['source_port_id']] for identifier,r in pcb_ports.items()})
 geometries={r['name']:[] for r in sources.values()}
 own_ids={'pcb_smtpad_id','pcb_plated_hole_id','cad_component_id','pcb_courtyard_id','pcb_keepout_id'}
 for record in circuit:
  if record['type'] not in ('pcb_component','pcb_smtpad','pcb_plated_hole','pcb_solder_paste','cad_component','pcb_keepout') and not record['type'].startswith('pcb_courtyard_'):continue
  component=components.get(record.get('pcb_component_id'))
  if not component:continue
  name=identifiers[component['source_component_id']]
  normalized={key:(identifiers.get(value,value) if isinstance(value,str) else value) for key,value in record.items() if key not in own_ids and key!=record['type']+'_id'}
  geometries[name].append(json.dumps(quantize(normalized),sort_keys=True))
 return sources,{name:sorted(records) for name,records in geometries.items()}

before_sources,before=purchased_geometry(before_payload);after_sources,after=purchased_geometry(after_payload)
transformed,poses=undo_moves(after_payload);_,restored=purchased_geometry(transformed)
missing=sorted(set(before)-set(after));added=sorted(set(after)-set(before))
changed=sorted(name for name in before.keys()&after.keys() if before[name]!=after[name])
nonrigid=sorted(name for name in before.keys()&restored.keys() if before[name]!=restored[name])
before_names={r['name']:r for r in before_sources.values()};after_names={r['name']:r for r in after_sources.values()}
identity_changes=sorted(name for name in before_names.keys()&after_names.keys() if any(before_names[name].get(k)!=after_names[name].get(k) for k in ('manufacturer_part_number','supplier_part_numbers')))
parent=json.loads((folder/'parent-checkpoint-sha256.json').read_text())['files']
paths=[name for name in parent if name.startswith(('imports/','components/','models/','src/components/','src/models/','.tscircuit/autorouting-artifacts/','.tscircuit/components/'))]
asset_mismatches=[name for name in paths if not (root/name).is_file() or hashlib.sha256((root/name).read_bytes()).hexdigest()!=parent[name]]
result={'before_native_sha256':hashlib.sha256(before_payload).hexdigest(),'after_native_sha256':hashlib.sha256(after_payload).hexdigest(),'before_purchased_count':len(before),'after_purchased_count':len(after),'changed_purchased_geometry':changed,'changed_part_identities':identity_changes,'stationary_purchased_geometry_count':len(before)-len(changed),'missing':missing,'added':added,'nonrigid_geometry_changes':nonrigid,'permitted_rigid_poses':poses,'genuine_assets_and_solver_cache_files_checked':len(paths),'asset_mismatches':asset_mismatches,'numeric_rounding_decimal_places':9,'scope':'All native purchased component, pads, plated holes, solder paste, CAD assets/pose, actual courtyard outline/rectangle and owned keepout fields. Original numbered ports and imported assets retained. Only C81 180-degree rigid rotation/translation and R93 translation allowed. Inverse transform is comparison-only; untouched native remains intact.','passed':changed==['C81','R93'] and not(missing or added or nonrigid or identity_changes or asset_mismatches),'fabrication_ready':False}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(0 if result['passed'] else 1)
