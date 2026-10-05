# Propose explicit native source paths; does not edit Circuit JSON or autorouting caches.
import contextlib,io,json,math,runpy,sys
from pathlib import Path
base=Path('evidence/a7-routing-2026-10-05')
sys.argv=['audit-signals.py','native-local-power-10x','ground-planning-input-audit.json']
with contextlib.redirect_stdout(io.StringIO()): a=runpy.run_path(str(base/'audit-signals.py'))
j=a['j'];root=a['root'];pt=a['point'];bd=a['bbox_distance'];bounds=a['bounds'];sd=a['segment_distance'];ps=a['point_segment']
sc={x['source_component_id']:x for x in j if x['type']=='source_component'}
pc={x['pcb_component_id']:x for x in j if x['type']=='pcb_component'}
sp={x['source_port_id']:x for x in j if x['type']=='source_port'}
net=next(x for x in j if x['type']=='source_net' and x['name']=='GND');gnd=root(net['source_net_id'])
pads=[x for x in j if x['type'] in ['pcb_smtpad','pcb_plated_hole']]
vias=[x for x in j if x['type']=='pcb_via'];holes=[x for x in j if x['type'] in ['pcb_hole','pcb_plated_hole']]
keep=[x for x in j if x['type']=='pcb_keepout'];outline=list(map(pt,next(x for x in j if x['type']=='pcb_board')['outline']))
other_segments=[]
for t in a['traces']:
 if a['trace_root'](t)==gnd:continue
 for p,q in zip(t['route'],t['route'][1:]):
  if p['route_type']==q['route_type']=='wire': other_segments.append((pt(p),pt(q),max(p['width'],q['width'])/2,p['layer']))
otherpads=[x for x in pads if not x.get('pcb_port_id') or root(a['ports'][x['pcb_port_id']])!=gnd]
planned=[];paths={};unresolved=[];opens={p for x in j if x['type']=='pcb_port_not_connected_error' for p in x['pcb_port_ids']}
def via_ok(q):
 if any(bd(q,q,bounds(p))<.35001 for p in pads):return False # drill-to-any-pad .2
 if any(bd(q,q,bounds(p))<.55001 for p in otherpads):return False
 if any(math.dist(q,pt(v))<.80001 for v in vias+planned):return False # conservative different copper, drilling .25
 if any(bd(q,q,bounds(h))<.55001 for h in holes):return False
 if any(bd(q,q,bounds(k))<.35001 for k in keep):return False
 if min(sd(q,q,c,d) for c,d in zip(outline,outline[1:]+outline[:1]))<.60001:return False
 if any(ps(q,c,d)<r+.55001 for c,d,r,l in other_segments):return False
 return True
def segment_ok(p,q):
 if any(bd(p,q,bounds(x))<.35001 for x in otherpads if 'top' in x.get('layers',[x.get('layer')])):return False
 if any(sd(p,q,c,d)<r+.35001 for c,d,r,l in other_segments if l=='top'):return False
 if any(bd(p,q,bounds(h))<.40001 for h in holes):return False
 if any(bd(p,q,bounds(k))<.15001 for k in keep):return False
 if min(sd(p,q,c,d) for c,d in zip(outline,outline[1:]+outline[:1]))<.40001:return False
 return True
for p in (x for x in j if x['type']=='pcb_port' and root(x['source_port_id'])==gnd and x['pcb_port_id'] in opens):
 comp=pc[p['pcb_component_id']];name=sc[comp['source_component_id']]['name'];pin=sp[p['source_port_id']]['pin_number'];key=f'{name}.pin{pin}'
 if name in ['J3','J7','U2']:continue
 # Only actual one-port ground source traces can take the native via path.
 traces=[t for t in a['source_traces'].values() if t.get('connected_source_port_ids')==[p['source_port_id']] and net['source_net_id'] in t.get('connected_source_net_ids',[])]
 if not traces:unresolved.append({'port':key,'reason':'not a one-port ground trace'});continue
 pos=pt(p);target=None
 for distance in [i/10 for i in range(6,36,2)]:
  for angle in range(0,360,30):
   rad=math.radians(angle);q=(round(pos[0]+distance*math.cos(rad),6),round(pos[1]+distance*math.sin(rad),6))
   if via_ok(q) and segment_ok(pos,q):target=q;break
  if target:break
 if target is None:unresolved.append({'port':key,'reason':'no straight clearance-qualified ordinary-via escape within 3.4 mm'});continue
 # Native pcbPath numeric coordinates are local to source component, rotated with it.
 dx,dy=target[0]-comp['display_offset_x'],target[1]-comp['display_offset_y'];r=math.radians(-comp['rotation']);local=(round(dx*math.cos(r)-dy*math.sin(r),6),round(dx*math.sin(r)+dy*math.cos(r),6))
 paths[key]=[{'x':local[0],'y':local[1]},{'x':local[0],'y':local[1],'via':True,'fromLayer':'top','toLayer':'bottom'}]
 planned.append({'x':target[0],'y':target[1],'port':key})
(base/'ground-escape-proposal.json').write_text(json.dumps({'paths':paths,'global_vias':planned,'unresolved':unresolved},indent=2)+'\n')
print(json.dumps({'proposed_paths':len(paths),'unresolved':unresolved},indent=2))
