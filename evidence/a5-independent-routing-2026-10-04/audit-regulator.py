import json, math
from pathlib import Path
base=Path('evidence/a5-independent-routing-2026-10-04')
j=json.loads((base/'native-regulator/circuit.json').read_text())
before=json.loads((base/'before-circuit.json').read_text())
parent={}
def root(k):
 parent.setdefault(k,k)
 if parent[k]!=k: parent[k]=root(parent[k])
 return parent[k]
def join(ids):
 if ids:
  for k in ids[1:]: parent[root(k)]=root(ids[0])
source_traces={x['source_trace_id']:x for x in j if x['type']=='source_trace'}
for x in source_traces.values(): join(x.get('connected_source_port_ids',[])+x.get('connected_source_net_ids',[]))
ports={x['pcb_port_id']:x['source_port_id'] for x in j if x['type']=='pcb_port'}
def trace_root(t):
 x=source_traces[t['source_trace_id']];return root((x.get('connected_source_port_ids',[])+x.get('connected_source_net_ids',[]))[0])
def point(p): return p['x'],p['y']
def point_segment(p,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];den=dx*dx+dy*dy
 t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/den)) if den else 0
 return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def segment_distance(a,b,c,d):
 if max(a[0],b[0])+1e-12>=min(c[0],d[0]) and max(c[0],d[0])+1e-12>=min(a[0],b[0]) and max(a[1],b[1])+1e-12>=min(c[1],d[1]) and max(c[1],d[1])+1e-12>=min(a[1],b[1]) and cross(a,b,c)*cross(a,b,d)<=0 and cross(c,d,a)*cross(c,d,b)<=0:return 0
 return min(point_segment(a,c,d),point_segment(b,c,d),point_segment(c,a,b),point_segment(d,a,b))
def bbox_distance(a,b,box):
 x0,y0,x1,y1=box
 if any(x0<=p[0]<=x1 and y0<=p[1]<=y1 for p in [a,b]): return 0
 pts=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
 return min(segment_distance(a,b,pts[i],pts[(i+1)%4]) for i in range(4))
def bounds(x):
 if x.get('points'):
  return min(p['x'] for p in x['points']),min(p['y'] for p in x['points']),max(p['x'] for p in x['points']),max(p['y'] for p in x['points'])
 c=x.get('center',x);cx,cy=c['x'],c['y'];diameter=x.get('outer_diameter',x.get('hole_diameter',2*x.get('radius',0)))
 w=x.get('width',x.get('outer_width',x.get('rect_pad_width',diameter)));h=x.get('height',x.get('outer_height',x.get('rect_pad_height',diameter)))
 if x.get('ccw_rotation',0)%180:
  # Circumscribed square is conservative for every angle, without a coordinate transform.
  w=h=math.hypot(w,h)
 if not w or not h: raise ValueError(('Unreviewed geometry',x))
 return cx-w/2,cy-h/2,cx+w/2,cy+h/2
traces=[x for x in j if x['type']=='pcb_trace'];new=[x for x in traces if x not in before]
assert len(new)==3 and not any(x['type']=='pcb_via' for x in j)
minima={k:{'clearance_mm':1e9} for k in ['different_net_pad','different_net_trace','ordinary_drill','keepout','board_edge']}
board=next(x for x in j if x['type']=='pcb_board');outline=list(map(point,board['outline']))
def record(k,gap,ids):
 if gap<minima[k]['clearance_mm']:minima[k]={'clearance_mm':gap,'ids':ids}
for t in new:
 r=t['route'];assert all(p['route_type']=='wire' and p['width']==0.2 and p['layer']=='top' for p in r)
 for p,q in zip(r,r[1:]):
  a,b=point(p),point(q);radius=max(p['width'],q['width'])/2
  for x in j:
   if x['type'] in ['pcb_smtpad','pcb_plated_hole']:
    if p['layer'] not in x.get('layers',[x.get('layer')]):continue
    pid=x.get('pcb_port_id')
    if pid and root(ports[pid])==trace_root(t):continue
    record('different_net_pad',bbox_distance(a,b,bounds(x))-radius,[t['pcb_trace_id'],x.get('pcb_smtpad_id',x.get('pcb_plated_hole_id'))])
   if x['type']=='pcb_hole':
    record('ordinary_drill',bbox_distance(a,b,bounds(x))-radius,[t['pcb_trace_id'],x['pcb_hole_id']])
   if x['type']=='pcb_plated_hole':
    hole=dict(x);hole['width']=x.get('hole_width',x.get('hole_diameter'));hole['height']=x.get('hole_height',x.get('hole_diameter'));hole.pop('points',None)
    record('ordinary_drill',bbox_distance(a,b,bounds(hole))-radius,[t['pcb_trace_id'],x['pcb_plated_hole_id']])
   if x['type']=='pcb_keepout' and p['layer'] in x['layers']:
    record('keepout',bbox_distance(a,b,bounds(x))-radius,[t['pcb_trace_id'],x['pcb_keepout_id']])
  for other in traces:
   if other==t or trace_root(other)==trace_root(t):continue
   for c,d in zip(other['route'],other['route'][1:]):
    if c['route_type']=='wire' and d['route_type']=='wire' and c['layer']==d['layer']==p['layer']:
     record('different_net_trace',segment_distance(a,b,point(c),point(d))-radius-max(c['width'],d['width'])/2,[t['pcb_trace_id'],other['pcb_trace_id']])
  record('board_edge',min(segment_distance(a,b,c,d) for c,d in zip(outline,outline[1:]+outline[:1]))-radius,[t['pcb_trace_id']])
result={'scope':'Three newly generated REG_FB/REG_PG traces only, conservative circumscribed pad/drill/keepout bounds; all native original records retained. Not whole-board DRC or thermal approval.','trace_count':len(new),'width_mm':0.2,'layers':['top'],'vias':0,'minima':minima,'requirements_mm':{'different_net_pad':0.2,'different_net_trace':0.2,'ordinary_drill':0.25,'keepout':0.0,'board_edge':0.25}}
result['violations']=[k for k,v in minima.items() if v['clearance_mm']+1e-6<result['requirements_mm'][k]]
(base/'regulator-geometry-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
