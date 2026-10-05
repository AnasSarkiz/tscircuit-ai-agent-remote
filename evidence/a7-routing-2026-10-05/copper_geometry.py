"""Independent Circuit JSON copper geometry. No generated records are edited."""
import sys,json,math
from pathlib import Path
sys.path.insert(0,str(Path('.geometry-runtime').resolve()))
from shapely.geometry import Point,LineString,Polygon,box
from shapely.affinity import rotate,translate
from shapely.ops import unary_union

def xy(x):
 p=x.get('center',x);return p['x'],p['y']
def disk(x,y,r):
 # Circumscribed approximation; never shrink a keepout/copper clearance.
 return Point(x,y).buffer(r/math.cos(math.pi/512),quad_segs=128)
def capsule(x,y,w,h,angle=0):
 r=min(w,h)/2
 if abs(w-h)<1e-9:g=disk(0,0,r)
 else:g=LineString([(-(w-h)/2,0),((w-h)/2,0)]).buffer(r/math.cos(math.pi/512),quad_segs=128) if w>h else LineString([(0,-(h-w)/2),(0,(h-w)/2)]).buffer(r/math.cos(math.pi/512),quad_segs=128)
 return translate(rotate(g,angle,origin=(0,0)),x,y)
def shape(x,drill=False):
 if x.get('points') and not drill:return Polygon([(p['x'],p['y']) for p in x['points']]).buffer(0)
 cx,cy=xy(x);typ=x.get('hole_shape',x.get('shape','circle')) if drill else x.get('pad_shape',x.get('shape','circle'))
 if x['type']=='pcb_hole':typ=x['hole_shape']
 diam=x.get('hole_diameter',0) if drill or x['type']=='pcb_hole' else x.get('outer_diameter',2*x.get('radius',0))
 w=x.get('hole_width',diam) if drill else x.get('rect_pad_width',x.get('outer_width',x.get('width',diam)))
 h=x.get('hole_height',diam) if drill else x.get('rect_pad_height',x.get('outer_height',x.get('height',diam)))
 angle=x.get('hole_ccw_rotation',x.get('ccw_rotation',0)) if drill else x.get('rect_ccw_rotation',x.get('ccw_rotation',0))
 if typ=='circle':return disk(cx,cy,diam/2 if diam else x['radius'])
 if 'pill' in typ:return capsule(cx,cy,w,h,angle)
 if typ in ['rect','rotated_rect']:
  g=box(-w/2,-h/2,w/2,h/2);r=x.get('corner_radius',0)
  if r:g=box(-w/2+r,-h/2+r,w/2-r,h/2-r).buffer(r/math.cos(math.pi/512),quad_segs=128)
  return translate(rotate(g,angle,origin=(0,0)),cx,cy)
 raise ValueError(('Unsupported actual geometry',x))

class Copper:
 def __init__(self,path):
  self.j=json.loads(Path(path).read_text());self.parent={};self.st={x['source_trace_id']:x for x in self.j if x['type']=='source_trace'}
  for t in self.st.values():self.join(t.get('connected_source_port_ids',[])+t.get('connected_source_net_ids',[]))
  for x in self.j:
   if x['type']=='source_component_internal_connection':self.join(x['source_port_ids'])
  self.ports={x['pcb_port_id']:x for x in self.j if x['type']=='pcb_port'}
  self.pc={x['pcb_component_id']:x for x in self.j if x['type']=='pcb_component'}
  self.sc={x['source_component_id']:x for x in self.j if x['type']=='source_component'}
  self.sp={x['source_port_id']:x for x in self.j if x['type']=='source_port'}
  self.nets={x['source_net_id']:x['name'] for x in self.j if x['type']=='source_net'}
  self.traces=[x for x in self.j if x['type']=='pcb_trace'];self.vias=[x for x in self.j if x['type']=='pcb_via']
  self.pads=[x for x in self.j if x['type'] in ['pcb_smtpad','pcb_plated_hole']]
  self.pad_shapes={x.get('pcb_smtpad_id',x.get('pcb_plated_hole_id')):shape(x) for x in self.pads}
  self.holes=[(x,shape(x,True)) for x in self.j if x['type'] in ['pcb_hole','pcb_plated_hole']]
  self.keepouts=[(x,shape(x)) for x in self.j if x['type']=='pcb_keepout']
  b=next(x for x in self.j if x['type']=='pcb_board');self.board=Polygon([xy(p) for p in b['outline']])
  self.segments=[]
  for t in self.traces:
   for p,q in zip(t['route'],t['route'][1:]):
    if p['route_type']==q['route_type']=='wire' and math.dist(xy(p),xy(q))>1e-9:
     width=max(p['width'],q['width']) if t.get('route_thickness_mode')=='interpolated' else p['width']
     self.segments.append((t,p['layer'],LineString([xy(p),xy(q)]),width/2))
 def root(self,k):
  self.parent.setdefault(k,k)
  if self.parent[k]!=k:self.parent[k]=self.root(self.parent[k])
  return self.parent[k]
 def join(self,ids):
  if ids:
   for k in ids[1:]:self.parent[self.root(k)]=self.root(ids[0])
 def trace_net(self,t):
  s=self.st[t['source_trace_id']];return self.root((s.get('connected_source_port_ids',[])+s.get('connected_source_net_ids',[]))[0])
 def port_net(self,p):return self.root(p['source_port_id'])
 def key(self,p):return self.sc[self.pc[p['pcb_component_id']]['source_component_id']]['name']+'.pin'+str(self.sp[p['source_port_id']]['pin_number'])
 def local(self,p,points):
  c=self.pc[p['pcb_component_id']];theta=math.radians(-c['rotation']);origin=c['display_offset_x'],c['display_offset_y'];out=[]
  for node in points:
   x,y=node['x']-origin[0],node['y']-origin[1]
   out.append({**node,'x':round(x*math.cos(theta)-y*math.sin(theta),8),'y':round(x*math.sin(theta)+y*math.cos(theta),8)})
  return out
