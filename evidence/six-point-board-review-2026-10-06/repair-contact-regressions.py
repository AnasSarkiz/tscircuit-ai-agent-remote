"""Restore measured lost contacts with ordinary vias and a native test-pad move."""
import json
import math
import runpy
from pathlib import Path
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

directory = Path('evidence/six-point-board-review-2026-10-06')
helpers = runpy.run_path('scripts/routing/plan-power-copper.py')
circuit = json.loads((directory/'own-pad-native/circuit.json').read_text())
physical = json.loads((directory/'own-pad-copper-audit.json').read_text())
planner = helpers['Planner'](circuit)
planner.via_copper_clearance = .27
nets = {r['name']: r for r in circuit if r['type'] == 'source_net'}
result = {'classification': 'authored contact repairs; native replay required', 'vias': [], 'pours': [], 'unresolved': []}

def reserve_via(net, xy):
    root = planner.root(nets[net]['source_net_id'])
    if Point(xy).intersects(helpers['via_obstacles'](planner, {'root': root, 'via_outer_mm': .45, 'via_hole_mm': .3})):
        result['unresolved'].append({'net': net, 'point': xy, 'reason': 'Full-span via does not clear all copper/drills/pads'})
        return False
    result['vias'].append({'net': net, 'x': xy[0], 'y': xy[1], 'outer_mm': .45, 'hole_mm': .3,
                           'classification': 'manual native full-span contact repair'})
    hole = Point(xy).buffer(.15)
    planner.holes.append(hole); planner.plated_hole_roots[hole.wkb] = root
    for layer in ('top', 'inner1', 'inner2', 'bottom'):
        planner.copper.append((root, layer, Point(xy).buffer(.225)))
    return True

def main_group(net):
    groups = {}
    root = planner.root(nets[net]['source_net_id'])
    for port in planner.ports.values():
        if planner.root(port['source_port_id']) != root:
            continue
        if planner.source_ports[port['source_port_id']].get('source_component_id') not in planner.source_components:
            continue
        group = physical['physical_port_groups'][port['pcb_port_id']]
        if len(group) == 1:
            groups[group[0]] = groups.get(group[0], 0)+1
    return max(groups, key=groups.get)

# The old branch ended on another bottom route that has also moved to inner2.
# Join its actual new main-island vias on inner2 without an unnecessary drill.
root = planner.root(nets['MIC_WS']['source_net_id'])
group = main_group('MIC_WS')
targets = [(r['x'], r['y']) for r in circuit if r['type'] == 'pcb_via' and
           planner.via_root(r) == root and physical['physical_feature_groups'][r['pcb_via_id']] == group]
obstacles = helpers['inner_obstacles'](planner, {'root': root, 'width': .202,
             'new_vias': targets, 'layer': 'inner2', 'copper_clearance_mm': .27})
for target in sorted(targets, key=lambda xy: math.dist(xy, (14.3,-27.5))):
    route = planner.grid_route(((14.3,-27.5), target, obstacles))
    if not route:
        continue
    contour = LineString(route).buffer(.101, cap_style=2, join_style=1)
    result['pours'].append({'net': 'MIC_WS', 'layer': 'inner2', 'path_mm': route,
        'nominal_width_mm': .2, 'drawn_width_mm': .202,
        'outline': [{'x': round(x,6), 'y': round(y,6)} for x,y in list(contour.exterior.coords)[:-1]],
        'classification': 'manual native restored low-current terminal contact'})
    planner.copper.append((root, 'inner2', contour))
    break
else:
    result['unresolved'].append({'net': 'MIC_WS', 'reason': 'No inner2 contact to actual new main island'})

