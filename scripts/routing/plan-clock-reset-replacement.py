"""Free the clock's south escape by replacing one real reset trace.

Keep component placement, native pad geometry, required widths, and full-span
drill clearances. This emits authored proposals requiring fresh native audits.
"""
import argparse,json,runpy
from pathlib import Path
from shapely.geometry import Point,LineString,Polygon
b=runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')));h=b['helpers']


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('native');ap.add_argument('output');args=ap.parse_args()
    c=json.loads(Path(args.native).read_text());sources={r['source_trace_id']:r for r in c if r['type']=='source_trace'}
    trace=next(r for r in c if r['type']=='pcb_trace' and sources[r['source_trace_id']].get('name')=='MANUAL_LCD_RESET_N_128')
    if any(q['route_type']!='wire' or q['layer']!='top' or q['width']!=.2 for q in trace['route']):raise ValueError('Unexpected original reset geometry')
    p=h['Planner'](c,{'relocated_trace_layers':{trace['pcb_trace_id']:{layer:None for layer in ('top','bottom','inner1','inner2')}}});p.set_grid(.05);p.set_copper_reserve(.0001);p.via_copper_clearance=.27
    nets={r['name']:r for r in c if r['type']=='source_net'};ports={p.port_name(q):q for q in p.ports.values() if p.source_ports[q['source_port_id']].get('source_component_id') in p.source_components}
    base=list(p.copper),list(p.holes),dict(p.plated_hole_roots);failures=[]
    for xy in [(9.325,9.5),(9.325,9.4),(9.325,9.3),(9.325,9.6),(9.5,9.4),(9.1,9.4)]:
        p.copper,p.holes,p.plated_hole_roots=list(base[0]),list(base[1]),dict(base[2]);result={'classification':'authored clock repair and complete reset-trace replacement; native qualification required','paths':[],'pours':[],'vias':[],'unresolved':[],'retired_manual_path_indices':[128],'source_native':args.native}
        def escape(net,selector,position=None):
            root=p.root(nets[net]['source_net_id']);port=ports[selector];origin=(port['x'],port['y'])
            if position is None:
                found=h['pad_escape'](p,{'root':root,'net':nets[net],'origin':origin,'width':.2,'new_vias':[],'via_outer_mm':.45,'via_hole_mm':.3,'distribution_layers':('inner2','inner1'),'distribution_width_mm':.202,'copper_clearance_mm':.27})
                if not found:return None
                position,points=found
            else:
                if Point(position).intersects(h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3})):return None
                points=[origin,position]
                if LineString(points).intersects(p.obstacles(root,'top',.2)):return None
            result['paths'].append(h['escape_record'](p,{'root':root,'net':nets[net],'port':port,'width':.2,'positions':points,'via_outer_mm':.45,'via_hole_mm':.3}));return position
        def connect(net,first,last):
            root=p.root(nets[net]['source_net_id']);route=h['wide_multilayer_route'](p,{'root':root,'first':first,'last':last,'width':.202,'new_vias':[first,last],'layers':('inner2','inner1'),'via_outer_mm':.45,'via_hole_mm':.3,'copper_clearance_mm':.27,'multi_anchor':True})
            if not route:return False
            parts,vias=route;regions=b['region_records'](net,{'parts':parts,'width':.2});result['pours'].extend(regions)
            for r in regions:p.copper.append((root,r['layer'],Polygon([(q['x'],q['y']) for q in r['outline']])))
            for v in vias:b['reserve_via'](p,{'root':root,'position':v});result['vias'].append({'net':net,'x':v[0],'y':v[1],'hole_mm':.3,'outer_mm':.45})
            return True
        clock=escape('LCD_SCLK','.U14 > .pin15',xy)
        if clock is None:failures.append({'exit':xy,'reason':'Clock escape blocked'});continue
        r45=escape('LCD_SCLK','.R45 > .pin1')
        if r45 is None or not connect('LCD_SCLK',clock,r45):failures.append({'exit':xy,'reason':'Clock distribution blocked'});continue
        reset=escape('LCD_RESET_N','.U14 > .pin17');r43=escape('LCD_RESET_N','.R43 > .pin1')
        if reset is None or r43 is None or not connect('LCD_RESET_N',reset,r43):failures.append({'exit':xy,'reason':'Reset replacement blocked'});continue
        result['failed_candidates']=failures;Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'complete':True,'clock_exit':xy,'paths':len(result['paths']),'regions':len(result['pours'])}));return 0
    Path(args.output).write_text(json.dumps({'classification':'incomplete actual clock/reset planning','paths':[],'pours':[],'vias':[],'unresolved':failures},indent=2)+'\n');print(json.dumps({'complete':False,'unresolved':failures}));return 1


if __name__=='__main__':raise SystemExit(main())
