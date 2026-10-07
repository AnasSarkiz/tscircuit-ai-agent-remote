"""Plan two real outer-layer speaker lanes around a shared clearance corridor.

This authors manual geometry, never solver results. Endpoint fanout, actual
through drills, full-width lane clearance and preserved VSYS anchors are checked
before proposing source integration. Native build/preservation gates remain
mandatory. Original circuit JSON and saved phase output stay untouched.
"""
import argparse
import hashlib
import json
import math
import runpy
import time
from pathlib import Path

from shapely.geometry import LineString, Point, Polygon

helpers = runpy.run_path(str(Path(__file__).with_name('plan-power-copper.py')))
geometry = runpy.run_path(str(Path(__file__).with_name('audit-copper.py')))
bridges = runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')))


def component_ports(planner):
    return {planner.port_name(port): port for port in planner.ports.values()
            if planner.source_ports[port['source_port_id']].get('source_component_id')
            in planner.source_components}


def relocate_clock_star(planner, specification):
    source = json.loads(Path('src/board/connection-copper.json').read_text())
    original = source['paths'][35]
    if original['net'] != 'AMP_LRCLK' or original['from'] != '.R70 > .pin1':
        raise ValueError('Clock-star retirement must match the recorded actual source escape')
    root = planner.root(specification['nets']['AMP_LRCLK']['source_net_id'])
    trace = next((record for record in planner.circuit if record['type'] == 'pcb_trace'
                  and planner.source_traces[record['source_trace_id']].get('name') == 'CONNECTION_ESCAPE_AMP_LRCLK_35'), None)
    if trace is None:
        if 35 not in source.get('retired_connection_path_indices', []):
            raise ValueError('Missing clock trace without an explicit source retirement')
        anchor = source['vias'][51]
        if anchor['net'] != 'AMP_LRCLK' or math.dist((anchor['x'], anchor['y']), (-16.7, 8.8)) > 1e-6:
            raise ValueError('Preserved clock-star anchor changed')
        matches = [record for record in planner.circuit if record['type'] == 'pcb_via'
                   and planner.via_root(record) == root
                   and math.dist((record['x'], record['y']), (anchor['x'], anchor['y'])) < 1e-6]
        if len(matches) != 1:
            raise ValueError('Expected one actual native clock-star via')
        via = matches[0]
    else:
        via = next(record for record in planner.circuit if record['type'] == 'pcb_via'
                   and record.get('pcb_trace_id') == trace['pcb_trace_id'])
    hole = geometry['drill_contour'](via)
    traces = ([LineString([(first['x'], first['y']), (last['x'], last['y'])]).buffer(first['width']/2)
              for first, last in zip(trace['route'], trace['route'][1:])
              if first['route_type'] == last['route_type'] == 'wire']
              if trace is not None else [])
    regions = [source['pours'][index] for index in (44, 47)]
    if any(region['net'] != 'AMP_LRCLK' for region in regions):
        raise ValueError('Clock-star regions changed; refuse an ambiguous retirement')
    shapes = [Polygon([(point['x'], point['y']) for point in region['outline']]) for region in regions]
    via_land = Point(via['x'], via['y']).buffer(via['outer_diameter']/2)
    planner.holes = [contour for contour in planner.holes if not contour.equals(hole)]
    planner.copper = [(other_root, layer, contour) for other_root, layer, contour in planner.copper
                      if not (other_root == root and (contour.equals(via_land)
                          or layer == 'top' and any(contour.equals(line) for line in traces)
                          or layer == 'inner2' and any(contour.difference(shape.buffer(1e-6)).area <= 1e-8 for shape in shapes)))]
    target_points = [tuple(regions[0]['path_mm'][-1]), tuple(regions[1]['path_mm'][0])]
    port = component_ports(planner)[original['from']]
    via_blocks = helpers['via_obstacles'](planner, {'root': root, 'via_outer_mm': .45, 'via_hole_mm': .3})
    top_blocks = planner.obstacles(root, 'top', .2)
    root_names = {planner.root(record['source_net_id']): record['name']
                  for record in planner.circuit if record['type'] == 'source_net'}
    for position in ((-19.4, 9.4), (-20., 10.), (-18.8, 6.3), (-16.7, 8.8)):
        point_shape = Point(position)
        blockers = [{'net': root_names.get(other_root, other_root), 'layer': layer,
                     'distance_mm': point_shape.distance(contour), 'bounds_mm': contour.bounds}
                    for other_root, layer, contour in planner.copper
                    if other_root != root and point_shape.distance(contour) < .435]
        print(json.dumps({'clock_star_clearance_diagnosis_mm': position,
                          'blocking_copper': blockers,
                          'blocking_drills': [contour.bounds for contour in planner.holes
                                              if point_shape.distance(contour) < .41]}), flush=True)
    positions = [(-20.25, 5.4), (-20.6, 4.9), (-20.8, 5.4),
                 (-19.4, 9.4), (-19.4, 8.8), (-20., 10.), (-20.2, 9.75), (-18.8, 6.3)]
    positions.extend((round(port['x']+distance*math.cos(math.radians(degrees)), 6),
                      round(port['y']+distance*math.sin(math.radians(degrees)), 6))
                     for distance in (.8, 1.2, 1.6, 2.) for degrees in range(0, 360, 30))
    corridor = LineString([(-16.25, 5.8), (-16.25, 10.)])
    legal_candidates = [(round(-23.+x*.2, 6), round(3.8+y*.2, 6))
                        for x in range(48) for y in range(37)]
    legal_candidates = [position for position in legal_candidates
                        if not Point(position).intersects(via_blocks)
                        and Point(position).distance(corridor) >= 1.15]
    legal_candidates.sort(key=lambda position: math.dist(position, (port['x'], port['y'])))
    print(json.dumps({'legal_clock_candidates_clear_of_speaker_corridor': len(legal_candidates),
                      'nearest_candidates_mm': legal_candidates[:12]}), flush=True)
    positions.extend(legal_candidates)
    counters = {'via_blocked': 0, 'neck_blocked': 0, 'peer_route_blocked': 0}
    for position in positions:
        if Point(position).intersects(via_blocks) or Point(position).distance(corridor) < 1.15:
            counters['via_blocked'] += 1
            continue
        neck = planner.grid_route(((port['x'], port['y']), position, top_blocks))
        if not neck:
            counters['neck_blocked'] += 1
            continue
        saved_copper, saved_holes, saved_roots = list(planner.copper), list(planner.holes), dict(planner.plated_hole_roots)
        bridges['reserve_via'](planner, {'root': root, 'position': position})
        planner.copper.append((root, 'top', LineString(neck).buffer(.1)))
        pours = []
        for target in target_points:
            route = helpers['wide_multilayer_route'](planner, {
                'root': root, 'first': position, 'last': target, 'width': .202,
                'new_vias': [position, *target_points], 'layers': ('inner2', 'inner1'),
                'via_outer_mm': .45, 'via_hole_mm': .3, 'first_layer': 'inner2',
                'last_layer': 'inner2', 'multi_anchor': True})
            if route is None or route[1]:
                counters['peer_route_blocked'] += 1
                print(json.dumps({'clock_star_attempt_mm': position, 'target_mm': target,
                                  'route_found': route is not None,
                                  'required_transition_count': len(route[1]) if route else None}), flush=True)
                break
            pours.extend(bridges['region_records']('AMP_LRCLK', {'parts': route[0], 'width': .2}))
        else:
            escape = helpers['escape_record'](planner, {'root': root, 'net': specification['nets']['AMP_LRCLK'],
                                                       'port': port, 'width': .2, 'positions': neck,
                                                       'via_outer_mm': .45, 'via_hole_mm': .3})
            for region in pours:
                planner.copper.append((root, region['layer'], Polygon([(p['x'], p['y']) for p in region['outline']])))
            return {'classification': 'Manual clock-star relocation; native qualification required',
                    'retired_connection_path_index': 35, 'retired_connection_region_indices': [44, 47],
                    'original_native_trace_id': trace['pcb_trace_id'] if trace else None,
                    'retired_connection_via_index': 51 if trace is None else None,
                    'original_native_via_id': via['pcb_via_id'],
                    'paths': [escape], 'pours': pours, 'new_star_mm': position,
                    'preserved_original_clock_peer_anchors_mm': target_points}
        planner.copper, planner.holes, planner.plated_hole_roots = saved_copper, saved_holes, saved_roots
    print(json.dumps({'clock_relocation_failure_stage_counts': counters}), flush=True)
    raise ValueError('No qualified clock-star relocation found; no board sources changed')


