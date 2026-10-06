"""Run required source checks serially inside the exact publication runtime.

Use the cloud budget supervisor around this script. Completed check logs and
receipts survive a subsequent budget stop; an unfinished check never passes.
"""
import argparse
import json
import subprocess
import time
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('runtime', type=Path)
parser.add_argument('output', type=Path)
args = parser.parse_args()
runtime = args.runtime.resolve()
output = args.output.resolve()
output.mkdir(parents=True, exist_ok=True)
results = []
for check in ('netlist', 'pin_specification', 'source', 'schematic-placement', 'placement'):
    command = ['bun', 'node_modules/.bin/tsci', 'check', check, 'index.circuit.tsx']
    started = time.monotonic()
    print(json.dumps({'starting_source_check': check}), flush=True)
    with (output/f'check-{check}.log').open('w') as stream:
        result = subprocess.run(command, cwd=runtime, stdout=stream, stderr=subprocess.STDOUT)
    receipt = {'command': command, 'cwd': str(runtime), 'exit_code': result.returncode,
               'completed': True, 'elapsed_seconds': round(time.monotonic()-started, 2)}
    (output/f'check-{check}.json').write_text(json.dumps(receipt, indent=2)+'\n')
    results.append(receipt)
    print(json.dumps({'source_check': check, 'exit_code': result.returncode}), flush=True)
(output/'source-checks.json').write_text(json.dumps({'results': results,
    'passed': all(r['exit_code']==0 for r in results)}, indent=2)+'\n')
raise SystemExit(0 if all(r['exit_code']==0 for r in results) else 1)
