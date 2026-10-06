"""A new through drill cannot leave an illegal nearby transition available."""
import runpy
import unittest
from pathlib import Path
from types import SimpleNamespace
import numpy as np

helpers = runpy.run_path(str(Path(__file__).parents[1] / 'plan-power-copper.py'))


class ProspectiveViaReachabilityTests(unittest.TestCase):
    def test_new_drill_removes_only_available_nearby_layer_transition(self):
        xs, ys = np.meshgrid(np.array([-1., -.5, 0., .5, 1.]), np.array([0.]))
        planner = SimpleNamespace(grid_x=xs, grid_y=ys)
        original_blocked = np.zeros(xs.shape, dtype=bool)
        labels = [np.array([[1,1,1,1,0]]), np.array([[0,0,0,2,2]])]
        starts, targets = [(0,0,2)], [(1,0,4)]
        self.assertTrue(helpers['multilayer_components_reachable'](labels, original_blocked, starts, targets))
        reserved = helpers['prospective_via_blocked'](planner, {
            'via_blocked': original_blocked, 'target': (0., 0.), 'via_hole_mm': .3})
        self.assertEqual(reserved.tolist(), [[False,True,True,True,False]])
        self.assertFalse(helpers['multilayer_components_reachable'](labels, reserved, starts, targets))
        self.assertFalse(original_blocked.any())


if __name__ == '__main__':
    unittest.main()
