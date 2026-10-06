"""A dense search finds small legal slots without changing clearance obstacles."""
import math
import runpy
import unittest
from pathlib import Path
from shapely.geometry import Point, box

candidates = runpy.run_path(str(Path(__file__).parents[1] / 'plan-microphone-ground-traces.py'))['ground_via_candidates']


class GroundViaCandidateTests(unittest.TestCase):
    def test_dense_search_finds_slot_between_coarse_angles(self):
        obstacles = box(-7, -7, 7, 7).difference(box(1.02, .07, 1.03, .08))
        specification = {'origin': (0, 0), 'via_obstacles': obstacles}
        coarse = candidates(specification)
        self.assertFalse(any(not Point(xy).intersects(obstacles) for xy in coarse))
        dense = candidates({**specification, 'grid_mm': .025})
        self.assertEqual(dense, [(1.025, .075)])
        self.assertFalse(Point(dense[0]).intersects(obstacles))

    def test_dense_search_obeys_annulus_and_exact_obstacles(self):
        obstacles = box(-7, -7, .5, 7)
        dense = candidates({'origin': (0, 0), 'grid_mm': .05, 'via_obstacles': obstacles})
        self.assertTrue(dense)
        for xy in dense:
            self.assertGreaterEqual(math.hypot(*xy) + 1e-10, .9)
            self.assertLessEqual(math.hypot(*xy), 6. + 1e-10)
            self.assertFalse(Point(xy).intersects(obstacles))

    def test_search_radius_does_not_replace_exact_clearance_obstacles(self):
        obstacles = box(-7, -7, 7, 7).difference(box(.62, -.005, .63, .005))
        specification = {'origin': (0, 0), 'grid_mm': .025, 'via_obstacles': obstacles}
        self.assertEqual(candidates(specification), [])
        dense = candidates({**specification, 'minimum_distance_mm': .4})
        self.assertEqual(dense, [(.625, 0.)])
        self.assertFalse(Point(dense[0]).intersects(obstacles))


if __name__ == '__main__':
    unittest.main()
