"""Join verified physical islands with authored native escapes and copper strips.

Uses existing numbered source nets. Does not assign deferred connector contacts,
change imported definitions, or turn manual geometry into autorouter caches.
"""
import argparse
import json
import math
import runpy
from pathlib import Path
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

helpers = runpy.run_path(str(Path(__file__).with_name('plan-power-copper.py')))
contacts = runpy.run_path(str(Path(__file__).with_name('plan-existing-copper-routes.py')))


def island_vias(planner, specification):
    return [(r['x'], r['y']) for r in planner.circuit if r['type'] == 'pcb_via'
            and planner.via_root(r) == specification['root']
            and specification['physical']['physical_feature_groups'][r['pcb_via_id']] == specification['group']]


def region_records(net, specification):
    records = []
    for layer, points in specification['parts']:
        if len(points) < 2 or LineString(points).length < 1e-6:
            continue
        drawn_width = specification.get('drawn_width_mm', specification['width']+.002)
        if drawn_width < specification['width'] or not math.isfinite(drawn_width):
            raise ValueError('Drawn copper must preserve the finite nominal width')
        line = LineString(points)
        # Flat end caps beside short bends make offset buffers non-monotonic:
        # a larger radius can remove a small wedge of the nominal envelope.
        # Keep that required envelope explicitly while adding real reserve.
        contour = line.buffer(drawn_width/2, quad_segs=64, cap_style=2, join_style=1).union(
            line.buffer(specification['width']/2, quad_segs=64, cap_style=2, join_style=1))
        if contour.geom_type != 'Polygon' or contour.interiors:
            raise ValueError('Strip must have one simple native outline')
        # Rounding distinct floating-point vertices can make adjacent points
        # identical. Remove zero-length edges in authored native outlines;
        # this preserves their exact rounded shape and required copper width.
        outline = []
        for x, y in list(contour.exterior.coords)[:-1]:
            vertex = {'x':round(x,6), 'y':round(y,6)}
            if not outline or vertex != outline[-1]:
                outline.append(vertex)
        if len(outline) > 1 and outline[0] == outline[-1]:
            outline.pop()
        records.append({'net':net, 'layer':layer, 'nominal_width_mm':specification['width'],
                        'drawn_width_mm':drawn_width, 'path_mm':points,
                        'outline':outline})
    return records


def reserve_via(planner, specification):
    hole = Point(specification['position']).buffer(.15)
    planner.holes.append(hole)
    planner.plated_hole_roots[hole.wkb] = specification['root']
    for layer in ('top','inner1','inner2','bottom'):
        planner.copper.append((specification['root'], layer, Point(specification['position']).buffer(.225)))


def main_escape(planner, specification):
    net, root = specification['net'], specification['root']
    width = net.get('trace_width') or .2
    obstacles = helpers['via_obstacles'](planner, {'root':root,'via_outer_mm':.45,'via_hole_mm':.3})
    targets = specification.get('existing_targets')
    if targets is None:
        targets = contacts['main_targets'](planner, specification)
    for layer,x,y in sorted(targets):
        if layer != 'top' or Point(x,y).intersects(obstacles):
            continue
        reserve_via(planner, {'root':root,'position':(x,y)})
        return {'position':(x,y),'paths':[], 'vias':[{'net':net['name'],'x':x,'y':y,'hole_mm':.3,'outer_mm':.45}]}
    for port in specification['ports']:
        found=helpers['pad_escape'](planner,{'net':net,'root':root,'width':width,
            'origin':(port['x'],port['y']),'new_vias':[], 'via_outer_mm':.45,'via_hole_mm':.3,
            'distribution_layers':('inner2','inner1'),'distribution_width_mm':width+.002,
            'copper_clearance_mm':.27})
        if found:
            position, points = found
            escape=helpers['escape_record'](planner,{'port':port,'net':net,'root':root,'width':width,
                'positions':points,'via_outer_mm':.45,'via_hole_mm':.3})
            return {'position':position,'paths':[escape],'vias':[]}
    return None


