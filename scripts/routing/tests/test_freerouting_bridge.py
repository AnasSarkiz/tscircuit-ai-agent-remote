"""Transfers must preserve physical copper, net identity and fabrication rules."""
import argparse
import contextlib
import io
import json
import runpy
import tempfile
import unittest
from pathlib import Path

from shapely.geometry import Polygon, box
from shapely.ops import unary_union

BRIDGE = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'freerouting_bridge.py'))
DESIGN = '''(pcb test (parser (string_quote ")) (unit um) (resolution um 1000)
 (structure (layer top (type signal)) (layer inner1 (type signal))
 (layer inner2 (type signal)) (layer bottom (type signal))
 (boundary (rect pcb -5000 -5000 5000 5000))
 (rule (width 200) (clearance 210) (clearance 270 (type wire_area)))
 (plane SIGNAL (polygon bottom 0 -4000 -4000 4000 -4000 4000 4000 -4000 4000)
 (window (polygon bottom 0 -1000 -1000 1000 -1000 1000 1000 -1000 1000)))
 (keepout keep (rect top -4000 3000 -3000 4000)))
 (placement (component pad (place pad_0 2000 2000 front 0 (lock_type position))))
 (library (image pad (pin pad_stack 1 0 0))
 (padstack pad_stack (shape (rect top -100 -100 100 100)) (attach off))
 (padstack through (shape (circle top 700 0 0)) (shape (circle inner1 700 0 0))
 (shape (circle inner2 700 0 0)) (shape (circle bottom 700 0 0)) (attach off)))
 (network (net SIGNAL (pins pad_0-1))
 (class ROUTE_SIGNAL SIGNAL (circuit (use_via through)) (rule (width 300))))
 (wiring (wire (path top 300 1000 2000 2000 2000) (net SIGNAL) (type fix))
 (via through 1000 2000 (net SIGNAL) (type fix))))'''
SESSION = '''(session test (base_design original.dsn)
 (placement (resolution um 1000) (component pad (place pad_0 2000000 2000000 front 0)))
 (was_is) (routes (resolution um 1000)
 (library_out (padstack through (shape (circle top 700000 0 0))
 (shape (circle inner1 700000 0 0)) (shape (circle inner2 700000 0 0))
 (shape (circle bottom 700000 0 0))))
 (network_out (net SIGNAL (wire (path top 300000 1000000 2000000 2000000 2000000))
 (via through 1000000 2000000)))))'''


