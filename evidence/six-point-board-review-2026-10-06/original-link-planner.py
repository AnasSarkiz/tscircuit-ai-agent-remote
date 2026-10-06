"""Replace authored high-current distribution with top/bottom native regions.

Preserve the native scene and saved router output. Plan against all unrelated
copper and exact imported pad/drill contours. A proposal needs native replay
and independent geometry/connectivity validation before acceptance.
"""
import argparse
import hashlib
import json
import math
import runpy
from pathlib import Path

from shapely.geometry import LineString, Point

helpers = runpy.run_path(str(Path(__file__).with_name('plan-power-copper.py')))
HIGH_CURRENT_NETS = ('PACK_BAT', 'VSYS', 'VBUS', 'V3V3', 'VMOTOR', 'HAPTIC_N')


def replacement_links(regions, existing_vias):
    links = list(regions)
    # Collapse an authored bend shared by exactly two pieces, when that bend
    # is not a plated terminal. This preserves terminal connectivity while
    # allowing the replacement centreline to choose a different path.
    changed = True
    while changed:
        changed = False
        for index, first in enumerate(links):
            for endpoint in (first['path_mm'][0], first['path_mm'][-1]):
                if any(math.dist(endpoint, via) < 1e-5 for via in existing_vias):
                    continue
                adjoining = [(other_index, other) for other_index, other in enumerate(links)
                             if other_index != index and other['net'] == first['net']
                             and other['nominal_width_mm'] == first['nominal_width_mm']
                             and any(math.dist(endpoint, p) < 1e-5 for p in (other['path_mm'][0], other['path_mm'][-1]))]
                if len(adjoining) != 1:
                    raise ValueError('Non-via power junction requires a separately qualified terminal')
                other_index, other = adjoining[0]
                first_end = first['path_mm'][-1] if math.dist(endpoint, first['path_mm'][0]) < 1e-5 else first['path_mm'][0]
                last_end = other['path_mm'][-1] if math.dist(endpoint, other['path_mm'][0]) < 1e-5 else other['path_mm'][0]
                combined = {**first, 'path_mm': [first_end, last_end]}
                links = [item for position, item in enumerate(links) if position not in (index, other_index)] + [combined]
                changed = True
                break
            if changed:
                break
    return links


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit_json', type=Path)
    parser.add_argument('authored_regions', type=Path)
    parser.add_argument('output_json', type=Path)
    parser.add_argument('--grid-mm', type=float, choices=(.05, .1), default=.1)
    args = parser.parse_args()
    circuit = json.loads(args.circuit_json.read_text())
    authored = json.loads(args.authored_regions.read_text())
    nets = {record['name']: record for record in circuit if record['type'] == 'source_net'}
    replaced_net_ids = {nets[name]['source_net_id'] for name in HIGH_CURRENT_NETS}
    retired_pour_ids = {record['pcb_copper_pour_id'] for record in circuit
                        if record['type'] == 'pcb_copper_pour' and record['source_net_id'] in replaced_net_ids}
    planner = helpers['Planner'](circuit, retired_pour_ids)
    planner.set_grid(args.grid_mm)
    planner.via_copper_clearance = .27
    existing_vias = [(record['x'], record['y']) for record in circuit if record['type'] == 'pcb_via']
    originals = [region for region in authored['pours'] if region['net'] in HIGH_CURRENT_NETS]
    links = replacement_links(originals, existing_vias)
    output = {**authored, 'pours': [region for region in authored['pours'] if region['net'] not in HIGH_CURRENT_NETS],
              'vias': list(authored['vias']), 'unresolved': [],
              'classification': 'authored outer-layer high-current replacement; requires native replay and audit',
              'source_circuit_json': str(args.circuit_json),
              'source_sha256': hashlib.sha256(args.circuit_json.read_bytes()).hexdigest(),
              'retired_pour_ids': sorted(retired_pour_ids), 'replaced_authored_region_count': len(originals)}
    for name in HIGH_CURRENT_NETS:
        root = planner.root(nets[name]['source_net_id'])
        for index, region in enumerate(link for link in links if link['net'] == name):
            width = region['nominal_width_mm'] + .002
            own_vias = [(record['x'], record['y']) for record in output['vias'] if record['net'] == name]
            own_vias += [p for p in existing_vias if planner.plated_hole_roots.get(Point(p).buffer(.15).wkb) == root]
            result = helpers['wide_multilayer_route'](planner, {
                'first': region['path_mm'][0], 'last': region['path_mm'][-1], 'root': root,
                'width': width, 'new_vias': own_vias, 'layers': ('top', 'bottom'),
                'via_outer_mm': .45, 'via_hole_mm': .3, 'copper_clearance_mm': .27})
            if result is None:
                output['unresolved'].append({'net': name, 'link': index, 'terminals_mm': [region['path_mm'][0], region['path_mm'][-1]],
                                             'nominal_width_mm': region['nominal_width_mm'], 'reason': 'No top/bottom path at required width and clearances'})
            else:
                parts, new_vias = result
                for layer, route in parts:
                    if len(route) < 2 or LineString(route).length < 1e-6:
                        continue
                    contour = LineString(route).buffer(width / 2, cap_style=2, join_style=2)
                    if contour.geom_type != 'Polygon' or contour.interiors:
                        raise ValueError('Native region needs one simple outline')
                    output['pours'].append({**region, 'layer': layer, 'path_mm': route,
                        'outline': [{'x': round(x, 6), 'y': round(y, 6)} for x, y in list(contour.exterior.coords)[:-1]],
                        'drawn_width_mm': width, 'classification': 'manual native outer-layer power region; thermal qualification pending'})
                    planner.copper.append((root, layer, contour))
                for x, y in new_vias:
                    output['vias'].append({'net': name, 'x': x, 'y': y, 'hole_mm': .3, 'outer_mm': .45,
                                          'classification': 'manual native through via between outer power regions'})
                    hole = Point(x, y).buffer(.15)
                    planner.holes.append(hole)
                    planner.plated_hole_roots[hole.wkb] = root
                    for layer in ('top', 'inner1', 'inner2', 'bottom'):
                        planner.copper.append((root, layer, Point(x, y).buffer(.225)))
            args.output_json.write_text(json.dumps(output, indent=2) + '\n')
            print(json.dumps({'net': name, 'link': index, 'routed': result is not None,
                              'unresolved_count': len(output['unresolved'])}), flush=True)
    return 1 if output['unresolved'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