def planning_scene(native, preserve_vsys=False):
    circuit = json.loads(native.read_text())
    planner = helpers['Planner'](circuit)
    planner.set_grid(.05)
    nets = {record['name']: record for record in circuit if record['type'] == 'source_net'}
    pair_roots = {planner.root(nets[name]['source_net_id']) for name in ('SPEAKER_P', 'SPEAKER_N')}
    vsys_root = planner.root(nets['VSYS']['source_net_id'])
    regions = []
    for filename in ('src/board/manual-power-copper.json', 'src/board/connection-copper.json'):
        source = json.loads(Path(filename).read_text())
        for index, region in enumerate(source['pours']):
            if region['net'] == 'VSYS' and region['layer'] in ('top', 'bottom') and region['nominal_width_mm'] == 1.:
                regions.append({'source': filename, 'index': index, 'region': region})
    fixed = ('src/board/manual-power-copper.json', 13)
    removable = [] if preserve_vsys else [record for record in regions if (record['source'], record['index']) != fixed]
    shapes = [(record['region']['layer'], Polygon([(p['x'], p['y']) for p in record['region']['outline']]))
              for record in removable]
    planner.copper = [(root, layer, contour) for root, layer, contour in planner.copper
                      if root not in pair_roots and not (root == vsys_root and any(
                          layer == region_layer and contour.difference(shape.buffer(1e-6)).area <= 1e-8
                          for region_layer, shape in shapes))]
    retired_via_holes = {geometry['drill_contour'](record).wkb
                         for record in circuit if record['type'] == 'pcb_via' and planner.via_root(record) in pair_roots}
    planner.holes = [hole for hole in planner.holes if hole.wkb not in retired_via_holes]
    anchors = sorted({tuple(point) for record in regions
                      for point in (record['region']['path_mm'][0], record['region']['path_mm'][-1])})
    return planner, {'nets': nets, 'pair_roots': pair_roots, 'vsys_root': vsys_root,
                     'source_regions': regions, 'removable_regions': removable,
                     'fixed_region': fixed, 'anchors': anchors}


