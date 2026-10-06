"""Replace authored high-current distribution with top/bottom native regions.

Preserve the native scene and saved router output. Plan against all unrelated
copper and exact imported pad/drill contours. A proposal needs native replay
and independent geometry/connectivity validation before acceptance.
"""
import argparse
import hashlib
import json
import math
import runpy
from pathlib import Path

from shapely.geometry import LineString, Point, Polygon

helpers = runpy.run_path(str(Path(__file__).with_name('plan-power-copper.py')))
HIGH_CURRENT_NETS = ('PACK_BAT', 'VSYS', 'VBUS', 'V3V3', 'VMOTOR', 'HAPTIC_N')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit_json', type=Path)
    parser.add_argument('authored_regions', type=Path)
    parser.add_argument('output_json', type=Path)
    parser.add_argument('--grid-mm', type=float, choices=(.05, .1), default=.1)
    parser.add_argument('--relocated-signals', type=Path)
    parser.add_argument('--manual-escapes', type=Path)
    parser.add_argument('--branch-requirements', type=Path)
    args = parser.parse_args()
    circuit = json.loads(args.circuit_json.read_text())
    authored = json.loads(args.authored_regions.read_text())
    nets = {record['name']: record for record in circuit if record['type'] == 'source_net'}
    distribution_names = set(region['net'] for region in authored['pours'])
    replaced_net_ids = {nets[name]['source_net_id'] for name in distribution_names}
    retired_pour_ids = {record['pcb_copper_pour_id'] for record in circuit
                        if record['type'] == 'pcb_copper_pour' and record['source_net_id'] in replaced_net_ids}
    retired_via_ids = {record['pcb_via_id'] for record in circuit
                       if record['type'] == 'pcb_via' and record.get('source_net_id') in replaced_net_ids}
    relocated_trace_layers = {}
    if args.relocated_signals:
        relocation = json.loads(args.relocated_signals.read_text())
        source_traces = {record['source_trace_id']: record for record in circuit if record['type'] == 'source_trace'}
        names = {f"MANUAL_{path['net']}_{path['original_path_index']}" for path in relocation['paths']}
        relocated_trace_layers = {record['pcb_trace_id']: {'bottom': None} for record in circuit
                                 if record['type'] == 'pcb_trace' and source_traces[record['source_trace_id']].get('name') in names}
    planner = helpers['Planner'](circuit, {'retired_feature_ids': retired_pour_ids | retired_via_ids,
                                         'relocated_trace_layers': relocated_trace_layers})
    if args.relocated_signals:
        for region in relocation['pours']:
            region_root = planner.root(nets[region['net']]['source_net_id'])
            planner.copper.append((region_root, region['layer'], Polygon([(p['x'],p['y']) for p in region['outline']])))
        for via in relocation.get('vias', []):
            via_root = planner.root(nets[via['net']]['source_net_id'])
            hole = Point(via['x'],via['y']).buffer(.15)
            planner.holes.append(hole);planner.plated_hole_roots[hole.wkb] = via_root
            for layer in ('top','inner1','inner2','bottom'):
                planner.copper.append((via_root,layer,Point(via['x'],via['y']).buffer(.225)))
    planner.set_grid(args.grid_mm)
    planner.via_copper_clearance = .27
    existing_vias = [(record['x'], record['y']) for record in circuit if record['type'] == 'pcb_via']
    originals = list(authored['pours'])
    output = {**authored, 'pours': [],
              'vias': [via for via in authored['vias'] if via['net'] not in distribution_names], 'unresolved': [],
              'classification': 'authored outer-layer high-current replacement; requires native replay and audit',
              'source_circuit_json': str(args.circuit_json),
              'source_sha256': hashlib.sha256(args.circuit_json.read_bytes()).hexdigest(),
              'retired_pour_ids': sorted(retired_pour_ids), 'retired_via_ids': sorted(retired_via_ids), 'replaced_authored_region_count': len(originals)}
    output['relocated_trace_layers'] = relocated_trace_layers
    manual_escapes = json.loads(args.manual_escapes.read_text())['paths'] if args.manual_escapes else []
    output['changed_escape_paths'] = []
    branch_requirements = json.loads(args.branch_requirements.read_text())['branches'] if args.branch_requirements else []
    output['branch_requirements'] = branch_requirements
    for name in (*HIGH_CURRENT_NETS, *sorted(distribution_names - set(HIGH_CURRENT_NETS))):
        root = planner.root(nets[name]['source_net_id'])
        terminals = list(dict.fromkeys((record['x'], record['y']) for record in circuit
                         if record['type'] == 'pcb_via' and record.get('pcb_trace_id')
                         and planner.via_root(record) == root))
        nominal_width = max(region['nominal_width_mm'] for region in originals if region['net'] == name)
        if len(terminals) < 2:
            raise ValueError(f'{name}: missing native escaped terminals')
        distribution_layers = ('top', 'bottom') if name in HIGH_CURRENT_NETS else ('inner2', 'inner1')
        own_obstacles = [helpers['inner_obstacles'](planner, {'root': root, 'width': nominal_width+.002,
                         'layer': layer, 'new_vias': terminals, 'copper_clearance_mm': .27}) for layer in distribution_layers]
        deferred_branches = [terminal for terminal in terminals if any(
            branch['net']==name and any(path['net']==name and path['from']==branch['terminal'] and
            math.dist(path['global_path_mm'][-1],terminal)<1e-5 for path in manual_escapes) for branch in branch_requirements)]
        trunk_terminals = [terminal for terminal in terminals if terminal not in deferred_branches]
        if not trunk_terminals:
            raise ValueError('A distribution tree needs a real supply trunk terminal')
        terminal_seed = next((terminal for terminal in trunk_terminals if any(not Point(terminal).intersects(obstacle) for obstacle in own_obstacles)), trunk_terminals[0])
        connected, remaining = [terminal_seed], [terminal for terminal in trunk_terminals if terminal != terminal_seed]
        reescaped = set()
        rejected = set()
        index = 0
        branch_only = False
        while remaining or deferred_branches:
            if not remaining:
                remaining, deferred_branches = deferred_branches, []
                branch_only = True
            candidates = [] if branch_only else sorted((math.dist(first, last), first, last) for first in connected for last in remaining
                                if (first, last) not in rejected)
            if not candidates:
                # Terminal-specific load requirements distinguish pull-ups,
                # control supplies and measurement/bypass branches from trunks.
                # Only an explicitly reviewed branch may use another width/layer.
                branch_routed = False
                for terminal in list(remaining):
                    authored = next((path for path in manual_escapes if path['net']==name and
                                    math.dist(path['global_path_mm'][-1],terminal)<1e-5), None)
                    requirement = next((branch for branch in branch_requirements if authored and
                                        branch['net']==name and branch['terminal']==authored['from']), None)
                    if not requirement:
                        continue
                    for target in sorted(connected,key=lambda point:math.dist(point,terminal)):
                        branch_result = helpers['wide_multilayer_route'](planner, {
                            'first':terminal,'last':target,'root':root,'width':requirement['nominal_width_mm']+.002,
                            'new_vias':terminals,'layers':requirement['layers'],'via_outer_mm':.45,'via_hole_mm':.3,
                            'copper_clearance_mm':.27})
                        if not branch_result:
                            continue
                        parts,extra_vias = branch_result
                        for layer,route in parts:
                            if len(route)<2 or LineString(route).length<1e-6:
                                continue
                            contour = LineString(route).buffer((requirement['nominal_width_mm']+.002)/2,quad_segs=64,cap_style=2,join_style=1)
                            output['pours'].append({'net':name,'layer':layer,'path_mm':route,
                                'nominal_width_mm':requirement['nominal_width_mm'],'drawn_width_mm':requirement['nominal_width_mm']+.002,
                                'outline':[{'x':round(x,6),'y':round(y,6)} for x,y in list(contour.exterior.coords)[:-1]],
                                'classification':'manual native low-current terminal branch','branch_terminal':requirement['terminal'],
                                'current_basis':requirement['basis']})
                            planner.copper.append((root,layer,contour))
                        for x,y in extra_vias:
                            output['vias'].append({'net':name,'x':x,'y':y,'hole_mm':.3,'outer_mm':.45})
                            hole = Point(x,y).buffer(.15);planner.holes.append(hole);planner.plated_hole_roots[hole.wkb]=root
                            for layer in ('top','inner1','inner2','bottom'):
                                planner.copper.append((root,layer,Point(x,y).buffer(.225)))
                        remaining.remove(terminal);connected.append(terminal)
                        branch_routed = True
                        print(json.dumps({'net':name,'reviewed_low_current_branch':requirement['terminal'],'width_mm':requirement['nominal_width_mm']}),flush=True)
                        break
                if branch_routed:
                    continue
                moved = False
                if name in HIGH_CURRENT_NETS:
                    for terminal in list(remaining):
                        for original_index, original in enumerate(manual_escapes):
                            if original_index in reescaped or original['net'] != name or original['to'] != 'net.'+name:
                                continue
                            if math.dist(original['global_path_mm'][-1], terminal) > 1e-5:
                                continue
                            reescaped.add(original_index)
                            port = next((port for port in planner.ports.values() if planner.port_name(port) == original['from']), None)
                            if not port:
                                raise ValueError('Missing native pad for authored escape')
                            escape = helpers['pad_escape'](planner, {
                                'root': root, 'width': original['width'], 'origin': (port['x'],port['y']),
                                'net': nets[name], 'new_vias': terminals, 'distribution_layers': distribution_layers,
                                'distribution_width_mm': nominal_width+.002, 'via_outer_mm': .45, 'via_hole_mm': .3,
                                'connected_targets': connected,
                                'copper_clearance_mm': .27})
                            if escape is None:
                                continue
                            new_terminal, positions = escape
                            record = helpers['escape_record'](planner, {'port':port,'net':nets[name],'root':root,
                                'positions':positions,'width':original['width'],'via_outer_mm':.45,'via_hole_mm':.3})
                            output['changed_escape_paths'].append({'original_path_index':original_index,'path':record,
                                'retired_via_position_mm':terminal})
                            terminals[terminals.index(terminal)] = new_terminal
                            remaining[remaining.index(terminal)] = new_terminal
                            print(json.dumps({'net':name,'relocated_escape':original_index,'old_via':terminal,'new_via':new_terminal}),flush=True)
                            moved = True
                            break
                    if moved:
                        continue
                output['unresolved'].append({'net': name, 'unreachable_terminals_mm': remaining,
                                             'nominal_width_mm': nominal_width, 'reason': 'No legal distribution tree at required width'})
                args.output_json.write_text(json.dumps(output, indent=2) + '\n')
                break
            _, first, last = candidates[0]
            width = nominal_width + .002
            region = {'net': name, 'nominal_width_mm': nominal_width, 'path_mm': [first, last]}
            own_vias = terminals + [(via['x'], via['y']) for via in output['vias'] if via['net'] == name]
            result = helpers['wide_multilayer_route'](planner, {
                'first': first, 'last': last, 'root': root, 'width': width, 'new_vias': own_vias,
                'layers': ('top', 'bottom') if name in HIGH_CURRENT_NETS else ('inner2', 'inner1'),
                'via_outer_mm': .45, 'via_hole_mm': .3, 'copper_clearance_mm': .27})
            if result is None:
                rejected.add((first, last))
                print(json.dumps({'net': name, 'rejected_edge_mm': [first, last]}), flush=True)
                continue
            else:
                connected.append(last)
                remaining.remove(last)
                parts, new_vias = result
                for layer, route in parts:
                    if len(route) < 2 or LineString(route).length < 1e-6:
                        continue
                    contour = LineString(route).buffer(width / 2, quad_segs=64, cap_style=2, join_style=1)
                    if contour.geom_type != 'Polygon' or contour.interiors:
                        raise ValueError('Native region needs one simple outline')
                    output['pours'].append({**region, 'layer': layer, 'path_mm': route,
                        'outline': [{'x': round(x, 6), 'y': round(y, 6)} for x, y in list(contour.exterior.coords)[:-1]],
                        'drawn_width_mm': width, 'classification': 'manual native outer-layer high-current region; thermal qualification pending' if name in HIGH_CURRENT_NETS else 'manual native low-current distribution region'})
                    planner.copper.append((root, layer, contour))
                for x, y in new_vias:
                    output['vias'].append({'net': name, 'x': x, 'y': y, 'hole_mm': .3, 'outer_mm': .45,
                                          'classification': 'manual native through via between outer power regions'})
                    hole = Point(x, y).buffer(.15)
                    planner.holes.append(hole)
                    planner.plated_hole_roots[hole.wkb] = root
                    for layer in ('top', 'inner1', 'inner2', 'bottom'):
                        planner.copper.append((root, layer, Point(x, y).buffer(.225)))
            args.output_json.write_text(json.dumps(output, indent=2) + '\n')
            print(json.dumps({'net': name, 'link': index, 'routed': result is not None,
                              'unresolved_count': len(output['unresolved']), 'remaining_terminals': len(remaining)}), flush=True)
            index += 1
    return 1 if output['unresolved'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
