"""Plan display fanout together so the LDO output does not trap the clock pad.

Replace actual authored DC/CS regions at their original widths; preserve all
numbered component terminals, imported footprints, and other native copper.
"""
import argparse,json,math,runpy
from pathlib import Path
from shapely.geometry import Point,LineString,Polygon
b=runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')));h=b['helpers']


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('native');ap.add_argument('output');args=ap.parse_args();c=json.loads(Path(args.native).read_text());probe=h['Planner'](c);nets={r['name']:r for r in c if r['type']=='source_net'};roots={name:probe.root(nets[name]['source_net_id']) for name in ('LCD_DC','LCD_CS_N','LCD_SCLK')};sources={r['source_trace_id']:r for r in c if r['type']=='source_trace'};old=next(r for r in c if r['type']=='pcb_trace' and sources[r['source_trace_id']].get('name')=='CONNECTION_ESCAPE_LCD_DC_6');features={r['pcb_copper_pour_id'] for r in c if r['type']=='pcb_copper_pour' and probe.root(r['source_net_id']) in {roots['LCD_DC'],roots['LCD_CS_N']}};features.update(r['pcb_via_id'] for r in c if r['type']=='pcb_via' and (r.get('pcb_trace_id')==old['pcb_trace_id'] or (not r.get('pcb_trace_id') and probe.via_root(r) in {roots['LCD_DC'],roots['LCD_CS_N']})));cs_targets=[(r['x'],r['y']) for r in c if r['type']=='pcb_via' and r['pcb_via_id'] not in features and probe.via_root(r)==roots['LCD_CS_N']];dc_target=next((r['x'],r['y']) for r in c if r['type']=='pcb_via' and r['pcb_via_id'] not in features and probe.via_root(r)==roots['LCD_DC']);del probe
    p=h['Planner'](c,{'relocated_trace_layers':{old['pcb_trace_id']:{layer:None for layer in ('top','bottom','inner1','inner2')}},'retired_feature_ids':features});p.set_grid(.05);p.set_copper_reserve(.0001);p.via_copper_clearance=.27;ports={p.port_name(q):q for q in p.ports.values() if p.source_ports[q['source_port_id']].get('source_component_id') in p.source_components};base=list(p.copper),list(p.holes),dict(p.plated_hole_roots);failures=[]
    def add_region(net,parts,width):
        regions=b['region_records'](net,{'parts':parts,'width':width})
        for r in regions:p.copper.append((roots[net],r['layer'],Polygon([(q['x'],q['y']) for q in r['outline']])))
        return regions
    for dc in [(8.1,12.2),(8.,12.3),(8.1,12.3),(8.,12.2)]:
      for clock in [(9.0,12.074),(8.3,13.2),(8.2,13.3),(8.35,13.3),(8.4,13.4)]:
        p.copper,p.holes,p.plated_hole_roots=list(base[0]),list(base[1]),dict(base[2]);p.set_grid(.01,(7.5,10.5,11.,14.5));result={'classification':'authored simultaneous DC/clock fanout and width-preserving control corridors; native qualification required','paths':[],'pours':[],'vias':[],'unresolved':[],'replaced_connection_escape_indices':[6],'replaced_region_nets':['LCD_DC','LCD_CS_N'],'source_native':args.native,'local_escape_grid_mm':.01,'local_escape_grid_bounds_mm':[7.5,10.5,11.,14.5]}
        escaped=True
        for net,selector,xy in [('LCD_DC','.U14 > .pin16',dc),('LCD_SCLK','.U14 > .pin15',clock)]:
            port=ports[selector];root=roots[net];origin=(port['x'],port['y'])
            if Point(xy).intersects(h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3})):escaped=False;failures.append({'dc':dc,'clock':clock,'reason':selector+' via blocked'});break
            points=p.grid_route((origin,xy,p.obstacles(root,'top',.2)))
            if not points:escaped=False;failures.append({'dc':dc,'clock':clock,'reason':selector+' top escape blocked'});break
            result['paths'].append(h['escape_record'](p,{'root':root,'net':nets[net],'port':port,'width':.2,'positions':points,'via_outer_mm':.45,'via_hole_mm':.3}))
        if not escaped:continue
        p.set_grid(.05)
        port=ports['.R45 > .pin1'];found=h['pad_escape'](p,{'root':roots['LCD_SCLK'],'net':nets['LCD_SCLK'],'origin':(port['x'],port['y']),'width':.2,'new_vias':[clock],'via_outer_mm':.45,'via_hole_mm':.3,'distribution_layers':('inner2','inner1'),'distribution_width_mm':.202,'copper_clearance_mm':.27})
        if not found:failures.append({'dc':dc,'clock':clock,'reason':'R45 escape blocked'});continue
        r45,points=found;result['paths'].append(h['escape_record'](p,{'root':roots['LCD_SCLK'],'net':nets['LCD_SCLK'],'port':port,'width':.2,'positions':points,'via_outer_mm':.45,'via_hole_mm':.3}))
        connections=[('LCD_SCLK',clock,r45,.2),('LCD_DC',dc,dc_target,.2)]
        if len(cs_targets)<2:raise ValueError('CS must preserve its actual two pad escapes')
        connected=[cs_targets[0]];remaining=list(cs_targets[1:])
        while remaining:
            _,first,last=min((math.dist(first,last),first,last) for first in connected for last in remaining);connections.append(('LCD_CS_N',first,last,.3));connected.append(last);remaining.remove(last)
        routed=True
        for net,first,last,width in connections:
            route=h['wide_multilayer_route'](p,{'root':roots[net],'first':first,'last':last,'width':width+.002,'new_vias':[first,last],'layers':('inner2','inner1'),'via_outer_mm':.45,'via_hole_mm':.3,'copper_clearance_mm':.27,'multi_anchor':True})
            if not route:routed=False;failures.append({'dc':dc,'clock':clock,'reason':net+' inner corridor blocked'});break
            parts,new_vias=route;result['pours'].extend(add_region(net,parts,width))
            for xy in new_vias:b['reserve_via'](p,{'root':roots[net],'position':xy});result['vias'].append({'net':net,'x':xy[0],'y':xy[1],'hole_mm':.3,'outer_mm':.45})
        if routed:
            result['failed_candidate_checks']=failures;Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'complete':True,'dc_exit':dc,'clock_exit':clock,'regions':len(result['pours'])}));return 0
    Path(args.output).write_text(json.dumps({'classification':'unsuccessful actual display corridor planning','paths':[],'pours':[],'vias':[],'unresolved':failures},indent=2)+'\n');print(json.dumps({'complete':False,'failed_candidates':len(failures)}));return 1

if __name__=='__main__':raise SystemExit(main())
