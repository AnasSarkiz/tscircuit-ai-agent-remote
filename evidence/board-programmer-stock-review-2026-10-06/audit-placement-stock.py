"""Measure native bypass placements and retain exact dated supplier evidence.

No numeric distance rule, current stock, or hardware success is inferred.
"""
import csv
import datetime
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REVIEW = Path(__file__).resolve().parent
PRIOR = ROOT / 'evidence/order-readiness-2026-10-06'


def read_json(path):
    return json.loads(path.read_text())


def capacitor_distance(context, row):
    capacitor = context['ports'][row['pcb_port_id']]
    supply = context['supply']
    ground = context['pins'][(row['reference'], 2)]
    return {
        'capacitor': row['reference'],
        'capacitance_f': context['components'][row['reference']]['capacitance'],
        'supply_pin_center_mm': {'x': capacitor['x'], 'y': capacitor['y']},
        'supply_pin_center_distance_mm': math.hypot(capacitor['x'] - supply['x'],
                                                   capacitor['y'] - supply['y']),
        'same_supply_copper_island': bool(set(row['physical_island_ids']) &
                                         set(context['supply_pin']['physical_island_ids'])),
        'native_cap_supply_error': row['native_port_error'],
        'ground_island_ids': ground['physical_island_ids'],
    }


def measure_decoupling(context):
    supplies = [
        ('U1', 2, 'V3V3', ['C30', 'C31', 'C32']),
        ('U12', 3, 'V3V3', []),
        ('U2', 10, 'VSYS', ['C4']), ('U2', 6, 'V3V3', ['C5']),
        ('U13', 1, 'V3V3', ['C40']), ('U13', 5, 'VLCD', ['C41']),
        ('U14', 20, 'VLCD', ['C42', 'C43']),
        ('U3', 2, 'VSYS', ['C50', 'C51']),
        ('U3', 7, 'VSYS', ['C50', 'C51']),
        ('U3', 8, 'VSYS', ['C50', 'C51']),
        ('U22', 1, 'VSYS', ['C70']), ('U22', 5, 'VMOTOR', ['C71']),
        ('U23', 1, 'MIC_INPUT', ['C73']), ('U23', 5, 'VMIC', ['C74', 'C75']),
        ('U24', 5, 'VMIC', []),
        ('U4', 5, 'VMIC', ['C80']), ('U5', 5, 'VMIC', ['C81']),
        ('U7', 5, 'V3V3', ['C25']), ('U26', 5, 'V3V3', ['C78']),
    ]
    measurements = []
    for reference, pin_number, net, assigned in supplies:
        supply_pin = context['pins'][(reference, pin_number)]
        assert supply_pin['named_nets'] == [net], (reference, pin_number, supply_pin)
        supply = context['ports'][supply_pin['pcb_port_id']]
        measurement_context = {**context, 'supply': supply, 'supply_pin': supply_pin}
        capacitors = []
        for row in context['pins'].values():
            if not row['reference'].startswith('C') or row['pin_number'] != 1:
                continue
            if row['named_nets'] != [net]:
                continue
            ground = context['pins'][(row['reference'], 2)]
            if ground['named_nets'] != ['GND']:
                continue
            capacitors.append(capacitor_distance(measurement_context, row))
        capacitors.sort(key=lambda row: row['supply_pin_center_distance_mm'])
        assert capacitors, (reference, pin_number)
        assigned_rows = [row for row in capacitors if row['capacitor'] in assigned]
        assert len(assigned_rows) == len(assigned), (reference, assigned)
        measurements.append({
            'reference': reference, 'pin': pin_number, 'net': net,
            'ic_supply_pin_center_mm': {'x': supply['x'], 'y': supply['y']},
            'nearest_same_rail_bypass': capacitors[0],
            'assigned_bypass_measurements': assigned_rows,
            'scope': 'Euclidean native port-centre distance; not routed length, loop inductance or a datasheet maximum-distance rule.',
        })
    (REVIEW / 'decoupling-placement.json').write_text(json.dumps({
        'target_native_sha256': context['sha256'],
        'measurements': measurements,
        'placement_electrical_qualification': 'blocked',
        'scope': 'Current assigned capacitors and nearest same-rail capacitor with GND return. No invented pass threshold.',
    }, indent=2) + '\n')
    return measurements


