"""Author an ordinary outer-layer speaker trace with a full nominal-width trunk.

The pad neck retains the explicit five-mm limit. This plan is not an autorouter
cache, and requires a fresh native build and preservation/clearance checks.
"""
import argparse
import json
import math
import runpy
from pathlib import Path
from shapely.geometry import LineString

helpers = runpy.run_path(str(Path(__file__).with_name('plan-power-copper.py')))


def trunk_path(specification):
    start = specification['start']
    parts = specification['parts']
    local_points = []
    global_points = []
    segment_layers = []
    for index, (layer, positions) in enumerate(parts):
        if index:
            x_mm, y_mm = positions[0]
            local_points.append({'x': round(x_mm-start[0], 6), 'y': round(y_mm-start[1], 6),
                                 'via': True, 'fromLayer': parts[index-1][0], 'toLayer': layer})
        for point_index, (x_mm, y_mm) in enumerate(positions):
            if index or point_index:
                local_points.append({'x': round(x_mm-start[0], 6), 'y': round(y_mm-start[1], 6)})
            global_points.append([x_mm, y_mm])
            segment_layers.append(layer)
    return {'net': specification['net'], 'from_proposal_via_index': 0,
            'from_layer': parts[0][0], 'to': specification['target_selector'], 'width': .6,
            'pcbPath': local_points, 'global_path_mm': global_points,
            'segment_layers': segment_layers,
            'classification': 'Manual native ordinary outer trace; full .6mm trunk, not a saved router result'}


