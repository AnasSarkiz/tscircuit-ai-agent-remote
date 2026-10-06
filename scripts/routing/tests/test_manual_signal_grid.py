"""Verify fine pin-escape grids and disconnected free-space rejection."""
import runpy
import unittest
from pathlib import Path

import numpy as np
from shapely.geometry import LineString, Point, box
from shapely.ops import unary_union

helpers = runpy.run_path(str(Path(__file__).parents[1] / 'plan-manual-signals.py'))
Planner = helpers['ManualSignalPlanner']
power_helpers = runpy.run_path(str(Path(__file__).parents[1] / 'plan-power-copper.py'))


class ManualSignalGridTests(unittest.TestCase):
    def planner(self):
        return Planner([{'type': 'pcb_board', 'outline': [
            {'x': x, 'y': y} for x, y in [(-25, -32.5), (25, -32.5), (25, 32.5), (-25, 32.5)]]}])

    def test_fine_grid_resolves_a_corridor_between_coarse_rows(self):
        planner = self.planner()
        obstacles = unary_union([box(-.4, -33, .4, .015), box(-.4, .085, .4, 33)])
        endpoints = ((-2, .05), (2, .05), obstacles)
        self.assertIsNone(planner.grid_route(endpoints))
        planner.set_grid(.05)
        route = planner.grid_route(endpoints)
        self.assertIsNotNone(route)
        self.assertFalse(LineString(route).intersects(obstacles))

    def test_separate_free_space_islands_have_no_route(self):
        self.assertIsNone(self.planner().grid_route(((-2, 0), (2, 0), box(-.4, -33, .4, 33))))

    def test_round_obstacle_grazing_an_edge_gets_a_clear_detour(self):
        obstacle = Point(.05, -.699).buffer(1, quad_segs=128)
        route = self.planner().grid_route(((-1, .3), (1, .3), obstacle))
        self.assertIsNotNone(route)
        self.assertFalse(LineString(route).intersects(obstacle))

    def test_via_escape_uses_the_clear_detour_past_a_round_obstacle(self):
        obstacle = Point(.05, -.699).buffer(1, quad_segs=128)
        via_obstacles = box(-30, -40, 30, 40).difference(box(.99, .29, 1.01, .31))
        exits = self.planner().grid_escape((-1, .3), (obstacle, via_obstacles))
        self.assertTrue(exits)
        self.assertTrue(all(not LineString(route).intersects(obstacle) for _, route in exits))

    def test_escape_mask_rejects_unreachable_ordinary_via_exits(self):
        planner = self.planner()
        allowed = np.zeros(planner.grid_x.shape,dtype=bool)
        allowed |= (planner.grid_x > 1.8) & (abs(planner.grid_y) < .1)
        exits = planner.grid_escape((-1,0), (box(10,10,11,11),box(12,12,13,13),allowed))
        self.assertTrue(exits)
        self.assertTrue(all(position[0]>1.8 for position,route in exits))
        with self.assertRaises(ValueError):
            planner.grid_escape((-1,0), (box(10,10,11,11),box(12,12,13,13),np.zeros((2,2),dtype=bool)))

    def test_diagonal_contact_does_not_connect_free_grid_components(self):
        labels = helpers['connected_grid_labels'](np.array([[False, True], [True, False]]))
        self.assertNotEqual(labels[0, 0], labels[1, 1])

    def test_multiple_scanline_runs_join_through_a_later_row(self):
        labels = helpers['connected_grid_labels'](np.array([[False, True, False], [False, False, False]]))
        self.assertEqual(labels[0, 0], labels[0, 2])
        self.assertEqual(labels[0, 0], labels[1, 1])

    def test_layer_components_need_a_legal_via_at_both_crossings(self):
        labels = [np.array([[1, 1, 0, 2, 2]]), np.array([[3, 3, 3, 3, 3]])]
        starts, targets = [(0, 0, 0)], [(0, 0, 4)]
        reachable = power_helpers['multilayer_components_reachable']
        self.assertTrue(reachable(labels, np.array([[False, True, True, True, False]]), starts, targets))
        self.assertFalse(reachable(labels, np.array([[False, True, True, True, True]]), starts, targets))

    def test_qualified_usb_exit_preserves_the_required_copper_clearance(self):
        circuit = [{'type': 'pcb_board', 'outline': [
            {'x': x, 'y': y} for x, y in [(-25, -32.5), (25, -32.5), (25, 32.5), (-25, 32.5)]]}]
        for index in range(2):
            circuit.extend([
                {'type': 'source_net', 'source_net_id': f'net_{index}', 'name': f'NET_{index}'},
                {'type': 'source_component', 'source_component_id': f'component_{index}', 'name': f'PIN_{index}'},
                {'type': 'source_port', 'source_port_id': f'source_port_{index}', 'source_component_id': f'component_{index}', 'name': 'pin1'},
                {'type': 'pcb_port', 'pcb_port_id': f'port_{index}', 'source_port_id': f'source_port_{index}', 'x': index * .5, 'y': 0},
                {'type': 'pcb_smtpad', 'pcb_smtpad_id': f'pad_{index}', 'pcb_port_id': f'port_{index}',
                 'shape': 'rect', 'layer': 'top', 'x': index * .5, 'y': 0, 'width': .3, 'height': 1.3},
                {'type': 'source_trace', 'source_trace_id': f'trace_{index}',
                 'connected_source_port_ids': [f'source_port_{index}'], 'connected_source_net_ids': [f'net_{index}']},
            ])
        planner = Planner(circuit)
        root = planner.root('net_0')
        self.assertTrue(Point(0, 0).intersects(planner.obstacles(root, 'top', .2979)))
        planner.set_copper_reserve(.0001)
        self.assertFalse(Point(0, 0).intersects(planner.obstacles(root, 'top', .2979)))
        foreign_pad = box(.35, -.65, .65, .65)
        actual_copper = LineString([(0, 0), (0, 2)]).buffer(.2979 / 2)
        self.assertGreaterEqual(actual_copper.distance(foreign_pad), .2)
        with self.assertRaises(ValueError):
            planner.set_copper_reserve(-.01)
        proposal = {'net': 'NET_0', 'from': '.PIN_0 > .pin1', 'to': '.PIN_1 > .pin1',
                    'width': .2, 'global_path_mm': [(0, 0), (.5, 0)],
                    'segment_layers': ['top', 'top'], 'pcbPath': []}
        with self.assertRaises(ValueError):
            planner.reserve_proposals({'paths': [proposal]})
        circuit[-1]['connected_source_net_ids'] = ['net_0']
        planner = Planner(circuit)
        self.assertNotEqual(planner.physical_root('port_0'), planner.physical_root('port_1'))
        planner.reserve_proposals({'paths': [proposal]})
        self.assertEqual(planner.physical_root('port_0'), planner.physical_root('port_1'))
        # Reservation changes planning only; the untouched circuit remains open.
        audit = helpers['geometry_helpers']['audit'](circuit)
        self.assertEqual(audit['physically_open_net_count'], 1)


if __name__ == '__main__':
    unittest.main()
