"""Propose restoration of preserved native paths that clear new routing.

This only selects source paths. It never writes circuit JSON or a solver cache;
every selected path still requires native generation and independent audit.
"""
import argparse
import json
import runpy
from pathlib import Path

from shapely.geometry import LineString, Point

helpers = runpy.run_path(str(Path(__file__).with_name('plan-power-copper.py')))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit_json')
    parser.add_argument('retired_paths')
    parser.add_argument('output_json')
    parser.add_argument('--reserve-proposals', action='append', default=[])
    args = parser.parse_args()
    planner = helpers['Planner'](json.loads(Path(args.circuit_json).read_text()))
    replacements = set()
    for filename in args.reserve_proposals:
        proposals = json.loads(Path(filename).read_text())
        replacements.update(path['net'] for path in proposals.get('paths', []))
        planner.reserve_proposals(proposals)
    nets = {record['name']: record for record in planner.circuit if record['type'] == 'source_net'}
    paths, rejected = [], []
    for path in json.loads(Path(args.retired_paths).read_text())['paths']:
        if path['net'] in replacements:
            rejected.append({'from': path['from'], 'net': path['net'], 'reason': 'Net has replacement source paths'})
            continue
        root = planner.root(nets[path['net']]['source_net_id'])
        positions, layers = path['global_path_mm'], path['segment_layers']
        obstacles = {layer: planner.obstacles(root, layer, path['width']) for layer in set(layers)}
        blocked = any(LineString([first, last]).intersects(obstacles[layers[index + 1]])
                      for index, (first, last) in enumerate(zip(positions, positions[1:])))
        via_points = [positions[index] for index in range(1, len(positions) - 1)
                      if layers[index] != layers[index + 1]]
        if path['pcbPath'] and path['pcbPath'][-1].get('via'):
            via_points.append(positions[-1])
        if not blocked and via_points:
            via_obstacles = helpers['via_obstacles'](planner, {'root': root})
            blocked = any(Point(point).intersects(via_obstacles) for point in via_points)
        if blocked:
            rejected.append({'from': path['from'], 'to': path['to'], 'net': path['net'],
                             'reason': 'Preserved path conflicts with reserved copper or ordinary drill clearance'})
            continue
        paths.append(path)
        planner.reserve_proposals({'paths': [path]})
    Path(args.output_json).write_text(json.dumps({'classification': 'source path restoration proposals; native audit required',
        'source_circuit_json': args.circuit_json, 'paths': paths, 'rejected': rejected}, indent=2) + '\n')
    print(json.dumps({'selected': len(paths), 'rejected': len(rejected)}))


if __name__ == '__main__':
    main()
