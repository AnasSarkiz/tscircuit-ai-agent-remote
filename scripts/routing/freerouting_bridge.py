"""Transfer native copper to Specctra without changing supplier definitions.

All session output remains proposals until native regeneration and physical
clearance, width, connectivity and original-copper preservation audits pass.
"""
import argparse
import collections
import hashlib
import json
import math
import re
import runpy
from pathlib import Path

from shapely import constrained_delaunay_triangles
from shapely.affinity import rotate, translate
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

HELPERS = runpy.run_path(str(Path(__file__).with_name('plan-manual-signals.py')))
AUDIT = HELPERS['geometry_helpers']
LAYERS = ('top', 'inner1', 'inner2', 'bottom')
MANUAL_OR_DEFERRED_NETS = {'GND', 'USB_DP', 'USB_DN', 'SPEAKER_P', 'SPEAKER_N'}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def number(mm):
    """DSN coordinates in micrometres, with nanometre integer resolution."""
    return f'{mm * 1000:.6f}'.rstrip('0').rstrip('.') or '0'


def polygon_scope(shape, layer):
    if not isinstance(shape, Polygon) or not shape.is_valid or shape.is_empty:
        raise ValueError('Expected a nonempty valid polygon')
    xy = ' '.join(f'{number(x)} {number(y)}' for x, y in list(shape.exterior.coords)[:-1])
    return f'(polygon {layer} 0 {xy})'


def area_scope(shape, layer):
    outer = polygon_scope(shape, layer)
    windows = ' '.join(f'(window {polygon_scope(Polygon(ring), layer)})' for ring in shape.interiors)
    return f'{outer} {windows}'


def convex_pieces(shape):
    if shape.convex_hull.difference(shape).area <= 1e-12 and not shape.interiors:
        return [shape]
    pieces = list(constrained_delaunay_triangles(shape).geoms)
    combined = unary_union(pieces)
    if combined.symmetric_difference(shape).area > 1e-10:
        raise ValueError('Convex decomposition did not preserve native pad copper')
    if any(not shape.covers(piece) for piece in pieces):
        raise ValueError('Convex decomposition extends outside native copper')
    return pieces


def native_pad_primitives(record, contour):
    """Keep native circles/capsules analytical in the external file format."""
    kind = record.get('shape')
    if kind not in ('circle', 'pill', 'rotated_pill'):
        return [{'contour': piece, 'circle_diameter_mm': None} for piece in convex_pieces(contour)]
    center_record = record.get('center', record)
    center = center_record['x'], center_record['y']
    diameter = record.get('outer_diameter', record.get('hole_diameter', 2 * record.get('radius', 0)))
    width = record.get('width', record.get('outer_width', record.get('rect_pad_width', diameter)))
    height = record.get('height', record.get('outer_height', record.get('rect_pad_height', diameter)))
    if kind == 'circle' or width == height:
        return [{'contour': contour, 'circle_diameter_mm': width}]
    radius = min(width, height) / 2
    dx, dy = max(0, width - height) / 2, max(0, height - width) / 2
    angle = record.get('rect_ccw_rotation', record.get('ccw_rotation', 0))
    primitives = []
    for offset in (-1, 1):
        end = rotate(Point(center[0] + offset * dx, center[1] + offset * dy), angle, origin=center)
        primitives.append({'contour': end.buffer(radius, quad_segs=128),
                           'circle_diameter_mm': radius * 2})
    rectangle = box(center[0] - (dx or radius), center[1] - (dy or radius),
                    center[0] + (dx or radius), center[1] + (dy or radius))
    primitives.append({'contour': rotate(rectangle, angle, origin=center), 'circle_diameter_mm': None})
    combined = unary_union([primitive['contour'] for primitive in primitives])
    if not combined.buffer(.00002).covers(contour) or not contour.buffer(.00002).covers(combined):
        raise ValueError('Analytical pad primitives changed native pad geometry')
    return primitives


def primitive_scope(primitive, layer):
    contour = primitive['contour']
    if primitive['circle_diameter_mm'] is None:
        return polygon_scope(contour, layer)
    center = contour.centroid
    return f'(circle {layer} {number(primitive["circle_diameter_mm"])} {number(center.x)} {number(center.y)})'


def native_pour(record):
    if record['shape'] != 'brep':
        raise ValueError('Only actual native BREP pours are supported')
    brep = record['brep_shape']
    return Polygon([(p['x'], p['y']) for p in brep['outer_ring']['vertices']],
                   [[(p['x'], p['y']) for p in ring['vertices']] for ring in brep['inner_rings']])


def partition_pour(shape, tile_mm):
    """Partition complex regions exactly; never simplify or fill their holes."""
    vertex_count = len(shape.exterior.coords) + sum(len(ring.coords) for ring in shape.interiors)
    if not tile_mm or vertex_count <= 500:
        return [shape]
    min_x, min_y, max_x, max_y = shape.bounds
    pieces = []
    for x_index in range(math.floor(min_x / tile_mm), math.ceil(max_x / tile_mm)):
        for y_index in range(math.floor(min_y / tile_mm), math.ceil(max_y / tile_mm)):
            tile = box(x_index * tile_mm, y_index * tile_mm,
                       (x_index + 1) * tile_mm, (y_index + 1) * tile_mm)
            intersection = shape.intersection(tile)
            candidates = list(intersection.geoms) if hasattr(intersection, 'geoms') else [intersection]
            pieces.extend(piece for piece in candidates if isinstance(piece, Polygon) and not piece.is_empty)
    if unary_union(pieces).symmetric_difference(shape).area > 1e-10:
        raise ValueError('Copper region partition changed actual native geometry')
    return pieces


