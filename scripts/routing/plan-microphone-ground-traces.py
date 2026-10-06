"""Join real microphone ground lands using native pad-edge straight traces.

The imported ground-port centres lie near their acoustic holes. Native
pcbStraightLine clips sufficiently wide wires at the pad boundary, preserving
the imported definitions and the ordinary drill/copper rules.
"""
import argparse,json,math,runpy,hashlib
from pathlib import Path
from shapely.geometry import Point,LineString,Polygon,box
from shapely.ops import unary_union
h=runpy.run_path(str(Path(__file__).with_name('plan-power-copper.py')))


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('native');ap.add_argument('output');ap.add_argument('--replace-clock-escapes',action='store_true');ap.add_argument('--width-mm',type=float,choices=(.36,.4),default=.4);ap.add_argument('--ports',nargs='+',choices=('.U4 > .pin3','.U5 > .pin3'),default=['.U4 > .pin3','.U5 > .pin3']);ap.add_argument('--ground-landing-pad',action='store_true',help='Use an explicit native top ground/test pad instead of a new drill; current native plane contact and component clearance must be retained');ap.add_argument('--copper-audit');args=ap.parse_args();c=json.loads(Path(args.native).read_text());clocks=[]
    if args.replace_clock_escapes:
        sources={r['source_trace_id']:r for r in c if r['type']=='source_trace'}
        names={name for selector,name in (('.U4 > .pin3','MANUAL_INNER_ESCAPE_246_0'),('.U5 > .pin3','CONNECTION_ESCAPE_MIC_BCLK_21')) if selector in args.ports}
        clocks=[r for r in c if r['type']=='pcb_trace' and sources[r['source_trace_id']].get('name') in names]
        if len(clocks)!=len(names):raise ValueError('Expected the selected actual microphone clock escapes')
    p=h['Planner'](c,{'relocated_trace_layers':{r['pcb_trace_id']:{'top':None} for r in clocks}});p.set_grid(.05);p.set_copper_reserve(.01);p.via_copper_clearance=.27
    net=next(r for r in c if r['type']=='source_net' and r['name']=='GND');root=p.root(net['source_net_id']);result={'classification':'authored native pad-edge ground traces; final native geometry/preservation qualification required','straight_paths':[],'paths':[],'pours':[],'vias':[],'ground_landings':[],'unresolved':[],'source_native':args.native}
    for selector in args.ports:
        port=next(r for r in p.ports.values() if p.port_name(r)==selector);origin=(port['x'],port['y']);pad,shape=next((r,s) for r,s in p.pads if r.get('pcb_port_id')==port['pcb_port_id']);bounds=shape.bounds;width=args.width_mm
        if width<=min(bounds[2]-bounds[0],bounds[3]-bounds[1])/2:raise ValueError('Native straight-line clipping would retain the unsafe centre')
        obstacles=p.obstacles(root,'top',width);via_obstacles=h['via_obstacles'](p,{'root':root,'via_outer_mm':.45,'via_hole_mm':.3});found=None
        if args.ground_landing_pad:
            if not args.copper_audit:raise ValueError('Ground landing requires the matching actual copper audit')
            physical=json.loads(Path(args.copper_audit).read_text())
            if physical['source_sha256']!=hashlib.sha256(Path(args.native).read_bytes()).hexdigest():raise ValueError('Ground audit does not bind this native input')
            groups=physical['physical_port_groups'][port['pcb_port_id']]
            if len(groups)!=1:raise ValueError('Ground port lacks one verified physical island')
            ground=unary_union([Polygon([(v['x'],v['y']) for v in r['brep_shape']['outer_ring']['vertices']], [[(v['x'],v['y']) for v in ring['vertices']] for ring in r['brep_shape']['inner_rings']]) for r in c if r['type']=='pcb_copper_pour' and r['source_net_id']==net['source_net_id'] and r['layer']=='top' and physical['physical_feature_groups'][r['pcb_copper_pour_id']]==groups[0]])
            pad_obstacles=p.obstacles(root,'top',.5)
            drill_obstacles=unary_union([hole.buffer(.5) for hole in p.holes])
            bodies=unary_union([box(r['center']['x']-r['width']/2,r['center']['y']-r['height']/2,r['center']['x']+r['width']/2,r['center']['y']+r['height']/2).buffer(.25) for r in p.components.values() if r.get('source_component_id') in p.source_components])
            for distance in (1.7,2.,2.3,2.6,3.,3.5,4.,4.5,5.,5.5,6.):
              for degrees in range(0,360,15):
                angle=math.radians(degrees);xy=(round(origin[0]+distance*math.cos(angle),6),round(origin[1]+distance*math.sin(angle),6));position=Point(xy)
                if position.intersects(pad_obstacles) or position.intersects(drill_obstacles) or position.intersects(bodies) or position.buffer(.25).intersection(ground).area<.02:continue
                hit=LineString([origin,xy]).intersection(shape.envelope.boundary)
                if hit.geom_type!='Point':continue
                start=(hit.x,hit.y);line=LineString([start,xy]);clipped_end=line.interpolate(max(0,line.length-.25));wire=LineString([start,(clipped_end.x,clipped_end.y)])
                if wire.intersects(obstacles) or wire.buffer(width/2).intersection(shape).area<1e-5:continue
                result['ground_landings'].append({'name':'TP9','net':'GND','x':xy[0],'y':xy[1],'diameter_mm':.5,'basis':'Native top-only pad, no purchased component or drill; existing plane contact and body clearance checked'})
                result['straight_paths'].append({'net':'GND','from':selector,'to':'.TP9 > .pin1','width':width,'planned_clipped_start_mm':start,'planned_end_mm':[clipped_end.x,clipped_end.y],'classification':'Native pad-edge ground join to top pad in the existing ground plane'})
                p.copper.append((root,'top',wire.buffer(width/2)));p.copper.append((root,'top',position.buffer(.25)));found='native-ground-pad';break
              if found:break
            if not found:result['unresolved'].append({'port':selector,'reason':'No clear native ground landing and pad-edge wire retaining actual ground-plane contact'})
            continue
        # An existing ground land can provide a genuine direct join without a
        # new drill. Use the installed native clipping rule at both endpoints.
        for target in sorted(p.ports.values(),key=lambda r:math.dist(origin,(r['x'],r['y']))):
            if target['pcb_port_id']==port['pcb_port_id'] or p.root(target['source_port_id'])!=root or math.dist(origin,(target['x'],target['y']))>6:continue
            if target['source_port_id'] not in p.source_ports or p.source_ports[target['source_port_id']].get('source_component_id') not in p.source_components:continue
            pads=[s for r,s in p.pads if r.get('pcb_port_id')==target['pcb_port_id'] and 'top' in r.get('layers',[r.get('layer')])]
            if not pads:continue
            target_shape=pads[0];xy=(target['x'],target['y']);start_hit=LineString([origin,xy]).intersection(shape.envelope.boundary)
            if start_hit.geom_type!='Point':continue
            start=(start_hit.x,start_hit.y);end=xy;tb=target_shape.bounds
            if width>min(tb[2]-tb[0],tb[3]-tb[1])/2:
                end_hit=LineString([xy,origin]).intersection(target_shape.envelope.boundary)
                if end_hit.geom_type!='Point':continue
                end=(end_hit.x,end_hit.y)
            wire=LineString([start,end])
            if wire.length<.05 or wire.intersects(obstacles) or wire.buffer(width/2).intersection(shape).area<1e-5 or wire.buffer(width/2).intersection(target_shape).area<1e-5:continue
            result['straight_paths'].append({'net':'GND','from':selector,'to':p.port_name(target),'width':width,'planned_clipped_start_mm':start,'planned_end_mm':end,'classification':'Native pad-edge trace to an existing real same-net ground land; no added drill'})
            p.copper.append((root,'top',wire.buffer(width/2)));found='existing-ground';break
        if found:continue
        for distance in (.9,1.1,1.3,1.5,1.7,2.,2.3,2.6,3.,3.5,4.,4.5,5.,5.5,6.):
          for degrees in range(0,360,15):
            angle=math.radians(degrees);xy=(round(origin[0]+distance*math.cos(angle),6),round(origin[1]+distance*math.sin(angle),6))
            if Point(xy).intersects(via_obstacles):continue
            # Match core's computeLineRectIntersection for this polygon land.
            intersection=LineString([origin,xy]).intersection(shape.envelope.boundary)
            if intersection.geom_type!='Point':continue
            start=(intersection.x,intersection.y);wire=LineString([start,xy])
            if wire.intersects(obstacles) or wire.buffer(width/2).intersection(shape).area<1e-5:continue
            found=(xy,start);break
          if found:break
        if found:
            xy,start=found;result['vias'].append({'net':'GND','x':xy[0],'y':xy[1],'hole_mm':.3,'outer_mm':.45});result['straight_paths'].append({'net':'GND','from':selector,'width':width,'proposal_via_index':len(result['vias'])-1,'planned_clipped_start_mm':start,'planned_end_mm':xy,'classification':'native pcbStraightLine using original imported pad bounds; actual replay required'})
            p.copper.append((root,'top',LineString([start,xy]).buffer(width/2)));hole=Point(xy).buffer(.15);p.holes.append(hole);p.plated_hole_roots[hole.wkb]=root
            for layer in ('top','inner1','inner2','bottom'):p.copper.append((root,layer,Point(xy).buffer(.225)))
        else:result['unresolved'].append({'port':selector,'reason':'No qualified straight pad-edge ground join and full-span via'})
    if args.replace_clock_escapes and not result['unresolved']:
        b=runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')))
        result['retired_clock_escape_ids']=[r['pcb_trace_id'] for r in clocks]
        for trace in clocks:
            port=p.ports[trace['route'][0]['start_pcb_port_id']];clocknet=next(r for r in c if r['type']=='source_net' and p.root(r['source_net_id'])==p.root(port['source_port_id']));clockroot=p.root(clocknet['source_net_id']);target=next((r['x'],r['y']) for r in trace['route'] if r['route_type']=='via')
            found=h['pad_escape'](p,{'root':clockroot,'net':clocknet,'width':.2,'origin':(port['x'],port['y']),'new_vias':[target],'via_outer_mm':.45,'via_hole_mm':.3,'distribution_layers':('inner1','inner2'),'distribution_width_mm':.202,'copper_clearance_mm':.27,'connected_targets':[target]})
            if not found:result['unresolved'].append({'port':p.port_name(port),'reason':'No replacement clock escape preserving original connection'});continue
            xy,points=found
            path=h['escape_record'](p,{'root':clockroot,'net':clocknet,'port':port,'positions':points,'width':.2,'via_outer_mm':.45,'via_hole_mm':.3})
            routed=h['wide_multilayer_route'](p,{'root':clockroot,'first':xy,'last':target,'width':.202,'new_vias':[xy,target],'layers':('inner1','inner2'),'via_outer_mm':.45,'via_hole_mm':.3,'copper_clearance_mm':.27,'multi_anchor':True})
            if not routed:result['unresolved'].append({'port':p.port_name(port),'reason':'Replacement clock corridor incomplete'});continue
            parts,vias=routed;result['paths'].append(path);result['pours'].extend(b['region_records'](clocknet['name'],{'parts':parts,'width':.2}));result['vias'].extend({'net':clocknet['name'],'x':pos[0],'y':pos[1],'hole_mm':.3,'outer_mm':.45} for pos in [target]+vias)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'complete':not result['unresolved'],'straight_paths':result['straight_paths'],'replacement_paths':len(result['paths']),'unresolved':result['unresolved']}));return 1 if result['unresolved'] else 0


if __name__=='__main__':raise SystemExit(main())
