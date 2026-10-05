import json
from pathlib import Path
import sys
base=Path('evidence/a7-routing-2026-10-05')
current=Path(sys.argv[1])
def groups(j):
 parent={}
 def root(k):
  parent.setdefault(k,k)
  if parent[k]!=k: parent[k]=root(parent[k])
  return parent[k]
 def join(ids):
  for k in ids[1:]:parent[root(k)]=root(ids[0])
 names={x['source_component_id']:x['name'] for x in j if x['type']=='source_component'}
 labels={x['source_port_id']:f"{names[x['source_component_id']]}.{x.get('pin_number',x['name'])}" for x in j if x['type']=='source_port'}
 labels.update({x['source_net_id']:'net.'+x['name'] for x in j if x['type']=='source_net'})
 for k in labels:root(k)
 for x in j:
  if x['type']=='source_trace':join(x.get('connected_source_port_ids',[])+x.get('connected_source_net_ids',[]))
  if x['type']=='source_component_internal_connection':join(x['source_port_ids'])
 g={}
 for k,v in labels.items():g.setdefault(root(k),[]).append(v)
 return sorted(sorted(v) for v in g.values())
a=groups(json.load(open(base/'before/circuit.json')));b=groups(json.load(open(current)))
r={'baseline':'52f4795 A6 / before/circuit.json','current':str(current),'groups_before':len(a),'groups_after':len(b),'identical_source_connectivity':a==b,'scope':'All named nets and every physical component source port including intentionally open battery outer contacts. Trace names, PCB phase assignments and resistor identities are not net changes.'}
(base/'source-equivalence.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));assert a==b
