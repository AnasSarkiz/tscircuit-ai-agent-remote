"""Reject current-critical regulator profiles that violate the local escape contract."""
import copy
import json
import runpy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDIT = runpy.run_path(str(ROOT / 'scripts/routing/audit-regulator-switch-widths.py'))['audit']


class RegulatorSwitchWidths(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = json.loads((ROOT / 'dist/index/circuit.json').read_text())

    def candidate(self):
        circuit = copy.deepcopy(self.native)
        source = next(r for r in circuit if r['type'] == 'source_trace' and r.get('name') == 'REG_L1')
        trace = next(r for r in circuit if r['type'] == 'pcb_trace' and r['source_trace_id'] == source['source_trace_id'])
        return circuit, trace

    def test_actual_native_has_both_qualified_local_profiles(self):
        self.assertEqual({r['name'] for r in AUDIT(self.native)}, {'REG_L1', 'REG_L2'})

    def test_undersized_escape_is_rejected(self):
        circuit, trace = self.candidate()
        trace['route'][0]['width'] = .274
        with self.assertRaises(AssertionError):
            AUDIT(circuit)

    def test_inner_layer_switch_path_is_rejected(self):
        circuit, trace = self.candidate()
        for point in trace['route']:
            point['layer'] = 'inner1'
        with self.assertRaises(AssertionError):
            AUDIT(circuit)

    def test_missing_wide_trunk_is_rejected(self):
        circuit, trace = self.candidate()
        for point in trace['route']:
            point['width'] = min(point['width'], .7)
        with self.assertRaises(AssertionError):
            AUDIT(circuit)

    def test_extended_narrow_escape_is_rejected(self):
        circuit, trace = self.candidate()
        trace['route'][1]['x'] += 2
        with self.assertRaises(AssertionError):
            AUDIT(circuit)
