"""Compare every native wire segment with source minima and net nominal widths.

Net nominal widths and explicit branch widths are reported separately: a narrow
pad escape is not automatically an error or an approved current-carrying path.
This audit never grants thermal, impedance, or fabrication approval.
"""
import argparse
import hashlib
import json
import math
import runpy
from collections import Counter, defaultdict
from pathlib import Path

MINIMUM_WIDTH_MM = .2
TOLERANCE_MM = 1e-9


def positive_width(width_mm):
    if not isinstance(width_mm, (int, float)) or not math.isfinite(width_mm) or width_mm <= 0:
        raise ValueError(f'Invalid width in mm: {width_mm!r}')
    return width_mm


def electrical_roots(circuit):
    helpers = runpy.run_path(str(Path(__file__).with_name('audit-copper.py')))
    electrical = helpers['DisjointSets']()
    source_traces = {record['source_trace_id']: record for record in circuit if record['type'] == 'source_trace'}
    for source_trace in source_traces.values():
        electrical.join(source_trace.get('connected_source_port_ids', []) + source_trace.get('connected_source_net_ids', []))
    for record in circuit:
        if record['type'] == 'source_component_internal_connection':
            electrical.join(record['source_port_ids'])
        if record['type'] == 'source_component':
            for port_ids in record.get('internally_connected_source_port_ids', []):
                electrical.join(port_ids)
    via_sources = {record['source_manually_placed_via_id']: record for record in circuit
                   if record['type'] == 'source_manually_placed_via'}
    for record in circuit:
        if record['type'] == 'source_port':
            via = via_sources.get(record.get('source_component_id'))
            if via and via.get('source_net_id'):
                electrical.join([record['source_port_id'], via['source_net_id']])
    nets_by_root = defaultdict(list)
    for record in circuit:
        if record['type'] == 'source_net':
            nets_by_root[electrical.root(record['source_net_id'])].append(record)
    return electrical, source_traces, nets_by_root


def measure_trace(pcb_trace, context):
    electrical, source_traces, nets_by_root = context
    if pcb_trace.get('route_thickness_mode') not in (None, 'constant'):
        raise ValueError(f"Unsupported thickness mode: {pcb_trace.get('route_thickness_mode')}")
    source_trace = source_traces[pcb_trace['source_trace_id']]
    terminals = source_trace.get('connected_source_port_ids', []) + source_trace.get('connected_source_net_ids', [])
    if not terminals:
        raise ValueError(f"Unassigned trace: {pcb_trace['pcb_trace_id']}")
    nets = nets_by_root.get(electrical.root(terminals[0]), [])
    if len(nets) > 1:
        raise ValueError(f"Merged named nets: {[net['name'] for net in nets]}")
    net = nets[0] if nets else None
    net_width_mm = positive_width(net['trace_width']) if net and 'trace_width' in net else None
    source_width_mm = positive_width(source_trace['min_trace_thickness']) if 'min_trace_thickness' in source_trace else None
    segments = []
    route = pcb_trace['route']
    for point in route:
        if point['route_type'] == 'wire':
            positive_width(point['width'])
        elif point['route_type'] != 'via':
            raise ValueError(f"Unsupported route point: {point['route_type']}")
    for index, (start, end) in enumerate(zip(route, route[1:])):
        length_mm = math.dist((start['x'], start['y']), (end['x'], end['y']))
        if start['route_type'] == 'via' or end['route_type'] == 'via':
            if length_mm > TOLERANCE_MM:
                raise ValueError(f"Via with displaced adjacent wire: {pcb_trace['pcb_trace_id']}:{index}")
            continue
        if start['layer'] != end['layer']:
            raise ValueError(f"Wire changes layer without via: {pcb_trace['pcb_trace_id']}:{index}")
        # Native constant-mode segments use their start-point width. Later
        # points can widen the next segment; min(endpoint widths) would hide it.
        width_mm = start['width']
        segments.append({
            'segment_index': index, 'layer': start['layer'], 'length_mm': length_mm,
            'start_mm': [start['x'], start['y']], 'end_mm': [end['x'], end['y']],
            'width_mm': width_mm,
            'below_board_minimum': width_mm + TOLERANCE_MM < MINIMUM_WIDTH_MM,
            'below_source_minimum': source_width_mm is not None and width_mm + TOLERANCE_MM < source_width_mm,
            'below_net_nominal': net_width_mm is not None and width_mm + TOLERANCE_MM < net_width_mm,
        })
    if not segments:
        raise ValueError(f"No measurable wire segments: {pcb_trace['pcb_trace_id']}")
    return {
        'pcb_trace_id': pcb_trace['pcb_trace_id'], 'source_trace_id': source_trace['source_trace_id'],
        'source_display_name': source_trace.get('display_name'), 'net': net['name'] if net else None,
        'source_minimum_mm': source_width_mm, 'net_nominal_mm': net_width_mm,
        'minimum_actual_width_mm': min(segment['width_mm'] for segment in segments),
        'maximum_actual_width_mm': max(segment['width_mm'] for segment in segments),
        'wire_length_mm': sum(segment['length_mm'] for segment in segments),
        'below_board_minimum': any(segment['below_board_minimum'] for segment in segments),
        'below_source_minimum': any(segment['below_source_minimum'] for segment in segments),
        'below_net_nominal': any(segment['below_net_nominal'] for segment in segments),
        'segments': segments,
    }


def audit(circuit):
    context = electrical_roots(circuit)
    measurements = [measure_trace(record, context) for record in circuit if record['type'] == 'pcb_trace']
    if not measurements:
        raise ValueError('No native traces to verify')
    widths = Counter(segment['width_mm'] for trace in measurements for segment in trace['segments'])
    return {
        'scope': 'Every native constant-width wire segment; physical route widths compared independently with explicit source minima, named-net nominal widths and 0.20 mm board minimum. Copper-region widths, continuity and clearances require separate geometric audits. Nominal-width discrepancies remain review items, never automatically approved pad escapes.',
        'checked_trace_count': len(measurements), 'checked_wire_segment_count': sum(widths.values()),
        'trace_count_below_board_minimum': sum(trace['below_board_minimum'] for trace in measurements),
        'trace_count_below_source_minimum': sum(trace['below_source_minimum'] for trace in measurements),
        'trace_count_below_net_nominal': sum(trace['below_net_nominal'] for trace in measurements),
        'wire_segment_width_histogram': {str(width): count for width, count in sorted(widths.items())},
        'current_capacity_qualified': False, 'impedance_qualified': False,
        'fabrication_ready': False, 'measurements': measurements,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit_json')
    parser.add_argument('output_json')
    args = parser.parse_args()
    native_path = Path(args.circuit_json)
    native_bytes = native_path.read_bytes()
    result = {'source_circuit_json': str(native_path), 'source_sha256': hashlib.sha256(native_bytes).hexdigest(),
              **audit(json.loads(native_bytes))}
    Path(args.output_json).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: record for key, record in result.items() if key != 'measurements'}))
    return int(any(result[key] for key in (
        'trace_count_below_board_minimum', 'trace_count_below_source_minimum', 'trace_count_below_net_nominal')))


if __name__ == '__main__':
    raise SystemExit(main())
