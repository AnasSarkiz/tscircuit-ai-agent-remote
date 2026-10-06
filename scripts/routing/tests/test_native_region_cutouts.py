"""A clearance-legal diagonal must still preserve width after native clipping."""
import runpy
import unittest
from pathlib import Path
from types import SimpleNamespace
from shapely.geometry import Point, box

helpers = runpy.run_path(str(Path(__file__).resolve().parents[1]/'plan-power-copper.py'))


class NativeRegionCutoutTests(unittest.TestCase):
    def planner(self):
        return SimpleNamespace(pads=[({'layer': 'top', 'pcb_port_id': 'p'}, box(0,0,1,1))],
            ports={'p': {'source_port_id': 'foreign'}}, root=lambda identity: identity,
            copper=[], holes=[], plated_hole_roots={}, keepouts=[], board=box(-5,-5,5,5))

    def test_square_pad_margin_prevents_a_native_width_neck(self):
        centre = Point(1.48,1.48)
        pad = box(0,0,1,1)
        # Actual contour clearance can pass while the native rectangular pour
        # cutout intersects the requested 0.8-mm strip radius at a diagonal.
        self.assertGreater(centre.distance(pad)-.4, .21)
        self.assertTrue(centre.buffer(.4).intersects(box(-.21,-.21,1.21,1.21)))
        obstacles = helpers['inner_obstacles'](self.planner(), {
            'root': 'supply', 'width': .802, 'layer': 'top',
            'new_vias': [], 'copper_clearance_mm': .27})
        self.assertTrue(obstacles.covers(centre))
        self.assertFalse(obstacles.covers(Point(1.9,1.9)))

    def test_same_net_pad_remains_a_valid_contact(self):
        obstacles = helpers['inner_obstacles'](self.planner(), {
            'root': 'foreign', 'width': .802, 'layer': 'top', 'new_vias': []})
        self.assertFalse(obstacles.covers(Point(.5,.5)))


if __name__ == '__main__':
    unittest.main()
