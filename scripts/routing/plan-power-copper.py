"""Plan native power pours and ordinary pad escapes, never solver replay caches.

Top escapes end at native trace vias. Inner2 pours provide wide distribution;
all footprints remain genuine imports. Plans require native replay, physical
connectivity, clearance and current qualification before acceptance.
"""
import argparse
import json
import math
import heapq
import runpy
from pathlib import Path

import numpy as np
from shapely import contains_xy
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

Planner = runpy.run_path(str(Path(__file__).with_name('plan-manual-signals.py')))["ManualSignalPlanner"]


def via_obstacles(planner, specification):
    root = specification['root']
    radius = specification.get('via_outer_mm', .7) / 2
    drill_radius = specification.get('via_hole_mm', .3) / 2
    shapes = []
    for record, shape in planner.pads:
        port = planner.ports.get(record.get('pcb_port_id'))
        own = port and planner.root(port['source_port_id']) == root
        shapes.append(shape.buffer(planner.copper_clearance + (drill_radius if own else radius)))
    shapes.extend(shape.buffer(.26 + drill_radius) for shape in planner.holes)
    shapes.extend(shape.buffer(.21 + radius) for _, shape in planner.keepouts)
    shapes.extend(shape.buffer(radius + max(planner.copper_clearance, planner.via_copper_clearance)) for other_root, _, shape in planner.copper if other_root != root)
    shapes.append(box(-26, -34, 26, 34).difference(planner.board.buffer(-.26-radius)))
    return unary_union(shapes)


def pad_escape(planner, specification):
    root, width, origin = specification['root'], specification['width'], specification['origin']
    top_obstacles = planner.obstacles(root, 'top', width)
    exits = via_obstacles(planner, specification)
    if specification.get('distribution_layers'):
        wide_obstacles = [inner_obstacles(planner, {**specification, 'layer': layer,
            'width': specification['distribution_width_mm']}) for layer in specification['distribution_layers']]
        # A through-via exit must admit the required distribution width on
        # at least one selected routing layer, as well as a legal top escape.
        exits = unary_union([exits, wide_obstacles[0].intersection(wide_obstacles[1])])
    elif specification['net']['name'] != 'GND':
        exits = unary_union([exits, inner_obstacles(planner, {'root': root,
            'width': specification['net'].get('trace_width', .3), 'new_vias': specification['new_vias']})])
    reachable_context = None
    if specification.get('connected_targets'):
        grid_data = [planner.grid_data(obstacle) for obstacle in wide_obstacles]
        targets = []
        for index, obstacle in enumerate(wide_obstacles):
            for terminal in specification['connected_targets']:
                options=planner.grid_anchor_options((terminal,), (grid_data[index][0], obstacle))[0]
                targets.extend((index,*anchor[0]) for anchor in options)
        reachable_context = {'grid_data':grid_data,'obstacles':wide_obstacles,'targets':targets,
            'via_blocked':planner.grid_data(via_obstacles(planner,specification))[0]}
        if not targets:
            return None
    for distance in np.arange(.6, 3.41, .2):
        for degrees in range(0, 360, 30):
            radians = math.radians(degrees)
            target = (round(origin[0] + float(distance)*math.cos(radians), 6),
                      round(origin[1] + float(distance)*math.sin(radians), 6))
            if (not Point(target).intersects(exits) and not LineString([origin, target]).intersects(top_obstacles)
                and (reachable_context is None or via_exit_reachable(planner, {**reachable_context,'target':target}))):
                return target, [origin, target]
    grid_obstacles = (top_obstacles, exits)
    if reachable_context:
        labels = [record[1] for record in reachable_context['grid_data']]
        allowed_exits = np.zeros(labels[0].shape,dtype=bool)
        for layer, layer_labels in enumerate(labels):
            for identifier in np.unique(layer_labels):
                if not identifier:
                    continue
                y,x = np.argwhere(layer_labels==identifier)[0]
                if multilayer_components_reachable(labels,reachable_context['via_blocked'],[(layer,int(y),int(x))],
                                                  reachable_context['targets'],planner.layer_component_cache):
                    allowed_exits |= layer_labels==identifier
        grid_obstacles = (top_obstacles, exits, allowed_exits)
    candidates = planner.grid_escape(origin, grid_obstacles)
    return candidates[0] if candidates else None


