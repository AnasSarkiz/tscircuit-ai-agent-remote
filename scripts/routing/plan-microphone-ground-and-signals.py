"""Reserve a real microphone ground join before replacing its clock/data escapes.

The signal vias beside the curved ground land constrain its native pad-edge
join. Retire only those authored escapes and replace their complete connections
to existing clock/data corridors. No supplier definition or native JSON changes.
"""
import argparse
import json
import runpy
from pathlib import Path
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import unary_union

helpers = runpy.run_path(str(Path(__file__).with_name('plan-power-copper.py')))
bridges = runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')))
ground_helpers = runpy.run_path(str(Path(__file__).with_name('plan-microphone-ground-traces.py')))


def reserve_ground(planner, specification):
    port = specification['port']
    origin = (port['x'], port['y'])
    root = specification['root']
    width_mm = .36
    pad = next(shape for record, shape in planner.pads if record.get('pcb_port_id') == port['pcb_port_id'])
    if width_mm <= min(pad.bounds[2]-pad.bounds[0], pad.bounds[3]-pad.bounds[1])/2:
        raise ValueError('Native clipping would retain the unsafe ground-port centre')
    obstacles = planner.obstacles(root, 'top', width_mm)
    via_obstacles = helpers['via_obstacles'](planner, {'root': root, 'via_outer_mm': .45, 'via_hole_mm': .3})
    candidates = ground_helpers['ground_via_candidates']({
        'origin': origin, 'grid_mm': .025, 'minimum_distance_mm': .4, 'via_obstacles': via_obstacles})
    for xy in candidates:
        if Point(xy).intersects(via_obstacles):
            continue
        hit = LineString([origin, xy]).intersection(pad.envelope.boundary)
        if hit.geom_type != 'Point':
            continue
        start = (hit.x, hit.y)
        wire = LineString([start, xy])
        if wire.intersects(obstacles) or wire.buffer(width_mm/2).intersection(pad).area < 1e-5:
            continue
        planner.copper.append((root, 'top', wire.buffer(width_mm/2)))
        bridges['reserve_via'](planner, {'root': root, 'position': xy})
        return {'net': 'GND', 'from': planner.port_name(port), 'width': width_mm,
                'proposal_via_index': 0, 'planned_clipped_start_mm': start, 'planned_end_mm': xy,
                'classification': 'Manual native pad-edge ground trace; fresh native qualification required'}
    return None


