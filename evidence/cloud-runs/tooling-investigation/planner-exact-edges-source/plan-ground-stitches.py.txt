"""Join isolated ground pours to the actual inner ground plane with native vias.

Plans are proposals until native generation and the independent copper audit
confirm every annulus contact. No connector contacts or replay caches are added.
"""
import argparse
import json
import runpy
from pathlib import Path

import numpy as np
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

helpers = runpy.run_path(str(Path(__file__).with_name('plan-power-copper.py')))
Planner = helpers['Planner']


def pour_shape(record):
    brep = record['brep_shape']
    return Polygon([(p['x'], p['y']) for p in brep['outer_ring']['vertices']],
                   [[(p['x'], p['y']) for p in ring['vertices']] for ring in brep['inner_rings']])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit_json')
    parser.add_argument('copper_audit')
    parser.add_argument('output_json')
    parser.add_argument('--reserve-proposals', action='append', default=[])
    args = parser.parse_args()
    circuit = json.loads(Path(args.circuit_json).read_text())
    physical = json.loads(Path(args.copper_audit).read_text())
    planner = Planner(circuit)
    for filename in args.reserve_proposals:
        planner.reserve_proposals(json.loads(Path(filename).read_text()))
    root = planner.root(next(r['source_net_id'] for r in circuit if r['type'] == 'source_net' and r['name'] == 'GND'))
    groups = physical['physical_feature_groups']
    ground = [r for r in circuit if r['type'] == 'pcb_copper_pour' and planner.root(r['source_net_id']) == root]
    plane = unary_union([pour_shape(r) for r in ground if r['layer'] == 'inner1'])
    main_groups = {groups[r['pcb_copper_pour_id']] for r in ground if r['layer'] == 'inner1'}
    islands = {}
    for record in ground:
        group = groups[record['pcb_copper_pour_id']]
        if record['layer'] == 'top' and group not in main_groups:
            islands.setdefault(group, []).append(pour_shape(record))
    vias, unresolved = [], []
    for group, shapes in islands.items():
        island = unary_union(shapes)
        obstacles = helpers['via_obstacles'](planner, root)
        min_x, min_y, max_x, max_y = island.bounds
        candidates = [(float(x), float(y)) for x in np.arange(min_x, max_x, .1) for y in np.arange(min_y, max_y, .1)]
        candidates.sort(key=lambda p: Point(p).distance(island.representative_point()))
        for position in candidates:
            point = Point(position)
            annulus = point.buffer(.35).difference(point.buffer(.15))
            if point.intersects(obstacles) or annulus.intersection(island).area < .01 or annulus.intersection(plane).area < .01:
                continue
            vias.append({'net': 'GND', 'x': position[0], 'y': position[1], 'hole_mm': .3, 'outer_mm': .7,
                         'classification': 'manual native ground-plane stitching via', 'isolated_native_group': group})
            planner.holes.append(point.buffer(.15))
            for layer in ('top', 'inner1', 'inner2', 'bottom'):
                planner.copper.append((root, layer, point.buffer(.35)))
            break
        else:
            unresolved.append({'isolated_native_group': group, 'reason': 'No ordinary via with annulus contact to both the island and inner1 GND plane'})
    Path(args.output_json).write_text(json.dumps({'classification': 'native via proposals, not solver caches',
        'source_circuit_json': args.circuit_json, 'vias': vias, 'unresolved': unresolved}, indent=2) + '\n')
    print(json.dumps({'ground_stitches': len(vias), 'unresolved': unresolved}))


if __name__ == '__main__':
    main()