def via_exit_reachable(planner, specification):
    starts=[]
    for layer,obstacle in enumerate(specification['obstacles']):
        options=planner.grid_anchor_options((specification['target'],), (specification['grid_data'][layer][0],obstacle))[0]
        starts.extend((layer,*anchor[0]) for anchor in options)
    return multilayer_components_reachable([record[1] for record in specification['grid_data']],
        specification['via_blocked'],starts,specification['targets'],planner.layer_component_cache)


def escape_record(planner, specification):
    port, net, root = specification['port'], specification['net'], specification['root']
    positions, width = specification['positions'], specification['width']
    component = planner.components[port['pcb_component_id']]
    rotation = math.radians(-component['rotation'])
    local = []
    for x, y in positions[1:]:
        dx, dy = x-component['display_offset_x'], y-component['display_offset_y']
        local.append({'x': round(dx*math.cos(rotation)-dy*math.sin(rotation), 6),
                      'y': round(dx*math.sin(rotation)+dy*math.cos(rotation), 6)})
    local.append({**local[-1], 'via': True, 'fromLayer': 'top', 'toLayer': 'bottom'})
    for start, end in zip(positions, positions[1:]):
        planner.copper.append((root, 'top', LineString([start,end]).buffer(width/2)))
    target = positions[-1]
    via_hole_radius = specification.get('via_hole_mm', .3) / 2
    via_pad_radius = specification.get('via_outer_mm', .7) / 2
    hole = Point(target).buffer(via_hole_radius)
    planner.holes.append(hole)
    planner.plated_hole_roots[hole.wkb] = root
    for layer in ('top','inner1','inner2','bottom'):
        planner.copper.append((root, layer, Point(target).buffer(via_pad_radius)))
    return {'net': net['name'], 'from': planner.port_name(port), 'to': 'net.'+net['name'], 'width': width,
            'pcbPath': local, 'global_path_mm': positions, 'segment_layers': ['top']*len(positions),
            'classification': 'manual native ordinary via escape; power current qualification pending' if net['name'] != 'GND' else 'manual native GND via escape',
            'top_length_mm': sum(math.dist(a,b) for a,b in zip(positions,positions[1:])),
            'via_outer_mm': specification.get('via_outer_mm', .7),
            'via_hole_mm': specification.get('via_hole_mm', .3)}


def inner_obstacles(planner, specification):
    root, width, new_vias = specification['root'], specification['width'], specification['new_vias']
    layer = specification.get('layer', 'inner2')
    clearance = specification.get('copper_clearance_mm', .21)
    # Native rectangular-pad cutouts expand each bounding-box edge, including
    # square corners. Reserve that expansion before the round strip radius so
    # actual Euclidean clearance cannot mask a narrowed native region.
    shapes = [shape.envelope.buffer(clearance, join_style=2).buffer(width/2) for record,shape in planner.pads
              if layer in record.get('layers', [record.get('layer')]) and
              (not (port := planner.ports.get(record.get('pcb_port_id'))) or planner.root(port['source_port_id']) != root)]
    shapes.extend(shape.buffer(clearance+width/2) for other_root, copper_layer, shape in planner.copper if other_root != root and copper_layer == layer)
    own_via_holes = [Point(p).buffer(.15) for p in new_vias]
    # Only this net's intended plated terminals are exempt from ordinary hole
    # clearance. Other holes and all foreign copper remain obstacles.
    shapes.extend(shape.buffer(.26+width/2) for shape in planner.holes
                  if planner.plated_hole_roots.get(shape.wkb) != root
                  and not any(shape.equals(hole) for hole in own_via_holes))
    shapes.extend(shape.buffer(.21+width/2) for record,shape in planner.keepouts if layer in record['layers'])
    shapes.append(box(-26,-34,26,34).difference(planner.board.buffer(-.26-width/2)))
    return unary_union(shapes)