def write_json(path, record):
    Path(path).write_text(json.dumps(record, indent=2) + '\n')


def net_name(root, names):
    return names.setdefault(root, 'UNNAMED_' + root)


def via_stack(specification, context):
    diameter, hole = specification['outer_mm'], specification['hole_mm']
    name = f'VIA_{round(diameter * 1e6)}_{round(hole * 1e6)}'
    if name not in context['manifest']['via_padstacks']:
        shapes = ' '.join(f'(shape (circle {layer} {number(diameter)} 0 0))' for layer in LAYERS)
        context['library'].append(f'(padstack {name} {shapes} (attach off))')
        context['manifest']['via_padstacks'][name] = {'outer_mm': diameter, 'hole_mm': hole, 'layers': list(LAYERS)}
    return name


def export_design(args):
    circuit = json.loads(Path(args.circuit_json).read_text())
    planner = HELPERS['ManualSignalPlanner'](circuit)
    named_nets = {planner.root(r['source_net_id']): r for r in circuit if r['type'] == 'source_net'}
    names = {root: record['name'] for root, record in named_nets.items()}
    nets = collections.defaultdict(list)
    manifest = {'classification': 'DSN transfer from untouched native geometry, not accepted routing',
        'source_circuit_json': args.circuit_json, 'source_sha256': sha256(args.circuit_json),
        'layers': list(LAYERS), 'unit': 'um', 'resolution': 1000,
        'clearance_mm': .21, 'wire_to_existing_region_reserve_mm': .27,
        'pad_to_pad_clearance_mm': .1, 'hole_reserve_mm': .26,
        'pour_partition_tile_mm': args.pour_tile_mm,
        'expected_engine_grid_mm': args.engine_grid_mm,
        'pins': {}, 'features': [], 'via_padstacks': {}, 'active_nets': args.nets,
        'pad_metal_regions': []}

    structure = [f'(layer {layer} (type signal) (property (index {index})))'
                 for index, layer in enumerate(LAYERS)]
    board = next(r for r in circuit if r['type'] == 'pcb_board')
    shape = Polygon([(p['x'], p['y']) for p in board['outline']])
    structure += [f'(boundary {polygon_scope(shape, "pcb")})',
                  '(snap_angle none)', '(control (via_at_smd off))',
                  '(rule (width 200) (clearance 210) (clearance 270 (type wire_area)) '
                  '(clearance 270 (type via_area)) (clearance 100 (type smd_smd)) '
                  '(clearance 0 (type via_padviareserve)) '
                  '(clearance 0 (type wire_drillreserve)) (clearance 0 (type via_drillreserve)))']
    manifest['features'].append({'type': 'pcb_board', 'id': board['pcb_board_id'], 'outline_mm': list(shape.exterior.coords)})
    library, placement, wiring = [], [], []
    export_context = {'library': library, 'manifest': manifest}
    protected = set(MANUAL_OR_DEFERRED_NETS)
    for port in planner.ports.values():
        source = planner.source_ports[port['source_port_id']]
        component = planner.source_components.get(source.get('source_component_id'))
        if component and component['name'] in ('J3', 'J7'):
            protected.add(net_name(planner.root(port['source_port_id']), names))
    forbidden = set(args.nets).intersection(protected)
    if forbidden:
        raise ValueError(f'Contact-dependent or matched/ground routing must remain manual: {sorted(forbidden)}')
    if any(name not in {r['name'] for r in named_nets.values()} for name in args.nets):
        raise ValueError('An active net is not present in native source')

    for record, contour in planner.pads:
        identifier = record[record['type'] + '_id']
        port = planner.ports.get(record.get('pcb_port_id'))
        root = planner.root(port['source_port_id']) if port else 'FLOATING_' + identifier
        name = net_name(root, names)
        layers = record.get('layers', [record.get('layer')])
        if not set(layers).issubset(LAYERS):
            raise ValueError(f'Unsupported native pad layers: {layers}')
        primitives = native_pad_primitives(record, contour)
        pieces = [primitive['contour'] for primitive in primitives]
        for index, primitive in enumerate(primitives):
            piece = primitive['contour']
            center = piece.centroid if primitive['circle_diameter_mm'] else piece.representative_point()
            # Placement aligned to the measured engine grid prevents rounded local
            # coordinates from creating gaps between adjacent convex pieces.
            center = Point(round(center.x / args.engine_grid_mm) * args.engine_grid_mm,
                           round(center.y / args.engine_grid_mm) * args.engine_grid_mm)
            pad_id = f'{identifier}_{index}'
            local = translate(piece, xoff=-center.x, yoff=-center.y)
            local_primitive = {'contour': local, 'circle_diameter_mm': primitive['circle_diameter_mm']}
            shapes = ' '.join(f'(shape {primitive_scope(local_primitive, layer)})' for layer in layers)
            library += [f'(padstack PS_{pad_id} {shapes} (attach off))',
                        f'(image IMG_{pad_id} (pin PS_{pad_id} 1 0 0))']
            placement.append(f'(component IMG_{pad_id} (place {pad_id} {number(center.x)} {number(center.y)} front 0 (lock_type position)))')
            pin = f'{pad_id}-1'
            nets[name].append(pin)
            manifest['pins'][pin] = {'native_pad_id': identifier, 'native_port_id': record.get('pcb_port_id'),
                'net': name, 'selector': planner.port_name(port) if port else None,
                'center_mm': [center.x, center.y], 'layers': layers,
                'polygon_mm': list(piece.exterior.coords)}
        # Via-only obstacles also apply to same-net pads. No via-in-pad is allowed.
        for layer in layers:
            # Via keepouts can be concave areas; only circular/capsule native
            # pads benefit from analytical pieces here.
            keepout_primitives = primitives if record.get('shape') in ('circle', 'pill', 'rotated_pill') else [{'contour': contour, 'circle_diameter_mm': None}]
            for index, primitive in enumerate(keepout_primitives):
                # The 0.70/0.30 mm via's outer radius already reserves the
                # required 0.20 mm ordinary-drill-to-pad gap. Adding another
                # generic clearance here would count that reserve twice.
                structure.append(f'(via_keepout PAD_VIA_{identifier}_{layer}_{index} {primitive_scope(primitive, layer)} (clearance_class padviareserve))')
        manifest['features'].append({'type': record['type'], 'id': identifier,
            'net': name, 'layers': layers, 'convex_piece_count': len(pieces),
            'convex_decomposition_error_mm2': unary_union(pieces).symmetric_difference(contour).area})
        if record['type'] == 'pcb_smtpad':
            # The public router models pin contacts at their centres, not
            # between touching pad outlines. Represent the same existing metal
            # as a fixed area so arbitrary native trace endpoints and convex
            # fragments remain electrically coupled. This adds no copper: every
            # area is covered by the authentic native pad.
            metal = primitives[-1] if record.get('shape') in ('pill', 'rotated_pill') else primitives[0] if record.get('shape') == 'circle' else {'contour': contour, 'circle_diameter_mm': None}
            if metal['contour'].difference(contour).area > 1e-10:
                raise ValueError('Transferred pad metal extends beyond authentic native copper')
            for layer in layers:
                # Specctra structure planes create plane-classified nets before
                # the network scope is read. The router then treats every pad
                # touching this metal as already routed to a plane and skips
                # genuine remaining connections. Fixed wiring areas preserve
                # exactly the same copper without changing signal-net semantics.
                wiring.append(f'(wire {primitive_scope(metal, layer)} (net "{name}") (type fix) (clearance_class smd))')
                manifest['pad_metal_regions'].append({'native_pad_id': identifier, 'net': name,
                    'layer': layer, 'classification': 'existing native pad metal, not added board copper'})

    standard_via = via_stack({'outer_mm': .7, 'hole_mm': .3}, export_context)
    structure.append(f'(via {standard_via})')
    for record in circuit:
        ty = record['type']
        if ty == 'pcb_trace':
            source = planner.source_traces[record['source_trace_id']]
            root = planner.root((source.get('connected_source_port_ids', []) + source.get('connected_source_net_ids', []))[0])
            name = net_name(root, names)
            count = 0
            for first, last in zip(record['route'], record['route'][1:]):
                if first['route_type'] == last['route_type'] == 'wire' and first['layer'] == last['layer']:
                    width = max(first['width'], last['width']) if record.get('route_thickness_mode') == 'interpolated' else first['width']
                    xy = ' '.join(f'{number(p["x"])} {number(p["y"])}' for p in (first, last))
                    if (first['x'], first['y']) != (last['x'], last['y']):
                        wiring.append(f'(wire (path {first["layer"]} {number(width)} {xy}) (net "{name}") (type fix))')
                        count += 1
                elif first['route_type'] not in ('wire', 'via') or last['route_type'] not in ('wire', 'via'):
                    raise ValueError('Unsupported native trace route point')
            manifest['features'].append({'type': ty, 'id': record['pcb_trace_id'], 'net': name, 'fixed_segments': count})
        elif ty == 'pcb_via':
            if set(record['layers']) != set(LAYERS):
                raise ValueError('Existing ordinary via does not span the full board')
            stack = via_stack({'outer_mm': record['outer_diameter'], 'hole_mm': record['hole_diameter']}, export_context)
            name = net_name(planner.via_root(record), names)
            wiring.append(f'(via {stack} {number(record["x"])} {number(record["y"])} (net "{name}") (type fix))')
            manifest['features'].append({'type': ty, 'id': record['pcb_via_id'], 'net': name,
                'padstack': stack, 'center_mm': [record['x'], record['y']]})
        elif ty == 'pcb_copper_pour':
            name = net_name(planner.root(record['source_net_id']), names)
            contour = native_pour(record)
            pieces = partition_pour(contour, args.pour_tile_mm)
            wiring.extend(f'(wire {area_scope(piece, record["layer"])} (net "{name}") (type fix))' for piece in pieces)
            manifest['features'].append({'type': ty, 'id': record['pcb_copper_pour_id'], 'net': name,
                'layer': record['layer'], 'area_mm2': contour.area, 'hole_count': len(contour.interiors),
                'dsn_region_count': len(pieces),
                'partition_error_mm2': unary_union(pieces).symmetric_difference(contour).area})
        elif ty == 'pcb_keepout':
            contour = AUDIT['pad_contour'](record)
            for layer in record['layers']:
                structure.append(f'(keepout KO_{record["pcb_keepout_id"]}_{layer} {polygon_scope(contour, layer)})')
            manifest['features'].append({'type': ty, 'id': record['pcb_keepout_id'], 'layers': record['layers']})
        elif ty in ('pcb_hole', 'pcb_plated_hole'):
            # Preserve actual drills as explicit obstacles, with an additional
            # 0.26 mm reserve. Existing plated-pad copper remains represented.
            drill = AUDIT['drill_contour'](record).buffer(.26, quad_segs=128)
            drill_width = record.get('hole_width', record.get('hole_diameter'))
            drill_height = record.get('hole_height', record.get('hole_diameter'))
            drill_record = {**record, 'shape': 'circle' if drill_width == drill_height else 'pill',
                'width': drill_width + .52, 'height': drill_height + .52,
                'ccw_rotation': record.get('hole_ccw_rotation', record.get('ccw_rotation', 0))}
            drill_record.pop('rect_ccw_rotation', None)
            drill_primitives = native_pad_primitives(drill_record, drill)
            for layer in LAYERS:
                for index, primitive in enumerate(drill_primitives):
                    # This obstacle already contains the full 0.26 mm hole
                    # reserve; do not add the generic wire gap a second time.
                    structure.append(f'(keepout DRILL_{record[ty + "_id"]}_{layer}_{index} {primitive_scope(primitive, layer)} (clearance_class drillreserve))')
            if ty == 'pcb_hole':
                manifest['features'].append({'type': ty, 'id': record['pcb_hole_id'], 'layers': list(LAYERS)})

    network = []
    for name in sorted(set(names.values())):
        network.append(f'(net "{name}" (pins {" ".join(nets[name])}))')
        root = next(root for root, named in names.items() if named == name)
        width = named_nets.get(root, {}).get('trace_width', .2)
        if width < .2:
            raise ValueError('Requested trace width below manufacturing minimum')
        class_name = 'ROUTE_' + name if name in args.nets else 'PRESERVE'
        if name in args.nets:
            network.append(f'(class "{class_name}" "{name}" (circuit (use_via {standard_via})) (rule (width {number(width)})))')
    ignored = sorted(set(names.values()).difference(args.nets))
    network.append(f'(class PRESERVE {" ".join(json.dumps(name) for name in ignored)} (circuit (use_via {standard_via})) (rule (width 200)))')
    design = '(pcb tscircuit_native_transfer\n (parser (string_quote ") (space_in_quoted_tokens on) (host_cad tscircuit) (host_version 0.0.2090))\n (resolution um 1000) (unit um)\n'
    for name, scopes in [('structure', structure), ('placement', placement), ('library', library), ('network', network), ('wiring', wiring)]:
        design += f' ({name}\n  ' + '\n  '.join(scopes) + '\n )\n'
    design += ')\n'
    target = Path(args.output_dsn)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(design)
    manifest['dsn_sha256'] = sha256(target)
    manifest['preserved_native_type_counts'] = dict(collections.Counter(f['type'] for f in manifest['features']))
    expected = collections.Counter(r['type'] for r in circuit if r['type'] in
        ('pcb_board', 'pcb_smtpad', 'pcb_plated_hole', 'pcb_trace', 'pcb_via', 'pcb_copper_pour', 'pcb_keepout', 'pcb_hole'))
    if dict(expected) != manifest['preserved_native_type_counts']:
        raise ValueError('Native copper/obstacle transfer omitted a feature')
    write_json(str(target) + '.manifest.json', manifest)
    print(json.dumps({'dsn': str(target), 'native_sha256': manifest['source_sha256'],
        'feature_counts': manifest['preserved_native_type_counts'], 'active_nets': args.nets}))


