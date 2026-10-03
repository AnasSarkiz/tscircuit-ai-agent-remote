"""Measure different-net rectangular SMT lands in preserved native fixtures."""
import hashlib
import itertools
import json
import math
from pathlib import Path

BOARD_DIRECTORY = Path(__file__).resolve().parents[2]
FIXTURE_PATHS = [
    'evidence/mcu-usb-review-2026-10-03/circuit.json',
    'evidence/type-c-current-review-2026-10-03/circuit.json',
    'evidence/display-review-2026-10-03/circuit.json',
    'evidence/hold-control-alternate-review-2026-10-03/circuit.json',
]


def pad_clearance_mm(pair):
    first, second = pair
    dx = max(abs(first['x'] - second['x']) - (first['width'] + second['width']) / 2, 0)
    dy = max(abs(first['y'] - second['y']) - (first['height'] + second['height']) / 2, 0)
    return math.hypot(dx, dy)


results = []
for fixture_path in FIXTURE_PATHS:
    circuit_bytes = (BOARD_DIRECTORY / fixture_path).read_bytes()
    elements = json.loads(circuit_bytes)
    source_components = {element['source_component_id']: element for element in elements if element['type'] == 'source_component'}
    source_ports = {element['source_port_id']: element for element in elements if element['type'] == 'source_port'}
    pcb_ports = {element['pcb_port_id']: element for element in elements if element['type'] == 'pcb_port'}
    components = []
    for component in elements:
        if component['type'] != 'pcb_component':
            continue
        pads = [element for element in elements if element['type'] == 'pcb_smtpad' and element['pcb_component_id'] == component['pcb_component_id']]
        comparisons = []
        skipped_same_net = 0
        skipped_unknown_net = 0
        for first, second in itertools.combinations(pads, 2):
            if first['shape'] != 'rect' or second['shape'] != 'rect':
                continue
            if first.get('rotation', 0) != 0 or second.get('rotation', 0) != 0:
                raise ValueError('Rotated rectangular land needs oriented geometry measurement')
            first_port = source_ports[pcb_ports[first['pcb_port_id']]['source_port_id']]
            second_port = source_ports[pcb_ports[second['pcb_port_id']]['source_port_id']]
            first_net = first_port.get('subcircuit_connectivity_map_key')
            second_net = second_port.get('subcircuit_connectivity_map_key')
            if first_net is None or second_net is None:
                skipped_unknown_net += 1
                continue
            if first_net == second_net:
                skipped_same_net += 1
                continue
            comparisons.append({'first_pad': first['pcb_smtpad_id'], 'second_pad': second['pcb_smtpad_id'], 'first_hints': first['port_hints'], 'second_hints': second['port_hints'], 'nominal_clearance_mm': pad_clearance_mm((first, second))})
        source_component = source_components[component['source_component_id']]
        minimum_pair = min(comparisons, key=lambda comparison: comparison['nominal_clearance_mm']) if comparisons else None
        components.append({'reference': source_component['name'], 'mpn': source_component.get('manufacturer_part_number'), 'supplier_part_numbers': source_component.get('supplier_part_numbers'), 'pad_count': len(pads), 'unmeasured_non_rectangular_pad_count': sum(pad['shape'] != 'rect' for pad in pads), 'different_net_rect_pairs_measured': len(comparisons), 'same_net_pairs_excluded': skipped_same_net, 'unknown_connectivity_pairs_excluded': skipped_unknown_net, 'minimum_pair': minimum_pair})
    results.append({'fixture': fixture_path, 'sha256': hashlib.sha256(circuit_bytes).hexdigest(), 'components': components})
result = {'scope': 'Nominal per-component different-net axis-aligned rectangular SMT-pad measurement only; does not qualify other shapes, inter-component placement, mask, paste, plated holes, routed copper or complete board', 'manufacturer_smt_different_net_pad_clearance_minimum_mm': 0.15, 'fixtures': results}
Path(__file__).with_name('rect-pad-clearances.json').write_text(json.dumps(result, indent=2) + '\n')
minimum_pairs = [(fixture['fixture'], component['reference'], component['minimum_pair']['nominal_clearance_mm']) for fixture in results for component in fixture['components'] if component['minimum_pair']]
print(json.dumps({'components_measured': len(minimum_pairs), 'minimum_clearance_mm': min(pair[2] for pair in minimum_pairs), 'below_manufacturer_nominal_minimum': [pair for pair in minimum_pairs if pair[2] < 0.15]}, indent=2))
