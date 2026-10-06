"""Check exact via geometry, supply layers and preserved physical contacts."""
import argparse
import hashlib
import itertools
import json
import runpy
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('native_json', type=Path)
parser.add_argument('copper_audit', type=Path)
parser.add_argument('output_json', type=Path)
args = parser.parse_args()
parent_path = Path('evidence/schematic-component-notes-2026-10-06/final-native/circuit.json')
parent = json.loads(parent_path.read_text())
current = json.loads(args.native_json.read_text())
parent_audit = json.loads(Path('evidence/six-point-board-review-2026-10-06/parent-copper-audit.json').read_text())
audit = json.loads(args.copper_audit.read_text())

def ports_by_label(circuit, result):
    components = {r['source_component_id']: r for r in circuit if r['type'] == 'source_component'}
    source_ports = {r['source_port_id']: r for r in circuit if r['type'] == 'source_port'}
    labels = {}
    for port in circuit:
        if port['type'] != 'pcb_port':
            continue
        source = source_ports[port['source_port_id']]
        component = components.get(source.get('source_component_id'))
        if component:
            label = (component['name'], source.get('pin_number', source['name']))
            if label in labels:
                raise ValueError(f'Duplicate numbered port: {label}')
            labels[label] = set(result['physical_port_groups'][port['pcb_port_id']])
    return labels

before = ports_by_label(parent, parent_audit)
after = ports_by_label(current, audit)
missing = sorted(set(before) - set(after))
splits = []
checked = 0
for first, last in itertools.combinations(before, 2):
    if before[first] & before[last]:
        checked += 1
        if first not in after or last not in after or not after[first] & after[last]:
            splits.append([first, last])

def purchased(circuit):
    return sorted((r['name'], r.get('manufacturer_part_number'),
                   tuple(r.get('supplier_part_numbers', {}).get('jlcpcb', [])))
                  for r in circuit if r['type'] == 'source_component' and
                  r.get('supplier_part_numbers', {}).get('jlcpcb'))

def j1_physical(circuit):
    source_id = next(r['source_component_id'] for r in circuit if r['type'] == 'source_component' and r['name'] == 'J1')
    pcb_id = next(r['pcb_component_id'] for r in circuit if r['type'] == 'pcb_component' and r['source_component_id'] == source_id)
    return [{k: v for k, v in r.items() if k != 'cable_insertion_center'}
            for r in circuit if r.get('pcb_component_id') == pcb_id and
            r['type'] in ('pcb_component', 'pcb_smtpad', 'pcb_plated_hole', 'pcb_hole', 'cad_component')]

def purchased_physical(circuit):
    source_ids = {r['source_component_id'] for r in circuit if r['type'] == 'source_component'
                  and r.get('supplier_part_numbers', {}).get('jlcpcb')}
    pcb_ids = {r['pcb_component_id'] for r in circuit if r['type'] == 'pcb_component'
               and r['source_component_id'] in source_ids}
    return [{k: v for k, v in r.items() if k != 'cable_insertion_center'} for r in circuit
            if r.get('pcb_component_id') in pcb_ids and r['type'] in
            ('pcb_component', 'pcb_smtpad', 'pcb_plated_hole', 'pcb_hole', 'cad_component')]

vias = [r for r in current if r['type'] == 'pcb_via']
bad_vias = [r['pcb_via_id'] for r in vias if r['hole_diameter'] != .3 or r['outer_diameter'] != .45 or
            r.get('from_layer') not in ('top', 'inner1', 'inner2', 'bottom') or
            r.get('to_layer') not in ('top', 'inner1', 'inner2', 'bottom') or
            set(r['layers']) != {'top', 'inner1', 'inner2', 'bottom'}]
