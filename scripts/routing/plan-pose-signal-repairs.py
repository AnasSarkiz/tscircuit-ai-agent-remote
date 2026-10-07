"""Repair real signal copper affected by the speaker placement change.

Original native output and Pipeline9 files remain immutable. Retire two exact
native paths, retain their measured terminal escapes, and author inner copper.
All proposals require a new native build and connection-preservation audit.
"""
import argparse
import hashlib
import json
import runpy
from pathlib import Path

from shapely.geometry import LineString, Point, Polygon

bridges = runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')))
helpers = bridges['helpers']
geometry = runpy.run_path(str(Path(__file__).with_name('audit-copper.py')))


def reserve_regions(planner, regions):
    nets = {record['name']: record for record in planner.circuit if record['type'] == 'source_net'}
    for region in regions:
        planner.copper.append((planner.root(nets[region['net']]['source_net_id']), region['layer'],
                               Polygon([(point['x'], point['y']) for point in region['outline']])))


def retained_escapes(planner, specification):
    trace, net = specification['trace'], specification['net']
    indices = [index for index, point in enumerate(trace['route']) if point['route_type'] == 'via']
    if len(indices) != 2:
        raise ValueError('Measured terminal escapes require exactly two original vias')
    paths, positions = [], []
    for endpoint, points in ((trace['route'][0], trace['route'][:indices[0]+1]),
                            (trace['route'][-1], list(reversed(trace['route'][indices[-1]:])))):
        identifier = endpoint.get('start_pcb_port_id') or endpoint.get('end_pcb_port_id')
        port = planner.ports[identifier]
        if planner.root(port['source_port_id']) != planner.root(net['source_net_id']):
            raise ValueError('Unexpected numbered terminal net')
        if any(point['route_type'] == 'wire' and (point['layer'] != 'top' or point['width'] != .2)
               for point in points):
            raise ValueError('Terminal escapes must retain the actual top-layer width')
        coordinates = []
        for point in points:
            xy = (point['x'], point['y'])
            if not coordinates or coordinates[-1] != xy:
                coordinates.append(xy)
        paths.append(helpers['escape_record'](planner, {
            'port': port, 'net': net, 'root': planner.root(net['source_net_id']),
            'width': .2, 'positions': coordinates, 'via_outer_mm': .45, 'via_hole_mm': .3}))
        positions.append(coordinates[-1])
    if [path['from'] for path in paths] != specification['expected_selectors']:
        raise ValueError('The preserved terminal identities changed')
    return paths, positions


