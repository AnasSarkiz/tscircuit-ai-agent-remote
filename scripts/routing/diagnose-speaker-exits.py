"""Measure candidate speaker escapes against preserved actual native copper."""
import json, math, runpy, sys
from pathlib import Path
from shapely.geometry import Point, LineString
h=runpy.run_path(str(Path(__file__).with_name('plan-power-copper.py')))
c=json.loads(Path(sys.argv[1]).read_text());p=h['Planner'](c);p.set_grid(.05)
net=next(r for r in c if r['type']=='source_net' and r['name']=='SPEAKER_N');root=p.root(net['source_net_id'])
port=next(r for r in p.ports.values() if p.port_name(r)=='.U3 > .pin10');origin=(port['x'],port['y'])
top=p.obstacles(root,'top',.275);vb=h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3})
found=[]
for y in (6.3,7,7.5,8,8.5,9,9.5,10):
 for x in (-16.5,-17,-17.5,-18,-16,-15.5):
  xy=(x,y);points=[origin,(origin[0],y),xy]
  line=LineString(points)
  if line.length>5:continue
  found.append({'via_mm':xy,'length_mm':line.length,'top_clear':not line.intersects(top),'via_clear':not Point(xy).intersects(vb),'points':points})
Path(sys.argv[2]).write_text(json.dumps(found,indent=2)+'\n')
print(json.dumps({'legal_escapes':[r for r in found if r['top_clear'] and r['via_clear']],'legal_vias':[r['via_mm'] for r in found if r['via_clear']]}))
