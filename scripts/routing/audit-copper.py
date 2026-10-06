"""Measure generated copper and its connectivity without trusting route markers.

Fail on unsupported geometry. Bounding boxes deliberately overestimate curved
pads only when an exact contour is unavailable. Actual contours establish
clearance and physical contact for all supported shapes.
"""
import argparse
import collections
import hashlib
import json
import math
from pathlib import Path

from shapely.affinity import rotate
from shapely.geometry import LineString, Point, Polygon, box
from shapely.strtree import STRtree

LAYERS = ('top', 'inner1', 'inner2', 'bottom')
TOLERANCE_MM = 1e-6


class DisjointSets:
    def __init__(self):
        self.parent = {}

    def root(self, identifier):
        self.parent.setdefault(identifier, identifier)
        if self.parent[identifier] != identifier:
            self.parent[identifier] = self.root(self.parent[identifier])
        return self.parent[identifier]

    def join(self, identifiers):
        if identifiers:
            for identifier in identifiers[1:]:
                self.parent[self.root(identifier)] = self.root(identifiers[0])


def position(record):
    center = record.get('center', record)
    return center['x'], center['y']


def pad_contour(record):
    shape = record.get('shape', record.get('hole_shape'))
    if shape == 'polygon':
        return Polygon([position(p) for p in record['points']])
    center = position(record)
    diameter = record.get('outer_diameter', record.get('hole_diameter', 2 * record.get('radius', 0)))
    width = record.get('width', record.get('outer_width', record.get('rect_pad_width', diameter)))
    height = record.get('height', record.get('outer_height', record.get('rect_pad_height', diameter)))
    if not width or not height:
        raise ValueError(f'Unsupported dimensions: {record}')
    x, y = center
    if shape == 'circle':
        contour = Point(center).buffer(width / 2, quad_segs=128)
    elif shape in ('rect', 'rotated_rect', 'rotated_pill_hole_with_rect_pad'):
        radius=record.get('corner_radius',0) if shape in ('rect','rotated_rect') else 0
        if not isinstance(radius,(int,float)) or not math.isfinite(radius) or radius<0:
            raise ValueError('Invalid native rectangle corner radius')
        # Match native rounded rectangles and SVG radius clamping. Genuine
        # imported pill pads are emitted as rotated_rect with corner_radius;
        # replacing those arcs with a bounding box blocks legal pad fanouts.
        radius=min(radius,width/2,height/2)
        if radius:
            dx,dy=width/2-radius,height/2-radius
            if dx<1e-12 and dy<1e-12:core=Point(center)
            elif dx<1e-12 or dy<1e-12:core=LineString([(x-dx,y-dy),(x+dx,y+dy)])
            else:core=box(x-dx,y-dy,x+dx,y+dy)
            contour=core.buffer(radius,quad_segs=128)
        else:contour = box(x-width/2, y-height/2, x+width/2, y+height/2)
    elif shape in ('pill', 'rotated_pill'):
        radius = min(width, height) / 2
        dx, dy = max(0, width-height)/2, max(0, height-width)/2
        contour = LineString([(x-dx, y-dy), (x+dx, y+dy)]).buffer(radius, quad_segs=128)
    else:
        raise ValueError(f'Unsupported shape: {shape}')
    return rotate(contour, record.get('rect_ccw_rotation', record.get('ccw_rotation', 0)), origin=center)


def drill_contour(record):
    if record['type'] in ('pcb_via', 'pcb_hole'):
        return pad_contour({**record, 'shape': record.get('hole_shape', 'circle'),
                            'width': record['hole_diameter'], 'height': record['hole_diameter']})
    width = record.get('hole_width', record.get('hole_diameter'))
    height = record.get('hole_height', record.get('hole_diameter'))
    drill = {**record, 'shape': 'circle' if width == height else 'pill', 'width': width, 'height': height,
             'ccw_rotation': record.get('hole_ccw_rotation', record.get('ccw_rotation', 0))}
    drill.pop('rect_ccw_rotation', None)
    return pad_contour(drill)


