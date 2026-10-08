"""Audit the actual trial before accepting/copying any native output."""
import gzip,json,subprocess,time
from pathlib import Path
p=Path(__file__).resolve().parent;root=p.parents[1];native=root/'.publish/board/dist/index/circuit.json';before=Path('/tmp/microphone-bypass-before.json')
before.write_bytes(gzip.decompress((p/'before/circuit.json.gz').read_bytes()))
commands=[('before-copper',['python3','scripts/routing/audit-copper.py',str(before),str(p/'before-copper-audit.json')]),('candidate-copper',['python3','scripts/routing/audit-copper.py',str(native),str(p/'final-copper-audit.json')]),('preservation',['python3','scripts/routing/audit-connection-preservation.py',str(before),str(p/'before-copper-audit.json'),str(native),str(p/'final-copper-audit.json'),str(p/'connection-preservation.json')]),('purchased-geometry',['python3',str(p/'qualify-purchased-geometry.py'),str(native),str(p/'purchased-geometry.json')])]
for source in ('connection-copper.json','manual-power-copper.json','inner-signal-copper.json'):commands.append((source,['python3','scripts/routing/audit-region-widths.py',str(native),str(root/'src/board'/source),str(p/(source+'.widths.json'))]))
receipts=[]
for name,command in commands:
 start=time.monotonic()
 with (p/(name+'.log')).open('w') as stream:r=subprocess.run(command,cwd=root,stdout=stream,stderr=subprocess.STDOUT)
 receipt={'name':name,'command':command,'exit_code':r.returncode,'completed':True,'elapsed_seconds':round(time.monotonic()-start,2)};receipts.append(receipt);print(json.dumps(receipt),flush=True)
(p/'candidate-audit-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
audit=json.loads((p/'final-copper-audit.json').read_text())
accepted=not(audit['short_count'] or audit['drc_violation_count']) and all(r['exit_code']==0 for r in receipts if r['name'] not in ('before-copper','candidate-copper'))
raise SystemExit(0 if accepted else 1)
