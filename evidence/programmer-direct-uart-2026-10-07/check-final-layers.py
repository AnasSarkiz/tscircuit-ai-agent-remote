"""Measure actual drill spans and layer placement of retained supply copper."""
import hashlib,json,runpy
from pathlib import Path
folder=Path(__file__).resolve().parent
path=Path('dist/index/circuit.json');c=json.loads(path.read_text())
vias=[r for r in c if r['type']=='pcb_via']
bad_vias=[r['pcb_via_id'] for r in vias if r['hole_diameter']!=.3 or r['outer_diameter']!=.45 or set(r['layers'])!={'top','inner1','inner2','bottom'}]
high={'PACK_BAT','VSYS','VBUS','V3V3','VMOTOR','HAPTIC_N','SPEAKER_P','SPEAKER_N'}
h=runpy.run_path('scripts/routing/audit-trace-widths.py');electrical,sources,net_roots=h['electrical_roots'](c)
checked=[];bad=[]
for r in c:
 if r['type']!='pcb_trace':continue
 source=sources[r['source_trace_id']];ports=source.get('connected_source_port_ids',[])+source.get('connected_source_net_ids',[])
 names={net['name'] for net in net_roots.get(electrical.root(ports[0]),[])}
 if not names.intersection(high) and source.get('min_trace_thickness',0)<.8:continue
 checked.append(r['pcb_trace_id'])
 if any(p['route_type']=='wire' and p['layer'] not in ('top','bottom') for p in r['route']):bad.append(r['pcb_trace_id'])
checked_regions=[];bad_regions=[]
for filename in ['manual-power-copper.json','connection-copper.json','inner-signal-copper.json']:
 source=json.loads(Path('src/board',filename).read_text());retired=set(source.get('retired_connection_region_indices',[]))
 for i,r in enumerate(source['pours']):
  if i in retired or r['net'] not in high or r.get('branch_terminal'):continue
  checked_regions.append({'source':filename,'index':i,'net':r['net'],'layer':r['layer']})
  if r['layer'] not in ('top','bottom'):bad_regions.append(checked_regions[-1])
result={'native_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'via_count':len(vias),'ordinary_vias_exact_0p30_hole_0p45_pad_full_span':bool(vias) and not bad_vias,'bad_vias':bad_vias,'high_current_native_trace_count':len(checked),'high_current_native_traces_outer_only':bool(checked) and not bad,'bad_high_current_traces':bad,'high_current_active_source_trunk_regions':len(checked_regions),'high_current_regions_outer_only':bool(checked_regions) and not bad_regions,'bad_high_current_regions':bad_regions,'scope':'All actual native through via drill/land/layers and all native supply/speaker or explicit >=0.8mm source-minimum traces. Active named high-current source trunks checked on all three authored region sources; only separately declared low-current branch terminals excluded. Widths/continuity/thermal suitability remain separate gates.','current_capacity_qualified':False,'fabrication_ready':False}
(folder/'final-native-compliance.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(0 if not(bad_vias or bad or bad_regions) else 1)
