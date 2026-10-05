"""Losslessly archive this task's trials; verify each byte before removing originals."""
from pathlib import Path
import zipfile,hashlib,json,shutil
base=Path('evidence/a7-routing-2026-10-05')
selected=[p for p in base.glob('native-*') if p.is_dir() and p.name!='native-latest-replay']
for folder in sorted(selected):
 archive=base/(folder.name+'.zip')
 if archive.exists():raise RuntimeError(f'Archive already exists: {archive}')
 hashes={}
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in sorted(folder.rglob('*')):
   if not f.is_file():continue
   key=f.relative_to(folder).as_posix();h=hashlib.sha256()
   with f.open('rb') as reader,z.open(key,'w') as writer:
    while chunk:=reader.read(1024*1024):h.update(chunk);writer.write(chunk)
   hashes[key]=h.hexdigest()
  z.writestr('archive-sha256-manifest.json',json.dumps(hashes,indent=2)+'\n')
 with zipfile.ZipFile(archive) as z:
  for key,expected in hashes.items():
   h=hashlib.sha256()
   with z.open(key) as reader:
    while chunk:=reader.read(1024*1024):h.update(chunk)
   if h.hexdigest()!=expected:raise RuntimeError(('Archive verification failed',folder,key))
 receipt={'original_directory':str(folder),'archive':str(archive),'files':len(hashes),'all_bytes_verified_sha256':True,'original_records_preserved_in_lossless_archive':True}
 (base/(folder.name+'-archive-receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
 shutil.rmtree(folder)
 print(json.dumps(receipt),flush=True)
