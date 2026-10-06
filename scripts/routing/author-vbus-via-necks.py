"""Author short, explicit VBUS necks where the .45 mm via meets .5 mm trunks.

This preserves the source endpoints and outer layers. It does not qualify the
neck's current capacity; fresh native clearance and width audits are required.
"""
import json
import runpy
from pathlib import Path
from shapely.geometry import LineString
from shapely.ops import substring

b = runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')))
source = Path('src/board/connection-copper.json')
data = json.loads(source.read_text())
replacements = []
for index, at_end in ((78, True), (79, False)):
    region = data['pours'][index]
    if region['net'] != 'VBUS' or region['nominal_width_mm'] != .5:
        raise ValueError('Expected original measured VBUS trunk')
    line = LineString(region['path_mm'])
    terminal = list(line.coords)[-1 if at_end else 0]
    if abs(terminal[0]+7) > 1e-5 or abs(terminal[1]+20.45) > 1e-5:
        raise ValueError('Unexpected native VBUS via endpoint')
    split = line.length-.35 if at_end else .35
    for first, last, width in ((0, split, .5 if at_end else .3),
                               (split, line.length, .3 if at_end else .5)):
        part = substring(line, first, last)
        records = b['region_records']('VBUS', {'parts': [(region['layer'], list(part.coords))], 'width': width})
        for record in records:
            if width == .3:
                record['neck_basis'] = 'Explicit .35 mm outer-layer neck at .45 mm native through-via land; current/stackup qualification pending'
        replacements.extend(records)
data['pours'][78:80] = replacements
neck = next(r for r in data['pad_necks'] if r['terminal'] == '.C1 > .pin1')
neck['outer_distribution_neck_length_mm'] += .7
neck['total_narrow_length_mm'] += .7
neck['via_necks'] = {'position_mm': [-7, -20.45], 'width_mm': .3,
                     'length_mm_per_layer': .35, 'layers': ['bottom', 'top']}
if neck['total_narrow_length_mm'] > 5:
    raise ValueError('Measured narrow sections exceed the authoring limit')
source.write_text(json.dumps(data, indent=2)+'\n')
print(json.dumps({'replacement_regions': len(replacements), 'total_narrow_length_mm': neck['total_narrow_length_mm'], 'current_qualified': False}))
