"""Native rounded SMT pads retain their actual arcs, bounds and rotation."""
import math,runpy,unittest
from pathlib import Path
from shapely.geometry import Point
pad=runpy.run_path(str(Path(__file__).parents[1]/'audit-copper.py'))['pad_contour']


class NativePadCornerTests(unittest.TestCase):
    def test_native_corner_radius_has_actual_curved_copper(self):
        shape=pad({'shape':'rotated_rect','x':0,'y':0,'width':2,'height':1,'corner_radius':.2,'ccw_rotation':0})
        self.assertEqual(shape.bounds,(-1,-.5,1,.5))
        self.assertFalse(shape.covers(Point(.95,.45)))
        self.assertTrue(shape.covers(Point(.5,.45)))
        self.assertAlmostEqual(shape.area,2-(4-math.pi)*.2**2,places=5)

    def test_imported_pill_pad_rotation_preserves_full_dimensions(self):
        shape=pad({'shape':'rotated_rect','x':2,'y':3,'width':1.742,'height':.364,'corner_radius':.182,'ccw_rotation':90})
        for actual,expected in zip(shape.bounds,(2-.182,3-.871,2+.182,3+.871)):self.assertAlmostEqual(actual,expected,places=10)
        self.assertTrue(shape.covers(Point(2,3)))
        self.assertFalse(shape.covers(Point(2.17,3.86)))
        self.assertGreater(shape.area,.59)


if __name__=='__main__':unittest.main()
