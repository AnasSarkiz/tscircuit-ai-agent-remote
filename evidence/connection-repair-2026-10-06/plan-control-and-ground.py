"""Complete reviewed mode/pull-up branches and independent ground islands."""
import json,runpy
from pathlib import Path
from shapely.geometry import Polygon
from shapely.ops import unary_union
b=runpy.run_path('scripts/routing/plan-connection-bridges.py');h=b['helpers'];d=Path('evidence/connection-repair-2026-10-06');c=json.loads((d/'relocated-native/circuit.json').read_text());physical=json.loads((d/'relocated-audit.json').read_text());plans=[json.loads((d/name).read_text()) for name in ['amplifier-proposal.json','status-contact-proposal.json','outer-five-mm-proposal.json']]
retired={r['original_pcb_trace_id']:{'top':None} for plan in plans for r in plan.get('retired_replay_connections',[])};retired.update({r['original_pcb_trace_id']:{'top':None,'bottom':None} for plan in plans for r in plan.get('retired_inner_escapes',[])})
p=h['Planner'](c,{'relocated_trace_layers':retired,'retired_feature_ids':{r['retired_via_id'] for plan in plans for r in plan.get('retired_inner_escapes',[])}});p.set_grid(.05);p.via_copper_clearance=.27;nets={r['name']:r for r in c if r['type']=='source_net'}
for plan in plans:
 p.reserve_proposals({**plan,'paths':[{**path,'via_outer_mm':.45,'via_hole_mm':.3} for path in plan['paths']]})
 for region in plan['pours']:p.copper.append((p.root(nets[region['net']]['source_net_id']),region['layer'],Polygon([(xy['x'],xy['y']) for xy in region['outline']])))
selectors={p.port_name(port):port for port in p.ports.values() if p.source_ports[port['source_port_id']].get('source_component_id') in p.source_components}
result={'classification':'authored control/ground connection proposals; native geometry and load qualification required','paths':[],'pours':[],'vias':[],'repaired_islands':[],'unresolved':[],'branch_requirements':[
 {'net':'VSYS','terminal':'.R62 > .pin1','nominal_width_mm':.3,'layers':['inner2','inner1'],'maximum_dc_current_a':.0055,'basis':'R62 is the verified1kohm gate pull-up. At5.5V even a grounded gate draws at most5.5mA.'},
 {'net':'VSYS','terminal':'.U3 > .pin2','nominal_width_mm':.3,'layers':['inner2','inner1'],'maximum_dc_current_a':None,'basis':'MAX98357A pin2 GAIN_SLOT is a gain-mode input; PVDD pins7/8 carry amplifier supply current separately. Exact gain-input current/width qualification remains blocked; the fresh official ADI datasheet request is policy-denied.'}]}
for name,labels in [('VSYS',['.R62 > .pin1','.U3 > .pin2']),('GND',['.C2 > .pin2','.R68 > .pin2','.Q9 > .pin2','.R82 > .pin2','.R84 > .pin2'])]:
 root=p.root(nets[name]['source_net_id']);groups={}
 for port in selectors.values():
  if p.root(port['source_port_id'])==root:
   group=physical['physical_port_groups'][port['pcb_port_id']]
   if len(group)==1:groups.setdefault(group[0],[]).append(port)
 main=max(groups,key=lambda g:len(groups[g]));targets=b['island_vias'](p,{'root':root,'physical':physical,'group':main});ground=[]
 if name=='GND':
  for r in c:
   if r['type']=='pcb_copper_pour' and r['layer']=='inner1' and p.root(r['source_net_id'])==root and physical['physical_feature_groups'][r['pcb_copper_pour_id']]==main:
    brep=r['brep_shape'];ground.append(Polygon([(xy['x'],xy['y']) for xy in brep['outer_ring']['vertices']], [[(xy['x'],xy['y']) for xy in ring['vertices']] for ring in brep['inner_rings']]))
 completed=set()
 for selector in labels:
  port=selectors[selector];group=physical['physical_port_groups'][port['pcb_port_id']][0]
  if group==main or group in completed:continue
  net={**nets[name],'trace_width':.3}
  found=b['repair_island'](p,{'root':root,'net':net,'ports':[port],'physical':physical,'group':group,'targets':targets,'ground':unary_union(ground)})
  if found:
   if name=='VSYS':
    for region in found['pours']:region['branch_terminal']=selector
   for kind in ['paths','pours','vias']:result[kind].extend(found[kind])
   targets.append(found['connected_start']);completed.add(group);result['repaired_islands'].append({'net':name,'ports':[p.port_name(v) for v in groups[group]]})
  else:result['unresolved'].append({'net':name,'port':selector,'reason':'No qualified escape/strip to actual main island'})
  print(json.dumps({'net':name,'port':selector,'routed':bool(found)}),flush=True);(d/'control-ground-proposal.json').write_text(json.dumps(result,indent=2)+'\n')
