"""Accept only a completed genuine native trial; copper gates are checked separately."""
import json,hashlib,gzip,shutil,tarfile
from collections import Counter
from pathlib import Path
folder=Path(__file__).resolve().parent;root=folder.parents[1];stage=root/'.publish/board';native=stage/'dist/index/circuit.json'
outcome=json.loads((folder/'native-build.log.outcome.json').read_text())
assert outcome['completed_command'] and outcome['termination'] is None
assert outcome['exit_code'] in (0,1)
manifest=json.loads((folder/'generation-source-manifest.json').read_text())['files']
assert all(hashlib.sha256((stage/name).read_bytes()).hexdigest()==sha for name,sha in manifest.items())
payload=native.read_bytes();parent=gzip.decompress((folder/'before/circuit.json.gz').read_bytes());assert payload!=parent
circuit=json.loads(payload);errors=[r for r in circuit if 'error' in r['type']]
assert all(r['type']=='pcb_port_not_connected_error' for r in errors),errors
baseline_errors=[r for r in json.loads(parent) if 'error' in r['type']]
assert sorted(r['message'] for r in errors)==sorted(r['message'] for r in baseline_errors), 'New native error or unexplained disappearance'
receipts=json.loads((folder/'candidate-audit-receipts.json').read_text())
assert all(r['completed'] and (r['name'] in ('before-copper','candidate-copper') or r['exit_code']==0) for r in receipts)
audit=json.loads((folder/'final-copper-audit.json').read_text())
assert audit['source_sha256']==hashlib.sha256(payload).hexdigest() and audit['short_count']==0 and audit['drc_violation_count']==0 and audit['physically_open_net_count']==12
assert json.loads((folder/'connection-preservation.json').read_text())['preserved']
assert json.loads((folder/'purchased-geometry.json').read_text())['passed']
assert json.loads((folder/'local-bypass-qualification.json').read_text())['passed']
(folder/'native-circuit.json.gz').write_bytes(gzip.compress(payload,mtime=0))
summary={'native_sha256':hashlib.sha256(payload).hexdigest(),'native_bytes':len(payload),'completed_build_outcome':outcome,'native_record_counts':dict(Counter(r['type'] for r in circuit)),'native_error_count':len(errors),'fabrication_ready':False,'generation_source_exact':True}
(folder/'native-generation.json').write_text(json.dumps(summary,indent=2)+'\n');(folder/'remaining-native-errors.json').write_text(json.dumps(errors,indent=2)+'\n')
with tarfile.open(folder/'completed-source-and-events.tar.gz','w:gz') as archive:
 for path in stage.rglob('*'):
  if path.is_file() and 'node_modules' not in path.relative_to(stage).parts and ('dist' not in path.relative_to(stage).parts or 'autorouter-debug' in path.relative_to(stage).parts):archive.add(path,arcname=path.relative_to(stage).as_posix())
shutil.copyfile(native,root/'dist/index/circuit.json');shutil.copyfile(folder/'placement.json',root/'dist/placement/circuit.json')
print(json.dumps({key:summary[key] for key in ['native_sha256','native_bytes','native_error_count','generation_source_exact']}))
