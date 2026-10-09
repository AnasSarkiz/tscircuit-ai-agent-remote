"""Preserve parent bindings and bind every actual task change, without self hashing."""
import hashlib
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[2]
folder = Path(__file__).resolve().parent
parent = json.loads((folder / 'parent-checkpoint-sha256.json').read_text())
bindings = dict(parent['files'])
paths = set(subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'], cwd=root, text=True).splitlines())
paths.update(subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=root, text=True).splitlines())
paths.update(p.relative_to(root).as_posix() for p in folder.rglob('*') if p.is_file())
paths.update(p.relative_to(root / '.publish/board').as_posix() for p in (root / '.publish/board').rglob('*') if p.is_file() and 'node_modules' not in p.parts)
paths.update(['context/build-checkpoint.json', 'CLOUD_HANDOFF.md', 'scripts/cloud/setup.sh'])
paths.discard('context/checkpoint-sha256.json')
for name in sorted(paths):
    path = root / name
    if path.is_file():
        bindings[name] = hashlib.sha256(path.read_bytes()).hexdigest()
native_sha = hashlib.sha256((root / 'dist/index/circuit.json').read_bytes()).hexdigest()
manifest = {
    'algorithm': 'sha256', 'accepted_version': '0.0.11-wip-generator-qualification',
    'native_sha256': native_sha,
    'classification': 'Actual generated canonical-runtime WIP .11. Connection, full-board DRC, style, stock and fabrication gates remain failed; public delivery is verified separately.',
    'parent_manifest_archive': str((folder / 'parent-checkpoint-sha256.json').relative_to(root)),
    'parent_bound_file_count': len(parent['files']),
    'scope': 'Preserve every parent binding; bind actual task changes, evidence and regular publication runtime paths. Exclude this manifest itself and ignored private/runtime directories.',
    'files': dict(sorted(bindings.items())),
}
(root / 'context/checkpoint-sha256.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'bound_files': len(bindings), 'native_sha256': native_sha}))
