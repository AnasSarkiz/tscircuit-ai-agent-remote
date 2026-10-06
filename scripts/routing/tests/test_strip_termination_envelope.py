"""Preserve required copper at short bends beside flat strip terminations."""
import runpy
import unittest
from pathlib import Path
from shapely.geometry import LineString,Polygon

b=runpy.run_path(str(Path(__file__).parents[1]/'plan-connection-bridges.py'))


class StripTerminationEnvelopeTests(unittest.TestCase):
    def test_serialization_reserve_does_not_remove_nominal_corner_copper(self):
        # Reduced from the measured VBUS transition that lost copper as its
        # reserve increased. This verifies physical coverage, not an outline's
        # vertex list or an implementation-specific point count.
        line=LineString([(-7.4,-20.9),(-7.35,-20.85),(-7.35,-20.8),
                         (-7.25,-20.7),(-7.25,-20.667156)])
        required=line.buffer(.25,quad_segs=64,cap_style=2)
        self.assertGreater(required.difference(line.buffer(.255,quad_segs=64,cap_style=2)).area,.0005)
        record=b['region_records']('VBUS',{'parts':[('bottom',list(line.coords))],
            'width':.5,'drawn_width_mm':.51})[0]
        authored=Polygon([(p['x'],p['y']) for p in record['outline']])
        self.assertLessEqual(required.difference(authored.buffer(.000001)).area,1e-8)
        self.assertEqual(record['nominal_width_mm'],.5)

    def test_drawn_width_cannot_lower_nominal_requirement(self):
        with self.assertRaises(ValueError):
            b['region_records']('VBUS',{'parts':[('top',[(0,0),(1,0)])],
                'width':.5,'drawn_width_mm':.49})


if __name__=='__main__':unittest.main()
