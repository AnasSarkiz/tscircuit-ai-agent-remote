"""Check that a repair can contact a real isolated-pad target without crossing nets."""
import runpy
import unittest
from pathlib import Path
from types import SimpleNamespace

helpers = runpy.run_path(str(Path(__file__).parents[1] / 'plan-existing-copper-routes.py'))


class ExistingCopperTargetTests(unittest.TestCase):
    def test_pad_targets_require_the_same_net_and_actual_main_island(self):
        planner = SimpleNamespace(
            ports={name: {'pcb_port_id': name, 'source_port_id': net, 'x': x, 'y': 0}
                   for name, net, x in [('main', 'wanted', 1), ('open', 'wanted', 2), ('foreign', 'other', 3)]},
            circuit=[], root=lambda identifier: identifier)
        physical = {'physical_port_groups': {'main': [7], 'open': [8], 'foreign': [7]}}
        targets = helpers['main_targets'](planner, {'physical':physical,'group':7,'root':'wanted'})
        self.assertEqual(targets, {('top',1,0)})

    def test_connected_through_via_is_a_target_on_all_four_layers(self):
        planner = SimpleNamespace(ports={}, root=lambda identifier: identifier, via_root=lambda record: record['net'],
            circuit=[{'type':'pcb_via','pcb_via_id':'connected','net':'wanted','x':1,'y':2},
                     {'type':'pcb_via','pcb_via_id':'isolated','net':'wanted','x':3,'y':4}])
        physical={'physical_feature_groups':{'connected':7,'isolated':8},'physical_port_groups':{}}
        targets=helpers['main_targets'](planner,{'physical':physical,'group':7,'root':'wanted'})
        self.assertEqual(targets,{(layer,1,2) for layer in ('top','inner1','inner2','bottom')})


if __name__=='__main__':unittest.main()
