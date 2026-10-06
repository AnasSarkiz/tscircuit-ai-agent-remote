"""Inventory current real parts, pin assignments, physical islands and paste."""
import csv
import hashlib
import json
import runpy
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FOLDER = Path(__file__).resolve().parent
NATIVE = FOLDER / 'native-build/circuit.json'


def main():
    native_bytes = NATIVE.read_bytes()
    circuit = json.loads(native_bytes)
    copper_audit = json.loads((FOLDER / 'copper-audit.json').read_text())
    if copper_audit['source_sha256'] != hashlib.sha256(native_bytes).hexdigest():
        raise ValueError('Copper audit does not match native input')
    helpers = runpy.run_path(str(ROOT / 'scripts/routing/audit-trace-widths.py'))
    electrical, _, nets_by_root = helpers['electrical_roots'](circuit)
    pcb_components = {record['source_component_id']: record for record in circuit
                      if record['type'] == 'pcb_component'}
    pcb_ports = {record['source_port_id']: record for record in circuit if record['type'] == 'pcb_port'}
    source_ports = defaultdict(list)
    for record in circuit:
        if record['type'] == 'source_port':
            source_ports[record['source_component_id']].append(record)
    pads = defaultdict(list)
    for record in circuit:
        if record['type'] in ('pcb_smtpad', 'pcb_plated_hole'):
            pads[record['pcb_component_id']].append(record)
    pasted = {record['pcb_smtpad_id'] for record in circuit
              if record['type'] == 'pcb_solder_paste' and record.get('pcb_smtpad_id')}
    error_ports = {port_id for record in circuit if record['type'].endswith('_error')
                   for port_id in record.get('pcb_port_ids', [])}
    open_names = {record['net'] for record in copper_audit['physically_open_nets']}
    inventory, pin_assignments = [], []
    parts = defaultdict(list)
    for source_component in circuit:
        if source_component['type'] != 'source_component':
            continue
        reference = source_component['name']
        pcb_component = pcb_components[source_component['source_component_id']]
        native_feature = source_component['ftype'] == 'simple_test_point'
        jlc_codes = source_component.get('supplier_part_numbers', {}).get('jlcpcb', [])
        if not native_feature and len(jlc_codes) != 1:
            raise ValueError(f'Missing exact purchased supplier identity: {reference}')
        if jlc_codes:
            parts[jlc_codes[0]].append(reference)
        smt_pads = [pad for pad in pads[pcb_component['pcb_component_id']] if pad['type'] == 'pcb_smtpad']
        missing_paste = [pad for pad in smt_pads if not pad.get('is_covered_with_solder_mask')
                         and pad['pcb_smtpad_id'] not in pasted and not native_feature]
        inventory.append({
            'reference': reference, 'mpn': source_component.get('manufacturer_part_number'),
            'jlc': jlc_codes, 'native_feature': native_feature,
            'layer': pcb_component['layer'], 'rotation_degrees': pcb_component['rotation'],
            'center_mm': pcb_component['center'],
            'smt_pad_count': len(smt_pads),
            'pads_without_native_paste': [{'id': pad['pcb_smtpad_id'], 'shape': pad['shape'],
                                         'pin_hints': pad.get('port_hints', [])} for pad in missing_paste],
        })
        for source_port in source_ports[source_component['source_component_id']]:
            pcb_port = pcb_ports[source_port['source_port_id']]
            nets = nets_by_root.get(electrical.root(source_port['source_port_id']), [])
            names = [net['name'] for net in nets]
            pin_assignments.append({
                'reference': reference, 'pin_number': source_port.get('pin_number'),
                'source_port_name': source_port['name'], 'port_hints': source_port.get('port_hints', []),
                'named_nets': names, 'pcb_port_id': pcb_port['pcb_port_id'],
                'physical_island_ids': copper_audit['physical_port_groups'][pcb_port['pcb_port_id']],
                'net_has_missing_physical_connections': bool(open_names.intersection(names)),
                'native_port_error': pcb_port['pcb_port_id'] in error_ports,
            })
    (FOLDER / 'component-inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')
    (FOLDER / 'pin-assignments.json').write_text(json.dumps(pin_assignments, indent=2) + '\n')
    with (FOLDER / 'pin-assignments.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(pin_assignments[0]))
        writer.writeheader()
        for pin in pin_assignments:
            writer.writerow({key: ';'.join(map(str, entry)) if isinstance(entry, list) else entry
                             for key, entry in pin.items()})
    summary = {
        'source_sha256': hashlib.sha256(native_bytes).hexdigest(),
        'physical_component_count': len(inventory),
        'purchased_component_count': sum(not part['native_feature'] for part in inventory),
        'native_pad_count': sum(part['native_feature'] for part in inventory),
        'supplier_identity_count': len(parts), 'supplier_quantities': dict(sorted(parts.items())),
        'pins_in_current_assignment_inventory': len(pin_assignments),
        'purchased_pads_without_native_paste': sum(len(part['pads_without_native_paste']) for part in inventory),
        'paste_blocked_components': [part['reference'] for part in inventory if part['pads_without_native_paste']],
        'all_components_on_top': all(part['layer'] == 'top' for part in inventory),
        'fresh_supplier_stock_checked': False,
        'scope': 'Exact native purchased-part identities, current pin-to-net table, physical island membership and paste coverage. Island IDs are within this audit only; open-net flags do not identify a correct/main island. No complete datasheet, orientation, stock, stencil or assembly approval inferred.',
        'fabrication_ready': False,
    }
    (FOLDER / 'component-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({key: entry for key, entry in summary.items() if key != 'supplier_quantities'}))


if __name__ == '__main__':
    main()