def connect(planner, specification):
    root = planner.root(specification['net']['source_net_id'])
    route = helpers['wide_multilayer_route'](planner, {
        'root': root, 'first': specification['positions'][0], 'last': specification['positions'][1],
        'width': .202, 'new_vias': specification['positions'], 'layers': ('inner2', 'inner1'),
        'via_outer_mm': .45, 'via_hole_mm': .3, 'copper_clearance_mm': .27})
    if route is None:
        return None
    parts, positions = route
    regions = bridges['region_records'](specification['net']['name'], {'parts': parts, 'width': .2})
    reserve_regions(planner, regions)
    vias = []
    for xy in positions:
        bridges['reserve_via'](planner, {'root': root, 'position': xy})
        vias.append({'net': specification['net']['name'], 'x': xy[0], 'y': xy[1],
                     'hole_mm': .3, 'outer_mm': .45})
    return {'pours': regions, 'vias': vias}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('native', type=Path)
    parser.add_argument('speaker_proposal', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    circuit = json.loads(args.native.read_text())
    speaker = json.loads(args.speaker_proposal.read_text())
    if hashlib.sha256(args.native.read_bytes()).hexdigest() != speaker['native_sha256']:
        raise ValueError('Speaker proposal belongs to another native output')
    ids = ('saved_phase_null_18_0', 'saved_phase_null_22_0')
    traces = {identifier: next(record for record in circuit if record.get('pcb_trace_id') == identifier)
              for identifier in ids}
    retired_vias = {record['pcb_via_id'] for record in circuit if record['type'] == 'pcb_via'
                    and record.get('pcb_trace_id') in ids}
    retired_vias.add(speaker['clock_relocation']['original_native_via_id'])
    retired_vias.update(record['pcb_via_id'] for record in circuit if record['type'] == 'pcb_via'
                       and record.get('pcb_trace_id') == next(
                           path['pcb_trace_id'] for path in circuit if path['type'] == 'pcb_trace'
                           and path.get('source_trace_id') == next(
                               source['source_trace_id'] for source in circuit if source['type'] == 'source_trace'
                               and source.get('name') == 'CONNECTION_ESCAPE_SPEAKER_P_49')))
    planner = helpers['Planner'](circuit, {
        'relocated_trace_layers': {identifier: {layer: None for layer in ('top', 'bottom', 'inner1', 'inner2')}
                                  for identifier in ids}, 'retired_feature_ids': retired_vias})
    planner.set_grid(.05)
    planner.via_copper_clearance = .27
    nets = {record['name']: record for record in circuit if record['type'] == 'source_net'}
    pair_roots = {planner.root(nets[name]['source_net_id']) for name in ('SPEAKER_P', 'SPEAKER_N')}
    pair_holes = {geometry['drill_contour'](record).wkb for record in circuit
                  if record['type'] == 'pcb_via' and planner.via_root(record) in pair_roots}
    planner.holes = [hole for hole in planner.holes if hole.wkb not in pair_holes]
    source = json.loads(Path('src/board/connection-copper.json').read_text())
    clock_root = planner.root(nets['AMP_LRCLK']['source_net_id'])
    clock_shapes = [Polygon([(point['x'], point['y']) for point in source['pours'][index]['outline']])
                    for index in (44, 47)]
    planner.copper = [(root, layer, shape) for root, layer, shape in planner.copper
                      if root not in pair_roots and not (root == clock_root and layer == 'inner2'
                      and any(shape.difference(original.buffer(1e-6)).area <= 1e-8 for original in clock_shapes))]
    planner.reserve_proposals(speaker['clock_relocation'])
    reserve_regions(planner, speaker['clock_relocation']['pours'])
    for net, lane in speaker['bundle']['lanes'].items():
        root = planner.root(nets[net]['source_net_id'])
        planner.copper.append((root, 'top', LineString(lane['neck_mm']).buffer(.275/2)))
        planner.copper.extend((root, layer, LineString(points).buffer(.6/2))
                              for layer, points in lane['parts_mm'])
        planner.copper.append((root, lane['parts_mm'][-1][0], LineString(lane['finish_mm']).buffer(.6/2)))
    result = {'classification': 'Authored real signal replacements; native qualification pending',
              'source_native_sha256': speaker['native_sha256'], 'paths': [], 'pours': [], 'vias': [],
              'retired_native_vias': sorted(retired_vias), 'retired_replay_connections': [], 'unresolved': []}
    specifications = [
        {'trace': traces[ids[0]], 'net': nets['MCU_AUDIO_BCLK'], 'expected_selectors': ['.U1 > .pin17', '.R66 > .pin1'],
         'phase_index': 18, 'cache_file': 'routes/a7/mcu-amplifier-bclk.json', 'cache_index': 0},
        {'trace': traces[ids[1]], 'net': nets['SERVICE_UART_TX'], 'expected_selectors': ['.R38 > .pin2', '.J6 > .pin5'],
         'phase_index': 22, 'cache_file': 'routes/a7/service-uart.json', 'cache_index': 0},
    ]
    for specification in specifications:
        paths, positions = retained_escapes(planner, specification)
        proposal = connect(planner, {'net': specification['net'], 'positions': positions})
        if proposal is None:
            result['unresolved'].append({'net': specification['net']['name'], 'reason': 'No qualified complete inner connection'})
        else:
            result['paths'].extend(paths)
            for key in ('pours', 'vias'):
                result[key].extend(proposal[key])
            cache = json.loads(Path(specification['cache_file']).read_text())
            result['retired_replay_connections'].append({
                'phase_index': specification['phase_index'],
                'connection': cache[specification['cache_index']]['connection'],
                'original_pcb_trace_id': specification['trace']['pcb_trace_id']})
        print(json.dumps({'net': specification['net']['name'], 'qualified': proposal is not None}), flush=True)
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    proposal = connect(planner, {'net': nets['AMP_BCLK'], 'positions': [(-19.2, 2.752097), (-13.65, 9.4)]})
    if proposal is None:
        result['unresolved'].append({'net': 'AMP_BCLK', 'reason': 'New amplifier escape is not connected to the retained clock network'})
    else:
        for key in ('pours', 'vias'):
            result[key].extend(proposal[key])
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'complete': not result['unresolved'], 'paths': len(result['paths']),
                      'regions': len(result['pours']), 'vias': len(result['vias'])}))
    return 1 if result['unresolved'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