def offset_lanes(centerline):
    line = LineString(centerline)
    lanes = {}
    for net, distance in (('SPEAKER_N', .4), ('SPEAKER_P', -.4)):
        lane = line.offset_curve(distance, join_style=2, mitre_limit=2)
        if lane.geom_type != 'LineString' or not lane.is_simple:
            raise ValueError('Shared corridor must produce two continuous non-crossing lanes')
        points = list(lane.coords)
        if math.dist(points[-1], centerline[0]) < math.dist(points[0], centerline[0]):
            points.reverse()
        lanes[net] = points
    if LineString(lanes['SPEAKER_P']).distance(LineString(lanes['SPEAKER_N'])) < .8-1e-6:
        raise ValueError('Offset lane bends violate the unchanged 0.20 mm copper gap')
    return lanes


def multilayer_lanes(parts):
    """Offset a shared outer-layer centreline, with paired real through vias."""
    vertices, edge_layers = [], []
    for layer, points in parts:
        if vertices and math.dist(vertices[-1], points[0]) > 1e-6:
            raise ValueError('Layer transitions must share an actual position')
        if not vertices:
            vertices.append(points[0])
        for position in points[1:]:
            if math.dist(vertices[-1], position) < 1e-6:
                continue
            vertices.append(position)
            edge_layers.append(layer)
    normals = []
    for first, last in zip(vertices, vertices[1:]):
        length_mm = math.dist(first, last)
        normals.append((-(last[1]-first[1])/length_mm, (last[0]-first[0])/length_mm))
    offsets = [normals[0]]
    for previous, following in zip(normals, normals[1:]):
        denominator = 1+previous[0]*following[0]+previous[1]*following[1]
        if denominator < 1-1e-6:
            raise ValueError('Pair corridor contains a bend sharper than 90 degrees')
        offsets.append(((previous[0]+following[0])/denominator,
                        (previous[1]+following[1])/denominator))
    offsets.append(normals[-1])
    result = {}
    for net, distance_mm in (('SPEAKER_N', .401), ('SPEAKER_P', -.401)):
        points = [(position[0]+normal[0]*distance_mm, position[1]+normal[1]*distance_mm)
                  for position, normal in zip(vertices, offsets)]
        lane_parts, via_positions = [], []
        current_layer, current_points = edge_layers[0], [points[0]]
        for index, layer in enumerate(edge_layers):
            if layer != current_layer:
                lane_parts.append((current_layer, current_points))
                via_positions.append(points[index])
                current_layer, current_points = layer, [points[index]]
            current_points.append(points[index+1])
        lane_parts.append((current_layer, current_points))
        result[net] = {'parts_mm': lane_parts, 'transition_vias_mm': via_positions}
    return result


