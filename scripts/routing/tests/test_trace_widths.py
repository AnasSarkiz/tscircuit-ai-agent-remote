"""Catch undersized power routes missed by a global minimum-width check."""
import copy
import runpy
import unittest
from pathlib import Path

AUDIT = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'audit-trace-widths.py'))
BASE = [
    {'type': 'source_net', 'source_net_id': 'rail', 'name': 'POWER', 'trace_width': 1.0},
    {'type': 'source_trace', 'source_trace_id': 'branch', 'connected_source_port_ids': ['pin'],
     'connected_source_net_ids': ['rail'], 'min_trace_thickness': .3},
    {'type': 'pcb_trace', 'pcb_trace_id': 'wire', 'source_trace_id': 'branch', 'route': [
        {'route_type': 'wire', 'x': 0, 'y': 0, 'layer': 'top', 'width': .3},
        {'route_type': 'wire', 'x': 1, 'y': 0, 'layer': 'top', 'width': .3}]},
]


class TraceWidthTests(unittest.TestCase):
    def test_power_neck_meets_global_minimum_but_requires_net_width_review(self):
        result = AUDIT['audit'](BASE)
        self.assertEqual(result['trace_count_below_board_minimum'], 0)
        self.assertEqual(result['trace_count_below_source_minimum'], 0)
        self.assertEqual(result['trace_count_below_net_nominal'], 1)
        self.assertFalse(result['current_capacity_qualified'])

    def test_unnamed_switch_trace_still_checks_explicit_source_minimum(self):
        circuit = copy.deepcopy(BASE[1:])
        circuit[0]['connected_source_net_ids'] = []
        circuit[0]['min_trace_thickness'] = 1
        result = AUDIT['audit'](circuit)
        self.assertEqual(result['trace_count_below_source_minimum'], 1)
        self.assertIsNone(result['measurements'][0]['net'])

    def test_width_change_is_measured_segment_by_segment(self):
        circuit = copy.deepcopy(BASE)
        circuit[-1]['route'][1]['width'] = 1
        circuit[-1]['route'].append({'route_type': 'wire', 'x': 2, 'y': 0, 'layer': 'top', 'width': 1})
        trace = AUDIT['audit'](circuit)['measurements'][0]
        self.assertEqual([segment['width_mm'] for segment in trace['segments']], [.3, 1])
        self.assertEqual(trace['wire_length_mm'], 2)

    def test_missing_named_net_width_does_not_invent_a_nominal_requirement(self):
        circuit = copy.deepcopy(BASE)
        del circuit[0]['trace_width']
        self.assertEqual(AUDIT['audit'](circuit)['trace_count_below_net_nominal'], 0)

    def test_board_minimum_detects_undersized_signal(self):
        circuit = copy.deepcopy(BASE)
        circuit[-1]['route'][0]['width'] = .199
        self.assertEqual(AUDIT['audit'](circuit)['trace_count_below_board_minimum'], 1)

    def test_interpolation_cannot_be_silently_treated_as_constant_width(self):
        circuit = copy.deepcopy(BASE)
        circuit[-1]['route_thickness_mode'] = 'interpolated'
        with self.assertRaisesRegex(ValueError, 'Unsupported thickness mode'):
            AUDIT['audit'](circuit)

    def test_layer_jump_and_nonfinite_width_are_rejected(self):
        circuit = copy.deepcopy(BASE)
        circuit[-1]['route'][1]['layer'] = 'bottom'
        with self.assertRaisesRegex(ValueError, 'changes layer'):
            AUDIT['audit'](circuit)
        circuit[-1]['route'][1]['layer'] = 'top'
        circuit[-1]['route'][0]['width'] = float('nan')
        with self.assertRaisesRegex(ValueError, 'Invalid width'):
            AUDIT['audit'](circuit)

    def test_named_net_merge_is_rejected(self):
        circuit = copy.deepcopy(BASE)
        circuit.append({'type': 'source_net', 'source_net_id': 'other', 'name': 'OTHER'})
        circuit[1]['connected_source_net_ids'].append('other')
        with self.assertRaisesRegex(ValueError, 'Merged named nets'):
            AUDIT['audit'](circuit)


if __name__ == '__main__':
    unittest.main()
