"""Run actual project checks sequentially; preserve every failed gate."""
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FOLDER = Path(__file__).resolve().parent
RELATIVE = str(FOLDER.relative_to(ROOT))
NATIVE = 'dist/index/circuit.json'
commands = [
    ('typecheck', ['bun', 'run', 'typecheck']),
    ('format-check', ['bun', 'run', 'format:check']),
    ('routing-regressions', ['python', '-m', 'unittest', 'discover', '-s', 'scripts/routing/tests']),
    ('board-tests', ['bun', 'run', 'test']),
    ('schema-and-paste', ['bun', f'{RELATIVE}/audit-schema-and-paste.mjs', NATIVE, RELATIVE]),
    ('schema-assembly', ['bun', f'{RELATIVE}/audit-schema-assembly.mjs', NATIVE, RELATIVE]),
    ('resolved-bom', ['bun', f'{RELATIVE}/export-resolved-bom.mjs', NATIVE, RELATIVE]),
    ('regulator-profile', ['python', 'scripts/routing/audit-regulator-switch-widths.py', NATIVE, f'{RELATIVE}/regulator-profile.json']),
    ('trace-widths', ['python', 'scripts/routing/audit-trace-widths.py', NATIVE, f'{RELATIVE}/trace-widths.json']),
    ('schematic-guides', ['bun', 'scripts/audit-schematic-guides.mjs', NATIVE, f'{RELATIVE}/guide-coverage.json']),
    ('actual-srj', ['bun', 'scripts/routing/export-native-srj.tsx', NATIVE, f'{RELATIVE}/actual-native.srj.json']),
    ('official-shorts', ['bun', 'node_modules/.bin/tsci', 'check', 'shorts', NATIVE]),
    ('corrected-gerber-export', ['bun', f'{RELATIVE}/export-gerbers.mjs', NATIVE, f'{RELATIVE}/NOT-FOR-FABRICATION-qualified-gerbers']),
]
for region in ['connection-copper.json', 'manual-power-copper.json', 'inner-signal-copper.json']:
    commands.append((region+'.widths', ['python', 'scripts/routing/audit-region-widths.py', NATIVE, 'src/board/'+region, f'{RELATIVE}/{region}.widths.json']))
records = []
for name, command in commands:
    started = time.monotonic()
    print(json.dumps({'starting':name}), flush=True)
    with (FOLDER / ('final-'+name+'.log')).open('w') as stream:
        result = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    records.append({'name':name,'command':command,'exit_code':result.returncode,'elapsed_seconds':round(time.monotonic()-started,2),'completed':True})
    (FOLDER/'artifact-checks.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records[-1]),flush=True)
raise SystemExit(int(any(r['exit_code'] for r in records)))
