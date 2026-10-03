"""Measure untouched native PCB geometry; does not rewrite circuit output."""
import hashlib
import json
import math
from pathlib import Path

BOARD_DIRECTORY = Path(__file__).resolve().parents[2]
CIRCUIT_PATH = BOARD_DIRECTORY / 'evidence/core-alignment-2026-10-03/microphone-circuit.json'


def segment_distance_mm(point, segment):
    start, end = segment
    dx, dy = end['x'] - start['x'], end['y'] - start['y']
    length_squared = dx * dx + dy * dy
    fraction = 0 if length_squared == 0 else max(0, min(1, ((point['x'] - start['x']) * dx + (point['y'] - start['y']) * dy) / length_squared))
    return math.hypot(point['x'] - start['x'] - fraction * dx, point['y'] - start['y'] - fraction * dy)


def pad_boundary_distance_mm(hole, pad):
    if pad['shape'] == 'polygon':
        points = pad['points']
        return min(segment_distance_mm(hole, (points[index], points[(index + 1) % len(points)])) for index in range(len(points)))
    if pad['shape'] == 'rect':
        dx = max(abs(hole['x'] - pad['x']) - pad['width'] / 2, 0)
        dy = max(abs(hole['y'] - pad['y']) - pad['height'] / 2, 0)
        return math.hypot(dx, dy)
    raise ValueError(f"Unmeasured pad shape: {pad['shape']}")


circuit_bytes = CIRCUIT_PATH.read_bytes()
circuit_elements = json.loads(circuit_bytes)
holes = [element for element in circuit_elements if element['type'] == 'pcb_hole']
if len(holes) != 1 or holes[0]['hole_shape'] != 'circle':
    raise ValueError('Expected one native circular acoustic hole')
hole = holes[0]
measurements = []
for pad in circuit_elements:
    if pad['type'] != 'pcb_smtpad' or pad['pcb_component_id'] != hole['pcb_component_id']:
        continue
    clearance_mm = pad_boundary_distance_mm(hole, pad) - hole['hole_diameter'] / 2
    if clearance_mm <= 0:
        raise ValueError(f"Acoustic drill intersects {pad['pcb_smtpad_id']}")
    measurements.append({'pcb_smtpad_id': pad['pcb_smtpad_id'], 'port_hints': pad['port_hints'], 'shape': pad['shape'], 'nominal_drill_edge_to_pad_mm': clearance_mm})
minimum_clearance_mm = min(measurement['nominal_drill_edge_to_pad_mm'] for measurement in measurements)
result = {
    'scope': 'Read-only nominal native geometry measurement, not full-board DRC or fabrication approval',
    'component': 'ICS-43434 / C5656610',
    'native_circuit_path': str(CIRCUIT_PATH.relative_to(BOARD_DIRECTORY)),
    'native_circuit_sha256': hashlib.sha256(circuit_bytes).hexdigest(),
    'native_hole_diameter_mm': hole['hole_diameter'],
    'native_hole_center_mm': {'x': hole['x'], 'y': hole['y']},
    'pad_measurements': measurements,
    'minimum_nominal_drill_edge_to_pad_mm': minimum_clearance_mm,
    'jlcpcb_nominal_npth_to_track_minimum_mm': 0.2,
    'conditional_generic_finished_hole_range_mm': [hole['hole_diameter'] - 0.08, hole['hole_diameter'] + 0.13],
    'tdk_recommended_minimum_acoustic_hole_diameter_mm': 0.5,
    'conditional_maximum_drill_and_position_sweep_clearance_mm': minimum_clearance_mm - 0.13 / 2 - 0.075,
    'tolerance_caution': 'The conditional sweep is not a manufacturing violation: supplier nominal design rules may already budget tolerances, and the acoustic NPTH process must be confirmed. Do not double-count tolerances or apply PTH rules blindly.',
    'unresolved': ['Ground polygon solder paste generation (B-005)', 'Acoustic seal, solder mask and NPTH fabrication process acceptance', 'Full-board drill-to-copper measurement after actual routing'],
}
output_path = Path(__file__).with_name('microphone-hole-geometry.json')
output_path.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'minimum_nominal_clearance_mm': minimum_clearance_mm, 'conditional_hole_range_mm': result['conditional_generic_finished_hole_range_mm'], 'circuit_sha256': result['native_circuit_sha256']}))
