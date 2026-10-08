"""Run actual board checks, retaining unsuccessful fabrication gates."""
import json
import subprocess
import time
from pathlib import Path

folder = Path(__file__).resolve().parent
root = folder.parents[1]
relative = str(folder.relative_to(root))
native = 'dist/index/circuit.json'
commands = [
    ('typecheck', ['bun', 'run', 'typecheck']),
    ('format-check', ['bun', 'run', 'format:check']),
    ('routing-regressions', ['python3', '-m', 'unittest', 'discover', '-s', 'scripts/routing/tests']),
    ('board-tests', ['bun', 'run', 'test']),
    ('official-shorts', ['bun', 'node_modules/.bin/tsci', 'check', 'shorts', native]),
    ('schema-assembly', ['node', 'evidence/order-readiness-2026-10-06/audit-schema-assembly.mjs', native, relative]),
    ('resolved-bom', ['node', 'evidence/programmer-direct-uart-2026-10-07/export-resolved-bom.mjs', native, relative]),
    ('component-inventory', ['python3', 'evidence/order-readiness-2026-10-06/audit-components.py', '--native', native,
                             '--copper-audit', f'{relative}/final-copper-audit.json', '--output-dir', relative]),
    ('schematic-guides', ['bun', 'scripts/audit-schematic-guides.mjs', native, f'{relative}/guide-coverage.json']),
    ('actual-srj', ['bun', 'scripts/routing/export-native-srj.tsx', native, f'{relative}/final-native.srj.json']),
    ('render-copper', ['bun', 'scripts/routing/render-copper-review.mjs', native, f'{relative}/rendered']),
    ('render-schematic', ['bun', 'scripts/render-schematic-guides.mjs', native, f'{relative}/schematics']),
]
receipts = []
for name, command in commands:
    print(json.dumps({'starting': name}), flush=True)
    started = time.monotonic()
    with (folder / f'{name}.log').open('w') as stream:
        result = subprocess.run(command, cwd=root, stdout=stream, stderr=subprocess.STDOUT)
    receipt = {'name': name, 'command': command, 'exit_code': result.returncode,
               'elapsed_seconds': round(time.monotonic() - started, 2), 'completed': True}
    receipts.append(receipt)
    (folder / 'artifact-checks.json').write_text(json.dumps(receipts, indent=2) + '\n')
    print(json.dumps(receipt), flush=True)
raise SystemExit(0 if all(record['exit_code'] == 0 for record in receipts) else 1)
