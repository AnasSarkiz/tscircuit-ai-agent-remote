"""Check unchanged purchased geometry in each component's native local frame.

World geometry is compared exactly for stationary parts. The five declared
moves must match their proposed poses and preserve numbered contacts, actual
pad/drill contours and model definitions. This never qualifies enclosure fit
or assembler rotations.
"""
import hashlib
import argparse
import json
import math
import runpy
import subprocess
from pathlib import Path

from shapely.affinity import affine_transform
from shapely.geometry import Point

evidence = Path(__file__).parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('native', type=Path)
parser.add_argument('output', type=Path)
args = parser.parse_args()
paths = [Path('evidence/routing-zero-drc-2026-10-07/final-native/circuit.json'), args.native]
circuits = [json.loads(path.read_text()) for path in paths]
expected = {'U3': (-16.75, 3.5, 0), 'J4': (-17.5, 9.05, 90),
            'C50': (-13.7, 7.5, 90), 'R69': (-11.48, 7.5, 180), 'R70': (-21, 4.5, 180)}
helpers = runpy.run_path('scripts/routing/audit-copper.py')
physical_types = {'pcb_component', 'pcb_smtpad', 'pcb_plated_hole', 'pcb_hole', 'cad_component'}


def inventory(circuit):
    sources = {r['source_component_id']: r for r in circuit if r['type'] == 'source_component'
               and r.get('supplier_part_numbers', {}).get('jlcpcb')}
    boards = {sources[r['source_component_id']]['name']: r for r in circuit
              if r['type'] == 'pcb_component' and r['source_component_id'] in sources}
    return sources, boards


def inverse_matrices(boards):
    poses = {name: {'x': r['display_offset_x'], 'y': r['display_offset_y'], 'rotation': r['rotation']}
             for name, r in boards.items() if name in expected}
    result = subprocess.run(['bun', str(evidence / 'pcb-pose-inverse.mjs')],
                            input=json.dumps(poses), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def local(shape, matrix):
    return affine_transform(shape, [matrix['a'], matrix['c'], matrix['b'], matrix['d'], matrix['e'], matrix['f']])


def numeric_equal(first, second):
    if isinstance(first, dict) and isinstance(second, dict):
        return first.keys() == second.keys() and all(numeric_equal(first[k], second[k]) for k in first)
    if isinstance(first, list) and isinstance(second, list):
        return len(first) == len(second) and all(numeric_equal(a, b) for a, b in zip(first, second))
    if isinstance(first, (int, float)) and isinstance(second, (int, float)):
        return math.isclose(first, second, abs_tol=1e-6, rel_tol=0)
    return first == second


def records(circuit, board):
    return {r[f"{r['type']}_id"]: r for r in circuit
            if r.get('pcb_component_id') == board['pcb_component_id'] and r['type'] in physical_types}


def shape_equal(first, second, matrices):
    before = local(helpers['pad_contour'](first), matrices[0])
    after = local(helpers['pad_contour'](second), matrices[1])
    contour_ok = before.hausdorff_distance(after) <= 1e-6 and abs(before.area - after.area) <= 1e-8
    drills_ok = True
    if first['type'] in ('pcb_plated_hole', 'pcb_hole'):
        before_drill = local(helpers['drill_contour'](first), matrices[0])
        after_drill = local(helpers['drill_contour'](second), matrices[1])
        drills_ok = before_drill.hausdorff_distance(after_drill) <= 1e-6
    geometric = {'x', 'y', 'center', 'points', 'ccw_rotation', 'rect_ccw_rotation', 'hole_ccw_rotation', 'rotation', 'width', 'height',
                 'rect_pad_width', 'rect_pad_height', 'outer_width', 'outer_height'}
    metadata_ok = numeric_equal({k: v for k, v in first.items() if k not in geometric},
                                {k: v for k, v in second.items() if k not in geometric})
    return contour_ok and drills_ok and metadata_ok


inventories = [inventory(c) for c in circuits]
boards = [item[1] for item in inventories]
matrices = [inverse_matrices(b) for b in boards]
failures = []
moved = []
stationary = []
for name in sorted(boards[0]):
    if name not in boards[1]:
        failures.append(f'{name}: missing component')
        continue
    before, after = [records(c, b[name]) for c, b in zip(circuits, boards)]
    if name not in expected:
        stationary.append(name)
        if before != after:
            failures.append(f'{name}: stationary native records changed')
        continue
    pcb = boards[1][name]
    pose = (pcb['display_offset_x'], pcb['display_offset_y'], pcb['rotation'])
    if pose != expected[name]:
        failures.append(f'{name}: wrong proposed pose {pose}')
    if before.keys() != after.keys():
        failures.append(f'{name}: footprint record ownership changed')
        continue
    checked_contours = 0
    for identifier, old in before.items():
        new = after[identifier]
        if old['type'] in ('pcb_smtpad', 'pcb_plated_hole', 'pcb_hole'):
            checked_contours += 1
            if not shape_equal(old, new, [m[name] for m in matrices]):
                failures.append(f'{name}: changed local contour/contact {identifier}')
        elif old['type'] == 'cad_component':
            omitted = {'position', 'rotation'}
            if not numeric_equal({k: v for k, v in old.items() if k not in omitted},
                                 {k: v for k, v in new.items() if k not in omitted}):
                failures.append(f'{name}: changed intrinsic model definition')
            old_position = local(Point(old['position']['x'], old['position']['y']), matrices[0][name])
            new_position = local(Point(new['position']['x'], new['position']['y']), matrices[1][name])
            if old_position.distance(new_position) > 1e-6 or old['position']['z'] != new['position']['z']:
                failures.append(f'{name}: changed local model anchor')
            old_rotation = old['rotation']['z'] - boards[0][name]['rotation']
            new_rotation = new['rotation']['z'] - boards[1][name]['rotation']
            if (old_rotation - new_rotation) % 360 != 0 or any(old['rotation'][k] != new['rotation'][k] for k in ('x', 'y')):
                failures.append(f'{name}: changed intrinsic model rotation')
        elif old['type'] == 'pcb_component':
            omitted = {'center', 'width', 'height', 'rotation', 'display_offset_x', 'display_offset_y', 'pin1_location', 'cable_insertion_center'}
            if {k: v for k, v in old.items() if k not in omitted} != {k: v for k, v in new.items() if k not in omitted}:
                failures.append(f'{name}: changed component metadata')
    moved.append({'reference': name, 'before_pose': [boards[0][name][k] for k in ('display_offset_x', 'display_offset_y', 'rotation')],
                  'after_pose': list(pose), 'local_pad_drill_contours_checked': checked_contours})

sources = [sorted((r['name'], r.get('manufacturer_part_number'), r.get('supplier_part_numbers'))
                  for r in item[0].values()) for item in inventories]
if sources[0] != sources[1]:
    failures.append('Purchased supplier identities changed')
if len(stationary) != 120 or len(moved) != 5:
    failures.append(f'Unexpected inventory: {len(stationary)} stationary and {len(moved)} moved')
result = {'native_sha256': [hashlib.sha256(p.read_bytes()).hexdigest() for p in paths],
          'purchased_count': len(boards[1]), 'supplier_identities_unchanged': sources[0] == sources[1],
          'stationary_count': len(stationary), 'stationary_references': stationary, 'authorized_moves': moved,
          'failures': failures, 'passed': not failures, 'mechanical_fit_approved': False,
          'assembler_rotations_approved': False}
args.output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'stationary_references'}))
raise SystemExit(0 if result['passed'] else 1)
