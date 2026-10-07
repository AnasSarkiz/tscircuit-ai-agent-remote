"""Run actual speaker qualification checks serially against the accepted V7.

The older all-poses-unchanged compliance test remains a separate observation:
five explicitly justified component moves make that historical assertion false.
Neither native open ports nor source-width failures are waived here.
"""
import json
import argparse
import subprocess
import time
from pathlib import Path

evidence = Path(__file__).parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--native', type=Path, default=evidence / 'speaker-local-native-v6/circuit.json')
parser.add_argument('--output', type=Path, default=evidence / 'v6-qualification')
parser.add_argument('--copper-audit', type=Path, default=evidence / 'v6-copper-audit.json')
args = parser.parse_args()
native, output = args.native, args.output
output.mkdir(exist_ok=True)
commands = [
    ('connection-widths', ['python3', 'scripts/routing/audit-region-widths.py', str(native), 'src/board/connection-copper.json', str(output / 'connection-region-widths.json')]),
    ('power-widths', ['python3', 'scripts/routing/audit-region-widths.py', str(native), 'src/board/manual-power-copper.json', str(output / 'power-region-widths.json')]),
    ('inner-widths', ['python3', 'scripts/routing/audit-region-widths.py', str(native), 'src/board/inner-signal-copper.json', str(output / 'inner-region-widths.json')]),
    ('wire-widths', ['python3', 'scripts/routing/audit-trace-widths.py', str(native), str(output / 'trace-widths.json')]),
    ('preservation', ['python3', 'scripts/routing/audit-connection-preservation.py',
                      'evidence/routing-zero-drc-2026-10-07/final-native/circuit.json', 'evidence/routing-zero-drc-2026-10-07/final-qualification/copper-audit.json',
                      str(native), str(args.copper_audit), str(output / 'connection-preservation.json')]),
    ('historical-compliance', ['python3', 'evidence/six-point-board-review-2026-10-06/review-compliance.py',
                              str(native), str(args.copper_audit), str(output / 'historical-native-compliance.json')]),
]
receipts = []
for name, command in commands:
    print(json.dumps({'starting': name}), flush=True)
    started = time.monotonic()
    with (output / f'{name}.log').open('w') as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
    receipt = {'name': name, 'command': command, 'exit_code': result.returncode,
               'elapsed_seconds': round(time.monotonic() - started, 2), 'completed': True}
    receipts.append(receipt)
    (output / 'qualification-commands.json').write_text(json.dumps(receipts, indent=2) + '\n')
    print(json.dumps(receipt), flush=True)
raise SystemExit(0 if all(record['exit_code'] == 0 for record in receipts) else 1)