def replace_signal(planner, specification):
    net, port, target = specification['net'], specification['port'], specification['target']
    root = planner.root(net['source_net_id'])
    route_specification = {'root': root, 'net': net, 'width': .2,
                          'origin': (port['x'], port['y']), 'new_vias': [target],
                          'via_outer_mm': .45, 'via_hole_mm': .3,
                          'distribution_layers': ('inner1', 'inner2'), 'distribution_width_mm': .202,
                          'copper_clearance_mm': .27, 'connected_targets': [target]}
    escape = helpers['pad_escape'](planner, route_specification)
    if escape is None:
        return None
    xy, positions = escape
    path = helpers['escape_record'](planner, {**route_specification, 'port': port, 'positions': positions})
    route = helpers['wide_multilayer_route'](planner, {
        **route_specification, 'width': .202, 'first': xy, 'last': target,
        'new_vias': [xy, target], 'layers': ('inner1', 'inner2'), 'multi_anchor': True})
    if route is None:
        return None
    parts, vias = route
    pours = bridges['region_records'](net['name'], {'parts': parts, 'width': .2})
    for region in pours:
        planner.copper.append((root, region['layer'], Polygon([(v['x'], v['y']) for v in region['outline']])))
    for position in vias:
        bridges['reserve_via'](planner, {'root': root, 'position': position})
    return {'path': path, 'pours': pours,
            'vias': [{'net': net['name'], 'x': position[0], 'y': position[1], 'hole_mm': .3, 'outer_mm': .45}
                     for position in vias]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('native')
    parser.add_argument('output')
    parser.add_argument('--source', default='src/board/connection-copper.json')
    args = parser.parse_args()
    circuit = json.loads(Path(args.native).read_text())
    authored = json.loads(Path(args.source).read_text())
    data_region = authored['pours'][43]
    if data_region['net'] != 'MIC_SD' or authored['paths'][31]['from'] != '.U4 > .pin6':
        raise ValueError('Expected the recorded U4 data escape and its complete authored branch')
    traces = {r['source_trace_id']: r for r in circuit if r['type'] == 'source_trace'}
    selected = {traces[r['source_trace_id']].get('name'): r for r in circuit
                if r['type'] == 'pcb_trace' and traces[r['source_trace_id']].get('name')
                in ('MANUAL_INNER_ESCAPE_246_0', 'CONNECTION_ESCAPE_MIC_SD_31', 'CONNECTION_ESCAPE_MIC_SD_32')}
    if len(selected) != 3:
        raise ValueError('The exact baseline microphone signal escapes are required')
    clock = selected['MANUAL_INNER_ESCAPE_246_0']
    data = selected['CONNECTION_ESCAPE_MIC_SD_31']
    target_data = selected['CONNECTION_ESCAPE_MIC_SD_32']
    vias = {r['pcb_trace_id']: r for r in circuit if r['type'] == 'pcb_via' and r.get('pcb_trace_id')}
    clock_via, data_via = vias[clock['pcb_trace_id']], vias[data['pcb_trace_id']]
    target_data_via = vias[target_data['pcb_trace_id']]
    data_net_id = next(r['source_net_id'] for r in circuit if r['type'] == 'source_net' and r['name'] == 'MIC_SD')
    authored_shape = Polygon([(v['x'], v['y']) for v in data_region['outline']])
    region_ids = []
    matched_shapes = []
    for record in circuit:
        if record['type'] != 'pcb_copper_pour' or record['source_net_id'] != data_net_id or record['layer'] != data_region['layer']:
            continue
        brep = record['brep_shape']
        shape = Polygon([(v['x'], v['y']) for v in brep['outer_ring']['vertices']],
                        [[(v['x'], v['y']) for v in ring['vertices']] for ring in brep['inner_rings']])
        if (shape.intersection(authored_shape).area > 1e-8
                and shape.difference(authored_shape.buffer(1e-6)).area <= 1e-8):
            region_ids.append(record['pcb_copper_pour_id'])
            matched_shapes.append(shape)
    if not region_ids or unary_union(matched_shapes).intersection(authored_shape).area < .99*authored_shape.area:
        raise ValueError('The selected authored data branch has no matching real native copper')
    retired_ids = [clock_via['pcb_via_id'], data_via['pcb_via_id'], *region_ids]
    planner = helpers['Planner'](circuit, {
        'relocated_trace_layers': {r['pcb_trace_id']: {'top': None} for r in (clock, data)},
        'retired_feature_ids': retired_ids})
    planner.set_grid(.05)
    planner.via_copper_clearance = .27
    nets = {r['name']: r for r in circuit if r['type'] == 'source_net'}
    ports = {planner.port_name(port): port for port in planner.ports.values()
             if planner.source_ports[port['source_port_id']].get('source_component_id') in planner.source_components}
    result = {'classification': 'Coupled manual microphone ground and signal replacement; native validation required',
              'paths': [], 'pours': [], 'vias': [], 'straight_paths': [], 'unresolved': [],
              'retired_connection_path_indices': [31], 'retired_connection_region_indices': [43],
              'retired_native_feature_ids': retired_ids,
              'retired_inner_escapes': [{'source_name': 'MANUAL_INNER_ESCAPE_246_0', 'original_path_index': 246,
                                        'escape_index': 0, 'original_pcb_trace_id': clock['pcb_trace_id'],
                                        'retired_via_id': clock_via['pcb_via_id']}]}
    ground = reserve_ground(planner, {'port': ports['.U4 > .pin3'], 'root': planner.root(nets['GND']['source_net_id'])})
    if ground is None:
        result['unresolved'].append('No safe native ground join after releasing both adjacent signal escapes')
    else:
        result['straight_paths'] = [ground]
        xy = ground['planned_end_mm']
        result['vias'].append({'net': 'GND', 'x': xy[0], 'y': xy[1], 'hole_mm': .3, 'outer_mm': .45})
        clock_target = (clock_via['x'], clock_via['y'])
        if Point(clock_target).intersects(helpers['via_obstacles'](planner, {
                'root': planner.root(nets['MIC_BCLK']['source_net_id']), 'via_outer_mm': .45, 'via_hole_mm': .3})):
            result['unresolved'].append('The reserved ground join blocks the original clock corridor termination')
        else:
            bridges['reserve_via'](planner, {'root': planner.root(nets['MIC_BCLK']['source_net_id']), 'position': clock_target})
            result['vias'].append({'net': 'MIC_BCLK', 'x': clock_target[0], 'y': clock_target[1], 'hole_mm': .3, 'outer_mm': .45})
            for name, selector, target in [('MIC_BCLK', '.U4 > .pin4', clock_target),
                                           ('MIC_SD', '.U4 > .pin6', (target_data_via['x'], target_data_via['y']))]:
                replacement = replace_signal(planner, {'net': nets[name], 'port': ports[selector], 'target': target})
                if replacement is None:
                    result['unresolved'].append(f'No complete replacement for {name}')
                else:
                    result['paths'].append(replacement['path'])
                    result['pours'].extend(replacement['pours'])
                    result['vias'].extend(replacement['vias'])
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'complete': not result['unresolved'], 'ground': result['straight_paths'],
                      'replacement_paths': len(result['paths']), 'unresolved': result['unresolved']}))
    return 1 if result['unresolved'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
