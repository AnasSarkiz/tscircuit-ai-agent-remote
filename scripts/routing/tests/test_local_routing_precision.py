"""Fine local sampling resolves a real corridor without changing its geometry."""
import runpy
import unittest
from unittest.mock import patch
from pathlib import Path
from shapely.geometry import LineString,box
from shapely.ops import unary_union

Planner=runpy.run_path(str(Path(__file__).parents[1]/'plan-manual-signals.py'))['ManualSignalPlanner']
wide_route=runpy.run_path(str(Path(__file__).parents[1]/'plan-power-copper.py'))['wide_multilayer_route']


class LocalRoutingPrecisionTests(unittest.TestCase):
    def test_fine_grid_finds_clear_corridor_missed_by_coarse_samples(self):
        planner=Planner([{'type':'pcb_board','outline':[{'x':x,'y':y} for x,y in [(-25,-32.5),(25,-32.5),(25,32.5),(-25,32.5)]]}])
        # These are the already expanded obstacle contours; their clearance
        # never changes between attempts. Only the planning samples change.
        obstacles=unary_union([box(-.1,-1,.1,.009),box(-.1,.031,.1,1)])
        endpoints=((-0.4,.02),(.4,.02),obstacles)
        bounds=(-.5,-.2,.5,.2)
        planner.set_grid(.05,bounds)
        self.assertIsNone(planner.grid_route(endpoints))
        planner.set_grid(.01,bounds)
        route=planner.grid_route(endpoints)
        self.assertIsNotNone(route)
        self.assertFalse(LineString(route).intersects(obstacles))
        self.assertEqual(route[0],endpoints[0])
        self.assertEqual(route[-1],endpoints[1])

    def test_fine_grid_cannot_allocate_a_full_board(self):
        planner=Planner([{'type':'pcb_board','outline':[{'x':x,'y':y} for x,y in [(-25,-32.5),(25,-32.5),(25,32.5),(-25,32.5)]]}])
        with self.assertRaises(ValueError):planner.set_grid(.01)
        with self.assertRaises(ValueError):planner.set_grid(.01,(-24.5,-32,24.5,32))

    def test_multiple_legal_anchors_reach_corridor_without_changing_clearance(self):
        planner=Planner([{'type':'pcb_board','outline':[{'x':x,'y':y} for x,y in [(-25,-32.5),(25,-32.5),(25,32.5),(-25,32.5)]]}])
        planner.set_grid(.05,(-.5,-.2,.5,.2))
        obstacles=unary_union([box(-.1,-1,.1,.009),box(-.1,.031,.1,1)])
        specification={'first':(-.4,.02),'last':(.4,.02),'layers':('top','bottom'),'preferred_width_mm':.2}
        with patch.dict(wide_route.__globals__,{'inner_obstacles':lambda *_:obstacles,'via_obstacles':lambda *_:box(2,2,3,3)}):
            self.assertIsNone(wide_route(planner,specification))
            route=wide_route(planner,{**specification,'multi_anchor':True})
        self.assertIsNotNone(route)
        parts,_=route
        self.assertEqual(parts[0][1][0],specification['first'])
        self.assertEqual(parts[-1][1][-1],specification['last'])
        for _,points in parts:self.assertFalse(LineString(points).intersects(obstacles))

    def test_unplated_strip_endpoint_cannot_jump_to_another_layer(self):
        planner=Planner([{'type':'pcb_board','outline':[{'x':x,'y':y} for x,y in [(-25,-32.5),(25,-32.5),(25,32.5),(-25,32.5)]]}])
        planner.set_grid(.05,(-.5,-.2,.5,.2))
        outside=box(2,2,3,3)
        specification={'first':(-.4,0),'last':(.4,0),'layers':('inner1','inner2'),'multi_anchor':True}
        with patch.dict(wide_route.__globals__,{'inner_obstacles':lambda _,s:box(-2,-2,2,2) if s['layer']=='inner1' else outside,'via_obstacles':lambda *_:outside}):
            self.assertIsNotNone(wide_route(planner,specification))
            self.assertIsNone(wide_route(planner,{**specification,'first_layer':'inner1','last_layer':'inner1'}))
        with self.assertRaises(ValueError):wide_route(planner,{**specification,'first_layer':'top'})


if __name__=='__main__':unittest.main()
