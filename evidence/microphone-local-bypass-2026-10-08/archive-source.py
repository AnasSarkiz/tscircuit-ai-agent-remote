"""Preserve exact runtime inputs before generation, never the stale prepared native."""
import hashlib,json,tarfile
from pathlib import Path
folder=Path(__file__).resolve().parent
root=folder.parents[1];stage=root/'.publish/board'
files=[p for p in stage.rglob('*') if p.is_file() and not p.is_symlink() and 'node_modules' not in p.relative_to(stage).parts and not any(q.startswith('.') for q in p.relative_to(stage).parts) and p.relative_to(stage).parts[0]!='dist']
regular_file_count=len(files)
orientation=json.loads((folder/'restored-supplier-cache.json').read_text())
files += [stage/r['path'] for r in orientation['records']]
assert all(hashlib.sha256((stage/r['path']).read_bytes()).hexdigest()==r['sha256'] for r in orientation['records'])
with tarfile.open(folder/'generation-source.tar.gz','w:gz') as archive:
 for path in files:archive.add(path,arcname=path.relative_to(stage).as_posix())
manifest={path.relative_to(stage).as_posix():hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
(folder/'generation-source-manifest.json').write_text(json.dumps({'classification':'Exact source/runtime/model files before canonical build; inherited prepared parent native excluded','files':manifest,'count':len(files),'regular_runtime_files':regular_file_count,'pinned_genuine_supplier_orientation_cache_files':len(orientation['records']),'supplier_cache_origin_receipt':'restored-supplier-cache.json','public_package_regular_source_files':regular_file_count,'active_dependency_link':'../../node_modules','active_frozen_bun':'1.3.9'},indent=2)+'\n')
print('Archived exact generation source files',len(files))