def qualify_multilayer_fanout(planner, specification):
    result, pair_copper, pair_holes = {}, {}, {}
    ports = component_ports(planner)
    for net, first, last in (('SPEAKER_P', '.U3 > .pin9', '.J4 > .pin1'),
                             ('SPEAKER_N', '.U3 > .pin10', '.J4 > .pin2')):
        root = planner.root(specification['nets'][net]['source_net_id'])
        lane = specification['lanes'][net]
        start_position = lane['parts_mm'][0][1][0]
        end_position = lane['parts_mm'][-1][1][-1]
        vias = [start_position, *lane['transition_vias_mm']]
        via_blocks = helpers['via_obstacles'](planner, {'root': root, 'via_outer_mm': .45, 'via_hole_mm': .3})
        if any(Point(position).intersects(via_blocks) for position in vias):
            return None
        neck = planner.grid_route(((ports[first]['x'], ports[first]['y']), start_position,
                                   planner.obstacles(root, 'top', .275)))
        finish_layer = lane['parts_mm'][-1][0]
        finish = planner.grid_route((end_position, (ports[last]['x'], ports[last]['y']),
                                     planner.obstacles(root, finish_layer, .6)))
        if not neck or not finish or LineString(neck).length+LineString(finish).length > 5:
            return None
        if any(LineString(points).intersects(planner.obstacles(root, layer, .6))
               for layer, points in lane['parts_mm']):
            return None
        copper = [('top', LineString(neck).buffer(.275/2)),
                  (finish_layer, LineString(finish).buffer(.6/2))]
        copper.extend((layer, LineString(points).buffer(.6/2)) for layer, points in lane['parts_mm'])
        copper.extend((layer, Point(position).buffer(.225)) for position in vias
                      for layer in ('top', 'inner1', 'inner2', 'bottom'))
        holes = [Point(position).buffer(.15) for position in vias]
        # Every new ordinary drill also clears its own route except the
        # intentional electrically attached via lands and adjacent segments.
        if any(first_hole.distance(last_hole) < .26 for index, first_hole in enumerate(holes)
               for last_hole in holes[index+1:]):
            return None
        pair_copper[net], pair_holes[net] = copper, holes
        result[net] = {**lane, 'selector': first, 'target_selector': last,
                       'neck_mm': neck, 'finish_mm': finish, 'start_via_mm': start_position,
                       'neck_width_mm': .275, 'trunk_width_mm': .6,
                       'length_mm': LineString(neck).length+LineString(finish).length+
                       sum(LineString(points).length for _, points in lane['parts_mm'])}
    first, last = 'SPEAKER_P', 'SPEAKER_N'
    if any(first_layer == last_layer and first_shape.distance(last_shape) < .2-1e-6
           for first_layer, first_shape in pair_copper[first] for last_layer, last_shape in pair_copper[last]):
        return None
    if any(first_hole.distance(last_hole) < .25-1e-6 for first_hole in pair_holes[first]
           for last_hole in pair_holes[last]):
        return None
    if any(hole.distance(shape) < .25-1e-6 for net in (first, last)
           for hole in pair_holes[net] for _, shape in pair_copper[last if net == first else first]):
        return None
    if abs(result[first]['length_mm']-result[last]['length_mm']) > 2:
        return None
    return result


def find_local_bundle(planner, specification):
    """Route to the nearby header while retaining every original VSYS strip."""
    ports = component_ports(planner)
    end_ports = [ports[name] for name in ('.J4 > .pin1', '.J4 > .pin2')]
    start_ports = [ports[name] for name in ('.U3 > .pin9', '.U3 > .pin10')]
    end = tuple(sum(port[axis] for port in end_ports)/2 for axis in ('x', 'y'))
    start_x = sum(port['x'] for port in start_ports)/2
    if end_ports[0]['y'] <= end_ports[1]['y'] or abs(end_ports[0]['x']-end_ports[1]['x']) > 1e-5:
        raise ValueError('Local fanout requires the verified rotated header pin order')
    for start_y in (6.1, 6.3, 6.5, 6.7, 7.):
        for end_x in (end[0], end[0]+.3, end[0]+.6, end[0]-.3):
            centerline = [(start_x, start_y), (start_x, end[1]), (end_x, end[1])]
            for layer in ('bottom', 'top'):
                parts = [(layer, centerline)]
                lanes = multilayer_lanes(parts)
                fanout = qualify_multilayer_fanout(planner, {**specification, 'lanes': lanes})
                print(json.dumps({'local_pair_trial': centerline, 'layer': layer,
                                  'qualified': fanout is not None}), flush=True)
                if fanout:
                    return {'centerline_parts_mm': parts, 'lanes': fanout,
                            'preserved_all_vsys_source_regions': True}
    return None


