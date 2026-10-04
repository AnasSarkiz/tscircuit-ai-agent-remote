import json,math,re
from pathlib import Path
j=json.load(open('evidence/a3-routing-2026-10-04/buydisplay/placement-top-contact/circuit.json'));sc={e['source_component_id']:e for e in j if e['type']=='source_component'};pc={e['pcb_component_id']:e for e in j if e['type']=='pcb_component'};names={i:sc[e['source_component_id']]['name'] for i,e in pc.items()};boxes={};centres={names[i]:(e['center']['x'],e['center']['y']) for i,e in pc.items()}
for e in j:
 if not e['type'].startswith('pcb_courtyard') or e.get('pcb_component_id') not in names:continue
 name=names[e['pcb_component_id']]
 if 'outline' in e: xs=[p['x'] for p in e['outline']];ys=[p['y'] for p in e['outline']];b=(min(xs),min(ys),max(xs),max(ys))
 else:
  x=e['center']['x'];y=e['center']['y'];w=e['width'];h=e['height'];r=math.radians(e.get('ccw_rotation',0));dw=(abs(w*math.cos(r))+abs(h*math.sin(r)))/2;dh=(abs(h*math.cos(r))+abs(w*math.sin(r)))/2;b=(x-dw,y-dh,x+dw,y+dh)
 boxes[name]=b
# Native source positions only. Never edit circuit JSON, footprints or clearance rules.
movable=['C25','C77','U14','R90','R91','U27','C82','C83','C84','C85','SW2','R34','R38','C30','C3','R62','R63','R64','R7','R102','R104','C71','R85']
fixed_moves={'J3':(3.4,21),'J4':(13.9,28),'J8':(19.1,19.25),'SW4':(21.9,30.4),'D3':(22,5),'J6':(-17.4,-10)}
# Correct C11063 native rotation to 90; outline coordinates then reverse relative old centre.
proposal={}
for n,(x,y) in fixed_moves.items():
 b=boxes[n];cx,cy=centres[n];boxes[n]=(b[0]+x-cx,b[1]+y-cy,b[2]+x-cx,b[3]+y-cy);centres[n]=(x,y);proposal[n]=(x,y)
preserve={'U1','J1','J3','J4','J6','J7','J8','SW4','SW5','D3','U2','L1','C4','C5','R5','R6','R31','R32'}
movable=list(dict.fromkeys([*movable,*[n for n,b in boxes.items() if n not in preserve and (b[2]-b[0])*(b[3]-b[1])<28]]))
shapes={n:tuple(q-centres[n][i%2] for i,q in enumerate(boxes.pop(n))) for n in movable}
# Manufacturing keepouts, viewport and fixed component courtyards retain margin.
obstacles=[(-25,-32.5,-24.75,32.5),(24.75,-32.5,25,32.5),(-22,31.675,-2,39.675),(-1,10,5,16),(-24.6,-32.6,-18.4,-26.4)]
preferred={'U14':(8,8),'U27':(13,-12),'C82':(16,-13),'C83':(16,-15.5),'C84':(13,-8.5),'C85':(13,-16),'R102':(10,-9),'R104':(13,-6.5),'R7':(0,-11),'R62':(-6.3,-14),'R63':(-6.3,-16),'R64':(-6.3,-18),'C3':(-4,-23.5),'SW2':(8.5,28),'C30':(-.5,10),'C25':(-21,-16.5),'C77':(-6.5,-23),'R90':(10,-24),'R91':(10,-22),'R34':(1,-22),'R38':(21,9.5),'C71':(18,2.5),'R85':(21,2.5)}
def collide(a,b):return a[0]<b[2]+.08 and a[2]>b[0]-.08 and a[1]<b[3]+.08 and a[3]>b[1]-.08
for n in sorted(movable,key=lambda n:-(shapes[n][2]-shapes[n][0])*(shapes[n][3]-shapes[n][1])):
 sh=shapes[n];goal=preferred.get(n,centres[n]);candidates=[]
 for xi in range(-92,93):
  for yi in range(-120,121):
   x=xi/4;y=yi/4;b=(sh[0]+x,sh[1]+y,sh[2]+x,sh[3]+y)
   if b[0]<-24.75 or b[2]>24.75 or b[1]<-32.25 or b[3]>32.25:continue
   candidates.append(((x-goal[0])**2+(y-goal[1])**2,x,y,b))
 if not candidates:raise RuntimeError('No candidate '+n)
 for _,x,y,b in sorted(candidates):
  if not any(collide(b,o) for o in [*boxes.values(),*obstacles]):break
 else:raise RuntimeError('No collision-free candidate '+n)
 proposal[n]=(x,y);boxes[n]=b
s=Path('src/board/placement.ts').read_text()
for n,(x,y) in proposal.items():
 s=re.sub(rf'({n}: \{{ pcbX: )[^,]+(, pcbY: )[^,]+',rf'\g<1>{x}\g<2>{y}',s)
s=re.sub(r'(J7: \{[^\n]*pcbRotation: )270',r'\g<1>90',s)
Path('src/board/placement.ts').write_text(s);Path('evidence/a3-routing-2026-10-04/buydisplay/placement-top-proposal.json').write_text(json.dumps(proposal,indent=2));print(json.dumps(proposal))