def parse_scopes(text):
    # Specctra's parser declaration contains a bare quote token. Other quoted
    # identifiers use the ordinary quoted-token form. No evaluation occurs.
    text = re.sub(r'\(string_quote\s+"\)', '(string_quote QUOTE)', text)
    # Freerouting writes component and pin as separately quoted identifiers.
    text = re.sub(r'("(?:[^"\\]|\\.)*")-("(?:[^"\\]|\\.)*")',
                  lambda match: json.dumps(json.loads(match[1]) + '-' + json.loads(match[2])), text)
    tokens = re.findall(r'"(?:[^"\\]|\\.)*"|[()]|[^\s()]+', text)
    stack, root = [], []
    current = root
    for token in tokens:
        if token == '(':
            nested = []
            current.append(nested)
            stack.append(current)
            current = nested
        elif token == ')':
            if not stack:
                raise ValueError('Unbalanced Specctra brackets')
            current = stack.pop()
        else:
            current.append(json.loads(token) if token.startswith('"') else token)
    if stack or len(root) != 1:
        raise ValueError('Expected one complete Specctra document')
    return root[0]


def scopes(node, name):
    return [child for child in node if isinstance(child, list) and child and child[0] == name]


def one_scope(node, name):
    matches = scopes(node, name)
    if len(matches) != 1:
        raise ValueError(f'Expected exactly one {name} scope, found {len(matches)}')
    return matches[0]


