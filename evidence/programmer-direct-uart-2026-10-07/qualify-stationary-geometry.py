"""Compare complete purchased geometry except the explicitly replaced J6.

Transient native IDs are resolved to real component names and numbered ports;
all remaining physical fields are compared exactly, including CAD assets/pose.
"""
import argparse,gzip,hashlib,json
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('after_native');parser.add_argument('output');args=parser.parse_args()
folder=Path(__file__).resolve().parent
before_payload=gzip.decompress((folder/'before/circuit.json.gz').read_bytes())
after_payload=Path(args.after_native).read_bytes()
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
  if record['type'] not in ('pcb_component','pcb_smtpad','pcb_plated_hole','cad_component','pcb_courtyard','pcb_keepout'):continue
  component=components.get(record.get('pcb_component_id'))
  if not component:continue
  name=identifiers[component['source_component_id']]
  normalized={key:(identifiers.get(value,value) if isinstance(value,str) else value) for key,value in record.items() if key not in own_ids}
  geometries[name].append(json.dumps(normalized,sort_keys=True))
 return sources,{name:sorted(records) for name,records in geometries.items()}
before_sources,before=purchased_geometry(before_payload);after_sources,after=purchased_geometry(after_payload)
missing=sorted(set(before)-set(after));added=sorted(set(after)-set(before))
changed=sorted(name for name in before.keys()&after.keys() if before[name]!=after[name])
part_changes=[]
before_by_name={r['name']:r for r in before_sources.values()};after_by_name={r['name']:r for r in after_sources.values()}
for name in before_by_name.keys()&after_by_name.keys():
 first,last=before_by_name[name],after_by_name[name]
 if any(first.get(k)!=last.get(k) for k in ['manufacturer_part_number','supplier_part_numbers']):part_changes.append(name)
result={'before_sha256':hashlib.sha256(before_payload).hexdigest(),'after_sha256':hashlib.sha256(after_payload).hexdigest(),'before_purchased_count':len(before),'after_purchased_count':len(after),'missing':missing,'added':added,'changed_purchased_geometry':changed,'changed_part_identities':sorted(part_changes),'stationary_purchased_geometry_count':len(before)-len(changed),'scope':'Full native purchased component/pad/plated-hole/CAD/courtyard/owned-keepout records; only native feature IDs normalized to component names/numbered ports, own transient IDs omitted. Exact physical fields remain unchanged. Explicit genuine J6 replacement is the sole permitted changed part.','passed':not (missing or added) and changed==['J6'] and sorted(part_changes)==['J6'],'fabrication_ready':False}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(0 if result['passed'] else 1)
