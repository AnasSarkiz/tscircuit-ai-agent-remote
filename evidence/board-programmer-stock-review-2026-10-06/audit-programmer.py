"""Review the exact published UART pinout against unchanged target copper.

Source topology is checked separately from physical contact. Existing physical
measurements are reused only after their native-input SHA256 is verified.
This does not qualify a cable, flashed programmer, supply or working hardware.
"""
import datetime
import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REVIEW = Path(__file__).resolve().parent
PREVIOUS = ROOT / 'evidence/order-readiness-2026-10-06'


def read_json(path):
    return json.loads(path.read_text())


def source_components(circuit):
    return {row['name']: row for row in circuit if row['type'] == 'source_component'}


def port_lookup(circuit):
    names = {row['source_component_id']: row['name']
             for row in circuit if row['type'] == 'source_component'}
    return {(names[row['source_component_id']], row.get('pin_number', row['name'])): row
            for row in circuit if row['type'] == 'source_port'
            and row.get('source_component_id') in names}


def electrically_joined(circuit, endpoints):
    ports = port_lookup(circuit)
    parent = {}

    def root(identifier):
        parent.setdefault(identifier, identifier)
        if parent[identifier] != identifier:
            parent[identifier] = root(parent[identifier])
        return parent[identifier]

    for trace in circuit:
        if trace['type'] != 'source_trace':
            continue
        identifiers = trace['connected_source_port_ids'] + trace['connected_source_net_ids']
        for identifier in identifiers[1:]:
            parent[root(identifier)] = root(identifiers[0])
    return len({root(ports[endpoint]['source_port_id']) for endpoint in endpoints}) == 1


def main():
    target_path = ROOT / 'dist/index/circuit.json'
    target_sha256 = hashlib.sha256(target_path.read_bytes()).hexdigest()
    target = read_json(target_path)
    host_path = REVIEW / 'programmer-source/dist/circuits/programmer/circuit.json.gz'
    host_native_bytes = gzip.decompress(host_path.read_bytes())
    host = json.loads(host_native_bytes)
    copper = read_json(PREVIOUS / 'copper-audit.json')
    inventory = read_json(PREVIOUS / 'component-summary.json')
    assert target_sha256 == copper['source_sha256'] == inventory['source_sha256']
    host_components = source_components(host)
    target_components = source_components(target)
    assert target_components['J6']['supplier_part_numbers']['jlcpcb'] == ['C160405']
    assert target_components['U1']['manufacturer_part_number'] == 'ESP32-S3-WROOM-1-N8R8'
    assert target_components['U12']['manufacturer_part_number'] == 'TPS3839G33DBZR'
    for reference, resistance in [('R35', 4700), ('R36', 10000),
                                  ('R37', 100000), ('R38', 1000)]:
        assert target_components[reference]['resistance'] == resistance
    assert host_components['J5']['supplier_part_numbers']['jlcpcb'] == ['C160403']
    assert host_components['R_UART_TX']['resistance'] == 100
    assert host_components['R_UART_RX']['resistance'] == 100
    host_checks = []
    for endpoints in [
        [('J5', 1), ('R_UART_TX', 2)],
        [('R_UART_TX', 1), ('U1', 11)],
        [('J5', 3), ('R_UART_RX', 2)],
        [('R_UART_RX', 1), ('U1', 12)],
        [('J5', 2), ('U1', 57)],
    ]:
        result = electrically_joined(host, endpoints)
        host_checks.append({'endpoints': endpoints, 'logical_connected': result})
        assert result, endpoints
    host_ports = port_lookup(host)
    assert [host_ports[('J5', pin)]['name'] for pin in [1, 2, 3]] == ['TX', 'GND', 'RX']
    assert host_ports[('U1', 11)]['name'] == 'GPIO8'
    assert host_ports[('U1', 12)]['name'] == 'GPIO9'

    assignments = read_json(PREVIOUS / 'pin-assignments.json')
    target_pins = {(row['reference'], row['pin_number']): row for row in assignments}
    target_checks = []
    for endpoints in [
        [('J6', 6), ('U1', 36)],
        [('J6', 5), ('R38', 2)],
        [('R38', 1), ('U1', 37)],
        [('J6', 1), ('J6', 7), ('J6', 8), ('U1', 1), ('U1', 40), ('U1', 41),
         ('U12', 1), ('R37', 2), ('SW1', 2), ('SW2', 2)],
        [('J6', 3), ('U1', 3), ('R35', 2), ('R37', 1), ('SW2', 1)],
        [('U12', 2), ('R35', 1)],
        [('J6', 4), ('U1', 27), ('R36', 2), ('SW1', 1)],
        [('J6', 2), ('U1', 2), ('U12', 3), ('R36', 1)],
    ]:
        rows = [target_pins[endpoint] for endpoint in endpoints]
        groups = [set(row['physical_island_ids']) for row in rows]
        physical_connected = all(len(group) == 1 for group in groups) and bool(set.intersection(*groups))
        logical_connected = electrically_joined(target, endpoints)
        no_port_errors = all(not row['native_port_error'] for row in rows)
        target_checks.append({'endpoints': endpoints, 'logical_connected': logical_connected,
                              'physical_connected': physical_connected,
                              'no_native_port_errors': no_port_errors})
        assert physical_connected and logical_connected and no_port_errors, endpoints

    report = {
        'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'target_native_sha256': target_sha256,
        'programmer_native_sha256': hashlib.sha256(host_native_bytes).hexdigest(),
        'programmer_version': '0.8.0',
        'programmer_release_id': '3d6952c4-e6ee-4711-a7c7-dded0cdef4eb',
        'host_source_checks': host_checks,
        'target_source_and_physical_checks': target_checks,
        'target_connector_pin_assignments': [target_pins[('J6', pin)] for pin in range(1, 9)],
        'adapter_mapping': [
            {'host': 'J5.1 TX', 'target': 'J6.6 MCU_UART_RX'},
            {'host': 'J5.2 GND', 'target': 'J6.1 GND'},
            {'host': 'J5.3 RX', 'target': 'J6.5 SERVICE_UART_TX'},
        ],
        'direct_cable_mating': False,
        'target_pins_unconnected_to_uart_cable': [2, 3, 4],
        'logic_voltage_v': 3.3,
        'uart_supplies_target_power': False,
        'automatic_boot_reset_control': False,
        'target_reset_supervisor': 'TPS3839G33DBZR, push-pull active-low output',
        'target_reset_series_resistance_ohms': 4700,
        'target_en_pulldown_resistance_ohms': 100000,
        'target_boot_pullup_resistance_ohms': 10000,
        'target_uart_tx_series_resistance_ohms': 1000,
        'target_ground_entire_board_connected': False,
        'target_power_paths_complete': False,
        'host_physical_copper_audited': False,
        'adapter_physical_continuity_verified': False,
        'flashed_firmware_verified': False,
        'programming_hardware_tested': False,
        'fabrication_ready': False,
    }
    (REVIEW / 'programmer-compatibility.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'host_logical_checks_passed': len(host_checks),
                      'target_logical_and_physical_checks_passed': len(target_checks),
                      'direct_cable_mating': False, 'programming_hardware_tested': False,
                      'fabrication_ready': False}, indent=2))


if __name__ == '__main__':
    main()
