import json,math,re
from pathlib import Path
j=json.load(open('dist/index/circuit.json'));sc={e['source_component_id']:e for e in j if e['type']=='source_component'};pc={e['pcb_component_id']:e for e in j if e['type']=='pcb_component'};names={i:sc[e['source_component_id']]['name'] for i,e in pc.items()};boxes={};centres={names[i]:(e['center']['x'],e['center']['y']) for i,e in pc.items()}
for e in j:
 if not e['type'].startswith('pcb_courtyard') or e.get('pcb_component_id') not in names:continue
 name=names[e['pcb_component_id']]
 if 'outline' in e:
  xs=[p['x'] for p in e['outline']];ys=[p['y'] for p in e['outline']];b=(min(xs),min(ys),max(xs),max(ys))
 else:
  x=e['center']['x'];y=e['center']['y'];w=e['width'];h=e['height'];r=math.radians(e.get('ccw_rotation',0));dw=(abs(w*math.cos(r))+abs(h*math.sin(r)))/2;dh=(abs(h*math.cos(r))+abs(w*math.sin(r)))/2;b=(x-dw,y-dh,x+dw,y+dh)
 boxes[name]=b
preserve={'U1','J1','J3','J4','J6','J7','J8','SW4','SW5','U2','L1','C4','C5','R5','R6','R7','R31','R32','U4','U5','U27','C82','C83','C84','C85','R102','R104','U26','C78','R99','R100','R38','C71','C70'}
movable=[n for n,b in boxes.items() if n not in preserve and (b[2]-b[0])*(b[3]-b[1])<28]
shapes={n:tuple(q-centres[n][i%2] for i,q in enumerate(boxes.pop(n))) for n in movable}
# Reserve actual PH bodies plus mated-plug/wire rail. This is conservative space, not a qualified cable path.
obstacles=[(-22,31.675,-2,39.675),(19,-26,25,-20),(-24.6,-32.6,-18.4,-26.4),(17.8,-19,26.3,26.7)]
def collide(a,b):return a[0]<b[2]+.08 and a[2]>b[0]-.08 and a[1]<b[3]+.08 and a[3]>b[1]-.08
# Native test pads have no supplier courtyard; retain their real copper bounds as obstacles.
for el in j:
 if el['type']=='pcb_component' and names.get(el['pcb_component_id'],'').startswith('TP'):
  x,y=el['center']['x'],el['center']['y'];obstacles.append((x-.65,y-.65,x+.65,y+.65))
proposal={}
for n in sorted(movable,key=lambda n:-(shapes[n][2]-shapes[n][0])*(shapes[n][3]-shapes[n][1])):
 sh=shapes[n];goal=centres[n];candidates=[]
 for xi in range(-92,93):
  for yi in range(-120,121):
   x=xi/4;y=yi/4;b=(sh[0]+x,sh[1]+y,sh[2]+x,sh[3]+y)
   if b[0]<-24.75 or b[2]>24.75 or b[1]<-32.25 or b[3]>32.25:continue
   candidates.append(((x-goal[0])**2+(y-goal[1])**2,x,y,b))
 for _,x,y,b in sorted(candidates):
  if not any(collide(b,o) for o in [*boxes.values(),*obstacles]):break
 else:raise RuntimeError('No collision-free candidate '+n)
 if (x,y)!=goal:proposal[n]=(x,y)
 boxes[n]=b
s=Path('src/board/placement.ts').read_text()
for n,(x,y) in proposal.items():s=re.sub(rf'({n}: \{{ pcbX: )[^,]+(, pcbY: )[^,]+',rf'\g<1>{x}\g<2>{y}',s)
Path('src/board/placement.ts').write_text(s);Path('evidence/a4-display-coverage-2026-10-04/placement-proposal.json').write_text(json.dumps(proposal,indent=2)+'\n');print(json.dumps(proposal))