def repair_island(planner, specification):
    net, root = specification['net'], specification['root']
    width = net.get('trace_width') or .2
    targets = specification['targets']
    starts = island_vias(planner, specification)
    alternatives = sorted(specification['ports'], key=lambda p:min((math.dist((p['x'],p['y']), t) for t in targets),default=0))
    for port in alternatives:
        print(json.dumps({'planning':net['name'],'port':planner.port_name(port),'existing_vias':len(starts)}),flush=True)
        saved_copper, saved_holes, saved_roots = list(planner.copper), list(planner.holes), dict(planner.plated_hole_roots)
        escape = None
        if not starts:
            if net['name'] == 'GND':
                top = planner.obstacles(root,'top',width)
                via_blocks = helpers['via_obstacles'](planner, {'root':root,'via_outer_mm':.45,'via_hole_mm':.3})
                from shapely import contains_xy
                allowed = contains_xy(specification['ground'],planner.grid_x,planner.grid_y)
                exits = planner.grid_escape((port['x'],port['y']), (top,via_blocks,allowed))
                found = exits[0] if exits else None
            else:
                found = helpers['pad_escape'](planner, {'root':root,'net':net,'width':width,
                    'origin':(port['x'],port['y']),'new_vias':targets,'via_outer_mm':.45,'via_hole_mm':.3,
                    'distribution_layers':('inner2','inner1'),'distribution_width_mm':width+.002,
                    'copper_clearance_mm':.27,'connected_targets':targets})
            if not found:
                continue
            start, positions = found
            escape = helpers['escape_record'](planner, {'port':port,'net':net,'root':root,
                'width':width,'positions':positions,'via_outer_mm':.45,'via_hole_mm':.3})
            candidates = [start]
        else:
            candidates = sorted(starts,key=lambda p:math.dist(p,(port['x'],port['y'])))[:3]
        if net['name'] == 'GND' and escape and Point(candidates[0]).buffer(.225).intersection(specification['ground']).area > .01:
            return {'paths':[escape],'pours':[],'vias':[],'connected_start':candidates[0]}
        for start in candidates:
            for target in sorted(targets,key=lambda p:math.dist(p,start))[:12]:
                route = helpers['wide_multilayer_route'](planner, {'first':start,'last':target,'root':root,
                    'width':width+.002,'new_vias':targets+candidates,'layers':('inner2','inner1'),
                    'via_outer_mm':.45,'via_hole_mm':.3,'copper_clearance_mm':.27})
                if not route:
                    continue
                parts, vias = route
                via_blocks = helpers['via_obstacles'](planner, {'root':root,'via_outer_mm':.45,'via_hole_mm':.3})
                if any(Point(xy).intersects(via_blocks) for xy in vias):
                    continue
                pours = region_records(net['name'], {'parts':parts,'width':width})
                for record in pours:
                    planner.copper.append((root,record['layer'],Polygon([(p['x'],p['y']) for p in record['outline']])))
                for xy in vias:
                    reserve_via(planner, {'position':xy,'root':root})
                return {'paths':[escape] if escape else [],'pours':pours,
                        'vias':[{'net':net['name'],'x':xy[0],'y':xy[1],'outer_mm':.45,'hole_mm':.3} for xy in vias],
                        'connected_start':start}
        planner.copper,planner.holes,planner.plated_hole_roots=saved_copper,saved_holes,saved_roots
        if starts:
            break
    return None


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit_json');parser.add_argument('copper_audit');parser.add_argument('output_json')
    parser.add_argument('nets',nargs='+');parser.add_argument('--reserve-proposals');parser.add_argument('--grid-mm',type=float,choices=(.05,.1),default=.1)
    parser.add_argument('--copper-reserve-mm',type=float)
    parser.add_argument('--ports',nargs='+',help='Only repair these verified numbered terminals')
    args=parser.parse_args()
    circuit=json.loads(Path(args.circuit_json).read_text());physical=json.loads(Path(args.copper_audit).read_text())
    if set(args.nets)&{'VBUS','VSYS','PACK_BAT','V3V3','VMOTOR','HAPTIC_N','SPEAKER_P','SPEAKER_N'}:
        raise ValueError('High-current trunks require the separate outer-layer planner')
    reserved=json.loads(Path(args.reserve_proposals).read_text()) if args.reserve_proposals else None
    changes={}
    if reserved:
        manual=json.loads(Path('src/board/manual-signal-paths.json').read_text())['paths']
        names={f"MANUAL_{manual[index]['net']}_{index}" for index in reserved.get('retired_manual_path_indices',[])}
        sources={r['source_trace_id']:r for r in circuit if r['type']=='source_trace'}
        retired={r['pcb_trace_id']:{layer:None for layer in ('top','bottom','inner1','inner2')}
                 for r in circuit if r['type']=='pcb_trace' and sources[r['source_trace_id']].get('name') in names}
        if len(retired)!=len(names):raise ValueError('Every reserved retirement must refer to a real native path')
        for item in reserved.get('retired_replay_connections',[]):
            trace_id=item['original_pcb_trace_id']
            if not any(record.get('pcb_trace_id')==trace_id for record in circuit):
                raise ValueError('Cached retirement must identify actual native copper')
            retired[trace_id]={layer:None for layer in ('top','bottom','inner1','inner2')}
        features={item for key in ('retired_native_vias','retired_authored_vias','retired_authored_regions') for item in reserved.get(key,[])}
        for item in reserved.get('retired_inner_escapes',[]):
            retired[item['original_pcb_trace_id']]={layer:None for layer in ('top','bottom','inner1','inner2')}
            features.add(item['retired_via_id'])
        for trace_id in reserved.get('retired_authored_traces',[]):retired[trace_id]={layer:None for layer in ('top','bottom','inner1','inner2')}
        changes={'relocated_trace_layers':retired,'retired_feature_ids':features}
    planner=helpers['Planner'](circuit,changes);planner.set_grid(args.grid_mm);planner.via_copper_clearance=.27
    if args.copper_reserve_mm is not None:planner.set_copper_reserve(args.copper_reserve_mm)
    if reserved:
        planner.reserve_proposals(reserved)
        nets_by_name={r['name']:r for r in circuit if r['type']=='source_net'}
        for region in reserved.get('pours',[]):
            planner.copper.append((planner.root(nets_by_name[region['net']]['source_net_id']),region['layer'],
                                   Polygon([(p['x'],p['y']) for p in region['outline']])))
    nets={r['name']:r for r in circuit if r['type']=='source_net'}
    result={'classification':'authored native connection proposals; actual replay/audit required','paths':[],'pours':[],'vias':[],'unresolved':[],'repaired_islands':[]}
    for name in args.nets:
        root=planner.root(nets[name]['source_net_id']);groups={}
        for port in planner.ports.values():
            if planner.root(port['source_port_id'])!=root or planner.source_ports[port['source_port_id']].get('source_component_id') not in planner.source_components:
                continue
            if planner.port_name(port).startswith(('.J3 >','.J7 >')):
                continue
            group=physical['physical_port_groups'][port['pcb_port_id']]
            if len(group)==1:groups.setdefault(group[0],[]).append(port)
        if len(groups)<2:
            continue
        main_group=max(groups,key=lambda g:len(groups[g]));targets=island_vias(planner,{'root':root,'physical':physical,'group':main_group})
        pending_escape=None
        if not targets and name != 'GND':
            pending_escape=main_escape(planner, {'net':nets[name],'root':root,'physical':physical,
                'group':main_group,'ports':groups[main_group]})
            if pending_escape:
                targets.append(pending_escape['position'])
        ground=[]
        if name=='GND':
            for record in circuit:
                if record['type']=='pcb_copper_pour' and record['layer']=='inner1' and planner.root(record['source_net_id'])==root and physical['physical_feature_groups'][record['pcb_copper_pour_id']]==main_group:
                    brep=record['brep_shape'];ground.append(Polygon([(p['x'],p['y']) for p in brep['outer_ring']['vertices']],
                        [[(p['x'],p['y']) for p in ring['vertices']] for ring in brep['inner_rings']]))
        for group,ports in groups.items():
            if group==main_group:
                continue
            if args.ports:
                ports=[port for port in ports if planner.port_name(port) in args.ports]
                if not ports:continue
            found=repair_island(planner,{'net':nets[name],'root':root,'group':group,'physical':physical,'ports':ports,'targets':targets,'ground':unary_union(ground)})
            labels=[planner.port_name(p) for p in ports]
            if found:
                if pending_escape:
                    result['paths'].extend(pending_escape['paths']);result['vias'].extend(pending_escape['vias'])
                    pending_escape=None
                for kind in ('paths','pours','vias'):result[kind].extend(found[kind])
                targets.append(found['connected_start']);result['repaired_islands'].append({'net':name,'ports':labels})
            else:
                result['unresolved'].append({'net':name,'ports':labels,'reason':'No qualified full-span escape/inner strip to actual main copper'})
            Path(args.output_json).write_text(json.dumps(result,indent=2)+'\n')
            print(json.dumps({'net':name,'repaired':bool(found),'ports':labels}),flush=True)
    return 0

if __name__=='__main__':raise SystemExit(main())
