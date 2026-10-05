import json,runpy,sys
from pathlib import Path
folder=sys.argv[1]
sys.argv=['audit-signals.py',folder,'wire-geometry-audit.json']
a=runpy.run_path('evidence/a7-routing-2026-10-05/audit-signals.py')
j=a['j'];point=a['point'];segment_distance=a['segment_distance'];root=a['root'];trace_root=a['trace_root']
def inside(p,vertices):
 result=False
 for q,r in zip(vertices,vertices[1:]+vertices[:1]):
  if (q[1]>p[1])!=(r[1]>p[1]) and p[0]<(r[0]-q[0])*(p[1]-q[1])/(r[1]-q[1])+q[0]:result=not result
 return result
results=[]
for plane in (p for p in j if p['type']=='pcb_copper_pour'):
 assert plane['shape']=='brep'
 outer=list(map(point,plane['brep_shape']['outer_ring']['vertices']))
 holes=[list(map(point,h['vertices'])) for h in plane['brep_shape']['inner_rings']]
 for trace in a['new']:
  if root(plane['source_net_id'])==trace_root(trace):continue
  for i,(p,q) in enumerate(zip(trace['route'],trace['route'][1:])):
   if p['route_type']!=q['route_type'] or p['route_type']!='wire' or p['layer']!=plane['layer']:continue
   first,last=point(p),point(q);middle=((p['x']+q['x'])/2,(p['y']+q['y'])/2)
   in_solid=inside(middle,outer) and not any(inside(middle,h) for h in holes)
   distance=min(segment_distance(first,last,c,d) for ring in [outer]+holes for c,d in zip(ring,ring[1:]+ring[:1]))
   clearance=-max(p['width'],q['width'])/2 if in_solid else distance-max(p['width'],q['width'])/2
   results.append({'trace':trace['pcb_trace_id'],'segment_index':i,'plane':plane['pcb_copper_pour_id'],'clearance_mm':clearance,'center_in_plane_copper':in_solid})
record={'scope':'Actual new wire copper to different-net native BREP plane on matching layers, including segment crossings. No plane geometry modification.','segments_checked':len(results),'minimum':min(results,key=lambda r:r['clearance_mm']) if results else None,'required_clearance_mm':0.2,'violations':[r for r in results if r['clearance_mm']+1e-6<0.2]}
Path('evidence/a7-routing-2026-10-05/'+folder+'-plane-audit.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
