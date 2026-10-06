"""Check wide outer copper keeps clearance through a short constrained section."""
import runpy
import unittest
from pathlib import Path
from shapely.geometry import LineString, Polygon

helpers=runpy.run_path(str(Path(__file__).parents[1]/'plan-outer-connections.py'))


class OuterConnectionWidthTests(unittest.TestCase):
    def test_constrained_section_does_not_narrow_the_whole_route(self):
        circuit=[
            {'type':'pcb_board','outline':[{'x':x,'y':y} for x,y in [(-25,-32.5),(25,-32.5),(25,32.5),(-25,32.5)]]},
            {'type':'source_net','source_net_id':'speaker','name':'SPEAKER_P'},
            {'type':'source_net','source_net_id':'neighbor','name':'NEIGHBOR'},
            {'type':'source_trace','source_trace_id':'neighbor_trace','connected_source_port_ids':[],
             'connected_source_net_ids':['neighbor']},
            {'type':'pcb_trace','pcb_trace_id':'neighbor_copper','source_trace_id':'neighbor_trace','route':[
                {'route_type':'wire','x':0,'y':.6,'layer':'bottom','width':.2},
                {'route_type':'wire','x':1,'y':.6,'layer':'bottom','width':.2}]},
        ]
        planner=helpers['helpers']['Planner'](circuit)
        regions,narrow=helpers['adaptive_regions'](planner,{'root':planner.root('speaker'),
            'net':'SPEAKER_P','parts':[('bottom',[(-2,0),(2,0)])],
            'nominal_width':.6,'neck_width':.275,'new_vias':[]})
        self.assertEqual({r['nominal_width_mm'] for r in regions},{.275,.6})
        self.assertGreater(narrow,0)
        self.assertLess(narrow,2.1)
        self.assertAlmostEqual(sum(LineString(r['path_mm']).length for r in regions),4)
        foreign=LineString([(0,.6),(1,.6)]).buffer(.1)
        for region in regions:
            self.assertEqual(region['layer'],'bottom')
            shape=Polygon([(p['x'],p['y']) for p in region['outline']])
            self.assertGreaterEqual(shape.distance(foreign),.27)
            required=LineString(region['path_mm']).buffer(region['nominal_width_mm']/2,cap_style=2)
            self.assertLess(required.difference(shape).area,1e-8)


    def test_route_prefers_full_width_detour_over_long_narrow_shortcut(self):
        circuit=[
            {'type':'pcb_board','outline':[{'x':x,'y':y} for x,y in [(-25,-32.5),(25,-32.5),(25,32.5),(-25,32.5)]]},
            {'type':'source_net','source_net_id':'speaker','name':'SPEAKER_P'},
            {'type':'source_net','source_net_id':'neighbor','name':'NEIGHBOR'},
            {'type':'source_trace','source_trace_id':'neighbor_trace','connected_source_port_ids':[],
             'connected_source_net_ids':['neighbor']},
            {'type':'pcb_trace','pcb_trace_id':'neighbor_copper','source_trace_id':'neighbor_trace','route':[
                {'route_type':'wire','x':-1,'y':.6,'layer':'bottom','width':.2},
                {'route_type':'wire','x':1,'y':.6,'layer':'bottom','width':.2}]},
        ]
        planner=helpers['helpers']['Planner'](circuit)
        planner.set_grid(.1)
        route=helpers['helpers']['wide_multilayer_route'](planner,{
            'root':planner.root('speaker'),'first':(-2,0),'last':(2,0),
            'width':.277,'preferred_width_mm':.602,'new_vias':[],
            'layers':('bottom','top'),'via_outer_mm':.45,'via_hole_mm':.3,
            'copper_clearance_mm':.27})
        self.assertIsNotNone(route)
        parts,vias=route
        regions,narrow=helpers['adaptive_regions'](planner,{'root':planner.root('speaker'),
            'net':'SPEAKER_P','parts':parts,'nominal_width':.6,'neck_width':.275,
            'new_vias':vias})
        self.assertEqual(narrow,0)
        self.assertTrue(all(region['nominal_width_mm']==.6 for region in regions))


if __name__=='__main__':unittest.main()
