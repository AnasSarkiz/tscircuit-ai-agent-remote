"""Accept only the narrow MCU correction after independent full-copper audits."""
import hashlib
import json
import math
from pathlib import Path
from shapely.geometry import LineString, Point

ROOT = Path(__file__).resolve().parents[2]
FOLDER = Path(__file__).resolve().parent
native_path = FOLDER / 'final-native/circuit.json'
native_bytes = native_path.read_bytes()
circuit = json.loads(native_bytes)
sha256 = hashlib.sha256(native_bytes).hexdigest()
copper = json.loads((FOLDER / 'final-copper.json').read_text())
regions = json.loads((FOLDER / 'final-region-widths.json').read_text())
widths = json.loads((FOLDER / 'final-trace-widths.json').read_text())
baseline = json.loads((ROOT / 'evidence/order-readiness-2026-10-06/copper-audit.json').read_text())
assert copper['source_sha256'] == regions['source_sha256'] == widths['source_sha256'] == sha256
assert not copper['violations'] and not copper['route_errors'] and not copper['merged_named_nets']
assert copper['drc_violation_count'] == copper['short_count'] == 0
assert regions['checked_region_count'] == 152 and regions['failed_region_count'] == 0
assert widths['trace_count_below_board_minimum'] == 0
assert widths['trace_count_below_source_minimum'] == 2
assert copper['physically_open_nets'] == baseline['physically_open_nets']
assert copper['native_errors'] == {'pcb_port_not_connected_error': 90}

components = {r['source_component_id']: r for r in circuit if r['type'] == 'source_component'}
source_ports = {r['source_port_id']: r for r in circuit if r['type'] == 'source_port'}
ports = {(components[source_ports[r['source_port_id']]['source_component_id']]['name'],
          source_ports[r['source_port_id']].get('pin_number')): r
         for r in circuit if r['type'] == 'pcb_port' and
         source_ports[r['source_port_id']]['source_component_id'] in components}
by_reference = {r['name']: r for r in components.values()}
assert by_reference['C30']['manufacturer_part_number'] == 'GRM188R61A226ME15D'
assert by_reference['C30']['supplier_part_numbers']['jlcpcb'] == ['C84419']
assert math.isclose(by_reference['C30']['capacitance'], 22e-6, rel_tol=1e-12)
assert math.isclose(by_reference['C31']['capacitance'], 100e-9, rel_tol=1e-12)

source_traces = {r['source_trace_id']: r for r in circuit if r['type'] == 'source_trace'}
def manual_route(endpoint):
    port = ports[endpoint]
    matches = [r for r in circuit if r['type'] == 'pcb_trace' and
               r['route'][0].get('start_pcb_port_id') == port['pcb_port_id'] and
               source_traces[r['source_trace_id']].get('name', '').startswith('MANUAL_')]
    assert len(matches) == 1, endpoint
    return matches[0]['route']

cap_route = manual_route(('C31', 1))
u1_route = manual_route(('U1', 2))
assert all(p['route_type'] == 'wire' and p['layer'] == 'top' and p['width'] >= .3 for p in cap_route)
assert u1_route[-1]['route_type'] == 'via'
supply_vias = [r for r in circuit if r['type'] == 'pcb_via' and
               r['x'] == u1_route[-1]['x'] and r['y'] == u1_route[-1]['y']]
assert len(supply_vias) == 1
supply_via = supply_vias[0]
# Contact need not land on the via centre. Measure overlap with its actual
# annular copper, including the drill, rather than an invented alignment tolerance.
via_center = Point(supply_via['x'], supply_via['y'])
via_annulus = via_center.buffer(supply_via['outer_diameter']/2).difference(
    via_center.buffer(supply_via['hole_diameter']/2))
