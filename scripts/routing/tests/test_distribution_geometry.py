"""Ordinary outer traces do not receive the rectangular pour-cutout expansion."""
import runpy
import unittest
from pathlib import Path
from shapely.geometry import Point, box

helpers = runpy.run_path(str(Path(__file__).parents[1] / 'plan-power-copper.py'))


class DistributionGeometryTests(unittest.TestCase):
    def test_wire_uses_actual_clearance_without_pour_corner_cutouts(self):
        pad = box(0, 0, 1, 1)
        planner = helpers['Planner'].__new__(helpers['Planner'])
        planner.parent = {}
        planner.pads = [({'layer': 'top', 'pcb_port_id': 'p'}, pad)]
        planner.ports = {'p': {'source_port_id': 'foreign'}}
        planner.copper = []
        planner.holes = []
        planner.plated_hole_roots = {}
        planner.keepouts = []
        planner.board = box(-5,-5,5,5)
        planner.copper_clearance = .21
        specification = {'root': 'speaker', 'width': .8, 'layer': 'top', 'new_vias': []}
        centre = Point(1.48, 1.48)
        self.assertGreater(centre.distance(pad) - .4, .21)
        self.assertTrue(helpers['distribution_obstacles'](planner, specification).covers(centre))
        self.assertFalse(helpers['distribution_obstacles'](planner, {
            **specification, 'routing_geometry': 'native_wire'}).covers(centre))

    def test_wire_rejects_inner_layer_and_unknown_geometry(self):
        specification = {'root': 'speaker', 'width': .6, 'layer': 'inner1',
                         'new_vias': [], 'routing_geometry': 'native_wire'}
        with self.assertRaises(ValueError):
            helpers['distribution_obstacles'](None, specification)
        with self.assertRaises(ValueError):
            helpers['distribution_obstacles'](None, {
                **specification, 'routing_geometry': 'unsupported'})


if __name__ == '__main__':
    unittest.main()
