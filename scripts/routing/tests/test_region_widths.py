"""Regression coverage for nominal strip width and route termination geometry."""
import contextlib
import io
import json
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class RegionWidthTests(unittest.TestCase):
    def check_width(self, actual_width_mm):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            circuit = root/'circuit.json'
            regions = root/'regions.json'
            result = root/'result.json'
            circuit.write_text(json.dumps([
                {'type': 'source_net', 'name': 'SIGNAL', 'source_net_id': 'source_net_0'},
                {'type': 'pcb_copper_pour', 'pcb_copper_pour_id': 'pcb_copper_pour_0',
                 'source_net_id': 'source_net_0', 'layer': 'bottom', 'shape': 'brep',
                 'brep_shape': {'outer_ring': {'vertices': [
                     {'x': -1, 'y': -actual_width_mm/2}, {'x': 1, 'y': -actual_width_mm/2},
                     {'x': 1, 'y': actual_width_mm/2}, {'x': -1, 'y': actual_width_mm/2}]},
                     'inner_rings': []}}]))
            regions.write_text(json.dumps({'pours': [{'net': 'SIGNAL', 'layer': 'bottom',
                'nominal_width_mm': .3, 'path_mm': [[-1, 0], [1, 0]]}]}))
            script = Path(__file__).resolve().parents[1]/'audit-region-widths.py'
            helper = runpy.run_path(str(script))
            with patch.object(sys, 'argv', [str(script), str(circuit), str(regions), str(result)]), contextlib.redirect_stdout(io.StringIO()):
                status = helper['main']()
            return status, json.loads(result.read_text())

    def test_flat_termination_does_not_falsely_require_copper_beyond_endpoint(self):
        status, result = self.check_width(.3)
        self.assertEqual(status, 0)
        self.assertEqual(result['failed_region_count'], 0)

    def test_actual_strip_narrowing_fails(self):
        status, result = self.check_width(.29)
        self.assertEqual(status, 1)
        self.assertEqual(result['failed_region_count'], 1)
        self.assertGreater(result['measurements'][0]['uncovered_required_copper_mm2'], .019)


if __name__ == '__main__':
    unittest.main()
