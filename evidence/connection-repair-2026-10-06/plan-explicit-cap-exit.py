import json,runpy
from pathlib import Path
from shapely.geometry import Point,LineString,Polygon
outer=runpy.run_path('scripts/routing/plan-outer-connections.py');b=outer['bridges'];h=b['helpers'];d=Path('evidence/connection-repair-2026-10-06');c=json.loads((d/'usb-ground-power-speaker-native/circuit.json').read_text());a=json.loads((d/'usb-ground-power-speaker-audit.json').read_text());combined=json.loads((d/'combined-control-corridors-reservation.json').read_text());new=json.loads((d/'usb-display-after-corridors-proposal.json').read_text());retired={r['original_pcb_trace_id']:{l:None for l in ('top','bottom','inner1','inner2')} for r in combined['retired_inner_escapes']};retired.update({i:{l:None for l in ('top','bottom','inner1','inner2')} for i in combined['retired_authored_traces']});features=set(combined['retired_authored_regions']+combined['retired_authored_vias']+[r['retired_via_id'] for r in combined['retired_inner_escapes']]);p=h['Planner'](c,{'relocated_trace_layers':retired,'retired_feature_ids':features});p.set_grid(.05);p.set_copper_reserve(.0001);p.via_copper_clearance=.27;nets={r['name']:r for r in c if r['type']=='source_net'}
for proposal in [combined,new]:
 p.reserve_proposals(proposal)
 for r in proposal['pours']:p.copper.append((p.root(nets[r['net']]['source_net_id']),r['layer'],Polygon([(q['x'],q['y']) for q in r['outline']])))
net=nets['VBUS'];root=p.root(net['source_net_id']);port=next(r for r in p.ports.values() if p.port_name(r)=='.C1 > .pin1');origin=(port['x'],port['y']);xy=(-11,-25.25)
if LineString([origin,xy]).intersects(p.obstacles(root,'top',.3)) or Point(xy).intersects(h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3})):raise ValueError('Explicit capacitor escape violates geometry')
path=h['escape_record'](p,{'root':root,'net':net,'port':port,'width':.3,'positions':[origin,xy],'via_outer_mm':.45,'via_hole_mm':.3});groups={}
for q in p.ports.values():
 if p.root(q['source_port_id'])==root and p.source_ports[q['source_port_id']].get('source_component_id') in p.source_components:
  g=a['physical_port_groups'][q['pcb_port_id']]
  if len(g)==1:groups.setdefault(g[0],[]).append(q)
group=max(groups,key=lambda x:len(groups[x]));targets=b['island_vias'](p,{'root':root,'physical':a,'group':group});result={'classification':'authored precise capacitor escape and outer .5mm trunk; native/current qualification required','paths':[],'pours':[],'vias':[],'unresolved':[],'pad_necks':[]}
for target in sorted(targets,key=lambda t:__import__('math').dist(xy,t)):
 route=h['wide_multilayer_route'](p,{'root':root,'first':xy,'last':target,'width':.302,'preferred_width_mm':.502,'new_vias':[xy]+targets,'layers':('bottom','top'),'via_outer_mm':.45,'via_hole_mm':.3,'copper_clearance_mm':.27})
 if not route:continue
 parts,new_vias=route;regions,narrow=outer['adaptive_regions'](p,{'root':root,'net':'VBUS','parts':parts,'nominal_width':.5,'neck_width':.3,'new_vias':[xy]+targets+new_vias});
 if narrow+path['top_length_mm']>5:continue
 result['paths'].append(path);result['pours']=regions;result['vias']=[{'net':'VBUS','x':x,'y':y,'hole_mm':.3,'outer_mm':.45} for x,y in new_vias];result['pad_necks'].append({'net':'VBUS','terminal':'.C1 > .pin1','width_mm':.3,'length_mm':path['top_length_mm'],'outer_distribution_neck_length_mm':narrow,'total_narrow_length_mm':narrow+path['top_length_mm'],'nominal_trunk_width_mm':.5,'layer':'top','status':'Measured proposal; transient/current/stackup qualification pending'});break
if not result['paths']:result['unresolved'].append({'net':'VBUS','port':'.C1 > .pin1','reason':'Explicit via is legal but no full-width outer trunk to actual main-island copper'})
(d/'explicit-cap-exit-proposal.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'complete':not result['unresolved'],'regions':len(result['pours']),'unresolved':result['unresolved']}))
