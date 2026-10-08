"""Fetch an integrity-checked official schema artifact for read-only analysis."""
import base64
import hashlib
import io
import json
import shutil
import tarfile
import urllib.request
from pathlib import Path

folder = Path(__file__).resolve().parent
root = folder.parents[1]
metadata = json.loads((folder / 'latest-official-versions.json').read_text())
package = next(p for p in metadata if p['name'] == 'circuit-json')
assert package['version'] == '0.0.521'
url = package['dist']['tarball']
assert url == 'https://registry.npmjs.org/circuit-json/-/circuit-json-0.0.521.tgz'
with urllib.request.urlopen(url, timeout=30) as response:
    payload = response.read()
integrity = 'sha512-' + base64.b64encode(hashlib.sha512(payload).digest()).decode()
assert integrity == package['dist']['integrity']
assert hashlib.sha1(payload).hexdigest() == package['dist']['shasum']
(folder / 'latest-official-schema.tgz').write_bytes(payload)
temporary = root / '.tools/schema-latest-download'
target = root / '.tools/schema-latest/node_modules/circuit-json'
assert not temporary.exists() and not target.exists()
temporary.mkdir(parents=True)
with tarfile.open(fileobj=io.BytesIO(payload), mode='r:gz') as archive:
    for member in archive.getmembers():
        assert member.name == 'package' or member.name.startswith('package/')
        assert '..' not in Path(member.name).parts and not member.islnk() and not member.issym()
    archive.extractall(temporary, filter='data')
target.parent.mkdir(parents=True, exist_ok=True)
shutil.move(temporary / 'package', target)
temporary.rmdir()
actual = json.loads((target / 'package.json').read_text())
assert actual['name'] == 'circuit-json' and actual['version'] == package['version']
receipt = {'official_tarball': url, 'version': actual['version'],
           'tarball_bytes': len(payload), 'tarball_sha256': hashlib.sha256(payload).hexdigest(),
           'published_integrity_exact': True, 'published_shasum_exact': True,
           'artifact_preserved': 'latest-official-schema.tgz',
           'fallback_reason': 'Separate Bun resolver reached its 180-second budget; exact official artifact avoids dependency resolution for this read-only schema comparison.',
           'genuine_artifact_modified': False, 'active_board_dependency_pins_changed': False,
           'zod_runtime': 'Existing frozen board node_modules; no installed bundle changes'}
(folder / 'latest-schema-official-artifact.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
