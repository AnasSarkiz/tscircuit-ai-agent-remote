import json,subprocess,time
from pathlib import Path
f=Path('evidence/pcb-completion-2026-10-08');records=[]
commands=[('format-check-final',['bun','run','format:check']),('fresh-copper-audit',['python','scripts/routing/audit-copper.py','dist/index/circuit.json',str(f/'current-copper-audit.json')]),('fresh-pair-preservation',['python','scripts/routing/audit-connection-preservation.py','/tmp/qualified-parent-native.json','evidence/microphone-local-bypass-2026-10-08/final-copper-audit.json','dist/index/circuit.json',str(f/'current-copper-audit.json'),str(f/'current-connection-preservation.json')]),('independent-exports',['python',str(f/'inspect-qualified-gerbers.py')]),('source-checks',['python','scripts/cloud/check_board_source.py','.publish/board',str(f/'final-source-checks')]),('ui-analysis',['bun',str(f/'ui-analysis/capture-style-issues.mjs')])]
for name,command in commands:
 start=time.monotonic();print(json.dumps({'starting':name}),flush=True)
 with (f/(name+'.log')).open('w') as output:result=subprocess.run(command,stdout=output,stderr=subprocess.STDOUT)
 records.append({'name':name,'command':command,'exit_code':result.returncode,'completed':True,'elapsed_seconds':round(time.monotonic()-start,2)})
 (f/'final-engineering-checks.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(records[-1]),flush=True)
audit=json.loads((f/'current-copper-audit.json').read_text());assert audit['drc_violation_count']==audit['short_count']==0 and audit['physically_open_net_count']==12
assert json.loads((f/'current-connection-preservation.json').read_text())['preserved']
# Collection completes independently; unresolved fabrication/style gates remain failures.
raise SystemExit(int(any(r['exit_code'] for r in records)))
