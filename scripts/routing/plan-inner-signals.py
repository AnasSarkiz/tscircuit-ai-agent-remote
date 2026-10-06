"""Route authored low-current regions on inner layers using through vias.

Retain original pad escapes and full-span vias. Retire only the bottom segments
selected for replacement in the planning view, never in native Circuit JSON.
"""
import argparse
import hashlib
import json
import runpy
from pathlib import Path
from shapely.geometry import LineString, Point

helpers = runpy.run_path(str(Path(__file__).with_name('plan-power-copper.py')))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit_json', type=Path)
    parser.add_argument('original_proposal', type=Path)
    parser.add_argument('power_regions', type=Path)
    parser.add_argument('output_json', type=Path)
    args = parser.parse_args()
    circuit = json.loads(args.circuit_json.read_text())
    proposal = json.loads(args.original_proposal.read_text())
    source_traces = {r['source_trace_id']:r for r in circuit if r['type']=='source_trace'}
    nets = {r['name']:r for r in circuit if r['type']=='source_net'}
    region_names = {r['net'] for r in json.loads(args.power_regions.read_text())['pours']}
    retired_net_ids = {nets[name]['source_net_id'] for name in region_names}
    retired_features = {r['pcb_copper_pour_id'] for r in circuit if r['type']=='pcb_copper_pour' and r['source_net_id'] in retired_net_ids}
    retired_features |= {r['pcb_via_id'] for r in circuit if r['type']=='pcb_via' and r.get('source_net_id') in retired_net_ids}
    names = {f"MANUAL_{r['net']}_{r['original_path_index']}" for r in proposal['paths']}
    retired_bottom = {r['pcb_trace_id']:{'bottom':None} for r in circuit
                      if r['type']=='pcb_trace' and source_traces[r['source_trace_id']].get('name') in names}
    planner = helpers['Planner'](circuit, {'retired_feature_ids':retired_features,'relocated_trace_layers':retired_bottom})
    planner.via_copper_clearance = .27
    output = {**proposal,'paths':[],'pours':[],'vias':[],'unresolved':[],
              'classification':'authored native inner-layer low-current rerouting; requires native replay',
              'source_circuit_json':str(args.circuit_json),'source_sha256':hashlib.sha256(args.circuit_json.read_bytes()).hexdigest()}
    for path in proposal['paths']:
        root = planner.root(nets[path['net']]['source_net_id'])
        first,last = path['region']['path_mm'][0],path['region']['path_mm'][-1]
        terminals = [(r['x'],r['y']) for r in circuit if r['type']=='pcb_via' and planner.via_root(r)==root]
        terminals += [(r['x'],r['y']) for r in output['vias'] if r['net']==path['net']]
        width = path['width']+.002
        result = helpers['wide_multilayer_route'](planner, {'first':first,'last':last,'root':root,
                  'width':width,'new_vias':terminals,'layers':('inner2','inner1'),
                  'via_outer_mm':.45,'via_hole_mm':.3,'copper_clearance_mm':.27})
        if result is None:
            output['unresolved'].append({'net':path['net'],'original_path_index':path['original_path_index']})
        else:
            parts,vias = result
            regions=[]
            for layer,route in parts:
                if len(route)<2 or LineString(route).length<1e-6:
                    continue
                contour = LineString(route).buffer(width/2,quad_segs=64,cap_style=2,join_style=1)
                if contour.geom_type!='Polygon' or contour.interiors:
                    raise ValueError('An authored signal region needs one simple outline')
                region={'net':path['net'],'layer':layer,'path_mm':route,'nominal_width_mm':path['width'],
                        'drawn_width_mm':width,'outline':[{'x':round(x,6),'y':round(y,6)} for x,y in list(contour.exterior.coords)[:-1]],
                        'classification':'manual native inner-layer low-current region; through vias only'}
                regions.append(region);output['pours'].append(region)
                planner.copper.append((root,layer,contour))
            updated={k:v for k,v in path.items() if k!='region'}
            updated['regions']=regions
            output['paths'].append(updated)
            for x,y in vias:
                output['vias'].append({'net':path['net'],'x':x,'y':y,'hole_mm':.3,'outer_mm':.45})
                hole=Point(x,y).buffer(.15);planner.holes.append(hole);planner.plated_hole_roots[hole.wkb]=root
                for layer in ('top','inner1','inner2','bottom'):
                    planner.copper.append((root,layer,Point(x,y).buffer(.225)))
        args.output_json.write_text(json.dumps(output,indent=2)+'\n')
        print(json.dumps({'net':path['net'],'original_path_index':path['original_path_index'],
                          'routed':result is not None,'unresolved_count':len(output['unresolved'])}),flush=True)
    return 1 if output['unresolved'] else 0


if __name__=='__main__':
    raise SystemExit(main())
