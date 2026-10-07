"""Replace the obsolete J6 supply detour with a 0.8 mm bottom-layer trunk.

Both existing endpoints and through-vias remain. No new connector supply is
introduced. Native regeneration/width/clearance/continuity gates are mandatory.
"""
import json,runpy,gzip
from pathlib import Path
folder=Path(__file__).resolve().parent
c=json.loads(gzip.decompress((folder/'pad-links-native/circuit.json.gz').read_bytes()))
Planner=runpy.run_path('scripts/routing/plan-manual-signals.py')['ManualSignalPlanner']
helpers=runpy.run_path('scripts/routing/plan-connection-bridges.py')
p=Planner(c);p.set_grid(.05);p.set_copper_reserve(.07)
net=next(r for r in c if r['type']=='source_net' and r['name']=='V3V3');root=p.root(net['source_net_id'])
source=json.loads(Path('src/board/manual-power-copper.json').read_text())
first=source['pours'][53]['path_mm'][0];last=source['pours'][55]['path_mm'][0]
route=p.grid_route((first,last,p.obstacles(root,'bottom',.802)))
result={'classification':'manual native outer-layer 0.8 mm V3V3 bottom bypass; proposal only until actual native width/continuity/clearance checks','retired_source_region_indices':[54],'replaced_source_region_indices':[53],'unchanged_source_via_indices':[27,28],'source_regions':[],'unresolved':[]}
if route:
 result['source_regions']=helpers['region_records']('V3V3',{'parts':[('bottom',route)],'width':.8,'drawn_width_mm':.802})
else:result['unresolved'].append('No complete 0.8 mm bottom-layer supply bypass')
(folder/'j6-supply-bypass-proposal.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:record for key,record in result.items() if key!='source_regions'}))
raise SystemExit(1 if result['unresolved'] else 0)