class FreeroutingBridgeTests(unittest.TestCase):
    def parse_session(self, session):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, manifest, qualification = root / 'circuit.json', root / 'original.dsn.manifest.json', root / 'qualified.json'
            source.write_text(json.dumps([{'type': 'source_net', 'name': 'SIGNAL', 'trace_width': .3}]))
            manifest.write_text(json.dumps({'source_circuit_json': str(source),
                'source_sha256': BRIDGE['sha256'](source), 'dsn_sha256': 'fixture-input-sha',
                'expected_engine_grid_mm': .00001,
                'active_nets': ['SIGNAL'], 'pins': {'pad_0-1': {'center_mm': [2, 2]}},
                'via_padstacks': {'through': {'outer_mm': .7, 'hole_mm': .3, 'layers': list(BRIDGE['LAYERS'])}}}))
            qualification.write_text(json.dumps({'qualified': True, 'original_sha256': 'fixture-input-sha',
                'actual_engine_pad_topology_checked': True, 'actual_engine_grid_mm': .00001,
                'active_net_semantics_checked': True}))
            session_path, output = root / 'result.ses', root / 'proposals.json'
            session_path.write_text(session)
            arguments = argparse.Namespace(session=session_path, manifest=manifest,
                                           qualification=qualification, output_json=output)
            with contextlib.redirect_stdout(io.StringIO()):
                BRIDGE['session_proposals'](arguments)
            return json.loads(output.read_text())

    def compare(self, transferred):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original, roundtrip = root / 'original.dsn', root / 'roundtrip.dsn'
            original.write_text(DESIGN)
            roundtrip.write_text(transferred)
            arguments = argparse.Namespace(original_dsn=original, roundtrip_dsn=roundtrip,
                                           output_json=root / 'result.json')
            with contextlib.redirect_stdout(io.StringIO()):
                BRIDGE['verify_transfer'](arguments)

    def test_exact_transfer_accepts_actual_geometry(self):
        self.compare(DESIGN)

    def test_separately_quoted_component_pin_identifiers(self):
        self.compare(DESIGN.replace('(pins pad_0-1)', '(pins "pad_0"-"1")'))

    def test_polyline_path_uses_infinite_line_intersections(self):
        polygon = ['polyline_path', 'top', '300', '1000', '1000', '1000', '3000',
                   '0', '2000', '3000', '2000', '2000', '1000', '2000', '3000']
        _, original = BRIDGE['dsn_shape'](['path', 'top', '300', '1000', '2000', '2000', '2000'], .001)
        _, transferred = BRIDGE['dsn_shape'](polygon, .001)
        self.assertLess(original.symmetric_difference(transferred).area, 1e-12)

    def test_lost_pour_window_rejected(self):
        with self.assertRaisesRegex(ValueError, 'pours .*changed'):
            self.compare(DESIGN.replace('(window (polygon bottom 0 -1000 -1000 1000 -1000 1000 1000 -1000 1000))', ''))

    def test_moved_pad_rejected(self):
        with self.assertRaisesRegex(ValueError, 'pads .*changed'):
            self.compare(DESIGN.replace('pad_0 2000 2000', 'pad_0 2100 2000'))

    def test_old_wire_lost_protection_rejected(self):
        with self.assertRaisesRegex(ValueError, 'SYSTEM_FIXED'):
            self.compare(DESIGN.replace('(type fix)', '(type protect)', 1))

    def test_partial_via_layer_span_rejected(self):
        with self.assertRaisesRegex(ValueError, 'layer span'):
            self.compare(DESIGN.replace('(shape (circle inner2 700 0 0))', ''))

    def test_weakened_clearance_rejected(self):
        with self.assertRaisesRegex(ValueError, 'rule was omitted or weakened'):
            self.compare(DESIGN.replace('(clearance 210)', '(clearance 190)'))

    def test_weakened_net_width_rejected(self):
        with self.assertRaisesRegex(ValueError, 'trace width was reduced'):
            self.compare(DESIGN.replace('(rule (width 300))', '(rule (width 200))'))

    def test_concave_pad_exact_decomposition(self):
        contour = Polygon([(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)])
        pieces = BRIDGE['convex_pieces'](contour)
        self.assertGreater(len(pieces), 1)
        self.assertEqual(unary_union(pieces).symmetric_difference(contour).area, 0)
        self.assertTrue(all(piece.convex_hull.equals(piece) for piece in pieces))

    def test_sub_geometry_tolerance_gap_still_rejects_split_pad(self):
        shapes = {('pcb_smtpad_1_0-1', 'top'): box(0, 0, 1, 1),
                  ('pcb_smtpad_1_1-1', 'top'): box(1.000005, 0, 2, 1)}
        with self.assertRaisesRegex(ValueError, 'split into disconnected'):
            BRIDGE['verify_native_pad_topology'](shapes)

    def test_touching_pad_pieces_preserve_topology(self):
        shapes = {('pcb_smtpad_1_0-1', 'top'): box(0, 0, 1, 1),
                  ('pcb_smtpad_1_1-1', 'top'): box(1, 0, 2, 1)}
        self.assertEqual(BRIDGE['verify_native_pad_topology'](shapes), 1)

    def test_signal_pad_metal_must_not_mark_net_as_plane(self):
        manifest = {'active_nets': ['SIGNAL']}
        engine = {'nets': [{'name': 'SIGNAL', 'contains_plane': True, 'net_class': 'ROUTE_SIGNAL'}]}
        with self.assertRaisesRegex(ValueError, 'classified as a plane'):
            BRIDGE['verify_active_net_semantics'](manifest, engine)
        engine['nets'][0]['contains_plane'] = False
        BRIDGE['verify_active_net_semantics'](manifest, engine)

    def test_preserved_class_cannot_silently_disable_active_net(self):
        manifest = {'active_nets': ['SIGNAL']}
        engine = {'nets': [{'name': 'SIGNAL', 'contains_plane': False, 'net_class': 'PRESERVE'}]}
        with self.assertRaisesRegex(ValueError, 'lost its routing class'):
            BRIDGE['verify_active_net_semantics'](manifest, engine)

    def test_pour_partition_preserves_holes_and_shared_edges(self):
        import math
        ring = [(1 + .4 * math.cos(index * math.tau / 512), 1 + .4 * math.sin(index * math.tau / 512))
                for index in range(512)]
        contour = Polygon([(-6, -6), (6, -6), (6, 6), (-6, 6)], [ring])
        pieces = BRIDGE['partition_pour'](contour, 5)
        self.assertGreater(len(pieces), 1)
        reconstructed = unary_union(pieces)
        self.assertLess(reconstructed.symmetric_difference(contour).area, 1e-12)
        self.assertEqual(reconstructed.geom_type, 'Polygon')
        self.assertEqual(len(reconstructed.interiors), 1)

    def test_pill_primitives_preserve_true_curved_copper(self):
        record = {'shape': 'pill', 'x': 2, 'y': 3, 'width': .3, 'height': 1.2, 'ccw_rotation': 90}
        contour = BRIDGE['AUDIT']['pad_contour'](record)
        primitives = BRIDGE['native_pad_primitives'](record, contour)
        reconstructed = unary_union([primitive['contour'] for primitive in primitives])
        self.assertEqual(len(primitives), 3)
        self.assertLess(reconstructed.symmetric_difference(contour).area, 1e-12)
        self.assertEqual(reconstructed.geom_type, 'Polygon')

    def test_radius_only_native_circle_keeps_diameter(self):
        record = {'shape': 'circle', 'x': 2, 'y': 3, 'radius': 1}
        contour = BRIDGE['AUDIT']['pad_contour'](record)
        primitive = BRIDGE['native_pad_primitives'](record, contour)[0]
        self.assertEqual(primitive['circle_diameter_mm'], 2)

    def test_polygon_pad_without_center_uses_its_authentic_vertices(self):
        contour = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        primitives = BRIDGE['native_pad_primitives']({'shape': 'polygon'}, contour)
        self.assertTrue(primitives[0]['contour'].equals(contour))

    def test_session_cannot_masquerade_as_qualified_design(self):
        with tempfile.TemporaryDirectory() as directory:
            session = Path(directory) / 'result.ses'
            session.write_text('(session test (routes (resolution um 1000)))')
            with self.assertRaisesRegex(ValueError, 'not a session'):
                BRIDGE['design_snapshot'](session)

    def test_session_integer_resolution_is_nanometres_not_micrometres(self):
        proposals = self.parse_session(SESSION)
        self.assertEqual(proposals['paths'][0]['path_mm'], [[1, 2], [2, 2]])
        self.assertAlmostEqual(proposals['paths'][0]['width_mm'], .3)
        self.assertEqual(proposals['vias'][0]['x'], 1)
        self.assertEqual(proposals['vias'][0]['layers'], ['top', 'inner1', 'inner2', 'bottom'])

    def test_official_cli_extensionless_base_design_accepted(self):
        proposals = self.parse_session(SESSION.replace('(base_design original.dsn)', '(base_design original)'))
        self.assertEqual(len(proposals['paths']), 1)

    def test_other_base_design_rejected(self):
        with self.assertRaisesRegex(ValueError, 'different base design'):
            self.parse_session(SESSION.replace('(base_design original.dsn)', '(base_design other)'))

    def test_session_unknown_drill_stack_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Unknown or undersized'):
            self.parse_session(SESSION.replace('(via through', '(via UNKNOWN'))

    def test_session_changed_resolution_rejected(self):
        with self.assertRaisesRegex(ValueError, 'unit/resolution differs'):
            self.parse_session(SESSION.replace('(resolution um 1000)', '(resolution um 100)'))

    def test_session_on_reserved_ground_layer_rejected(self):
        with self.assertRaisesRegex(ValueError, 'reserved GND layer'):
            self.parse_session(SESSION.replace('(path top', '(path inner1'))

    def test_session_changed_pad_placement_rejected(self):
        with self.assertRaisesRegex(ValueError, 'moved or rotated'):
            self.parse_session(SESSION.replace('pad_0 2000000', 'pad_0 2100000'))

    def test_session_new_copper_on_preserved_net_rejected(self):
        with self.assertRaisesRegex(ValueError, 'preserved net'):
            self.parse_session(SESSION.replace('(net SIGNAL', '(net GND'))

    def test_session_reduced_wire_width_rejected(self):
        with self.assertRaisesRegex(ValueError, 'reduced required width'):
            self.parse_session(SESSION.replace('top 300000', 'top 290000'))


if __name__ == '__main__':
    unittest.main()
