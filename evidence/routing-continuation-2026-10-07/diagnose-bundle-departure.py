"""Identify actual features preventing the shared amplifier departure."""
import json
import runpy
from pathlib import Path
from shapely.geometry import LineString

module = runpy.run_path('scripts/routing/plan-coupled-speaker.py')
planner, specification = module['planning_scene'](Path('dist/index/circuit.json'))
names = {planner.root(record['source_net_id']): record['name'] for record in planner.circuit
         if record['type'] == 'source_net'}
result = []
for x_mm, y_mm in ((-16.25, 7.), (-16.25, 9.), (-15.5, 8.), (-18., 7.5)):
    line = LineString([(x_mm, y_mm), (x_mm, y_mm+1.)])
    for layer in ('top', 'bottom'):
        pads = [{'id': record.get('pcb_smtpad_id', record.get('pcb_plated_hole_id')),
                 'net': names.get(planner.root(planner.ports[record['pcb_port_id']]['source_port_id']))
                 if record.get('pcb_port_id') in planner.ports else None,
                 'distance_mm': line.distance(shape)}
                for record, shape in planner.pads if layer in record.get('layers', [record.get('layer')])
                and line.distance(shape) < .91]
        copper = [{'net': names.get(root, root), 'distance_mm': line.distance(shape),
                   'bounds': list(shape.bounds)}
                  for root, copper_layer, shape in planner.copper if copper_layer == layer
                  and line.distance(shape) < .91]
        holes = [{'net': names.get(planner.plated_hole_roots.get(hole.wkb)),
                  'bounds': list(hole.bounds), 'distance_mm': line.distance(hole)}
                 for hole in planner.holes if line.distance(hole) < .96]
        result.append({'departure': [x_mm, y_mm], 'layer': layer,
                       'blocking_pads': pads, 'blocking_copper': copper, 'blocking_holes': holes})
Path('evidence/routing-continuation-2026-10-07/departure-blockers.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result))
