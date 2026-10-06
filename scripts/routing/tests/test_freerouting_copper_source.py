"""SES proposals must retain real trace widths and ordinary via restrictions."""
import copy
import runpy
import unittest
from pathlib import Path

from shapely.geometry import LineString, Polygon

SOURCE = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'freerouting_copper_source.py'))
PROPOSALS = {'paths': [{'net': 'SIGNAL', 'layer': 'bottom', 'width_mm': .3,
                       'path_mm': [[0, 0], [1, 0], [1, 1]]}], 'vias': []}


class FreeroutingCopperSourceTests(unittest.TestCase):
    def test_bent_region_covers_required_centerline_width(self):
        region = SOURCE['make_regions'](PROPOSALS)[0]
        actual = Polygon([(p['x'], p['y']) for p in region['outline']])
        required = LineString([[0, 0], [1, 0], [1, 1]]).buffer(.15, quad_segs=64)
        self.assertTrue(actual.covers(required))

    def test_zero_length_cannot_become_fake_connection(self):
        proposals = copy.deepcopy(PROPOSALS)
        proposals['paths'][0]['path_mm'] = [[0, 0], [0, 0]]
        with self.assertRaisesRegex(ValueError, 'Zero-length'):
            SOURCE['make_regions'](proposals)

    def test_reserved_ground_plane_rejected(self):
        proposals = copy.deepcopy(PROPOSALS)
        proposals['paths'][0]['layer'] = 'inner1'
        with self.assertRaisesRegex(ValueError, 'reserved layer'):
            SOURCE['make_regions'](proposals)

    def test_partial_via_span_rejected(self):
        proposals = copy.deepcopy(PROPOSALS)
        proposals['vias'] = [{'net': 'SIGNAL', 'x': 0, 'y': 0,
                             'layers': ['top', 'inner2'], 'hole_mm': .3, 'outer_mm': .7}]
        with self.assertRaisesRegex(ValueError, 'partial-span'):
            SOURCE['make_regions'](proposals)

    def test_self_intersecting_path_rejected(self):
        proposals = copy.deepcopy(PROPOSALS)
        proposals['paths'][0]['path_mm'] = [[0, 0], [1, 1], [0, 1], [1, 0]]
        with self.assertRaisesRegex(ValueError, 'self-intersecting'):
            SOURCE['make_regions'](proposals)


if __name__ == '__main__':
    unittest.main()
