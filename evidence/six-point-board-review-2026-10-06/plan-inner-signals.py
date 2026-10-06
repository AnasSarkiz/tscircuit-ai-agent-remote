"""Author native inner-layer regions while retaining exact outer pad escapes.
No solver cache is changed or created. This proposal requires native replay.
"""
import hashlib,json,runpy
from pathlib import Path
from shapely.geometry import LineString
p=Path('src/board/manual-signal-paths.json');manual=json.loads(p.read_text());out=[]
for index,path in enumerate(manual['paths']):
 if 'bottom' not in path['segment_layers']:continue
 markers=[i for i,point in enumerate(path['pcbPath']) if isinstance(point,dict) and point.get('via')]
 if len(markers) not in (1,2):raise ValueError('Unsupported outer escape topology')
 first=path['pcbPath'][markers[0]]
 first_escape=path['pcbPath'][:markers[0]+1]+[{'x':first['x'],'y':first['y']}]
 escapes=[{'from':path['from'],'to':'net.'+path['net'],'pcbPathRelativeTo':path['from'],'pcbPath':first_escape}]
 if len(markers)==2:
  last=path['pcbPath'][markers[-1]]
  reverse=[point for point in reversed(path['pcbPath'][markers[-1]+1:]) if isinstance(point,dict)]
  reverse += [{'x':last['x'],'y':last['y']},{'x':last['x'],'y':last['y'],'via':True,'fromLayer':'top','toLayer':'bottom'},{'x':last['x'],'y':last['y']}]
  escapes.append({'from':path['to'],'to':'net.'+path['net'],'pcbPathRelativeTo':path['from'],'pcbPath':reverse})
 segments=[(a,b) for i,(a,b) in enumerate(zip(path['global_path_mm'],path['global_path_mm'][1:])) if path['segment_layers'][i+1]=='bottom']
 centreline=[segments[0][0],*[b for a,b in segments]]
 shape=LineString(centreline).buffer((path['width']+.002)/2,cap_style=2,join_style=2)
 if shape.geom_type!='Polygon' or shape.interiors:raise ValueError('Inner signal needs a simple native region')
 out.append({'original_path_index':index,'net':path['net'],'from':path['from'],'to':path['to'],'width':path['width'],
   'escapes':escapes,'region':{'net':path['net'],'layer':'inner2','path_mm':centreline,'nominal_width_mm':path['width'],
   'drawn_width_mm':path['width']+.002,'outline':[{'x':round(x,6),'y':round(y,6)} for x,y in list(shape.exterior.coords)[:-1]],
   'classification':'manual native relocation of low-current signal to inner2; full-span outer pad-escape vias'}})
receipt={'classification':'authored native inner signal regions and unchanged pad escapes; not solver output',
         'original_source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'paths':out,'pours':[r['region'] for r in out]}
Path('evidence/six-point-board-review-2026-10-06/inner-signals-proposal.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'low_current_paths_proposed':len(out)}))