def dsn_shape(scope, scale_mm):
    kind, layer = scope[:2]
    coordinates = [float(coordinate) * scale_mm for coordinate in scope[2:]]
    if kind == 'polygon':
        shape = Polygon(list(zip(coordinates[1::2], coordinates[2::2])))
    elif kind == 'rect':
        shape = box(*coordinates)
    elif kind == 'circle':
        diameter, x, y = coordinates if len(coordinates) == 3 else [coordinates[0], 0, 0]
        shape = Point(x, y).buffer(diameter / 2, quad_segs=128)
    elif kind == 'path':
        width, xy = coordinates[0], list(zip(coordinates[1::2], coordinates[2::2]))
        shape = LineString(xy).buffer(width / 2, quad_segs=128) if width else Polygon(xy)
    elif kind == 'polyline_path':
        width = coordinates[0]
        lines = [coordinates[index:index + 4] for index in range(1, len(coordinates), 4)]
        xy = [line_intersection(first, last) for first, last in zip(lines, lines[1:])]
        shape = LineString(xy).buffer(width / 2, quad_segs=128)
    else:
        raise ValueError(f'Unsupported Specctra shape: {kind}')
    if shape.is_empty or not shape.is_valid:
        raise ValueError(f'Invalid Specctra {kind} shape')
    return layer, shape


