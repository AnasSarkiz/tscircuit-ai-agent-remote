"""Record actual checks serially; unresolved board gates remain failed."""
import argparse
import json
import subprocess
import time
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('native')
parser.add_argument('output')
args = parser.parse_args()
output = Path(args.output)
output.mkdir(parents=True, exist_ok=True)
commands = [
    ('copper', ['python3', 'scripts/routing/audit-copper.py', args.native, str(output/'copper-audit.json')]),
    ('connection-widths', ['python3', 'scripts/routing/audit-region-widths.py', args.native, 'src/board/connection-copper.json', str(output/'connection-region-widths.json')]),
    ('power-widths', ['python3', 'scripts/routing/audit-region-widths.py', args.native, 'src/board/manual-power-copper.json', str(output/'power-region-widths.json')]),
    ('inner-widths', ['python3', 'scripts/routing/audit-region-widths.py', args.native, 'src/board/inner-signal-copper.json', str(output/'inner-region-widths.json')]),
    ('wire-widths', ['python3', 'scripts/routing/audit-trace-widths.py', args.native, str(output/'trace-widths.json')]),
    ('preservation', ['python3', 'scripts/routing/audit-connection-preservation.py',
                      'dist/index/circuit.json', 'evidence/connection-repair-2026-10-06/final-copper-audit.json',
                      args.native, str(output/'copper-audit.json'), str(output/'connection-preservation.json')]),
    ('compliance', ['python3', 'evidence/six-point-board-review-2026-10-06/review-compliance.py',
                    args.native, str(output/'copper-audit.json'), str(output/'native-compliance.json')]),
]
receipts = []
for name, command in commands:
    print(json.dumps({'starting': name}), flush=True)
    started = time.monotonic()
    with (output/f'{name}.log').open('w') as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
    receipt = {'name': name, 'command': command, 'exit_code': result.returncode,
               'elapsed_seconds': round(time.monotonic()-started, 2), 'completed': True}
    receipts.append(receipt)
    (output/'qualification-commands.json').write_text(json.dumps(receipts, indent=2)+'\n')
    print(json.dumps(receipt), flush=True)
raise SystemExit(0 if all(record['exit_code'] == 0 for record in receipts) else 1)
