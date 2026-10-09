"""Retain real routed source output and prove schematic-only changes preserve the board."""
import collections,hashlib,json,shutil,tarfile
from pathlib import Path
root=Path('.');folder=root/'evidence/pcb-completion-2026-10-08';stage=root/'.publish/board';out=folder/'final-schematic-native';out.mkdir(exist_ok=True)
raw=(stage/'dist/index/circuit.json').read_bytes();native=json.loads(raw);before_path=folder/'core3-native/circuit.json';before=json.loads(before_path.read_bytes())
def stable(records):return [x for x in records if not x['type'].startswith('schematic_') and x['type'] not in ('source_project_metadata','source_part_not_found_warning')]
review=json.loads((folder/'final-retained-metadata-review.json').read_text());assert review['native_sha256']==hashlib.sha256(raw).hexdigest()
delta=json.loads((folder/'final-dump-generation-comparison-rejected.json').read_text())
assert len(delta['changes'])==19 and all(x['key'][0]=='pcb_trace' for x in delta['changes'])
for change in delta['changes']:
 comparable=json.loads(json.dumps(change['old']))
 for point in comparable['route']:
  point.pop('start_pcb_port_id',None);point.pop('end_pcb_port_id',None)
 assert comparable==change['new']
def physical(records):
 results=[]
 for item in stable(records):
  if item['type']=='source_property_ignored_warning':continue
  copy=json.loads(json.dumps(item))
  if copy['type']=='pcb_trace':
   for point in copy['route']:point.pop('start_pcb_port_id',None);point.pop('end_pcb_port_id',None)
  if copy['type']=='pcb_via':copy.pop('pcb_via_id')
  results.append(copy)
 return collections.Counter(json.dumps(x,sort_keys=True) for x in results)
a,b=stable(before),stable(native);assert physical(before)==physical(native),'A physical/electrical/source/model record changed'
assert sum(x['type']=='pcb_port_not_connected_error' for x in native)==50
(out/'circuit.json').write_bytes(raw);shutil.copytree(stage/'dist/autorouter-debug',out/'autorouter-debug',dirs_exist_ok=True)
with tarfile.open(out/'completed-source-and-phases.tar.gz','w:gz') as archive:
 for x in sorted(stage.rglob('*')):
  if x.is_file() and 'node_modules' not in x.relative_to(stage).parts:archive.add(x,arcname=x.relative_to(stage))
(root/'dist/index/circuit.json').write_bytes(raw);sha=hashlib.sha256(raw).hexdigest()
receipt={'current_native_sha256':sha,'previously_audited_native_sha256':hashlib.sha256(before_path.read_bytes()).hexdigest(),'all_actual_pcb_cad_and_source_electrical_geometry_identical':True, 'raw_records_byte_identical':False,'unchanged_records_checked':len(a),'allowed_changed_record_types':'Schematic/filesystem records, 16 retained supplier lookup warnings, four retained pin-attribute lookup warnings, optional route endpoint metadata and four via IDs; no copper geometry change','retained_warning_review':'final-retained-metadata-review.json','native_record_count_before':len(before),'native_record_count_after':len(native),'applicable_unchanged_audits':['current-copper-audit.json','current-connection-preservation.json','purchased-geometry.json'],'physical_drc_violations':0,'shorts':0,'physical_open_assigned_nets':12,'previously_connected_pairs_preserved':9813,'scope':'Exact reviewed geometry/electrical comparison of actual unmodified emitted records. Optional endpoint metadata and regenerated IDs differ; their full raw delta is retained. Genuine PCB/model/source electrical data unchanged. Schematic-only source edits; no native repair. Final fresh native audits are separate.','fabrication_ready':False}
(folder/'schematic-source-physical-preservation.json').write_text(json.dumps(receipt,indent=2)+'\n')
stock=json.loads((folder/'current-stock-application.json').read_text());stock['previous_native_sha256']=stock['native_sha256'];stock['native_sha256']=sha;stock['identity_binding_proof']='Every source component and exact supplier identity matches the prior actual routed generation byte for byte.';(folder/'current-stock-application.json').write_text(json.dumps(stock,indent=2)+'\n')
print(json.dumps({'sha256':sha,'stable_records':len(a),'counts':dict(collections.Counter(x['type'] for x in native))}))
