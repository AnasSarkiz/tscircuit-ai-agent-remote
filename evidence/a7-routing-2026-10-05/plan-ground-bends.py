# Explicit native ground-path candidates. Review generated geometry after rendering.
import contextlib,io,json,math,runpy,sys,heapq
from pathlib import Path
base=Path('evidence/a7-routing-2026-10-05')
sys.argv=['audit-signals.py','native-ground-corrected','ground-bends-input-audit.json']
with contextlib.redirect_stdout(io.StringIO()):a=runpy.run_path(str(base/'audit-signals.py'))
j=a['j'];root=a['root'];pt=a['point'];bd=a['bbox_distance'];bounds=a['bounds'];sd=a['segment_distance'];ps=a['point_segment'];tr=a['traces'];gnd=root(next(x['source_net_id'] for x in j if x['type']=='source_net' and x['name']=='GND'))
sc={x['source_component_id']:x['name'] for x in j if x['type']=='source_component'};pc={x['pcb_component_id']:x for x in j if x['type']=='pcb_component'};sp={x['source_port_id']:x for x in j if x['type']=='source_port'}
pads=[x for x in j if x['type'] in ['pcb_smtpad','pcb_plated_hole']];otherpads=[p for p in pads if not p.get('pcb_port_id') or root(a['ports'][p['pcb_port_id']])!=gnd]
keep=[x for x in j if x['type']=='pcb_keepout'];holes=[x for x in j if x['type']=='pcb_hole'];vias=[x for x in j if x['type']=='pcb_via'];outline=list(map(pt,next(x for x in j if x['type']=='pcb_board')['outline']))
others=[]
for t in tr:
 if a['trace_root'](t)==gnd:continue
 for p,q in zip(t['route'],t['route'][1:]):
  if p['route_type']==q['route_type']=='wire' and p['layer']=='top':others.append((pt(p),pt(q),p['width']/2))
ground_vias=[v for v in vias if a['trace_root'](next(t for t in tr if t['pcb_trace_id']==v['pcb_trace_id']))==gnd]
opens={p for x in j if x['type']=='pcb_port_not_connected_error' for p in x['pcb_port_ids']}
paths={};details=[];failed=[];step=.1
for port in (x for x in j if x['type']=='pcb_port' and x['pcb_port_id'] in opens and root(x['source_port_id'])==gnd):
 comp=pc[port['pcb_component_id']];name=sc[comp['source_component_id']];key=f"{name}.pin{sp[port['source_port_id']].get('pin_number')}"
 if name in ['J3','J7']:continue
 if not any(t.get('connected_source_port_ids')==[port['source_port_id']] for t in a['source_traces'].values()):continue
 start=pt(port);width=.2;r=width/2;local_others=[(c,d,v) for c,d,v in others if ps(start,c,d)<12];local_pads=[p for p in otherpads if bd(start,start,bounds(p))<12]
 def good(p,q):
  if any(bd(p,q,bounds(x))<r+.20001 for x in local_pads):return False
  if any(sd(p,q,c,d)<r+v+.20001 for c,d,v in local_others):return False
  if any(bd(p,q,bounds(h))<r+.25001 for h in holes):return False
  if any(bd(p,q,bounds(k))<r for k in keep):return False
  if min(sd(p,q,c,d) for c,d in zip(outline,outline[1:]+outline[:1]))<r+.25:return False
  # Other-net vias obstruct top wires on all through layers.
  if any(ps(pt(v),p,q)<v['outer_diameter']/2+r+.2 for v in vias if v not in ground_vias):return False
  return True
 targets=sorted([pt(v) for v in ground_vias if math.dist(start,pt(v))<10],key=lambda p:math.dist(start,p))
 def pos(k):return (round(start[0]+k[0]*step,6),round(start[1]+k[1]*step,6))
 queue=[(0.,0.,(0,0))];cost={(0,0):0.};parent={};end=None;target=None;cache={}
 while queue:
  _,g,k=heapq.heappop(queue)
  if g>cost[k]+1e-9:continue
  p=pos(k)
  for q in targets:
   if math.dist(p,q)<.5 and good(p,q):end=k;target=q;break
  if end is not None:break
  if len(cost)>18000:break
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
   n=(k[0]+dx,k[1]+dy)
   if abs(n[0])>70 or abs(n[1])>70:continue
   q=pos(n)
   if n not in cache:cache[n]=good(q,q)
   if not cache[n] or not good(p,q):continue
   ng=g+math.hypot(dx,dy)*step
   if ng>=cost.get(n,1e9):continue
   cost[n]=ng;parent[n]=k;h=min((math.dist(q,t) for t in targets),default=0);heapq.heappush(queue,(ng+h,ng,n))
 if end is None:failed.append(key);continue
 points=[target];k=end
 while k!=(0,0):points.append(pos(k));k=parent[k]
 points.append(start);points=points[::-1]
 # Greedy line-of-sight reduction, keeping every tested clearance floor unchanged.
 simplified=[points[0]];i=0
 while i<len(points)-1:
  n=len(points)-1
  while n>i+1 and not good(points[i],points[n]):n-=1
  simplified.append(points[n]);i=n
 rot=math.radians(-comp['rotation']);local=[]
 for x,y in simplified[1:]:
  dx=x-comp['display_offset_x'];dy=y-comp['display_offset_y'];local.append({'x':round(dx*math.cos(rot)-dy*math.sin(rot),6),'y':round(dx*math.sin(rot)+dy*math.cos(rot),6)})
 # Reuse an existing ground via; no new unneeded drill or duplicate via.
 local.append({**local[-1],'via':True,'fromLayer':'top','toLayer':'bottom'})
 paths[key]=local;details.append({'port':key,'width':width,'global_path':simplified,'existing_ground_via':target})
 print(key,len(simplified),flush=True)
(base/'ground-bend-proposal.json').write_text(json.dumps({'paths':paths,'details':details,'unresolved':failed},indent=2)+'\n')
print('proposed',len(paths),'unresolved',failed,flush=True)