def route_speaker(planner, routing_specification):
    net = next(record for record in planner.circuit if record['type'] == 'source_net' and record['name'] == routing_specification['net'])
    root = planner.root(net['source_net_id'])
    port = next(record for record in planner.ports.values() if planner.port_name(record) == routing_specification['selector'])
    target_port = next(record for record in planner.ports.values() if planner.port_name(record) == routing_specification['target_selector'])
    target = (target_port['x'], target_port['y'])
    specification = {'root': root, 'net': net, 'width': .275,
                     'origin': (port['x'], port['y']), 'new_vias': [target],
                     'via_outer_mm': .45, 'via_hole_mm': .3,
                     'distribution_layers': ('bottom', 'top'), 'distribution_width_mm': .6,
                     'routing_geometry': 'native_wire', 'connected_targets': [target]}
    result = {'classification': 'Manual native speaker wire proposal; full native validation required',
              'paths': [], 'pours': [], 'vias': [], 'pad_necks': [], 'unresolved': []}
    escape = helpers['pad_escape'](planner, specification)
    if escape is None:
        result['unresolved'].append('No legal pad escape reaching a .6mm outer native-wire corridor')
    else:
        start, positions = escape
        neck_length_mm = sum(math.dist(first, last) for first, last in zip(positions, positions[1:]))
        if neck_length_mm > 5:
            result['unresolved'].append({'reason': 'Pad neck exceeds five-mm authoring limit', 'length_mm': neck_length_mm})
        else:
            neck = helpers['escape_record'](planner, {**specification, 'port': port, 'positions': positions})
            route = helpers['wide_multilayer_route'](planner, {
                **specification, 'width': .6, 'first': start, 'last': target,
                'new_vias': [start, target], 'layers': ('bottom', 'top'), 'multi_anchor': True})
            if route is None:
                result['unresolved'].append('No complete .6mm outer native-wire trunk')
            else:
                parts, vias = route
                # The escape lands on a named structural via. Remove its
                # automatic via so the native build emits exactly one drill.
                neck['pcbPath'] = [point for point in neck['pcbPath'] if not point.get('via')]
                neck.pop('to')
                neck['to_proposal_via_index'] = 0
                result['paths'] = [neck, trunk_path({**routing_specification, 'start': start, 'parts': parts})]
                result['vias'] = [{'net': net['name'], 'x': start[0], 'y': start[1], 'hole_mm': .3, 'outer_mm': .45}]
                result['pad_necks'] = [{'net': net['name'], 'terminal': routing_specification['selector'],
                                       'width_mm': .275, 'length_mm': neck_length_mm,
                                       'nominal_trunk_width_mm': .6,
                                       'status': 'Measured proposal; load/stackup qualification pending'}]
                result['trunk_via_positions_mm'] = vias
                for layer, positions in parts:
                    planner.copper.append((root, layer, LineString(positions).buffer(.3)))
                bridges = runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')))
                for position in vias:
                    bridges['reserve_via'](planner, {'root': root, 'position': position})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('native')
    parser.add_argument('output')
    parser.add_argument('--replace-speaker-pair', action='store_true',
                        help='Author both complete speaker connections after retiring their actual copper for planning')
    parser.add_argument('--replace-positive-only', action='store_true',
                        help='Replace only the existing positive route while keeping the negative connection as a fixed constraint')
    parser.add_argument('--output-order', choices=('negative-first', 'positive-first'), default='negative-first')
    args = parser.parse_args()
    if args.replace_speaker_pair and args.replace_positive_only:
        parser.error('Select either pair replacement or positive-only replacement')
    circuit = json.loads(Path(args.native).read_text())
    planner = helpers['Planner'](circuit)
    result = {'classification': 'Manual native speaker wire proposal; full native validation required',
              'paths': [], 'pours': [], 'vias': [], 'pad_necks': [], 'unresolved': [],
              'retired_native_features': []}
    if args.replace_speaker_pair or args.replace_positive_only:
        retired_net_names = ('SPEAKER_P',) if args.replace_positive_only else ('SPEAKER_P', 'SPEAKER_N')
        roots = {planner.root(record['source_net_id']) for record in circuit
                 if record['type'] == 'source_net' and record['name'] in retired_net_names}
        sources = {record['source_trace_id']: record for record in circuit if record['type'] == 'source_trace'}
        retired_traces = {}
        retired_features = []
        for record in circuit:
            if record['type'] == 'pcb_trace':
                source = sources[record['source_trace_id']]
                terminals = source.get('connected_source_port_ids', []) + source.get('connected_source_net_ids', [])
                if terminals and planner.root(terminals[0]) in roots:
                    retired_traces[record['pcb_trace_id']] = {layer: None for layer in ('top', 'bottom', 'inner1', 'inner2')}
            elif record['type'] == 'pcb_via' and planner.via_root(record) in roots:
                retired_features.append(record['pcb_via_id'])
            elif record['type'] == 'pcb_copper_pour' and planner.root(record['source_net_id']) in roots:
                retired_features.append(record['pcb_copper_pour_id'])
        result['retired_native_features'] = list(retired_traces) + retired_features
        planner = helpers['Planner'](circuit, {'relocated_trace_layers': retired_traces,
                                             'retired_feature_ids': retired_features})
    planner.set_grid(.05)
    planner.via_copper_clearance = .27
    nets = [('SPEAKER_N', '.U3 > .pin10', '.J4 > .pin2')]
    if args.replace_positive_only:
        nets = [('SPEAKER_P', '.U3 > .pin9', '.J4 > .pin1')]
    if args.replace_speaker_pair:
        nets.append(('SPEAKER_P', '.U3 > .pin9', '.J4 > .pin1'))
        if args.output_order == 'positive-first':
            nets.reverse()
    for name, selector, target_selector in nets:
        candidate = route_speaker(planner, {'net': name, 'selector': selector, 'target_selector': target_selector})
        offset = len(result['vias'])
        for path in candidate['paths']:
            for key in ('from_proposal_via_index', 'to_proposal_via_index'):
                if key in path:
                    path[key] += offset
        for key in ('paths', 'pours', 'vias', 'pad_necks'):
            result[key].extend(candidate[key])
        result['unresolved'].extend({'net': name, 'reason': reason} for reason in candidate['unresolved'])
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'complete': not result['unresolved'], 'unresolved': result['unresolved'],
                      'paths': len(result['paths']), 'pad_necks': result['pad_necks']}))
    return 1 if result['unresolved'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