def multilayer_components_reachable(labels, via_blocked, starts, targets, cache=None):
    """Require a component chain through legal ordinary-via grid cells."""
    parents = {}

    def root(node):
        parents.setdefault(node, node)
        if parents[node] != node:
            parents[node] = root(parents[node])
        return parents[node]

    component_roots = None
    if cache is not None:
        for first_labels, last_labels, via_cells, roots in cache:
            if first_labels is labels[0] and last_labels is labels[1] and via_cells is via_blocked:
                component_roots = roots
                break
    if component_roots is None:
        transitions = (~via_blocked) & (labels[0] != 0) & (labels[1] != 0)
        pairs = np.unique(np.column_stack((labels[0][transitions], labels[1][transitions])), axis=0)
        for first, last in pairs:
            parents[root((0, int(first)))] = root((1, int(last)))
        component_roots = {node: root(node) for node in parents}
        if cache is not None:
            cache.append((labels[0], labels[1], via_blocked, component_roots))
            if len(cache) > 4:
                cache.pop(0)
    def component(node):
        layer, y, x = node
        identifier = (layer, int(labels[layer][y, x]))
        return component_roots.get(identifier, identifier)
    start_components = {component(node) for node in starts}
    return any(component(node) in start_components for node in targets)


def wide_multilayer_route(planner, specification):
    first, last = specification['first'], specification['last']
    layers = tuple(specification.get('layers', ('inner2', 'bottom')))
    if len(layers) != 2 or any(layer not in ('top', 'inner1', 'inner2', 'bottom') for layer in layers):
        raise ValueError('Wide distribution routing requires two supported layers')
    first_layer,last_layer=specification.get('first_layer'),specification.get('last_layer')
    if any(layer is not None and layer not in layers for layer in (first_layer,last_layer)):
        raise ValueError('Endpoint layers must be selected routing layers')
    obstacles = [inner_obstacles(planner, {**specification, 'layer': layer}) for layer in layers]
    preferred_width = specification.get('preferred_width_mm')
    if preferred_width is None:
        for layer, obstacle in zip(layers, obstacles):
            if (first_layer is not None and first_layer!=layer) or (last_layer is not None and last_layer!=layer):continue
            route = planner.grid_route((first, last, obstacle))
            if route:
                return [(layer, route)], []
    grid_data = [planner.grid_data(obstacle) for obstacle in obstacles]
    blocked = [data[0] for data in grid_data]
    preferred_blocked = [planner.grid_data(inner_obstacles(planner, {**specification, 'layer': layer,
        'width': preferred_width}))[0] for layer in layers] if preferred_width is not None else None
    via_blocked = planner.grid_data(via_obstacles(planner, specification))[0]
    starts, targets = {}, {}
    for index in range(2):
        if specification.get('multi_anchor'):
            start_options,target_options=planner.grid_anchor_options((first,last),(blocked[index],obstacles[index]))
            if first_layer is not None and layers[index]!=first_layer:start_options=[]
            if last_layer is not None and layers[index]!=last_layer:target_options=[]
            for options,destination in ((start_options,starts),(target_options,targets)):
                by_component={}
                for node,path in options:
                    identifier=int(grid_data[index][1][node])
                    if identifier not in by_component or LineString(path).length<LineString(by_component[identifier][1]).length:
                        by_component[identifier]=(node,path)
                for node,path in by_component.values():destination[(index,*node)]=path
        else:
            start, target = planner.grid_anchor((first, last), (blocked[index], obstacles[index]))
            if first_layer is not None and layers[index]!=first_layer:start=None
            if last_layer is not None and layers[index]!=last_layer:target=None
            if start:
                starts[(index, *start[0])] = start[1]
            if target:
                targets[(index, *target[0])] = target[1]
    if not starts or not targets:
        return None
    if not multilayer_components_reachable([data[1] for data in grid_data], via_blocked, starts, targets,
                                          planner.layer_component_cache):
        return None

    def heuristic(node):
        return min(math.hypot(node[1]-target[1], node[2]-target[2]) for target in targets)

    heap = [(heuristic(node), 0, node) for node in starts]
    heapq.heapify(heap)
    costs = {node: 0 for node in starts}
    previous = {}
    while heap:
        _, cost, node = heapq.heappop(heap)
        if cost > costs[node]:
            continue
        if node in targets:
            nodes, current = [node], node
            while current in previous:
                current = previous[current]
                nodes.append(current)
            nodes.reverse()
            parts, vias = [], []
            layer_index, positions = nodes[0][0], list(starts[nodes[0]])
            for next_node in nodes[1:]:
                position = (float(planner.x_coordinates[next_node[2]]), float(planner.y_coordinates[next_node[1]]))
                if next_node[0] != layer_index:
                    parts.append((layers[layer_index], positions))
                    vias.append(position)
                    layer_index, positions = next_node[0], [position]
                else:
                    positions.append(position)
            positions.extend(reversed(targets[node]))
            parts.append((layers[layer_index], positions))
            # Keep the weighted path: straightening it against only minimum
            # width obstacles would reintroduce the long narrow shortcut.
            if preferred_blocked is not None:
                return parts, vias
            simplified_parts = []
            for layer, positions in parts:
                obstacle = obstacles[layers.index(layer)]
                simplified, index = [positions[0]], 0
                while index < len(positions)-1:
                    candidate = len(positions)-1
                    while candidate > index+1 and LineString([positions[index],positions[candidate]]).intersects(obstacle):
                        candidate -= 1
                    if LineString([positions[index],positions[candidate]]).intersects(obstacle):
                        return None
                    simplified.append(positions[candidate]);index=candidate
                simplified_parts.append((layer, simplified))
            return simplified_parts, vias
        layer, y, x = node
        neighbors = []
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)):
            ny,nx=y+dy,x+dx
            if not 0 <= ny < blocked[layer].shape[0] or not 0 <= nx < blocked[layer].shape[1] or blocked[layer][ny,nx]:
                continue
            if dy and dx and (blocked[layer][y+dy,x] or blocked[layer][y,x+dx]):
                continue
            if not planner.grid_edge_clear((y,x), (ny,nx), obstacles[layer], blocked[layer]):
                continue
            penalty = 25 if preferred_blocked is not None and (preferred_blocked[layer][y,x] or preferred_blocked[layer][ny,nx]) else 1
            neighbors.append(((layer,ny,nx), math.hypot(dy,dx)*penalty))
        if not via_blocked[y,x] and not blocked[1-layer][y,x]:
            neighbors.append(((1-layer,y,x), 10))
        for neighbor, edge_cost in neighbors:
            next_cost = cost + edge_cost
            if next_cost < costs.get(neighbor, math.inf):
                costs[neighbor] = next_cost
                previous[neighbor] = node
                heapq.heappush(heap,(next_cost+heuristic(neighbor),next_cost,neighbor))
    return None


