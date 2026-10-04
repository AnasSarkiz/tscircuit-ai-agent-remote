import sys,json,math,runpy
from pathlib import Path
folder=sys.argv[1]
sys.argv=['audit-signals.py',folder,'wire-geometry-audit.json']
a=runpy.run_path('evidence/a6-bom-routing-2026-10-04/audit-signals.py')
j=a['j'];vias=a['vias'];point_segment=a['point_segment'];point=a['point'];bbox_distance=a['bbox_distance'];bounds=a['bounds'];root=a['root'];ports=a['ports'];trace_root=a['trace_root'];traces={t['pcb_trace_id']:t for t in a['traces']}
def inside(p,vertices):
 result=False
 for q,r in zip(vertices,vertices[1:]+vertices[:1]):
  if (q[1]>p[1])!=(r[1]>p[1]) and p[0]<(r[0]-q[0])*(p[1]-q[1])/(r[1]-q[1])+q[0]:result=not result
 return result
results=[]
for v in vias:
 p=point(v);own=trace_root(traces[v['pcb_trace_id']]);mins={k:1e9 for k in ['copper_to_pad','drill_to_any_pad','drill_to_other_drill','copper_to_other_trace','plane_antipad']}
 for x in j:
  if x['type'] in ['pcb_smtpad','pcb_plated_hole']:
   gap=bbox_distance(p,p,bounds(x));mins['drill_to_any_pad']=min(mins['drill_to_any_pad'],gap-v['hole_diameter']/2)
   if not x.get('pcb_port_id') or root(ports[x['pcb_port_id']])!=own:mins['copper_to_pad']=min(mins['copper_to_pad'],gap-v['outer_diameter']/2)
  if x['type'] in ['pcb_hole','pcb_plated_hole','pcb_via'] and x!=v:
   if x['type']=='pcb_plated_hole':hole={**x,'width':x.get('hole_width',x.get('hole_diameter')),'height':x.get('hole_height',x.get('hole_diameter'))}
   elif x['type']=='pcb_via':hole={**x,'width':x['hole_diameter'],'height':x['hole_diameter']}
   else:hole=x
   mins['drill_to_other_drill']=min(mins['drill_to_other_drill'],bbox_distance(p,p,bounds(hole))-v['hole_diameter']/2)
  if x['type']=='pcb_trace' and trace_root(x)!=own:
   for q,r in zip(x['route'],x['route'][1:]):
    if q['route_type']==r['route_type']=='wire':mins['copper_to_other_trace']=min(mins['copper_to_other_trace'],point_segment(p,point(q),point(r))-v['outer_diameter']/2-max(q['width'],r['width'])/2)
  if x['type']=='pcb_copper_pour' and x['layer'] in v['layers'] and root(x['source_net_id'])!=own:
   assert x['shape']=='brep'
   outer=list(map(point,x['brep_shape']['outer_ring']['vertices']))
   if inside(p,outer):
    holes=[list(map(point,h['vertices'])) for h in x['brep_shape']['inner_rings']]
    containing=[h for h in holes if inside(p,h)]
    clearance=max((min(point_segment(p,q,r) for q,r in zip(h,h[1:]+h[:1]))-v['outer_diameter']/2 for h in containing),default=-v['outer_diameter']/2)
    mins['plane_antipad']=min(mins['plane_antipad'],clearance)
 requirement={'copper_to_pad':0.2,'drill_to_any_pad':0.2,'drill_to_other_drill':0.25,'copper_to_other_trace':0.2,'plane_antipad':0.2}
 results.append({'via_id':v['pcb_via_id'],'hole_mm':v['hole_diameter'],'outer_mm':v['outer_diameter'],'layers':v['layers'],'min_clearances_mm':mins,'requirements_mm':requirement,'violations':[k for k in mins if mins[k]+1e-6<requirement[k]]})
record={'scope':'New ordinary through vias including same-net drill-to-pad clearance and actual native plane BREP apertures; conservative pad/hole bounding boxes.','vias':results}
Path('evidence/a6-bom-routing-2026-10-04/'+folder+'-via-audit.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
