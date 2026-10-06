"""A replacement signal cannot invalidate retained power copper or its anchors."""
import runpy
import unittest
from pathlib import Path
from types import SimpleNamespace
from shapely.geometry import LineString, Point

helpers = runpy.run_path(str(Path(__file__).parents[1] / 'plan-speaker-and-vsys.py'))


def region_record(specification):
    contour = LineString(specification['points']).buffer(.5, cap_style=2)
    return {'source': 'power.json', 'index': specification['index'], 'region': {
        'net': 'VSYS', 'layer': 'top', 'nominal_width_mm': 1.,
        'path_mm': specification['points'],
        'outline': [{'x': x, 'y': y} for x, y in list(contour.exterior.coords)[:-1]]}}


class VsysAnchorPreservationTests(unittest.TestCase):
    def test_only_clear_original_strips_join_anchor_groups(self):
        anchors = [(0., 0.), (4., 0.), (8., 0.), (12., 0.)]
        regions = [region_record({'index': index, 'points': [anchors[index], anchors[index+1]]})
                   for index in range(3)]
        planner = SimpleNamespace(copper=[])
        retained, groups = helpers['retained_anchor_groups'](planner, {
            'anchors': anchors, 'root': 'VSYS', 'source_regions': regions,
            'speaker_copper': [('SPEAKER_N', 'top', LineString([(2., -1.), (2., 1.)]).buffer(.3))],
            # The second strip clears the signal copper but crosses its real
            # through drill, so it must also be replaced.
            'speaker_drills': [Point(6., 0.).buffer(.15)]})
        self.assertEqual([record['index'] for record in retained], [2])
        self.assertEqual(groups, [[anchors[0]], [anchors[1]], [anchors[2], anchors[3]]])
        self.assertEqual(len(planner.copper), 1)


if __name__ == '__main__':
    unittest.main()
