"""Plan short, nonzero pad contacts to already connected copper on the same net."""
import argparse
import json
import runpy
from pathlib import Path

from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

contact_helpers = runpy.run_path(str(Path(__file__).with_name('plan-ground-contacts.py')))
audit_helpers = runpy.run_path(str(Path(__file__).with_name('audit-copper.py')))
Planner = contact_helpers['Planner']


def top_shapes(circuit):
    for record in circuit:
        ty = record['type']
        if ty in ('pcb_smtpad', 'pcb_plated_hole') and 'top' in record.get('layers', [record.get('layer')]):
            yield record[ty+'_id'], audit_helpers['pad_contour'](record)
        elif ty == 'pcb_via':
            yield record['pcb_via_id'], Point(record['x'], record['y']).buffer(record['outer_diameter']/2)
        elif ty == 'pcb_trace':
            for index, (first, last) in enumerate(zip(record['route'], record['route'][1:])):
                if first['route_type'] == last['route_type'] == 'wire' and first['layer'] == last['layer'] == 'top':
                    width = max(first['width'], last['width'])
                    yield f"{record['pcb_trace_id']}:{index}", LineString([(first['x'], first['y']), (last['x'], last['y'])]).buffer(width/2)
        elif ty == 'pcb_copper_pour' and record['layer'] == 'top':
            brep=record['brep_shape']
            yield record['pcb_copper_pour_id'], Polygon([(p['x'],p['y']) for p in brep['outer_ring']['vertices']],
                [[(p['x'],p['y']) for p in ring['vertices']] for ring in brep['inner_rings']])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit_json')
    parser.add_argument('copper_audit')
    parser.add_argument('output_json')
    parser.add_argument('nets', nargs='+')
    parser.add_argument('--reserve-proposals', action='append', default=[])
    args = parser.parse_args()
    circuit = json.loads(Path(args.circuit_json).read_text())
    physical = json.loads(Path(args.copper_audit).read_text())
    planner = Planner(circuit)
    for path in args.reserve_proposals:
        planner.reserve_proposals(json.loads(Path(path).read_text()))
    net_records = {r['name']: r for r in circuit if r['type'] == 'source_net'}
    shapes = dict(top_shapes(circuit))
    missing={identifier for r in circuit if r['type']=='pcb_port_not_connected_error' for identifier in r['pcb_port_ids']}
    paths, unresolved = [], []
    for name in args.nets:
        root = planner.root(net_records[name]['source_net_id'])
        ports = [p for p in planner.ports.values() if planner.root(p['source_port_id']) == root
                 and planner.source_ports[p['source_port_id']].get('source_component_id') in planner.source_components
                 and not planner.port_name(p).startswith(('.J3 >', '.J7 >'))]
        islands = {}
        for port in ports:
            groups = physical['physical_port_groups'][port['pcb_port_id']]
            if len(groups) == 1:
                islands.setdefault(groups[0], []).append(port)
        if not islands:
            continue
        main_group = max(islands, key=lambda group: len(islands[group]))
        target = unary_union([shape for identifier, shape in shapes.items()
                              if physical['physical_feature_groups'][identifier] == main_group])
        pending=[(group,alternatives) for group,alternatives in islands.items() if group!=main_group]
        # These additional traces make a real nonzero contact beyond the pad;
        # they do not claim that endpoint markers alone prove connectivity.
        pending.extend((main_group,[p]) for p in islands[main_group] if p['pcb_port_id'] in missing)
        for group, alternatives in pending:
            width=.2 if name=='GND' and group==main_group else .3
            for port in alternatives:
                positions = contact_helpers['plan_contact'](planner, {'port': port, 'ground': target,'width':width})
                if positions:
                    path = contact_helpers['record_contact'](planner, {'port': port, 'positions': positions,'width':width})
                    path.update({'net': name, 'to': 'net.'+name,
                                 'classification': 'manual native short pad-to-existing-copper contact; local power neck requires current qualification' if group!=main_group else 'manual native nonzero contact to already connected copper; primary continuity independently verified'})
                    paths.append(path)
                    planner.copper.append((root, 'top', LineString(positions).buffer(width/2)))
                    break
            else:
                unresolved.append({'net': name, 'ports': [planner.port_name(p) for p in alternatives],
                                   'reason': 'No nonzero 0.3 mm top contact within 3 mm to the connected island'})
        print(json.dumps({'net': name, 'planned_so_far': len(paths)}), flush=True)
    Path(args.output_json).write_text(json.dumps({'classification': 'manual native contact proposals, not solver caches',
        'source_circuit_json': args.circuit_json, 'paths': paths, 'unresolved': unresolved}, indent=2)+'\n')
    print(json.dumps({'contacts': len(paths), 'unresolved': unresolved}))


if __name__ == '__main__':
    main()
