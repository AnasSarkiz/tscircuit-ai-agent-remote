"""Encode preserved global pad escapes in each connected port's native frame."""
import argparse
import hashlib
import json
import math
import runpy
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('native_json', type=Path)
parser.add_argument('original_paths', type=Path)
parser.add_argument('inner_regions', type=Path)
parser.add_argument('output_json', type=Path)
args = parser.parse_args()
helpers = runpy.run_path(str(Path(__file__).with_name('plan-power-copper.py')))
planner = helpers['Planner'](json.loads(args.native_json.read_text()))
originals = json.loads(args.original_paths.read_text())['paths']
proposal = json.loads(args.inner_regions.read_text())
ports = {planner.port_name(port): port for port in planner.ports.values()
         if planner.source_ports[port['source_port_id']].get('source_component_id') in planner.source_components}
for path in proposal['paths']:
    original = originals[path['original_path_index']]
    transitions = [i for i in range(1, len(original['segment_layers']))
                   if original['segment_layers'][i] != original['segment_layers'][i-1]]
    if len(transitions) not in (1, 2):
        raise ValueError('Only ordinary top/bottom escapes are supported')
    escapes = [(original['from'], original['global_path_mm'][:transitions[0]])]
    if len(transitions) == 2:
        escapes.append((original['to'], list(reversed(original['global_path_mm'][transitions[1]-1:]))))
    path['escapes'] = []
    for selector, positions in escapes:
        port = ports[selector]
        if math.dist(positions[0], (port['x'], port['y'])) > 1e-5:
            raise ValueError('Escape must start at its own numbered pad')
        component = planner.components[port['pcb_component_id']]
        angle = math.radians(-component['rotation'])
        points = []
        for x, y in positions[1:]:
            dx, dy = x-component['display_offset_x'], y-component['display_offset_y']
            points.append({'x': round(dx*math.cos(angle)-dy*math.sin(angle), 6),
                           'y': round(dx*math.sin(angle)+dy*math.cos(angle), 6)})
        if not points:
            raise ValueError('Escape must include its through-via centre')
        points += [{**points[-1], 'via': True, 'fromLayer': 'top', 'toLayer': 'bottom'}, dict(points[-1])]
        path['escapes'].append({'from': selector, 'to': 'net.'+path['net'],
                                'pcbPathRelativeTo': selector, 'pcbPath': points})
proposal['escape_reanchor'] = {'native_json': str(args.native_json),
    'native_sha256': hashlib.sha256(args.native_json.read_bytes()).hexdigest(),
    'original_paths': str(args.original_paths),
    'scope': 'Same global outer pad escapes and via centres, each encoded relative to its own connected port component; native replay required'}
args.output_json.write_text(json.dumps(proposal, indent=2)+'\n')
print(json.dumps({'reanchored_paths': len(proposal['paths']),
                  'escapes': sum(len(path['escapes']) for path in proposal['paths'])}))
