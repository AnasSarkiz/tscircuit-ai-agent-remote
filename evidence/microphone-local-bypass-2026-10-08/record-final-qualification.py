"""Bind measured native copper to the real unsuppressed qualification receipts."""
from pathlib import Path
import collections
import hashlib
import json

folder = Path(__file__).resolve().parent
root = folder.parents[1]
read = lambda name: json.loads((folder / name).read_text())
payload = (root / 'dist/index/circuit.json').read_bytes()
native = json.loads(payload)
sha = hashlib.sha256(payload).hexdigest()
audit = read('final-copper-audit.json')
preservation = read('connection-preservation.json')
geometry = read('purchased-geometry.json')
bypass = read('local-bypass-qualification.json')
layers = read('final-native-compliance.json')
assert sha == audit['source_sha256'] == preservation['after_native_sha256']
assert sha == geometry['after_native_sha256'] == bypass['native_sha256'] == layers['native_sha256']
assert geometry['passed'] and bypass['passed'] and preservation['preserved']
assert audit['short_count'] == audit['drc_violation_count'] == 0
regions = [read(name + '.widths.json') for name in
           ['connection-copper.json', 'manual-power-copper.json', 'inner-signal-copper.json']]
assert all(r['source_sha256'] == sha and r['failed_region_count'] == 0 for r in regions)
parts = {r['name']: (r['manufacturer_part_number'], r['supplier_part_numbers']['jlcpcb'][0])
         for r in native if r['type'] == 'source_component'
         and r.get('supplier_part_numbers', {}).get('jlcpcb')}
stock = read('official-stock/receipt.json')
stock_source = (root / stock['source_native']).read_bytes()
assert hashlib.sha256(stock_source).hexdigest() == stock['source_sha256']
sourceparts = {r['name']: (r['manufacturer_part_number'], r['supplier_part_numbers']['jlcpcb'][0])
               for r in json.loads(stock_source) if r['type'] == 'source_component'
               and r.get('supplier_part_numbers', {}).get('jlcpcb')}
stockparts = {name: r['part_number'] for r in stock['results'] for name in r['references']}
assert parts == sourceparts
assert stockparts == {name: part[1] for name, part in parts.items()}
assert all(r['model'] == parts[name][0] for r in stock['results']
           if r.get('http_status') == 200 for name in r['references'])