def audit(circuit):
    electrical, physical = DisjointSets(), DisjointSets()
    traces = {r['source_trace_id']: r for r in circuit if r['type'] == 'source_trace'}
    pcb_traces = {r['pcb_trace_id']: r for r in circuit if r['type'] == 'pcb_trace'}
    ports = {r['pcb_port_id']: r for r in circuit if r['type'] == 'pcb_port'}
    source_ports = {r['source_port_id']: r for r in circuit if r['type'] == 'source_port'}
    components = {r['source_component_id']: r for r in circuit if r['type'] == 'source_component'}
    via_sources = {r['source_manually_placed_via_id']: r for r in circuit if r['type'] == 'source_manually_placed_via'}
    for record in traces.values():
        electrical.join(record.get('connected_source_port_ids', []) + record.get('connected_source_net_ids', []))
    for record in circuit:
        if record['type'] == 'source_component_internal_connection':
            electrical.join(record['source_port_ids'])
    for record in source_ports.values():
        via = via_sources.get(record.get('source_component_id'))
        if via and via.get('source_net_id'):
            electrical.join([record['source_port_id'], via['source_net_id']])

    def trace_root(record):
        source = traces[record['source_trace_id']]
        return electrical.root((source.get('connected_source_port_ids', []) + source.get('connected_source_net_ids', []))[0])

    def via_root(record):
        if record.get('pcb_trace_id'):
            return trace_root(pcb_traces[record['pcb_trace_id']])
        if record.get('source_trace_id'):
            return trace_root(record)
        if record.get('source_net_id'):
            return electrical.root(record['source_net_id'])
        raise ValueError(f'Unassigned native via: {record}')

    copper, drills, keepouts = [], [], []
    board = Polygon([position(p) for p in next(r for r in circuit if r['type'] == 'pcb_board')['outline']])
    route_errors, violations, minima = [], [], {}

    def copper_record(specification):
        copper.append(specification)

    def measure(category, gap, requirement, identifiers):
        if category not in minima or gap < minima[category]['clearance_mm']:
            minima[category] = {'clearance_mm': gap, 'requirement_mm': requirement, 'ids': identifiers}
        if gap + TOLERANCE_MM < requirement:
            violations.append({'category': category, 'clearance_mm': gap, 'requirement_mm': requirement, 'ids': identifiers})

    for record in circuit:
        ty = record['type']
        if ty in ('pcb_smtpad', 'pcb_plated_hole'):
            identifier = record[ty + '_id']
            port = ports.get(record.get('pcb_port_id'))
            root = electrical.root(port['source_port_id']) if port else 'unassigned_' + identifier
            contour = pad_contour(record)
            copper_record({'id': identifier, 'kind': 'pad', 'root': root, 'layers': record.get('layers', [record.get('layer')]),
                           'shape': contour, 'clearance_shape': contour, 'port_id': record.get('pcb_port_id')})
            if ty == 'pcb_plated_hole':
                drills.append({'id': identifier, 'shape': drill_contour(record), 'root': root, 'port_id': record.get('pcb_port_id'), 'plated': True})
        elif ty == 'pcb_trace':
            route = record['route']
            for index, (start, end) in enumerate(zip(route, route[1:])):
                if start['route_type'] == 'via' or end['route_type'] == 'via':
                    if math.dist(position(start), position(end)) > TOLERANCE_MM:
                        route_errors.append({'id': record['pcb_trace_id'], 'issue': 'Via disconnected from its adjacent wire', 'segment': index})
                    continue
                if start['route_type'] != 'wire' or end['route_type'] != 'wire' or start['layer'] != end['layer']:
                    raise ValueError(f'Unsupported or discontinuous route: {record}')
                width = max(start['width'], end['width']) if record.get('route_thickness_mode') == 'interpolated' else start['width']
                if width < 0.2 - TOLERANCE_MM:
                    route_errors.append({'id': record['pcb_trace_id'], 'issue': 'Trace below 0.2 mm', 'width_mm': width})
                contour = LineString([position(start), position(end)]).buffer(width/2, quad_segs=64)
                copper_record({'id': f"{record['pcb_trace_id']}:{index}", 'trace_id': record['pcb_trace_id'], 'kind': 'trace',
                               'root': trace_root(record), 'layers': [start['layer']], 'shape': contour, 'clearance_shape': contour,
                               'terminal_ports': [r[k] for r in route for k in ('start_pcb_port_id', 'end_pcb_port_id') if k in r]})
        elif ty == 'pcb_via':
            root, identifier = via_root(record), record['pcb_via_id']
            if set(record['layers']) != set(LAYERS):
                route_errors.append({'id': identifier, 'issue': 'Ordinary vias must span all four board layers',
                                     'layers': record['layers']})
            contour = Point(position(record)).buffer(record['outer_diameter']/2, quad_segs=128)
            copper_record({'id': identifier, 'kind': 'via', 'root': root, 'layers': record['layers'], 'shape': contour, 'clearance_shape': contour})
            drills.append({'id': identifier, 'shape': drill_contour(record), 'root': root, 'plated': True})
            # User's 2026-10-06 geometry requirement: 0.30 drill / 0.45 pad.
            # JLCPCB's official "Min. Via hole size/diameter" capability says
            # pad diameter >= drill + 0.10 mm (0.15 mm preferred). PTH land
            # annular-ring rules are separate from ordinary via requirements.
            for category, gap, minimum in [('via_hole', record['hole_diameter'], .3), ('via_outer', record['outer_diameter'], .45),
                                            ('via_annulus', (record['outer_diameter']-record['hole_diameter'])/2, .075)]:
                measure(category, gap, minimum, [identifier])
        elif ty == 'pcb_hole':
            drills.append({'id': record['pcb_hole_id'], 'shape': drill_contour(record), 'root': None, 'plated': False})
        elif ty == 'pcb_keepout':
            keepouts.append({'id': record['pcb_keepout_id'], 'shape': pad_contour(record), 'layers': record['layers']})
        elif ty == 'pcb_copper_pour':
            if record['shape'] != 'brep':
                raise ValueError(f'Unsupported pour: {record["shape"]}')
            brep = record['brep_shape']
            contour = Polygon([position(p) for p in brep['outer_ring']['vertices']],
                              [[position(p) for p in ring['vertices']] for ring in brep['inner_rings']])
            if not contour.is_valid:
                raise ValueError(f'Invalid native pour: {record["pcb_copper_pour_id"]}')
            copper_record({'id': record['pcb_copper_pour_id'], 'kind': 'pour', 'root': electrical.root(record['source_net_id']),
                           'layers': [record['layer']], 'shape': contour, 'clearance_shape': contour})

    drill_tree = STRtree([drill['shape'] for drill in drills])
    # Drill apertures contain no copper. Keep the original contours for DRC,
    # but never count a contact that exists only inside a drilled hole.
    for feature in copper:
        for drill_index in drill_tree.query(feature['shape']):
            feature['shape'] = feature['shape'].difference(drills[drill_index]['shape'])
    shapes = [feature['clearance_shape'] for feature in copper]
    tree = STRtree(shapes)
    for index, feature in enumerate(copper):
        physical.root(feature['id'])
        for other_index in tree.query(feature['clearance_shape'].buffer(.21)):
            if other_index <= index:
                continue
            other = copper[other_index]
            if not set(feature['layers']).intersection(other['layers']):
                continue
            if feature['root'] == other['root']:
                if feature['shape'].distance(other['shape']) <= TOLERANCE_MM:
                    physical.join([feature['id'], other['id']])
                continue
            kinds = {feature['kind'], other['kind']}
            requirement = .1 if kinds == {'pad'} else .2
            measure('copper_' + '_'.join(sorted(kinds)), feature['clearance_shape'].distance(other['clearance_shape']), requirement, [feature['id'], other['id']])
        if feature['kind'] in ('trace', 'via', 'pour'):
            gap = feature['clearance_shape'].distance(board.boundary) if board.covers(feature['clearance_shape']) else -1
            measure('board_edge', gap, .25, [feature['id']])
            for keepout in keepouts:
                if set(feature['layers']).intersection(keepout['layers']):
                    gap = feature['clearance_shape'].distance(keepout['shape'])
                    if feature['clearance_shape'].intersection(keepout['shape']).area > 1e-9:
                        gap = -1
                    measure('keepout', gap, 0, [feature['id'], keepout['id']])
        for drill_index in drill_tree.query(feature['clearance_shape'].buffer(.26)):
            drill = drills[drill_index]
            if feature['id'] == drill['id']:
                continue
            # Plated contacts join their own net intentionally; ordinary vias
            # must still keep their drills 0.2 mm from every component pad.
            if drill['plated'] and feature['root'] == drill['root'] and feature['kind'] in ('trace', 'pour'):
                continue
            if feature['kind'] == 'pad' and drill['id'].startswith('pcb_via'):
                measure('via_drill_to_pad', drill['shape'].distance(feature['clearance_shape']), .2, [drill['id'], feature['id']])
            elif feature['kind'] in ('trace', 'pour'):
                measure('copper_to_drill', drill['shape'].distance(feature['clearance_shape']), .25, [feature['id'], drill['id']])
    for index, drill in enumerate(drills):
        if not drill['id'].startswith('pcb_via'):
            continue
        for other_index in drill_tree.query(drill['shape'].buffer(.26)):
            other = drills[other_index]
            if other_index == index or other['id'].startswith('pcb_via') and other_index < index:
                continue
            measure('drill_to_drill', drill['shape'].distance(other['shape']), .25, [drill['id'], other['id']])

    features_by_port = collections.defaultdict(list)
    for feature in copper:
        if feature.get('port_id'):
            features_by_port[feature['port_id']].append(feature['id'])
    by_source_port = {port['source_port_id']: identifier for identifier, port in ports.items()}
    for record in circuit:
        if record['type'] == 'source_component_internal_connection':
            physical.join([feature for source_id in record['source_port_ids'] for feature in features_by_port.get(by_source_port.get(source_id), [])])
    nets = collections.defaultdict(list)
    for record in circuit:
        if record['type'] == 'source_net':
            nets[electrical.root(record['source_net_id'])].append(record['name'])
    net_merges = [names for names in nets.values() if len(names) > 1]
    connectivity = collections.defaultdict(lambda: collections.defaultdict(list))
    for identifier, port in ports.items():
        source = source_ports[port['source_port_id']]
        component = components.get(source.get('source_component_id'))
        if not component:
            continue
        root = electrical.root(port['source_port_id'])
        name = '/'.join(nets[root]) if root in nets else root
        label = f"{component['name']}.pin{source.get('pin_number', source['name'])}"
        feature_ids = features_by_port.get(identifier, [])
        groups = {physical.root(feature) for feature in feature_ids}
        if len(groups) != 1:
            route_errors.append({'id': identifier, 'issue': 'Physical port lacks one connected copper contact', 'features': feature_ids})
        connectivity[name][next(iter(groups), 'missing_' + identifier)].append(label)
    open_nets = [{'net': name, 'island_count': len(islands), 'islands': list(islands.values())}
                 for name, islands in connectivity.items() if len(islands) > 1]
    native_errors = collections.Counter(r['type'] for r in circuit if 'error' in r['type'])
    shorts = [v for v in violations if v['category'].startswith('copper_') and v['category'] != 'copper_to_drill' and v['clearance_mm'] <= TOLERANCE_MM]
    return {'scope': 'Every native wire, pad, through via and BREP pour; actual supported pad contours for DRC and connectivity, conservative interpolated wire thickness. No fabrication or thermal approval implied.',
            'copper_features': len(copper), 'native_errors': dict(native_errors), 'minima': minima,
            'minima_scope': 'Nearby copper pairs within 0.21 mm and drill pairs within 0.26 mm; STRtree excludes distant pairs without weakening any clearance requirement.',
            'drc_violation_count': len(violations) + len(route_errors), 'short_count': len(shorts),
            'violations': violations, 'route_errors': route_errors, 'merged_named_nets': net_merges,
            'physically_open_net_count': len(open_nets), 'physically_open_nets': open_nets,
            'physical_port_groups': {identifier: sorted({physical.root(f) for f in features_by_port.get(identifier, [])}) for identifier in ports},
            'physical_feature_groups': {feature['id']: physical.root(feature['id']) for feature in copper},
            'zero_drc_zero_shorts_and_connected': not (violations or route_errors or shorts or net_merges or open_nets or native_errors)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit_json')
    parser.add_argument('output_json')
    args = parser.parse_args()
    path = Path(args.circuit_json)
    result = audit(json.loads(path.read_text()))
    result['source_circuit_json'] = str(path)
    result['source_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    result['audit_script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['pad_contour_method'] = 'Native rounded rectangles honour corner_radius and rotation; rectangular bounds only where the native shape has no radius. Requirements and 0.000001 mm tolerance unchanged.'
    Path(args.output_json).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key not in ('violations', 'route_errors', 'physically_open_nets', 'physical_port_groups', 'physical_feature_groups')}, indent=2))
    return 0 if result['zero_drc_zero_shorts_and_connected'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