def line_intersection(first, last):
    ax, ay, bx, by = first
    cx, cy, dx, dy = last
    determinant = (bx - ax) * (dy - cy) - (by - ay) * (dx - cx)
    if abs(determinant) < 1e-18:
        raise ValueError('Parallel or degenerate lines in Specctra polyline')
    distance = ((cx - ax) * (dy - cy) - (cy - ay) * (dx - cx)) / determinant
    return ax + distance * (bx - ax), ay + distance * (by - ay)


def dsn_area(scope, scale_mm):
    outlines = [child for child in scope if isinstance(child, list) and child[0] in ('polygon', 'rect', 'circle', 'path')]
    if len(outlines) != 1:
        raise ValueError('Expected one Specctra area outline')
    layer, shape = dsn_shape(outlines[0], scale_mm)
    for window in scopes(scope, 'window'):
        window_layer, hole = dsn_shape(window[1], scale_mm)
        if window_layer != layer:
            raise ValueError('Area window on a different layer')
        shape = shape.difference(hole)
    return layer, shape


def design_snapshot(path):
    document = parse_scopes(Path(path).read_text())
    if document[0] != 'pcb':
        raise ValueError('Expected a complete PCB design, not a session')
    unit = one_scope(document, 'unit')[1]
    scale_mm = {'um': .001, 'mm': 1}.get(unit)
    if scale_mm is None:
        raise ValueError(f'Unsupported design unit {unit}')
    library = one_scope(document, 'library')
    stacks = {stack[1]: stack for stack in scopes(library, 'padstack')}
    images = {image[1]: image for image in scopes(library, 'image')}
    network = one_scope(document, 'network')
    pin_nets = {}
    for net in scopes(network, 'net'):
        for pin in one_scope(net, 'pins')[1:]:
            if pin in pin_nets:
                raise ValueError('Pin assigned to more than one net')
            pin_nets[pin] = net[1]
    pads, pours, keepouts, wires = {}, collections.defaultdict(list), collections.defaultdict(list), collections.defaultdict(list)
    vias = []
    for component in scopes(one_scope(document, 'placement'), 'component'):
        for place in scopes(component, 'place'):
            if place[4] != 'front':
                raise ValueError('Transferred pad unexpectedly moved to back side')
            x_mm, y_mm, angle = float(place[2]) * scale_mm, float(place[3]) * scale_mm, float(place[5])
            for pin in scopes(images[component[1]], 'pin'):
                identifier = place[1] + '-' + pin[2]
                if float(pin[3]) or float(pin[4]):
                    raise ValueError('Unexpected local pin offset in transferred pad')
                for shape_scope in scopes(stacks[pin[1]], 'shape'):
                    layer, contour = dsn_shape(shape_scope[1], scale_mm)
                    contour = translate(rotate(contour, angle, origin=(0, 0)), xoff=x_mm, yoff=y_mm)
                    pads[identifier, layer] = (pin_nets[identifier], contour)
    structure = one_scope(document, 'structure')
    plane_count = len(scopes(structure, 'plane'))
    for plane in scopes(structure, 'plane'):
        layer, contour = dsn_area(plane, scale_mm)
        pours[plane[1], layer].append(contour)
    for kind in ('keepout', 'via_keepout'):
        for keepout in scopes(structure, kind):
            layer, contour = dsn_area(keepout, scale_mm)
            keepouts[kind, layer].append(contour)
    for wire in scopes(one_scope(document, 'wiring'), 'wire'):
        paths = scopes(wire, 'path') + scopes(wire, 'polyline_path')
        if scopes(wire, 'polygon') or scopes(wire, 'rect') or scopes(wire, 'circle'):
            # Freerouting writes signal-layer conduction areas as polygon
            # wires. They are still copper regions, not routed centerlines.
            layer, contour = dsn_area(wire, scale_mm)
            pours[one_scope(wire, 'net')[1], layer].append(contour)
            plane_count += 1
            continue
        if len(paths) != 1:
            raise ValueError('Expected one wire centerline')
        layer, contour = dsn_shape(paths[0], scale_mm)
        net = one_scope(wire, 'net')[1]
        if one_scope(wire, 'type')[1] != 'fix':
            raise ValueError('Original trace lost its SYSTEM_FIXED protection')
        wires[net, layer].append(contour)
    for via in scopes(one_scope(document, 'wiring'), 'via'):
        if one_scope(via, 'type')[1] != 'fix':
            raise ValueError('Original via lost its SYSTEM_FIXED protection')
        layers = tuple(dsn_shape(shape[1], scale_mm)[0] for shape in scopes(stacks[via[1]], 'shape'))
        # The stack's identity, all layer shapes and native drill metadata are
        # verified independently below, rather than inferred from a name.
        vias.append((one_scope(via, 'net')[1], via[1], float(via[2]) * scale_mm, float(via[3]) * scale_mm, layers))
    return {'pads': pads, 'pours': {key: unary_union(shapes) for key, shapes in pours.items()},
        'keepouts': {key: unary_union(shapes) for key, shapes in keepouts.items()},
        'keepout_counts': {key: len(shapes) for key, shapes in keepouts.items()},
        'wires': {key: unary_union(shapes) for key, shapes in wires.items()},
        'vias': sorted(vias), 'stacks': stacks, 'scale_mm': scale_mm,
        'outline': dsn_area(next(boundary for boundary in scopes(structure, 'boundary')
            if any(isinstance(shape, list) and shape[0] == 'polygon' for shape in boundary))
            if len(scopes(structure, 'boundary')) > 1 else one_scope(structure, 'boundary'), scale_mm)[1],
        'layers': [layer[1] for layer in scopes(structure, 'layer')],
        'plane_count': plane_count, 'structure': structure, 'network': network}


