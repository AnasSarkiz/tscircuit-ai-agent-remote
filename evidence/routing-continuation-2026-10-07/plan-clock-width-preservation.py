"""Propose an amplifier clock escape without clipping original required strips."""
import json
import math
import runpy
from pathlib import Path

from shapely.geometry import Point, Polygon

evidence = Path(__file__).parent
native = evidence / 'speaker-local-native-v6/circuit.json'
circuit = json.loads(native.read_text())
bridges = runpy.run_path('scripts/routing/plan-connection-bridges.py')
helpers = bridges['helpers']
source = json.loads(Path('src/board/connection-copper.json').read_text())
source_trace_id = next(r['source_trace_id'] for r in circuit if r['type'] == 'source_trace'
                       and r.get('name') == 'CONNECTION_ESCAPE_AMP_BCLK_70')
trace = next(r for r in circuit if r['type'] == 'pcb_trace' and r['source_trace_id'] == source_trace_id)
retired_vias = {r['pcb_via_id'] for r in circuit if r['type'] == 'pcb_via' and r.get('pcb_trace_id') == trace['pcb_trace_id']}
# Only the first new amplifier bridge is replaced; its existing transition and
# inner2 continuation stay fixed. Original solver caches are not modified.
retired_vias.add('pcb_copper_pour_377')
planner = helpers['Planner'](circuit, {'relocated_trace_layers': {
    trace['pcb_trace_id']: {layer: None for layer in ('top', 'bottom', 'inner1', 'inner2')}},
    'retired_feature_ids': retired_vias})
planner.set_grid(.05)
planner.via_copper_clearance = .27
nets = {r['name']: r for r in circuit if r['type'] == 'source_net'}
root = planner.root(nets['AMP_BCLK']['source_net_id'])
for path in ['src/board/connection-copper.json', 'src/board/manual-power-copper.json', 'src/board/inner-signal-copper.json']:
    authored = json.loads(Path(path).read_text())
    retired = authored.get('retired_connection_region_indices', [])
    for index, region in enumerate(authored['pours']):
        if index in retired or region['net'] in ('AMP_BCLK', 'GND'):
            continue
        # Preserve the complete source envelope, including copper that the last
        # native pour generation clipped around the rejected clock via.
        shape = Polygon([(p['x'], p['y']) for p in region['outline']]).buffer(.06)
        planner.copper.append((planner.root(nets[region['net']]['source_net_id']), region['layer'], shape))
top_blocks = planner.obstacles(root, 'top', .2)
via_blocks = helpers['via_obstacles'](planner, {'root': root, 'via_outer_mm': .45, 'via_hole_mm': .3})
inner_blocks = helpers['distribution_obstacles'](planner, {'root': root, 'layer': 'inner1', 'width': .202,
    'new_vias': [], 'via_outer_mm': .45, 'via_hole_mm': .3, 'copper_clearance_mm': .27})
origin = (trace['route'][0]['x'], trace['route'][0]['y'])
target = tuple(source['pours'][108]['path_mm'][-1])
candidates = sorted([(round(-23.5 + x * .05, 6), round(.2 + y * .05, 6))
                     for x in range(115) for y in range(82)], key=lambda p: math.dist(p, origin))
result = None
counts = {'via_legal': 0, 'top_reachable': 0, 'inner_reachable': 0}
print(json.dumps({'origin_blocked': Point(origin).intersects(top_blocks), 'target_blocked': Point(target).intersects(inner_blocks)}), flush=True)
for candidate in candidates:
    if Point(candidate).intersects(via_blocks):
        continue
    counts['via_legal'] += 1
    top_route = planner.grid_route((origin, candidate, top_blocks))
    if not top_route:
        continue
    counts['top_reachable'] += 1
    inner_route = planner.grid_route((candidate, target, inner_blocks))
    if not inner_route:
        continue
    counts['inner_reachable'] += 1
    port = planner.ports[trace['route'][0]['start_pcb_port_id']]
    escape = helpers['escape_record'](planner, {'port': port, 'net': nets['AMP_BCLK'], 'root': root,
        'width': .2, 'positions': top_route, 'via_outer_mm': .45, 'via_hole_mm': .3})
    region = bridges['region_records']('AMP_BCLK', {'parts': [('inner1', inner_route)], 'width': .2})[0]
    result = {'classification': 'authored clock escape preserving original nominal strip widths; native qualification pending',
              'path': escape, 'pour': region, 'old_via_mm': [-19.2, 2.752097], 'new_via_mm': candidate}
    break
(evidence / 'clock-width-preservation-proposal-v2.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'qualified_local_candidate': result is not None, 'new_via_mm': result['new_via_mm'] if result else None, 'counts': counts}))
raise SystemExit(0 if result else 1)