def find_multilayer_bundle(planner, specification):
    pads = planner.pads
    planner.pads = [(record, shape) for record, shape in pads
                    if not (record.get('pcb_port_id') in planner.ports and
                            planner.root(planner.ports[record['pcb_port_id']]['source_port_id']) in specification['pair_roots'])]
    starts = [(-16.25, y_mm) for y_mm in (6.1, 6.2, 6.5, 6.8, 7., 7.5, 8.)]
    obstacles = {layer: planner.obstacles('speaker_bundle_space_only', layer, 1.402)
                 for layer in ('bottom', 'top')}
    for start in starts:
        for end_y_mm in (10., 11., 12.):
            end = (22.02499995, end_y_mm)
            first, last = (start[0], start[1]+.25), (end[0], end[1]+.5)
            for layer in ('bottom', 'top'):
                if any(LineString(points).intersects(obstacles[layer]) for points in ([start, first], [last, end])):
                    continue
                route = helpers['wide_multilayer_route'](planner, {
                    'root': 'speaker_bundle_space_only', 'first': first, 'last': last,
                    'width': 1.402, 'new_vias': [], 'layers': ('bottom', 'top'),
                    'first_layer': layer, 'last_layer': layer, 'multi_anchor': True,
                    'routing_geometry': 'native_wire',
                    # Planning envelope contains two .45/.30 mm vias at any
                    # allowed miter. Emitted holes/pads remain .30/.45 mm.
                    'via_outer_mm': .45 if specification.get('search_actual_pair_transitions') else 1.586,
                    'via_hole_mm': .3 if specification.get('search_actual_pair_transitions') else 1.434})
                if route is None:
                    print(json.dumps({'multilayer_pair_start_mm': start, 'end_mm': end,
                                      'layer': layer, 'reason': 'no conservative corridor'}), flush=True)
                    continue
                parts = route[0]
                parts[0][1].insert(0, start)
                parts[-1][1].append(end)
                planner.pads = pads
                try:
                    lanes = multilayer_lanes(parts)
                    fanout = qualify_multilayer_fanout(planner, {**specification, 'lanes': lanes})
                except ValueError as error:
                    fanout = None
                    print(json.dumps({'multilayer_pair_rejected': str(error)}), flush=True)
                if fanout:
                    return {'centerline_parts_mm': parts, 'lanes': fanout}
                print(json.dumps({'multilayer_pair_start_mm': start, 'end_mm': end,
                                  'layer': layer, 'reason': 'actual lane or fanout rejected'}), flush=True)
                planner.pads = [(record, shape) for record, shape in pads
                                if not (record.get('pcb_port_id') in planner.ports and
                                        planner.root(planner.ports[record['pcb_port_id']]['source_port_id']) in specification['pair_roots'])]
    planner.pads = pads
    return None


def endpoint_fanout(planner, specification):
    result = {}
    for net, first, last in (
        ('SPEAKER_P', '.U3 > .pin9', '.J4 > .pin1'),
        ('SPEAKER_N', '.U3 > .pin10', '.J4 > .pin2'),
    ):
        root = planner.root(specification['nets'][net]['source_net_id'])
        ports = component_ports(planner)
        start, end = ports[first], ports[last]
        lane = specification['lanes'][net]
        start_position = (start['x'], start['y'])
        end_position = (end['x'], end['y'])
        via_blocks = helpers['via_obstacles'](planner, {'root': root, 'via_outer_mm': .45, 'via_hole_mm': .3})
        if Point(lane[0]).intersects(via_blocks):
            return None
        neck = planner.grid_route((start_position, lane[0], planner.obstacles(root, 'top', .275)))
        finish = planner.grid_route((lane[-1], end_position, planner.obstacles(root, specification['layer'], .6)))
        if not neck or not finish or LineString(neck).length > 5 or LineString(finish).length > 5:
            return None
        trunk_obstacles = planner.obstacles(root, specification['layer'], .6)
        if LineString(lane).intersects(trunk_obstacles):
            return None
        result[net] = {'selector': first, 'target_selector': last, 'neck_mm': neck,
                       'trunk_mm': lane, 'finish_mm': finish,
                       'neck_width_mm': .275, 'trunk_width_mm': .6,
                       'layer': specification['layer'],
                       'length_mm': sum(LineString(points).length for points in (neck, lane, finish))}
    first, second = result['SPEAKER_P'], result['SPEAKER_N']
    for key, width in (('neck_mm', .275), ('trunk_mm', .6), ('finish_mm', .6)):
        if LineString(first[key]).distance(LineString(second[key])) < width+.2-1e-6:
            return None
    return result


