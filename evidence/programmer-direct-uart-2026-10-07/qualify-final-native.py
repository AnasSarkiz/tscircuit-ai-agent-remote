"""Run independent actual copper, full-width regions and preserved-contact gates."""
from pathlib import Path
import subprocess,json,time
folder=Path(__file__).resolve().parent
native='.publish/board/dist/index/circuit.json'
commands=[('final-copper-audit',['python3','scripts/routing/audit-copper.py',native,str(folder/'final-copper-audit.json')]),('connection-region-widths',['python3','scripts/routing/audit-region-widths.py',native,'src/board/connection-copper.json',str(folder/'connection-region-widths.json')]),('power-region-widths',['python3','scripts/routing/audit-region-widths.py',native,'src/board/manual-power-copper.json',str(folder/'power-region-widths.json')]),('inner-region-widths',['python3','scripts/routing/audit-region-widths.py',native,'src/board/inner-signal-copper.json',str(folder/'inner-region-widths.json')]),('trace-widths',['python3','scripts/routing/audit-trace-widths.py',native,str(folder/'trace-widths.json')]),('raw-contact-preservation',['python3','scripts/routing/audit-connection-preservation.py','/tmp/prototype-repairs/before-native.json','evidence/routing-continuation-2026-10-07/final-cli-copper-audit.json',native,str(folder/'final-copper-audit.json'),str(folder/'raw-contact-preservation.json')]),('contact-migration-preservation',['python3',str(folder/'qualify-contact-migration.py'),native,str(folder/'final-copper-audit.json'),str(folder/'contact-migration-preservation.json')]),('stationary-geometry',['python3',str(folder/'qualify-stationary-geometry.py'),native,str(folder/'stationary-geometry.json')])]
receipts=[]
for name,command in commands:
 started=time.monotonic()
 with (folder/f'{name}.log').open('w') as log:
  result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
 record={'name':name,'command':command,'exit_code':result.returncode,'elapsed_seconds':round(time.monotonic()-started,2),'completed':True}
 receipts.append(record)
 (folder/'final-qualification-commands.json').write_text(json.dumps(receipts,indent=2)+'\n')
 print(json.dumps(record),flush=True)
