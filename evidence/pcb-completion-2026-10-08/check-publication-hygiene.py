"""Check all new public evidence and uncompressed archives without printing values."""
import gzip
import json
import re
import tarfile
from pathlib import Path

folder = Path(__file__).resolve().parent
patterns = [re.compile(rb'gh[pousr]_[A-Za-z0-9]{30,}'),
            re.compile(rb'github_pat_[A-Za-z0-9_]{30,}'),
            re.compile(rb'eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}'),
            re.compile(rb'Bearer\s+[A-Za-z0-9_-]{30,}')]
found = []
checked = 0
for file in folder.rglob('*'):
    if not file.is_file() or file.name == 'publication-hygiene.json':
        continue
    if file.name.endswith('.tar.gz'):
        with tarfile.open(file) as archive:
            for member in archive:
                if not member.isfile():
                    continue
                data = archive.extractfile(member).read()
                checked += 1
                if any(pattern.search(data) for pattern in patterns):
                    found.append(file.name + '::' + member.name)
    else:
        data = gzip.decompress(file.read_bytes()) if file.suffix == '.gz' else file.read_bytes()
        checked += 1
        if any(pattern.search(data) for pattern in patterns):
            found.append(file.name)
receipt = {'checked_files_and_archive_members': checked, 'credential_pattern_files': found,
           'browser_html_policy': 'Latest UI captures visible text and screenshots only.',
           'scope': 'Concrete GitHub token, long bearer and JWT patterns over all new public evidence and complete uncompressed archive members. Values never printed. Latest browser HTML is not archived; earlier public HTML remains subject to this same credential scan. No auth store included.'}
(folder / 'publication-hygiene.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
raise SystemExit(1 if found else 0)