def compare_geometry(shapes, label):
    original, roundtrip = shapes
    # The engine uses nanometres; its DSN writer rounds micrometres to two
    # decimals. Twenty nanometres bound local+placement serialization; no omission
    # or convex hull substitution fits within this tolerance.
    if not original.buffer(.00002).covers(roundtrip) or not roundtrip.buffer(.00002).covers(original):
        raise ValueError(f'{label} changed during transfer: {original.symmetric_difference(roundtrip).area} mm²')
    return original.symmetric_difference(roundtrip).area


def verify_active_net_semantics(manifest, engine_rules):
    net_modes = {net['name']: net for net in engine_rules['nets']}
    for name in manifest['active_nets']:
        if name not in net_modes or net_modes[name]['contains_plane']:
            raise ValueError(f'Active signal net was omitted or classified as a plane: {name}')
        if net_modes[name]['net_class'] != 'ROUTE_' + name:
            raise ValueError(f'Active signal net lost its routing class: {name}')


def verify_native_pad_topology(topology_pads):
    native_pad_shapes = collections.defaultdict(list)
    for (pin, layer), contour in topology_pads.items():
        native_pad_id = pin.removesuffix('-1').rsplit('_', 1)[0]
        native_pad_shapes[native_pad_id, layer].append(contour)
    for identifier, pieces in native_pad_shapes.items():
        # Use the same 1 nm contact threshold as the native copper auditor.
        # Per-piece geometry tolerance alone must not conceal split pads.
        if unary_union(pieces).buffer(.0000005).geom_type != 'Polygon':
            raise ValueError(f'Native pad split into disconnected pieces in the engine: {identifier}')
    return len(native_pad_shapes)