def retain_stock(context):
    historical_path = ROOT / 'evidence/layout-bom-audit-2026-10-04/supplier-receipt.json'
    historical = read_json(historical_path)
    old = {row['jlc']: row for row in historical['records']}
    quantities = read_json(PRIOR / 'component-summary.json')['supplier_quantities']
    rows = []
    for part, references in sorted(quantities.items()):
        matching = old.get(part, {}).get('exact_results', [])
        receipt = historical_path
        checked_at = historical['checked_at_utc']
        if part == 'C22775':
            receipt = ROOT / 'evidence/a6-bom-routing-2026-10-04/C22775-current-stock.json'
            matching = read_json(receipt)['results']
            checked_at = '2026-10-04 (A6 saved lookup; exact UTC timestamp unavailable)'
        exact = [row for row in matching if 'C' + str(row['lcsc']) == part]
        assert len(exact) == 1, part
        listing = exact[0]
        rows.append({
            'jlcpcb_part': part, 'references': references,
            'required_per_board': len(references),
            'native_mpns': sorted({context['components'][ref]['manufacturer_part_number']
                                   for ref in references}),
            'historical_listing_mpn': listing['mfr'],
            'historical_stock': listing.get('stock'),
            'historical_checked_at': checked_at,
            'historical_receipt': str(receipt.relative_to(ROOT)),
            'current_stock': None,
            'current_availability_status': 'UNVERIFIED_PROXY_ACCESS_BLOCKED',
            'historical_covers_one_board_before_assembly_loss': listing.get('stock', 0) >= len(references),
            'historical_stock_covers_less_than_two_boards': listing.get('stock', 0) < 2 * len(references),
        })
    assert len(rows) == 43 and sum(row['required_per_board'] for row in rows) == 125
    (REVIEW / 'stock-audit.json').write_text(json.dumps({
        'manifest_created_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'target_native_sha256': context['sha256'], 'identity_count': 43,
        'purchased_count': 125, 'fresh_stock_verified_count': 0,
        'lookup_probe': 'supplier-http-receipt.json', 'parts': rows,
        'stock_reserved': False,
        'notes': [
            'Historical listings are not current stock or assembly reservations.',
            'Exact part identities remain; blocked access is not zero stock.',
            'Batch size, assembly allowance, minimum quantity, stock origin and actual JLC order feedback need qualification.',
            'External display, battery, speaker and motor are not PCB assembly parts.',
        ],
    }, indent=2) + '\n')
    fields = ['jlcpcb_part', 'references', 'required_per_board', 'native_mpns',
              'historical_stock', 'historical_checked_at', 'current_stock',
              'current_availability_status']
    with (REVIEW / 'stock-audit.csv').open('w', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: ', '.join(row[key]) if isinstance(row[key], list) else row[key]
                             for key in fields})
    return rows


def main():
    native_path = ROOT / 'dist/index/circuit.json'
    native = read_json(native_path)
    sha256 = hashlib.sha256(native_path.read_bytes()).hexdigest()
    assert sha256 == read_json(PRIOR / 'component-summary.json')['source_sha256']
    context = {
        'sha256': sha256,
        'components': {row['name']: row for row in native if row['type'] == 'source_component'},
        'ports': {row['pcb_port_id']: row for row in native if row['type'] == 'pcb_port'},
        'pins': {(row['reference'], row['pin_number']): row
                 for row in read_json(PRIOR / 'pin-assignments.json')},
    }
    measurements = measure_decoupling(context)
    stocks = retain_stock(context)
    print(json.dumps({
        'supply_positions_measured': len(measurements), 'stock_identities': len(stocks),
        'historical_low_margin_parts': [row['jlcpcb_part'] for row in stocks
                                       if row['historical_stock_covers_less_than_two_boards']],
        'fresh_stock_verified': False, 'placement_electrical_qualification': 'blocked',
    }, indent=2))


if __name__ == '__main__':
    main()
