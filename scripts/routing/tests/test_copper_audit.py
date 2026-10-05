"""Independent geometric regressions: contact, false route markers and shorts."""
import copy
import math
import runpy
import unittest
from pathlib import Path

AUDIT = runpy.run_path(str(Path(__file__).parents[1] / 'audit-copper.py'))['audit']


def fixture():
    records = [{'type': 'pcb_board', 'outline': [{'x':x,'y':y} for x,y in [(-5,-5),(5,-5),(5,5),(-5,5)]]},
               {'type':'source_net','source_net_id':'net_a','name':'A'},
               {'type':'source_net','source_net_id':'net_b','name':'B'}]
    for index, x in enumerate((-2,2)):
        suffix=str(index)
        records.extend([
            {'type':'source_component','source_component_id':'component_'+suffix,'name':'CONTACT_'+suffix},
            {'type':'source_port','source_port_id':'source_port_'+suffix,'source_component_id':'component_'+suffix,'name':'pin1','pin_number':1},
            {'type':'pcb_port','pcb_port_id':'pcb_port_'+suffix,'source_port_id':'source_port_'+suffix},
            {'type':'pcb_smtpad','pcb_smtpad_id':'pad_'+suffix,'pcb_port_id':'pcb_port_'+suffix,'shape':'rect','layer':'top','width':.5,'height':.5,'x':x,'y':0},
            {'type':'source_trace','source_trace_id':'source_trace_'+suffix,'connected_source_port_ids':['source_port_'+suffix],'connected_source_net_ids':['net_a']},
        ])
    return records


def trace(layer):
    return {'type':'pcb_trace','pcb_trace_id':'pcb_trace_0','source_trace_id':'source_trace_0',
            'route':[{'route_type':'wire','x':x,'y':0,'width':.2,'layer':layer, **{key:'pcb_port_'+str(index)}}
                     for index,(x,key) in enumerate([(-2,'start_pcb_port_id'),(2,'end_pcb_port_id')])]}


class CopperAuditTests(unittest.TestCase):
    def test_a_partial_layer_via_is_not_qualified_for_the_standard_stack(self):
        records = fixture() + [{'type': 'pcb_via', 'pcb_via_id': 'partial_via', 'source_net_id': 'net_a',
            'x': 0, 'y': 2, 'hole_diameter': .3, 'outer_diameter': .7, 'layers': ['top', 'inner1', 'inner2']}]
        result = AUDIT(records)
        self.assertGreater(result['drc_violation_count'], 0)
        self.assertFalse(result['zero_drc_zero_shorts_and_connected'])
        self.assertTrue(any(error['id'] == 'partial_via' for error in result['route_errors']))

    def test_copper_contact_connects_the_two_pads(self):
        records=fixture()+[trace('top')]
        result=AUDIT(records)
        self.assertTrue(result['zero_drc_zero_shorts_and_connected'])

    def test_route_markers_on_a_different_layer_do_not_close_an_open(self):
        result=AUDIT(fixture()+[trace('bottom')])
        self.assertEqual(result['physically_open_net_count'],1)
        self.assertFalse(result['zero_drc_zero_shorts_and_connected'])

    def test_foreign_net_contact_is_a_short(self):
        records=fixture()+[trace('top')]
        records[-2]['connected_source_net_ids']=['net_b']
        result=AUDIT(records)
        self.assertGreater(result['short_count'],0)
        self.assertFalse(result['zero_drc_zero_shorts_and_connected'])

    def test_same_net_ordinary_via_drill_still_clears_component_pad(self):
        records=fixture()+[trace('top'), {'type':'pcb_via','pcb_via_id':'pcb_via_0','pcb_trace_id':'pcb_trace_0',
            'x':-2,'y':0,'hole_diameter':.3,'outer_diameter':.7,'layers':['top','inner1','inner2','bottom']}]
        result=AUDIT(records)
        self.assertTrue(any(v['category']=='via_drill_to_pad' for v in result['violations']))

    def test_circular_antipad_uses_the_actual_pad_contour(self):
        records=fixture()
        pad=next(r for r in records if r.get('pcb_smtpad_id')=='pad_1')
        pad.update({'type':'pcb_plated_hole','pcb_plated_hole_id':'pad_1','shape':'circle','outer_diameter':1,'hole_diameter':.3,
                    'layers':['top','inner1','inner2','bottom']})
        for key in ('pcb_smtpad_id','layer','width','height'):pad.pop(key)
        circle=[{'x':2+.72*math.cos(index*2*math.pi/256),'y':.72*math.sin(index*2*math.pi/256)} for index in range(256)]
        records.append({'type':'pcb_copper_pour','pcb_copper_pour_id':'pour','source_net_id':'net_b','layer':'inner1','shape':'brep',
                        'brep_shape':{'outer_ring':{'vertices':[{'x':x,'y':y} for x,y in [(-4,-4),(4,-4),(4,4),(-4,4)]]},'inner_rings':[{'vertices':circle}]}})
        result=AUDIT(records)
        self.assertEqual(result['short_count'],0)
        self.assertFalse(any(v['category']=='copper_pad_pour' for v in result['violations']))

    def test_copper_inside_a_drill_does_not_contact_its_annulus(self):
        records=fixture()
        pad=next(r for r in records if r.get('pcb_smtpad_id')=='pad_1')
        pad.update({'type':'pcb_plated_hole','pcb_plated_hole_id':'pad_1','shape':'circle','outer_diameter':1,'hole_diameter':.6,
                    'layers':['top','inner1','inner2','bottom']})
        for key in ('pcb_smtpad_id','layer','width','height'):pad.pop(key)
        records.append({'type':'pcb_trace','pcb_trace_id':'tiny','source_trace_id':'source_trace_0',
                        'route':[{'route_type':'wire','x':x,'y':0,'width':.2,'layer':'top'} for x in [1.95,2.05]]})
        result=AUDIT(records)
        self.assertNotEqual(result['physical_feature_groups']['tiny:0'],result['physical_port_groups']['pcb_port_1'][0])


if __name__=='__main__':unittest.main()
