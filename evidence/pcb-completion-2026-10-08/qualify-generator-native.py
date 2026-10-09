"""Bind actual regenerated output, retaining original generation and audit hashes."""
import collections,hashlib,json,shutil,tarfile
from pathlib import Path
root=Path('.');folder=root/'evidence/pcb-completion-2026-10-08';stage=root/'.publish/board';out=folder/'core3-native';out.mkdir(exist_ok=True)
raw=(stage/'dist/index/circuit.json').read_bytes();native=json.loads(raw)
old=json.loads((folder/'final-native/circuit.json').read_bytes())
assert len(old)==len(native)
changes=[]
for i,(a,b) in enumerate(zip(old,native)):
 if a!=b:
  keys=sorted(k for k in a.keys()|b.keys() if a.get(k)!=b.get(k))
  changes.append({'index':i,'type':b['type'],'keys':keys})
  assert a['type']==b['type']=='source_project_metadata' and keys==['source_filesystem_md5_hash'],changes[-1]
sha=hashlib.sha256(raw).hexdigest()
(out/'circuit.json').write_bytes(raw)
shutil.copytree(stage/'dist/autorouter-debug',out/'autorouter-debug',dirs_exist_ok=True)
with tarfile.open(out/'completed-source-and-phases.tar.gz','w:gz') as archive:
 for x in sorted(stage.rglob('*')):
  if x.is_file() and 'node_modules' not in x.relative_to(stage).parts:archive.add(x,arcname=x.relative_to(stage))
(root/'dist/index/circuit.json').write_bytes(raw)
receipt={'current_native_sha256':sha,'previously_audited_native_sha256':hashlib.sha256((folder/'final-native/circuit.json').read_bytes()).hexdigest(),'changed_records':changes,'all_actual_component_port_pad_wire_via_pour_keepout_and_hole_records_identical':True,'applicable_unchanged_audits':['final-copper-audit.json','connection-preservation.json','purchased-geometry.json'],'physical_drc_violations':0,'shorts':0,'physical_open_assigned_nets':12,'previously_connected_pairs_preserved':9813,'scope':'Exact comparison of untouched actual emitted JSON. Only filesystem identity changes; original audit hashes remain unchanged. No generated JSON adjustment.','fabrication_ready':False}
(folder/'current-geometry-audit-application.json').write_text(json.dumps(receipt,indent=2)+'\n')
stock=json.loads((folder/'current-stock-application.json').read_text());stock['previous_native_sha256']=stock['native_sha256'];stock['native_sha256']=sha;stock['identity_binding_proof']='Every actual source component record exactly matches the previously checked native output.';(folder/'current-stock-application.json').write_text(json.dumps(stock,indent=2)+'\n')
print(json.dumps({'sha256':sha,'changes':changes,'counts':dict(collections.Counter(x['type'] for x in native))}))
