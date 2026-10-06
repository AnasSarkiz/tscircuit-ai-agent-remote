"""Verify authored strip widths against native copper, excluding drilled apertures."""
import argparse
import hashlib
import json
import runpy
from collections import defaultdict
from pathlib import Path

from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union


def measure_regions(circuit, regions):
    helpers = runpy.run_path(str(Path(__file__).with_name('audit-copper.py')))
    nets = {record['name']: record['source_net_id'] for record in circuit if record['type'] == 'source_net'}
    electrical = helpers['DisjointSets']()
    sources = {r['source_trace_id']: r for r in circuit if r['type'] == 'source_trace'}
    traces = {r['pcb_trace_id']: r for r in circuit if r['type'] == 'pcb_trace'}
    for source in sources.values():
        electrical.join(source.get('connected_source_port_ids', []) + source.get('connected_source_net_ids', []))
    for record in circuit:
        if record['type'] == 'source_component_internal_connection':
            electrical.join(record['source_port_ids'])
    native_regions = defaultdict(list)
    for record in circuit:
        if record['type'] == 'pcb_via':
            source_net = record.get('source_net_id')
            if source_net is None:
                source_id = record.get('source_trace_id') or traces[record['pcb_trace_id']]['source_trace_id']
                source = sources[source_id]
                source_net = (source.get('connected_source_port_ids', []) + source.get('connected_source_net_ids', []))[0]
            # A real plated land also carries copper at a pour termination.
            # Include only this electrically assigned native land on its actual
            # layers; its drilled aperture is still removed below. Foreign vias
            # and an undersized land cannot satisfy a missing required strip.
            land = Point(record['x'], record['y']).buffer(record['outer_diameter']/2, quad_segs=128)
            for layer in record['layers']:
                native_regions[(electrical.root(source_net), layer)].append(land)
            continue
        if record['type'] != 'pcb_copper_pour':
            continue
        if record['shape'] != 'brep':
            raise ValueError(f"Unsupported native pour: {record['shape']}")
        brep = record['brep_shape']
        native_regions[(electrical.root(record['source_net_id']), record['layer'])].append(Polygon(
            [(p['x'], p['y']) for p in brep['outer_ring']['vertices']],
            [[(p['x'], p['y']) for p in ring['vertices']] for ring in brep['inner_rings']]))
    copper = {key: unary_union(shapes) for key, shapes in native_regions.items()}
    drills = unary_union([helpers['drill_contour'](record) for record in circuit
                          if record['type'] in ('pcb_via', 'pcb_hole', 'pcb_plated_hole')])
    measurements = []
    for index, region in enumerate(regions):
        if 'path_mm' not in region:
            raise ValueError(f'Missing source centerline for region {index}')
        # Micrometre-scale geometric precision is recorded, not a relaxed
        # fabrication clearance. Actual minimum required widths remain intact.
        required = LineString(region['path_mm']).buffer(region['nominal_width_mm']/2,
                                                       quad_segs=64, cap_style=2).difference(drills)
        actual = copper.get((electrical.root(nets[region['net']]), region['layer']), Polygon())
        uncovered = required.difference(actual.buffer(0.000001))
        measurements.append({'source_region_index': index, 'net': region['net'],
            'layer': region['layer'], 'required_width_mm': region['nominal_width_mm'],
            'uncovered_required_copper_mm2': uncovered.area,
            'uncovered_required_copper_bounds_mm': list(uncovered.bounds) if not uncovered.is_empty else None,
            'required_width_preserved': uncovered.area <= 1e-8})
    return measurements


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit_json')
    parser.add_argument('region_source')
    parser.add_argument('output_json')
    args = parser.parse_args()
    native_path = Path(args.circuit_json)
    circuit = json.loads(native_path.read_text())
    regions = json.loads(Path(args.region_source).read_text())['pours']
    measurements = measure_regions(circuit, regions)
    result = {'source_circuit_json': str(native_path),
        'source_sha256': hashlib.sha256(native_path.read_bytes()).hexdigest(),
        'region_source': args.region_source,
        'scope': 'Required nominal-width buffered source centerlines with flat termination caps covered by actual same-net native BREP copper and actual plated via lands on their native layers; actual drilled apertures excluded; 0.000001 mm geometric tolerance.',
        'audit_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'checked_region_count': len(measurements),
        'failed_region_count': sum(not record['required_width_preserved'] for record in measurements),
        'measurements': measurements}
    Path(args.output_json).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: record for key, record in result.items() if key != 'measurements'}))
    return 1 if result['failed_region_count'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