cap_copper = LineString([(p['x'], p['y']) for p in cap_route]).buffer(cap_route[0]['width']/2)
assert cap_copper.intersection(via_annulus).area > 0
assert math.isclose(sum(math.dist((a['x'], a['y']), (b['x'], b['y']))
                       for a,b in zip(cap_route, cap_route[1:])), .8, abs_tol=1e-6)

def same_physical_island(endpoints):
    groups = [set(copper['physical_port_groups'][ports[p]['pcb_port_id']]) for p in endpoints]
    return all(len(group) == 1 for group in groups) and bool(set.intersection(*groups))

assert same_physical_island([('C31', 1), ('U1', 2)])
assert same_physical_island([('C31', 2), ('U1', 1), ('U1', 40), ('U1', 41)])
programmer_groups = [
    [('J6', 6), ('U1', 36)], [('J6', 5), ('R38', 2)], [('R38', 1), ('U1', 37)],
    [('J6', 1), ('J6', 7), ('J6', 8), ('U1', 1), ('U1', 40), ('U1', 41),
     ('U12', 1), ('R37', 2), ('SW1', 2), ('SW2', 2)],
    [('J6', 3), ('U1', 3), ('R35', 2), ('R37', 1), ('SW2', 1)],
    [('U12', 2), ('R35', 1)], [('J6', 4), ('U1', 27), ('R36', 2), ('SW1', 1)],
    [('J6', 2), ('U1', 2), ('U12', 3), ('R36', 1)],
]
assert all(same_physical_island(group) for group in programmer_groups)
for snapshot in (FOLDER / 'final-native/source-snapshot').rglob('*.txt'):
    original = ROOT / str(snapshot.relative_to(FOLDER / 'final-native/source-snapshot'))[:-4]
    assert snapshot.read_bytes() == original.read_bytes(), str(original)

cap = ports[('C31', 1)]
u1 = ports[('U1', 2)]
receipt = {
    'accepted_step': 'MCU local 100nF bypass and genuine 22uF bulk substitution',
    'native_sha256': sha256, 'native_bytes': len(native_bytes),
    'native_snapshot_matches_published_board_source': True,
    'drc_geometry_violations': 0, 'measured_shorts': 0,
    'physically_open_net_count': copper['physically_open_net_count'],
    'native_open_port_errors': 90, 'open_net_partitions_unchanged': True,
    'ground_islands': next(r['island_count'] for r in copper['physically_open_nets'] if r['net'] == 'GND'),
    'c31_to_u1_power_pin_distance_mm': math.dist((cap['x'],cap['y']), (u1['x'],u1['y'])),
    'c31_previous_distance_mm': next(cap['supply_pin_center_distance_mm']
        for supply in json.loads((ROOT / 'evidence/board-programmer-stock-review-2026-10-06/decoupling-placement.json').read_text())['measurements']
        if supply['reference'] == 'U1' for cap in supply['assigned_bypass_measurements'] if cap['capacitor'] == 'C31'),
    'c31_top_supply_branch_mm': .8, 'c31_and_u1_supply_and_ground_physically_joined': True,
    'c31_additional_supply_vias': 0, 'ordinary_via_count': sum(r['type'] == 'pcb_via' for r in circuit),
    'native_trace_count': sum(r['type'] == 'pcb_trace' for r in circuit),
    'native_pour_count': sum(r['type'] == 'pcb_copper_pour' for r in circuit),
    'all_152_authored_region_widths_pass': True,
    'programmer_target_physical_groups_checked': len(programmer_groups),
    'programmer_hardware_tested': False,
    'full_copper_gate_passed': False, 'fabrication_ready': False,
    'scope': 'Accepted only this implementation step. Full routing, current capacity, remaining bypasses, interface mating, stencil/schema/assembly, current stock and mechanical gates remain unresolved.',
}
(FOLDER / 'accepted-step.json').write_text(json.dumps(receipt, indent=2)+'\n')
(ROOT / 'dist/index/circuit.json').write_bytes(native_bytes)
print(json.dumps(receipt, indent=2))
