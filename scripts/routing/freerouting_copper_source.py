"""Translate validated SES centerlines into reviewable native copper source.

This writes proposals, not Circuit JSON or an autorouter cache. The resulting
regions still require native regeneration, width, clearance and connectivity
audits. A 1 um outward serialization reserve is explicit in the receipt.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

from shapely.geometry import LineString, Polygon

PROTECTED_NETS = {'GND', 'USB_DP', 'USB_DN', 'SPEAKER_P', 'SPEAKER_N'}
LAYERS = ['top', 'inner1', 'inner2', 'bottom']


def make_regions(proposals):
    regions = []
    for index, path in enumerate(proposals['paths']):
        if path['net'] in PROTECTED_NETS or path['layer'] not in ('top', 'inner2', 'bottom'):
            raise ValueError('Protected net or reserved layer in proposed copper')
        width = path['width_mm']
        coordinates = path['path_mm']
        if not math.isfinite(width) or width < .2 or any(not math.isfinite(x) for pair in coordinates for x in pair):
            raise ValueError('Invalid proposed dimensions')
        centerline = LineString(coordinates)
        if centerline.length <= 1e-6 or not centerline.is_simple:
            raise ValueError('Zero-length or self-intersecting proposed centerline')
        contour = centerline.buffer(width / 2 + .001, quad_segs=128)
        if not isinstance(contour, Polygon) or not contour.is_valid or contour.interiors:
            raise ValueError('Proposed wire requires unsupported copper-region holes')
        regions.append({'net': path['net'], 'layer': path['layer'],
            'outline': [{'x': round(x, 6), 'y': round(y, 6)} for x, y in list(contour.exterior.coords)[:-1]],
            'nominal_width_mm': width, 'path_mm': coordinates,
            'freerouting_wire_index': index})
    for via in proposals['vias']:
        if via['net'] in PROTECTED_NETS or via['layers'] != LAYERS or via['hole_mm'] < .3 or via['outer_mm'] < .7:
            raise ValueError('Protected net, partial-span or undersized proposed via')
        if any(not math.isfinite(via[key]) for key in ('x', 'y', 'hole_mm', 'outer_mm')):
            raise ValueError('Invalid proposed via dimensions')
    return regions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('proposals')
    parser.add_argument('output_json')
    args = parser.parse_args()
    proposal_path = Path(args.proposals)
    proposals = json.loads(proposal_path.read_text())
    source = {'classification': 'Unaccepted native copper proposals derived from the actual Freerouting SES; not manual routing or a solver cache',
        'native_source_sha256': proposals['native_source_sha256'],
        'dsn_sha256': proposals['dsn_sha256'], 'session_sha256': proposals['session_sha256'],
        'proposals_sha256': hashlib.sha256(proposal_path.read_bytes()).hexdigest(),
        'outward_serialization_reserve_mm': .001,
        'pours': make_regions(proposals), 'vias': proposals['vias']}
    Path(args.output_json).write_text(json.dumps(source, indent=2) + '\n')
    print(json.dumps({'unaccepted_regions': len(source['pours']), 'unaccepted_vias': len(source['vias'])}))


if __name__ == '__main__':
    main()