def verify_transfer(args):
    original, roundtrip = design_snapshot(args.original_dsn), design_snapshot(args.roundtrip_dsn)
    engine_rules_path = getattr(args, 'engine_rules', None)
    engine_rules = json.loads(Path(engine_rules_path).read_text()) if engine_rules_path else None
    if engine_rules and engine_rules['source_sha256'] != sha256(args.original_dsn):
        raise ValueError('Engine rule receipt belongs to another input')
    manifest_path = Path(str(args.original_dsn) + '.manifest.json')
    if engine_rules and manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        verify_active_net_semantics(manifest, engine_rules)
    if original['layers'] != roundtrip['layers'] or original['plane_count'] != roundtrip['plane_count']:
        raise ValueError('Board layers or copper region count changed')
    if original['keepout_counts'] != roundtrip['keepout_counts']:
        raise ValueError('Keepout count changed')
    engine_pads = {}
    if engine_rules:
        for pin in engine_rules['pin_shapes']:
            contour = Polygon(pin['polygon_mm']) if 'polygon_mm' in pin else Point(pin['center_mm']).buffer(pin['radius_mm'], quad_segs=128)
            engine_pads[pin['pin'], pin['layer']] = contour
        if engine_pads.keys() != original['pads'].keys():
            raise ValueError('Actual engine omitted an original pad')
        engine_tolerance_mm = engine_rules['engine_grid_mm'] * 2
        for identifier, contour in engine_pads.items():
            before = original['pads'][identifier][1]
            if not before.buffer(engine_tolerance_mm).covers(contour) or not contour.buffer(engine_tolerance_mm).covers(before):
                raise ValueError(f'Actual engine changed pad geometry beyond rounding precision: {identifier}')
    topology_pads = engine_pads or {identifier: net_shape[1] for identifier, net_shape in roundtrip['pads'].items()}
    native_pad_count = verify_native_pad_topology(topology_pads)
    differences = {}
    for category in ('pads', 'pours', 'keepouts', 'wires'):
        if original[category].keys() != roundtrip[category].keys():
            raise ValueError(f'Transfer omitted or added {category}: {len(original[category])} -> {len(roundtrip[category])}')
        errors = []
        for identifier in original[category]:
            before, after = original[category][identifier], roundtrip[category][identifier]
            if category == 'pads':
                if before[0] != after[0]:
                    raise ValueError('Native pad changed net identity')
                before, after = before[1], after[1]
            errors.append(compare_geometry((before, after), f'{category} {identifier}'))
        differences[category] = {'checked': len(errors), 'maximum_area_difference_mm2': max(errors, default=0)}
    if len(original['vias']) != len(roundtrip['vias']):
        raise ValueError('Existing via count changed')
    for before, after in zip(original['vias'], roundtrip['vias']):
        if before[:2] != after[:2] or before[4] != after[4] or math.dist(before[2:4], after[2:4]) > .00002:
            raise ValueError('Existing via net, position or layer span changed')
    for stack in {via[1] for via in original['vias']}:
        for before, after in zip(scopes(original['stacks'][stack], 'shape'), scopes(roundtrip['stacks'][stack], 'shape'), strict=True):
            before_layer, before_shape = dsn_shape(before[1], original['scale_mm'])
            after_layer, after_shape = dsn_shape(after[1], roundtrip['scale_mm'])
            if before_layer != after_layer:
                raise ValueError('Via layer shape changed')
            compare_geometry((before_shape, after_shape), f'via stack {stack} {before_layer}')
    compare_geometry((original['outline'], roundtrip['outline']), 'board outline')
    # Rule semantics must remain exact. Normalized output can add defaults,
    # but it may not omit or reduce an explicitly requested manufacturing rule.
    before_rules = one_scope(original['structure'], 'rule')
    after_rules = one_scope(roundtrip['structure'], 'rule')
    if engine_rules and engine_rules['system_fixed_copper_regions'] != original['plane_count']:
        raise ValueError('Original copper region protection was not retained in the engine')
    for rule in before_rules[1:]:
        if engine_rules and rule[0] == 'clearance':
            pair = one_scope(rule, 'type')[1].split('_') if scopes(rule, 'type') else ['wire', 'wire']
            pair = ['default' if name == 'wire' else name for name in pair]
            constraints = [constraint for constraint in engine_rules['clearances']
                           if sorted([constraint['first'], constraint['second']]) == sorted(pair)]
            if len(constraints) != len(LAYERS) or any(constraint['clearance_mm'] + 1e-9 < float(rule[1]) * original['scale_mm'] for constraint in constraints):
                raise ValueError(f'Engine did not retain original clearance: {rule}')
            continue
        matches = [candidate for candidate in after_rules[1:] if candidate[0] == rule[0] and candidate[2:] == rule[2:]]
        if len(matches) != 1 or float(matches[0][1]) * roundtrip['scale_mm'] + 1e-9 < float(rule[1]) * original['scale_mm']:
            raise ValueError(f'Manufacturing rule was omitted or weakened: {rule}')
    after_classes = {net_class[1]: net_class for net_class in scopes(roundtrip['network'], 'class')}
    for net_class in scopes(original['network'], 'class'):
        transferred = after_classes.get(net_class[1])
        if transferred is None:
            raise ValueError(f'Net class was omitted: {net_class[1]}')
        before_nets = {net for net in net_class[2:] if isinstance(net, str)}
        after_nets = {net for net in transferred[2:] if isinstance(net, str)}
        if before_nets != after_nets:
            raise ValueError('Routable/preserved net class membership changed')
        before_width = float(one_scope(one_scope(net_class, 'rule'), 'width')[1]) * original['scale_mm']
        after_width = float(one_scope(one_scope(transferred, 'rule'), 'width')[1]) * roundtrip['scale_mm']
        if after_width + 1e-9 < before_width:
            raise ValueError(f'Net trace width was reduced: {net_class[1]}')
    receipt = {'classification': 'Geometry transfer qualification only; not routed-board DRC',
        'original_sha256': sha256(args.original_dsn), 'roundtrip_sha256': sha256(args.roundtrip_dsn),
        'geometry': differences, 'existing_vias_checked': len(original['vias']),
        'copper_regions_checked': original['plane_count'], 'coordinate_tolerance_mm': .00002,
        'engine_rules_sha256': sha256(engine_rules_path) if engine_rules_path else None,
        'actual_engine_pad_topology_checked': bool(engine_pads),
        'active_net_semantics_checked': bool(engine_rules and manifest_path.exists()),
        'actual_engine_grid_mm': engine_rules['engine_grid_mm'] if engine_rules else None,
        'native_pad_layer_unions_checked': native_pad_count,
        'roundtrip_is_routing_input': False,
        'qualified': True}
    write_json(args.output_json, receipt)
    print(json.dumps(receipt))


