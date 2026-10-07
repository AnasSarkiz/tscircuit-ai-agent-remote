import math
import runpy
import unittest
from pathlib import Path

from shapely.geometry import LineString, Point

planner = runpy.run_path(str(Path(__file__).parents[1]/'plan-coupled-speaker.py'))
width_audit = runpy.run_path(str(Path(__file__).parents[1]/'audit-region-widths.py'))


class CoupledSpeakerLanesTest(unittest.TestCase):
    def test_local_header_bend_preserves_pin_order_gap_and_length_skew(self):
        lanes = planner['multilayer_lanes']([('top', [(0., 0.), (0., 2.), (-2., 2.)])])
        positive = LineString(lanes['SPEAKER_P']['parts_mm'][0][1])
        negative = LineString(lanes['SPEAKER_N']['parts_mm'][0][1])
        self.assertGreater(positive.coords[-1][1], negative.coords[-1][1])
        self.assertGreaterEqual(positive.distance(negative)-.6, .2)
        self.assertAlmostEqual(abs(positive.length-negative.length), 1.604)
        self.assertLess(abs(positive.length-negative.length), 2.)

    def test_outer_layer_transition_has_two_distinct_real_via_sites(self):
        lanes = planner['multilayer_lanes']([
            ('top', [(0., 0.), (0., 2.)]), ('bottom', [(0., 2.), (-2., 2.)]),
        ])
        via_sites = []
        for lane in lanes.values():
            self.assertEqual([layer for layer, _ in lane['parts_mm']], ['top', 'bottom'])
            self.assertEqual(len(lane['transition_vias_mm']), 1)
            via = lane['transition_vias_mm'][0]
            self.assertEqual(lane['parts_mm'][0][1][-1], via)
            self.assertEqual(lane['parts_mm'][1][1][0], via)
            via_sites.append(via)
        self.assertGreater(Point(via_sites[0]).buffer(.225).distance(Point(via_sites[1]).buffer(.225)), .2)
        self.assertGreater(math.dist(*via_sites)-.3, .25)

    def test_disconnected_transition_and_sharp_reversal_are_rejected(self):
        for parts in ([('top', [(0., 0.), (0., 2.)]), ('bottom', [(1., 2.), (2., 2.)])],
                      [('top', [(0., 0.), (0., 2.), (0., 1.)])]):
            with self.assertRaises(ValueError):
                planner['multilayer_lanes'](parts)

    def test_retired_region_keeps_other_original_source_indices(self):
        first, retired, last = {'net': 'first'}, {'net': 'retired'}, {'net': 'last'}
        indices, regions = width_audit['active_source_regions']({
            'pours': [first, retired, last], 'retired_connection_region_indices': [1],
        })
        self.assertEqual(indices, [0, 2])
        self.assertEqual(regions, [first, last])
        self.assertEqual(width_audit['active_source_regions']({'pours': [first, last]})[0], [0, 1])

    def test_invalid_retirement_cannot_silently_remove_a_width_requirement(self):
        for indices in ([1], [-1], [True], [0, 0], ['0'], [{'index': 0}], None):
            with self.assertRaises(ValueError):
                width_audit['active_source_regions']({
                    'pours': [{'net': 'required'}], 'retired_connection_region_indices': indices,
                })


if __name__ == '__main__':
    unittest.main()
