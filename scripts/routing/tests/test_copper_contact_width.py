"""Real pad escapes must use native signal/power widths, not a universal neck."""
import runpy
import unittest
from pathlib import Path

from shapely.geometry import box

CONTACTS = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'plan-copper-contacts.py'))


def channel_fixture(gap_mm):
    circuit = [{'type': 'pcb_board', 'outline': [
        {'x': x, 'y': y} for x, y in [(-5, -5), (5, -5), (5, 5), (-5, 5)]]},
        {'type': 'source_net', 'source_net_id': 'signal', 'name': 'SIGNAL'},
        {'type': 'source_net', 'source_net_id': 'blocker', 'name': 'BLOCKER'}]
    for index, (x, y, width, height, net) in enumerate([
        (0, 0, .2, .2, 'signal'), (1.5, 0, .2, .2, 'signal'),
        (0, gap_mm / 2 + .5, 8, 1, 'blocker'), (0, -gap_mm / 2 - .5, 8, 1, 'blocker')]):
        circuit.extend([
            {'type': 'source_component', 'source_component_id': f'c{index}', 'name': f'C{index}'},
            {'type': 'source_port', 'source_port_id': f's{index}', 'source_component_id': f'c{index}', 'name': 'pin1'},
            {'type': 'pcb_port', 'pcb_port_id': f'p{index}', 'source_port_id': f's{index}', 'x': x, 'y': y},
            {'type': 'pcb_smtpad', 'pcb_smtpad_id': f'pad{index}', 'pcb_port_id': f'p{index}',
             'shape': 'rect', 'layer': 'top', 'x': x, 'y': y, 'width': width, 'height': height},
            {'type': 'source_trace', 'source_trace_id': f't{index}',
             'connected_source_port_ids': [f's{index}'], 'connected_source_net_ids': [net]}])
    return CONTACTS['Planner'](circuit)


class CopperContactWidthTests(unittest.TestCase):
    def test_signal_width_can_escape_where_universal_point_three_cannot(self):
        planner = channel_fixture(.65)
        specification = {'port': planner.ports['p0'], 'ground': box(1, -.1, 2, .1),
                         'width': CONTACTS['contact_width']({'name': 'SIGNAL'}, False)}
        self.assertIsNotNone(CONTACTS['contact_helpers']['plan_contact'](planner, specification))
        specification['width'] = .3
        self.assertIsNone(CONTACTS['contact_helpers']['plan_contact'](planner, specification))

    def test_power_width_rejects_an_undersized_point_three_escape(self):
        planner = channel_fixture(.9)
        specification = {'port': planner.ports['p0'], 'ground': box(1, -.1, 2, .1),
                         'width': CONTACTS['contact_width']({'name': 'POWER', 'trace_width': .5}, False)}
        self.assertIsNone(CONTACTS['contact_helpers']['plan_contact'](planner, specification))
        specification['width'] = .3
        self.assertIsNotNone(CONTACTS['contact_helpers']['plan_contact'](planner, specification))


if __name__ == '__main__':
    unittest.main()
