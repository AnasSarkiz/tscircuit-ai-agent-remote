import gzip,json,runpy,math
from pathlib import Path
from shapely.geometry import LineString
native=gzip.decompress(Path('evidence/programmer-direct-uart-2026-10-07/updated-native/circuit.json.gz').read_bytes())
c=json.loads(native)
Planner=runpy.run_path('scripts/routing/plan-manual-signals.py')['ManualSignalPlanner']
p=Planner(c);p.set_grid(.05)
net=next(r for r in c if r['type']=='source_net' and r['name']=='GND');root=p.root(net['source_net_id'])
ports={p.port_name(r):r for r in p.ports.values() if p.source_ports[r['source_port_id']].get('source_component_id') in p.source_components}
result={'classification':'manual native J6 ground pad links; no new drills; existing main ground-plane contacts; native audit required','paths':[],'pours':[],'vias':[],'unresolved':[]}
for start_pin,end_pin in [(2,4),(4,5)]:
 first=ports[f'.J6 > .pin{start_pin}'];last=ports[f'.J6 > .pin{end_pin}']
 obstacles=p.obstacles(root,'top',.2)
 route=p.grid_route(((first['x'],first['y']),(last['x'],last['y']),obstacles))
 if not route:
  result['unresolved'].append([start_pin,end_pin]);continue
 component=p.components[first['pcb_component_id']]
 assert component['rotation']==0
 points=[{'x':round(x-component['display_offset_x'],6),'y':round(y-component['display_offset_y'],6)} for x,y in route[1:-1]]
 path={'net':'GND','from':p.port_name(first),'to':p.port_name(last),'width':.2,'pcbPath':points,'global_path_mm':route,'segment_layers':['top']*len(route),'classification':'manual native GND pad connection on existing main ground plane; no added drills'}
 result['paths'].append(path)
 p.copper.extend((root,'top',LineString([a,b]).buffer(.1)) for a,b in zip(route,route[1:]))
Path('evidence/programmer-direct-uart-2026-10-07/j6-pad-ground-routing.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
raise SystemExit(1 if result['unresolved'] else 0)