def session_proposals(args):
    manifest = json.loads(Path(args.manifest).read_text())
    qualification = json.loads(Path(args.qualification).read_text())
    if not qualification['qualified'] or not qualification.get('actual_engine_pad_topology_checked') or not qualification.get('active_net_semantics_checked') or qualification['original_sha256'] != manifest['dsn_sha256']:
        raise ValueError('Session input has no matching qualified geometry transfer')
    if qualification['actual_engine_grid_mm'] != manifest['expected_engine_grid_mm']:
        raise ValueError('Actual routing grid differs from the exported pad placement grid')
    source = Path(manifest['source_circuit_json'])
    if sha256(source) != manifest['source_sha256']:
        raise ValueError('The native board changed since export')
    circuit = json.loads(source.read_text())
    widths = {net['name']: net.get('trace_width', .2) for net in circuit if net['type'] == 'source_net'}
    document = parse_scopes(Path(args.session).read_text())
    if document[0] != 'session':
        raise ValueError('Expected a Specctra session')
    expected_base = Path(args.manifest).name.removesuffix('.manifest.json')
    # The official CLI writes its extensionless design name; the public writer
    # also accepts the full DSN filename. Both must identify this exact input.
    if one_scope(document, 'base_design')[1] not in (expected_base, Path(expected_base).stem, 'tscircuit_native_transfer'):
        raise ValueError('Session refers to a different base design')
    routes = one_scope(document, 'routes')
    resolution = one_scope(routes, 'resolution')
    if resolution[1:] != ['um', '1000']:
        raise ValueError('Session coordinate unit/resolution differs from qualified export')
    scale_mm = .001 / int(resolution[2])
    library = {stack[1]: stack for stack in scopes(one_scope(routes, 'library_out'), 'padstack')}
    placement = one_scope(document, 'placement')
    if one_scope(placement, 'resolution')[1:] != resolution[1:]:
        raise ValueError('Placement and route resolution differ')
    seen_pins = set()
    for component in scopes(placement, 'component'):
        for place in scopes(component, 'place'):
            identifier = place[1] + '-1'
            original = manifest['pins'].get(identifier)
            if original is None or identifier in seen_pins:
                raise ValueError('Session changed component identity')
            if place[4:6] != ['front', '0'] or math.dist(original['center_mm'], [float(place[2]) * scale_mm, float(place[3]) * scale_mm]) > qualification['actual_engine_grid_mm'] / 2:
                raise ValueError('Session moved or rotated an original pad')
            seen_pins.add(identifier)
    if seen_pins != manifest['pins'].keys():
        raise ValueError('Session omitted an original pad placement')
    was_is = scopes(document, 'was_is')
    if any(scope[1:] for scope in was_is):
        raise ValueError('Session changed original pin mappings')
    proposals = {'classification': 'Unaccepted Freerouting session proposals; native regeneration and full audits required',
        'native_source_sha256': manifest['source_sha256'], 'dsn_sha256': manifest['dsn_sha256'],
        'session_sha256': sha256(args.session), 'session_scale_mm_per_integer': scale_mm,
        'paths': [], 'vias': []}
    for net in scopes(one_scope(routes, 'network_out'), 'net'):
        name = net[1]
        if name not in manifest['active_nets']:
            raise ValueError(f'Session added routes to preserved net {name}')
        for item in net[2:]:
            if not isinstance(item, list):
                raise ValueError('Unexpected session route token')
            if item[0] == 'wire':
                path = one_scope(item, 'path')
                if path[1] not in ('top', 'inner2', 'bottom'):
                    raise ValueError('Session routed on the reserved GND layer')
                width = float(path[2]) * scale_mm
                if width + 1e-9 < widths[name]:
                    raise ValueError(f'Session reduced required width of {name}')
                coordinates = [float(coordinate) * scale_mm for coordinate in path[3:]]
                if len(coordinates) < 4 or len(coordinates) % 2:
                    raise ValueError('Invalid session wire centerline')
                proposals['paths'].append({'net': name, 'layer': path[1], 'width_mm': width,
                                          'path_mm': list(zip(coordinates[::2], coordinates[1::2]))})
            elif item[0] == 'via':
                specification = manifest['via_padstacks'].get(item[1])
                stack = library.get(item[1])
                if specification is None or stack is None or specification['hole_mm'] < .3 or specification['outer_mm'] < .7:
                    raise ValueError('Unknown or undersized session via stack')
                shapes = [dsn_shape(shape[1], scale_mm) for shape in scopes(stack, 'shape')]
                if [layer for layer, shape in shapes] != list(LAYERS):
                    raise ValueError('Session created a partial-span via')
                for layer, shape in shapes:
                    expected = Point(0, 0).buffer(specification['outer_mm'] / 2, quad_segs=128)
                    if shape.symmetric_difference(expected).area > 1e-10:
                        raise ValueError('Session changed via pad geometry')
                proposals['vias'].append({'net': name, 'x': float(item[2]) * scale_mm,
                    'y': float(item[3]) * scale_mm, 'hole_mm': specification['hole_mm'],
                    'outer_mm': specification['outer_mm'], 'layers': specification['layers']})
            else:
                raise ValueError(f'Unsupported session routing item: {item[0]}')
    write_json(args.output_json, proposals)
    print(json.dumps({'unaccepted_paths': len(proposals['paths']), 'unaccepted_vias': len(proposals['vias'])}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    export = commands.add_parser('export')
    export.add_argument('circuit_json'); export.add_argument('output_dsn')
    export.add_argument('--nets', nargs='+', required=True)
    export.add_argument('--pour-tile-mm', type=float, choices=[5], default=None)
    export.add_argument('--engine-grid-mm', type=float, choices=[.00001], default=.00001,
                        help='Measured internal grid of Freerouting 2.5.0 on this 50 x 65 mm board')
    verify = commands.add_parser('verify')
    verify.add_argument('original_dsn'); verify.add_argument('roundtrip_dsn'); verify.add_argument('output_json')
    verify.add_argument('--engine-rules')
    session = commands.add_parser('session')
    session.add_argument('session'); session.add_argument('manifest')
    session.add_argument('qualification'); session.add_argument('output_json')
    args = parser.parse_args()
    {'export': export_design, 'verify': verify_transfer, 'session': session_proposals}[args.command](args)


if __name__ == '__main__':
    main()
