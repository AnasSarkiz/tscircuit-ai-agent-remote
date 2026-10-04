import struct,json,itertools,numpy as np
from pathlib import Path
b=Path('evidence/a3-routing-2026-10-04/buydisplay/board.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];j=json.loads(b[20:20+n]);blobs=b[28+n:];out={};lcd=(-27.78,-25.475,26.78,15.025)
def transform(node):
 if 'matrix' in node:return np.array(node['matrix']).reshape(4,4).T
 x,y,z,w=node.get('rotation',[0,0,0,1]);m=np.eye(4);m[:3,:3]=[[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]];m[:3,:3]=m[:3,:3]@np.diag(node.get('scale',[1,1,1]));m[:3,3]=node.get('translation',[0,0,0]);return m
def accessor(i):
 a=j['accessors'][i];v=j['bufferViews'][a['bufferView']];dt={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']];size={'SCALAR':1,'VEC3':3}[a['type']];offset=v.get('byteOffset',0)+a.get('byteOffset',0);stride=v.get('byteStride',np.dtype(dt).itemsize*size)
 return np.ndarray((a['count'],size),dtype=dt,buffer=blobs,offset=offset,strides=(stride,np.dtype(dt).itemsize)).copy()
def clip(poly,axis,limit,lower):
 new=[]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  pi=(p[axis]>=limit) if lower else (p[axis]<=limit);qi=(q[axis]>=limit) if lower else (q[axis]<=limit)
  if pi:new.append(p)
  if pi!=qi:new.append(p+(q-p)*(limit-p[axis])/(q[axis]-p[axis]))
 return new
def walk(i,parent):
 node=j['nodes'][i];m=parent@transform(node);name=node.get('name',str(i))
 if 'mesh' in node:
  allpoints=[];under=[]
  for pr in j['meshes'][node['mesh']]['primitives']:
   xyz=accessor(pr['attributes']['POSITION']);ar=(m@np.c_[xyz,np.ones(len(xyz))].T).T[:,:3];ar=np.c_[-ar[:,0],ar[:,2],ar[:,1]];allpoints.extend(ar)
   if name=='U1':
    ids=accessor(pr['indices']).ravel() if 'indices' in pr else np.arange(len(ar))
    for inds in ids.reshape(-1,3):
     poly=list(ar[inds])
     for ax,limit,lower in [(0,lcd[0],True),(0,lcd[2],False),(1,lcd[1],True),(1,lcd[3],False)]:
      if poly:poly=clip(poly,ax,limit,lower)
     under.extend(poly)
  if allpoints:
   ar=np.array(allpoints);out[name]={'min':ar.min(axis=0).tolist(),'max':ar.max(axis=0).tolist()}
   if under:out[name]['max_z_under_lcd']=float(np.array(under)[:,2].max())
 for child in node.get('children',[]):walk(child,m)
for i in j['scenes'][j.get('scene',0)]['nodes']:walk(i,np.eye(4))
Path('evidence/a3-routing-2026-10-04/buydisplay/cad-bounds.json').write_text(json.dumps(out,indent=2))
print('module',out.get('U1'));print('connectors',{k:out.get(k) for k in ['J1','J3','J4','J6','J7','J8']})
print('under LCD',sorted([(k,v.get('max_z_under_lcd',v['max'][2])) for k,v in out.items() if k!='Box0' and v['min'][0]<lcd[2] and v['max'][0]>lcd[0] and v['min'][1]<lcd[3] and v['max'][1]>lcd[1]],key=lambda p:-p[1])[:20])