def plan_net(planner, specification):
    net, ground_ports = specification['net'], specification['ground_ports']
    root = planner.root(net['source_net_id'])
    ports = [p for p in planner.ports.values() if planner.root(p['source_port_id']) == root
             and planner.source_ports[p['source_port_id']].get('source_component_id') in planner.source_components
             and not planner.port_name(p).startswith(('.J3 >', '.J7 >'))]
    if net['name'] == 'GND':
        ports = [p for p in ports if planner.port_name(p) in ground_ports]
    unique = {}
    for port in ports:
        unique.setdefault(planner.physical_root(port['pcb_port_id']), []).append(port)
    paths, vias, unresolved = [], [], []
    for alternatives in unique.values():
        width = min(.3, net.get('trace_width', .3))
        result = None
        for port in alternatives:
            result = pad_escape(planner, {'root': root, 'width': width, 'origin': (port['x'],port['y']),
                                          'net': net, 'new_vias': vias})
            if result is not None:
                break
        if result is None:
            unresolved.append({'net':net['name'], 'port':planner.port_name(port), 'reason':'No ordinary via escape meeting pad/drill/copper clearance'})
            continue
        target, positions = result
        paths.append(escape_record(planner, {'port':port,'net':net,'root':root,'positions':positions,'width':width}))
        vias.append(target)
    pours, interlayer_vias = [], []
    if net['name'] != 'GND' and len(vias) >= 2:
        width = net.get('trace_width', .3)
        connected, remaining = [vias[0]], list(vias[1:])
        while remaining:
            _, first, last = min(((math.dist(a,b), a, b) for a in connected for b in remaining), key=lambda edge:edge[0])
            remaining.remove(last)
            drawn_width = width + (0.002 if specification.get('preserve_region_width') else 0)
            result = wide_multilayer_route(planner, {'first':first,'last':last,'root':root,'width':drawn_width,'new_vias':vias,
                'copper_clearance_mm': .27 if specification.get('preserve_region_width') else .21})
            if result is None:
                unresolved.append({'net':net['name'],'via_xy':last,'reason':'No wide inner2 distribution path'})
                continue
            parts, new_vias = result
            for layer, route in parts:
                if len(route) < 2 or LineString(route).length < 1e-6:
                    continue
                contour = LineString(route).buffer(drawn_width/2, join_style=2, cap_style=2)
                if not isinstance(contour, Polygon) or contour.interiors:
                    raise ValueError('Distribution outline requires explicit region decomposition')
                outline = [{'x':round(x,6),'y':round(y,6)} for x,y in list(contour.exterior.coords)[:-1]]
                pours.append({'net':net['name'],'layer':layer,'outline':outline,'nominal_width_mm':width,
                              'drawn_width_mm': drawn_width, 'path_mm':route,
                              'classification':'manual native routing copper region; electrical qualification pending'})
                planner.copper.append((root,layer,contour))
            for position in new_vias:
                vias.append(position)
                planner.holes.append(Point(position).buffer(.15))
                for layer in ('top','inner1','inner2','bottom'):
                    planner.copper.append((root,layer,Point(position).buffer(.35)))
                interlayer_vias.append({'net':net['name'],'x':round(position[0],6),'y':round(position[1],6),
                                       'hole_mm':.3,'outer_mm':.7,'classification':'manual native through via between power regions'})
            connected.append(last)
    return paths, pours, interlayer_vias, unresolved


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit_json');parser.add_argument('output_json');parser.add_argument('nets',nargs='+')
    parser.add_argument('--ground-audit', required=True)
    parser.add_argument('--reserve-paths', help='Additional authored paths that the native build has not rendered yet')
    parser.add_argument('--preserve-region-width', action='store_true', help='Reserve beyond native 0.26 mm cutouts and draw above the required width')
    parser.add_argument('--grid-mm', type=float, choices=(0.05, 0.1), default=0.1)
    args = parser.parse_args()
    circuit=json.loads(Path(args.circuit_json).read_text());planner=Planner(circuit)
    planner.set_grid(args.grid_mm)
    if args.preserve_region_width:
        planner.via_copper_clearance = .27
    if args.reserve_paths:
        for path in json.loads(Path(args.reserve_paths).read_text())['paths']:
            net=next(r for r in circuit if r['type']=='source_net' and r['name']==path['net'])
            root=planner.root(net['source_net_id']);positions=path['global_path_mm'];layers=path['segment_layers']
            for index,(first,last) in enumerate(zip(positions,positions[1:])):
                planner.copper.append((root,layers[index+1],LineString([first,last]).buffer(path['width']/2)))
                if index and layers[index] != layers[index+1]:
                    planner.holes.append(Point(first).buffer(.15))
                    for layer in ('top','inner1','inner2','bottom'):
                        planner.copper.append((root,layer,Point(first).buffer(.35)))
    physical=json.loads(Path(args.ground_audit).read_text())
    ground_islands=next(record['islands'] for record in physical['physically_open_nets'] if record['net']=='GND')
    ground_ports={'.'+label.split('.pin')[0]+' > .pin'+label.split('.pin')[1] for island in ground_islands[1:] for label in island if '.pin' in label}
    paths,pours,vias,unresolved=[],[],[],[]
    for name in args.nets:
        net=next(r for r in circuit if r['type']=='source_net' and r['name']==name)
        proposed,regions,layer_vias,failures=plan_net(planner,{'net':net,'ground_ports':ground_ports,
            'preserve_region_width': args.preserve_region_width})
        paths.extend(proposed);pours.extend(regions);vias.extend(layer_vias);unresolved.extend(failures)
        print(json.dumps({'net':name,'ordinary_via_escapes':len(proposed),'power_regions':len(regions),'unresolved':failures}),flush=True)
        Path(args.output_json).write_text(json.dumps({'classification':'manual native copper proposals; not solver caches',
            'source_circuit_json':args.circuit_json,'paths':paths,'pours':pours,'vias':vias,'unresolved':unresolved},indent=2)+'\n')


if __name__=='__main__':main()
