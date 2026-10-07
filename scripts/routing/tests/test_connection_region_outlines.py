"""Authored strip outlines retain copper without rounded zero-length edges."""
import runpy
import unittest
from pathlib import Path
from shapely.geometry import LineString, Polygon

region_records = runpy.run_path(str(Path(__file__).parents[1]/'plan-connection-bridges.py'))['region_records']


class ConnectionRegionOutlines(unittest.TestCase):
    def test_near_grid_endpoints_have_no_zero_length_edges(self):
        points = [[-19.999999999999936,-6.999999999999645],[-19.199999999999925,-8.199999999999662]]
        region = region_records('V3V3', {'parts':[('bottom',points)],'width':.8,'drawn_width_mm':.802})[0]
        vertices = region['outline']
        self.assertTrue(all(first != last for first,last in zip(vertices,vertices[1:]+vertices[:1])))
        actual = Polygon([(point['x'],point['y']) for point in vertices])
        required = LineString(points).buffer(.4,cap_style=2)
        self.assertTrue(actual.is_valid)
        self.assertLess(required.difference(actual.buffer(.000001)).area,1e-8)

    def test_bent_strip_preserves_its_rounded_copper_shape(self):
        points = [[1,1],[3,2],[3,5]]
        region = region_records('TEST', {'parts':[('top',points)],'width':.3,'drawn_width_mm':.302})[0]
        vertices = region['outline']
        actual = Polygon([(point['x'],point['y']) for point in vertices])
        contour = LineString(points).buffer(.151,quad_segs=64,cap_style=2,join_style=1).union(LineString(points).buffer(.15,quad_segs=64,cap_style=2,join_style=1))
        original_rounded = Polygon([(round(x,6),round(y,6)) for x,y in contour.exterior.coords])
        self.assertTrue(actual.equals(original_rounded))
        self.assertTrue(all(first != last for first,last in zip(vertices,vertices[1:]+vertices[:1])))
