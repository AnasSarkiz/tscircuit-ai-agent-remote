"""Plan the retained 0.8 mm V3V3 trunk clear of the genuine new J6 pads.

Retire the obsolete J6 power spur, relocate its distribution via, and retain
both real supply endpoints. This proposal requires native copper qualification.
"""
import json,runpy,gzip
from pathlib import Path
from shapely.geometry import Point
folder=Path(__file__).resolve().parent
c=json.loads(gzip.decompress((folder/'pad-links-native/circuit.json.gz').read_bytes()))
Planner=runpy.run_path('scripts/routing/plan-manual-signals.py')['ManualSignalPlanner']
helpers=runpy.run_path('scripts/routing/plan-connection-bridges.py')
power_helpers=runpy.run_path('scripts/routing/plan-power-copper.py')
p=Planner(c);p.set_grid(.05);p.set_copper_reserve(.07)
net=next(r for r in c if r['type']=='source_net' and r['name']=='V3V3');root=p.root(net['source_net_id'])
source=json.loads(Path('src/board/manual-power-copper.json').read_text())
first=source['pours'][53]['path_mm'][0];old_via=source['vias'][28];last=source['pours'][55]['path_mm'][-1]
via_obstacles=power_helpers['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3})
result={'classification':'manual native outer-layer 0.8 mm V3V3 bypass around new J6; proposal only until actual native width/continuity/clearance checks','retired_source_region_indices':[54],'replaced_source_region_indices':[53,55],'relocated_source_via_index':28,'previous_via':old_via,'source_regions':[],'unresolved':[]}
for candidate in [(-20.5,-8.2),(-21,-8),(-21,-8.5),(-21.5,-8.5)]:
 if Point(candidate).intersects(via_obstacles):continue
 top=p.grid_route((first,candidate,p.obstacles(root,'top',.802)))
 bottom=p.grid_route((candidate,last,p.obstacles(root,'bottom',.802)))
 if not (top and bottom):continue
 result['replacement_via']={**old_via,'x':candidate[0],'y':candidate[1],'classification':'manual native full-span retained V3V3 distribution via relocated away from J6; .30/.45 mm'}
 result['source_regions']=helpers['region_records']('V3V3',{'parts':[('top',top),('bottom',bottom)],'width':.8,'drawn_width_mm':.802})
 break
if not result['source_regions']:result['unresolved'].append('No complete 0.8 mm outer-layer supply bypass')
(folder/'j6-supply-bypass-proposal.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:record for key,record in result.items() if key!='source_regions'}))
raise SystemExit(1 if result['unresolved'] else 0)