# C73's old top route ended at an authored via retired by tree replacement.
start = (16.5, -13.7)
if reserve_via('MIC_INPUT', start):
    root = planner.root(nets['MIC_INPUT']['source_net_id'])
    group = main_group('MIC_INPUT')
    targets = [(r['x'], r['y']) for r in circuit if r['type'] == 'pcb_via' and
               planner.via_root(r) == root and physical['physical_feature_groups'][r['pcb_via_id']] == group]
    for target in sorted(targets, key=lambda p: math.dist(p, start)):
        route = helpers['wide_multilayer_route'](planner, {'first': start, 'last': target,
            'root': root, 'width': .302, 'new_vias': targets+[start], 'layers': ('inner2', 'inner1'),
            'via_outer_mm': .45, 'via_hole_mm': .3, 'copper_clearance_mm': .27})
        if not route:
            continue
        parts, vias = route
        for layer, points in parts:
            if len(points) < 2 or LineString(points).length < 1e-6:
                continue
            contour = LineString(points).buffer(.151, cap_style=2, join_style=1)
            result['pours'].append({'net': 'MIC_INPUT', 'layer': layer, 'path_mm': points,
                'nominal_width_mm': .3, 'drawn_width_mm': .302,
                'outline': [{'x': round(x, 6), 'y': round(y, 6)} for x,y in list(contour.exterior.coords)[:-1]],
                'classification': 'manual native restored low-current terminal contact'})
        for via in vias:
            if not reserve_via('MIC_INPUT', via):
                break
        break
    else:
        result['unresolved'].append({'net': 'MIC_INPUT', 'reason': 'No inner connection to main island'})

root = planner.root(nets['GND']['source_net_id'])
group = main_group('GND')
ground = []
for r in circuit:
    if r['type'] == 'pcb_copper_pour' and r['layer'] == 'top' and planner.root(r['source_net_id']) == root and physical['physical_feature_groups'][r['pcb_copper_pour_id']] == group:
        b = r['brep_shape']
        ground.append(Polygon([(p['x'],p['y']) for p in b['outer_ring']['vertices']],
                      [[(p['x'],p['y']) for p in ring['vertices']] for ring in b['inner_rings']]))
ground = unary_union(ground)
tp = next(p for p in planner.ports.values() if planner.source_ports[p['source_port_id']].get('source_component_id') in planner.source_components and planner.port_name(p) == '.TP1 > .pin1')
candidates = sorted(((round(tp['x']+dx/10, 6), round(tp['y']+dy/10, 6)) for dx in range(-80,81) for dy in range(-80,81)),
                    key=lambda p: math.dist(p, (tp['x'],tp['y'])))
for xy in candidates:
    pad = Point(xy).buffer(.5)
    contact = LineString([xy, (xy[0],xy[1]+.6)]).buffer(.15)
    if not ground.covers(pad.buffer(.1)) or not ground.covers(contact):
        continue
    if any(pad.distance(shape) < .25 for r,shape in planner.pads if r.get('pcb_port_id') != tp['pcb_port_id'] and 'top' in r.get('layers',[r.get('layer')])):
        continue
    if any(pad.distance(shape) < .25 for shape in planner.holes):
        continue
    if any(pad.distance(Polygon([(component['center']['x']-component['width']/2,component['center']['y']-component['height']/2),
        (component['center']['x']+component['width']/2,component['center']['y']-component['height']/2),
        (component['center']['x']+component['width']/2,component['center']['y']+component['height']/2),
        (component['center']['x']-component['width']/2,component['center']['y']+component['height']/2)])) < .25
        for component in planner.components.values() if component['pcb_component_id'] != tp['pcb_component_id']
        and component.get('source_component_id') in planner.source_components and not component.get('do_not_place')):
        continue
    result['TP1_move'] = {'from': [tp['x'],tp['y']], 'to': xy, 'pad_diameter_mm': 1,
        'scope': 'Native test pad only, wholly in measured main top GND island with a nonzero contact and clearance to pads/drills'}
    break
else:
    result['unresolved'].append({'net': 'GND', 'reason': 'No accessible main-island test-pad location within 8 mm'})
(directory/'contact-repairs-proposal.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result))
raise SystemExit(1 if result['unresolved'] else 0)
