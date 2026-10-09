"""Qualify local TPS63802 pad escapes independently of the wide switch trunks.

Native points are board-world mm: +X right, +Y top, with full-span vias only.
The resistance calculation uses copper at 125 C, 1 oz finished outer copper,
and the manufacturer's 5.75 A upper peak limit as a conservative DC bound.
End temperatures and complete board thermal performance require separate review.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path


def audit(native):
    source = {e['source_trace_id']: e for e in native if e['type'] == 'source_trace'}
    records = []
    for trace in native:
        if trace['type'] != 'pcb_trace' or source[trace['source_trace_id']].get('name') not in ['REG_L1', 'REG_L2']:
            continue
        segments = []
        for start, end in zip(trace['route'], trace['route'][1:]):
            assert start['route_type'] == end['route_type'] == 'wire'
            assert start['layer'] == end['layer'] == 'top'
            length = math.hypot(end['x'] - start['x'], end['y'] - start['y'])
            assert start['width'] >= .275
            resistance = 2.437e-8 * (length / 1000) / ((start['width'] / 1000) * .000035)
            segments.append({'length_mm': length, 'width_mm': start['width'], 'resistance_at_125_c_ohms': resistance})
        pad_escape_length = sum(s['length_mm'] for s in segments if s['width_mm'] < .4)
        trunk_length = sum(s['length_mm'] for s in segments if s['width_mm'] >= 1)
        assert pad_escape_length <= .751 and trunk_length >= 1
        resistance = sum(s['resistance_at_125_c_ohms'] for s in segments)
        records.append({'name': source[trace['source_trace_id']]['name'], 'segments': segments,
                        'pad_escape_length_mm': pad_escape_length, 'trunk_length_mm': trunk_length,
                        'peak_current_dc_bound_amps': 5.75, 'required_finished_outer_copper_mm': .035,
                        'voltage_drop_at_peak_bound_v': resistance * 5.75,
                        'dissipation_at_peak_dc_bound_w': resistance * 5.75 ** 2,
                        'local_width_profile_passes': True,
                        'full_board_thermal_qualification': False})
    assert {r['name'] for r in records} == {'REG_L1', 'REG_L2'}
    return records


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('native')
    parser.add_argument('output')
    args = parser.parse_args()
    payload = Path(args.native).read_bytes()
    result = {'source_sha256': hashlib.sha256(payload).hexdigest(), 'routes': audit(json.loads(payload)),
              'fabrication_ready': False, 'manufacturer_reference': 'TPS63802 SLVSEU9D electrical table and section 12'}
    Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