def find_bundle(planner, specification):
    # Exclude only the two terminal pad contours from the conservative bundle
    # space. Each actual lane/fanout is checked against them independently.
    original_pads = planner.pads
    planner.pads = [(record, shape) for record, shape in original_pads
                    if not (record.get('pcb_port_id') in planner.ports and
                            planner.root(planner.ports[record['pcb_port_id']]['source_port_id']) in specification['pair_roots'])]
    obstacles = {layer: planner.obstacles('speaker_bundle_space_only', layer, 1.4)
                 for layer in ('bottom', 'top')}
    planner.pads = original_pads
    counters = {'departure_blocked': 0, 'arrival_blocked': 0, 'no_centerline': 0,
                'offset_rejected': 0, 'fanout_rejected': 0}
    for layer in ('bottom', 'top'):
        for start_x_mm, start_y_mm in ((-16.25, 7.), (-16.25, 8.), (-16.25, 9.),
                                     (-15.5, 7.), (-15.5, 8.), (-17., 7.),
                                     (-14.5, 7.5), (-18., 7.5)):
            start = (start_x_mm, start_y_mm)
            for end_y_mm in (10., 11., 12., 9.5):
                end = (22.02499995, end_y_mm)
                # North departure and south arrival preserve pad ordering.
                first, last = (start[0], start[1]+1.), (end[0], end[1]+1.)
                if LineString([start, first]).intersects(obstacles[layer]):
                    counters['departure_blocked'] += 1
                    continue
                if LineString([last, end]).intersects(obstacles[layer]):
                    counters['arrival_blocked'] += 1
                    continue
                route = planner.grid_route((first, last, obstacles[layer]))
                if route is None:
                    counters['no_centerline'] += 1
                    continue
                centerline = [start, *route, end]
                try:
                    lanes = offset_lanes(centerline)
                except ValueError:
                    counters['offset_rejected'] += 1
                    continue
                fanout = endpoint_fanout(planner, {**specification, 'lanes': lanes, 'layer': layer})
                if fanout:
                    return {'centerline_mm': centerline, 'layer': layer, 'lanes': fanout}
                counters['fanout_rejected'] += 1
            print(json.dumps({'attempted_bundle_start_mm': start, 'layer': layer,
                              'failure_stage_counts': counters}), flush=True)
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('native', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--clear-clock-star', action='store_true')
    parser.add_argument('--paired-multilayer', action='store_true')
    parser.add_argument('--local-header', action='store_true')
    parser.add_argument('--search-actual-pair-transitions', action='store_true',
                        help='Explore centre transitions, then require both actual .30/.45 mm vias to clear independently')
    args = parser.parse_args()
    started = time.monotonic()
    planner, specification = planning_scene(args.native, preserve_vsys=args.local_header)
    specification['search_actual_pair_transitions'] = args.search_actual_pair_transitions
    result = {'classification': 'Authored coupled manual proposal; not autorouter output or accepted native copper',
              'native_sha256': hashlib.sha256(args.native.read_bytes()).hexdigest(),
              'fixed_vsys_region': specification['fixed_region'],
              'original_vsys_anchors_mm': specification['anchors'],
              'native_qualified': False, 'accepted': False}
    if args.clear_clock_star:
        result['clock_relocation'] = relocate_clock_star(planner, specification)
        args.output.write_text(json.dumps({**result, 'unresolved': ['Speaker lanes not yet qualified']}, indent=2)+'\n')
        print(json.dumps({'clock_star_relocated_mm': result['clock_relocation']['new_star_mm']}), flush=True)
    bundle = (find_local_bundle(planner, specification) if args.local_header else
              find_multilayer_bundle(planner, specification) if args.paired_multilayer else find_bundle(planner, specification))
    result['bundle'] = bundle
    result['unresolved'] = [] if bundle else ['No qualified full-width single-layer shared speaker corridor found']
    result['duration_seconds'] = round(time.monotonic()-started, 3)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'bundle_found': bundle is not None, 'duration_seconds': result['duration_seconds']}))
    return 0 if bundle else 1


if __name__ == '__main__':
    raise SystemExit(main())