regions = json.loads(Path('src/board/manual-power-copper.json').read_text())
high = {'PACK_BAT', 'VSYS', 'VBUS', 'V3V3', 'VMOTOR', 'HAPTIC_N'}
trace_helpers = runpy.run_path('scripts/routing/audit-trace-widths.py')
electrical, source_traces, net_roots = trace_helpers['electrical_roots'](current)
bad_high_wires = []
checked_high_traces = 0
for trace in current:
    if trace['type'] != 'pcb_trace':
        continue
    source = source_traces[trace['source_trace_id']]
    terminals = source.get('connected_source_port_ids', [])+source.get('connected_source_net_ids', [])
    names = {net['name'] for net in net_roots.get(electrical.root(terminals[0]), [])}
    if not names.intersection(high | {'SPEAKER_N', 'SPEAKER_P'}) and source.get('min_trace_thickness',0) < .8:
        continue
    checked_high_traces += 1
    if any(point['route_type'] == 'wire' and point['layer'] not in ('top','bottom') for point in trace['route']):
        bad_high_wires.append(trace['pcb_trace_id'])
high_regions = [r for r in regions['pours'] if r['net'] in high and not r.get('branch_terminal')]
bad_power_regions = [i for i, r in enumerate(regions['pours']) if r['net'] in high and
                     r['layer'] not in ('top', 'bottom') and not any(
                     b['net'] == r['net'] and b['terminal'] == r.get('branch_terminal') and
                     r['layer'] in b['layers'] and r['nominal_width_mm'] == b['nominal_width_mm']
                     for b in regions['branch_requirements'])]
result = {
    'native_json': str(args.native_json), 'native_sha256': hashlib.sha256(args.native_json.read_bytes()).hexdigest(),
    'parent_sha256': hashlib.sha256(parent_path.read_bytes()).hexdigest(),
    'via_count': len(vias), 'exact_0p30_drill_0p45_pad_and_full_span': bool(vias) and not bad_vias,
    'nonconforming_vias': bad_vias,
    'via_span_contract': 'Physical span is pcb_via.layers. In core0.0.2090 getAutoroutedViaLayers returns every board layer when allowBlindAndBuriedVias=false. from_layer/to_layer preserve the routing wire-layer transition, including inner-layer connections; they are not the physical drill span.',
    'authored_high_current_regions': len(high_regions),
    'authored_high_current_trunks_outer_only': bool(high_regions) and not bad_power_regions,
    'high_current_native_traces_checked': checked_high_traces,
    'high_current_native_wire_layers_outer_only': bool(checked_high_traces) and not bad_high_wires,
    'high_current_native_traces_on_inner_layers': bad_high_wires,
    'nonconforming_power_regions': bad_power_regions,
    'reviewed_inner_low_current_branches': [r for r in regions['branch_requirements']],
    'purchased_components': len(purchased(current)), 'supplier_identities_unchanged': purchased(parent) == purchased(current),
    'J1_native_footprint_pose_and_model_unchanged': j1_physical(parent) == j1_physical(current),
    'all_125_purchased_native_footprints_poses_and_models_unchanged': purchased_physical(parent) == purchased_physical(current),
    'J1_standard_connector_access_metadata': [r.get('cable_insertion_center') for r in current
        if r['type'] == 'pcb_component' and r.get('pcb_component_id') == next(
        x['pcb_component_id'] for x in current if x['type'] == 'pcb_component' and
        x['source_component_id'] == next(y['source_component_id'] for y in current
        if y['type'] == 'source_component' and y['name'] == 'J1'))],
    'previously_connected_port_pairs_checked': checked,
    'previously_connected_pairs_split': splits, 'missing_original_ports': missing,
    'no_previous_connections_lost': not (splits or missing),
    'native_error_count': sum('error' in r['type'] for r in current),
    'drc_violation_count': audit['drc_violation_count'], 'short_count': audit['short_count'],
    'physically_open_net_count': audit['physically_open_net_count'],
    'fabrication_approved': False,
}
args.output_json.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k not in ('reviewed_inner_low_current_branches', 'previously_connected_pairs_split')}))
raise SystemExit(0 if all((result['exact_0p30_drill_0p45_pad_and_full_span'],
    result['authored_high_current_trunks_outer_only'], result['supplier_identities_unchanged'],
    result['high_current_native_wire_layers_outer_only'],
    result['J1_native_footprint_pose_and_model_unchanged'], result['no_previous_connections_lost'],
    result['all_125_purchased_native_footprints_poses_and_models_unchanged'],
    not result['drc_violation_count'], not result['short_count'])) else 1)