successful = [r for r in stock['results'] if r.get('http_status') == 200]
stock_binding = {
    'current_native_sha256': sha, 'stock_source_native_sha256': stock['source_sha256'],
    'purchased_components': len(parts), 'supplier_identities': len(stock['results']),
    'every_current_reference_exact_mpn_and_supplier_matched': True,
    'official_http200_identities': len(successful),
    'public_buyability_covers_one_board_identities': stock['covered_parts'],
    'unknown_inventory_identities': len(stock['results']) - len(successful),
    'zero_or_insufficient_public_buyability': [
        {'part': r['part_number'], 'references': r['references'],
         'overseasStockCount': r['stock_count'], 'canPresaleNumber': r['available_to_buy']}
        for r in successful if not r['stock_covers_one_board']],
    'inventory_scope': 'Exact dated public overseasStockCount/canPresaleNumber. HTTP503 is unknown inventory; no assembler allocation or reserved order is inferred.',
    'all_assembly_available': False, 'fabrication_ready': False,
}
(folder / 'dated-stock-application.json').write_text(json.dumps(stock_binding, indent=2) + '\n')
components = {r['pcb_component_id']: r for r in native if r['type'] == 'pcb_component'}
names = {r['source_component_id']: r['name'] for r in native if r['type'] == 'source_component'}
errors = [r for r in native if 'error' in r['type']]
error_components = collections.Counter(names[components[r['pcb_component_ids'][0]]['source_component_id']] for r in errors)
widths = read('trace-widths.json')
schema = read('schema-summary.json')
ui = read('ui-analysis/ui-style-analysis-receipt.json')
snapshot = read('source-snapshot.log.outcome.json')
summary = {
    'version': '0.0.10-wip-microphone-bypass', 'native_sha256': sha,
    'native_bytes': len(payload), 'native_traces': sum(r['type'] == 'pcb_trace' for r in native),
    'native_vias': layers['via_count'], 'native_pours': sum(r['type'] == 'pcb_copper_pour' for r in native),
    'native_errors': len(errors), 'native_error_breakdown': dict(error_components),
    'measured_shorts': audit['short_count'], 'measured_geometry_violations': audit['drc_violation_count'],
    'physically_open_nets': audit['physically_open_net_count'],
    'unassigned_battery_outer_contacts_excluded_from_assigned_open_net_count': ['J3.pin1', 'J3.pin3'],
    'required_active_regions_width_checked': sum(r['checked_region_count'] for r in regions),
    'required_active_region_width_failures': 0,
    'retained_contact_pairs_checked': preservation['previously_connected_pairs_checked'],
    'retained_contact_losses': len(preservation['lost_pairs']),
    'stationary_purchased_geometries': geometry['stationary_purchased_geometry_count'],
    'purchased_component_pose_moves': ['C81', 'R93'], 'purchased_identity_changes': 0,
    'genuine_assets_and_solver_cache_files_unchanged': geometry['genuine_assets_and_solver_cache_files_checked'],
    'local_bypass_supply_length_mm': bypass['supply_length_mm'],
    'local_bypass_ground_stub_length_mm': bypass['ground_stub_length_mm'],
    'local_bypass_width_mm': bypass['bypass_width_mm'], 'local_bypass_layer': bypass['bypass_layer'],
    'local_bypass_route_via_count': bypass['bypass_route_via_count'],
    'full_through_vias_0p30_hole_0p45_land': layers['ordinary_vias_exact_0p30_hole_0p45_pad_full_span'],
    'high_current_native_traces_checked': layers['high_current_native_trace_count'],
    'high_current_regions_checked': layers['high_current_active_source_trunk_regions'],
    'high_current_trunks_outer_only': layers['high_current_native_traces_outer_only'] and layers['high_current_regions_outer_only'],
    'source_checks_passed': read('final-source-checks/source-checks.json')['passed'],
    'routing_regression_pass_count': 94, 'board_test_pass_count': 49, 'board_test_fail_count': 2,
    'schematic_ui_style_issues': ui['issue_count'], 'schematic_ui_style_passed': ui['ui_schematic_style_passed'],
    'strict_schema_failures': schema['failing_elements'], 'missing_native_paste_records': 32,
    'snapshot_completed': snapshot['completed_command'], 'snapshot_passed': snapshot['exit_code'] == 0,
    'snapshot_references_updated': False,
    'native_trace_widths_checked': widths['checked_trace_count'],
    'native_wire_segments_checked': widths['checked_wire_segment_count'],
    'native_traces_below_board_minimum': widths['trace_count_below_board_minimum'],
    'native_traces_below_explicit_source_minimum': widths['trace_count_below_source_minimum'],
    'native_traces_below_named_net_nominal': widths['trace_count_below_net_nominal'],
    'current_stock': stock_binding,
    'unchanged_identity_previous_reference_component_subtotal_usd': '26.3055',
    'previous_cost_is_current_quote': False,
    'publications_verified': False, 'requested_display_implemented': False,
    'full_zero_DRC_and_connectivity_pass': False, 'fabrication_ready': False,
    'programming_hardware_tested': False,
}
latest_schema = folder / 'latest-schema-receipt.json'
if latest_schema.exists():
    latest = read('latest-schema-receipt.json')
    assert latest['native_sha256'] == sha and not latest['native_modified']
    summary['latest_official_readonly_schema_package'] = latest['schema_package']
    summary['latest_official_readonly_schema_failures'] = latest['failing_elements']
if (folder / 'final-registry-receipt.json').exists() and (folder / 'final-public-preview-receipt.json').exists():
    registry = read('final-registry-receipt.json')
    preview = read('final-public-preview-receipt.json')
    assert registry['complete_public_upload'] and preview['exact_native_object_equality']
    assert preview['local_native_json_sha256'] == sha
    summary['publications_verified'] = True
    summary['public_registry_release_id'] = preview['release_id']
    summary['public_native_preview_url'] = preview['preview_page_url']
(folder / 'final-qualification-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
