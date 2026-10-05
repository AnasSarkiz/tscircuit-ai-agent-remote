"""Plan real pad-to-pour contacts; never use zero-length routing markers."""
import argparse
import json
import math
import runpy
from pathlib import Path

import numpy as np
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

helpers = runpy.run_path(str(Path(__file__).with_name('plan-manual-signals.py')))
Planner = helpers['ManualSignalPlanner']
outline_shape = helpers['outline_shape']


def contact_obstacles(planner, specification):
    port=specification['port'];width=specification.get('width',.3)
    root = planner.root(port['source_port_id'])
    shapes = [shape.buffer(.21+width/2) for record,shape in planner.pads if 'top' in record.get('layers',[record.get('layer')])
              and (not (pad_port := planner.ports.get(record.get('pcb_port_id'))) or planner.root(pad_port['source_port_id']) != root)]
    shapes.extend(shape.buffer(.21+width/2) for other_root,layer,shape in planner.copper if other_root != root and layer == 'top')
    own_drill = None
    for record, shape in planner.pads:
        if record['type']=='pcb_plated_hole' and record.get('pcb_port_id') == port['pcb_port_id']:
            own_drill=helpers['geometry_helpers']['drill_contour'](record)
    shapes.extend(shape.buffer(.26+width/2) for shape in planner.holes
                  if planner.plated_hole_roots.get(shape.wkb) != root
                  and (own_drill is None or not shape.equals(own_drill)))
    shapes.extend(shape.buffer(.21+width/2) for record,shape in planner.keepouts if 'top' in record['layers'])
    shapes.append(planner.board.envelope.buffer(2).difference(planner.board.buffer(-.26-width/2)))
    return unary_union(shapes)


def plan_contact(planner, specification):
    port, ground = specification['port'], specification['ground']
    own_pads=[shape for record,shape in planner.pads if record.get('pcb_port_id') == port['pcb_port_id']]
    if not own_pads:
        return None
    origin=(port['x'],port['y']);obstacles=contact_obstacles(planner,specification)
    for distance in np.arange(.4,3.01,.2):
        for degrees in range(0,360,45):
            radians=math.radians(degrees);target=(round(origin[0]+float(distance)*math.cos(radians),6),round(origin[1]+float(distance)*math.sin(radians),6))
            endpoint=Point(target)
            if min(endpoint.distance(pad) for pad in own_pads)<.05 or not ground.covers(endpoint) or endpoint.intersects(obstacles):
                continue
            if not LineString([origin,target]).intersects(obstacles):
                return [origin,target]
    return None


def record_contact(planner, specification):
    port,positions=specification['port'],specification['positions']
    component=planner.components[port['pcb_component_id']];rotation=math.radians(-component['rotation']);local=[]
    for x,y in positions[1:]:
        dx,dy=x-component['display_offset_x'],y-component['display_offset_y']
        local.append({'x':round(dx*math.cos(rotation)-dy*math.sin(rotation),6),'y':round(dx*math.sin(rotation)+dy*math.cos(rotation),6)})
    return {'net':'GND','from':planner.port_name(port),'to':'net.GND','width':specification.get('width',.3),'pcbPath':local,
            'global_path_mm':positions,'segment_layers':['top']*len(positions),
            'classification':'manual native pad-to-ground-pour contact; endpoint outside its pad'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('circuit_json');parser.add_argument('output_json');parser.add_argument('--power-plan',required=True);parser.add_argument('--ground-outline',required=True)
    args=parser.parse_args();circuit=json.loads(Path(args.circuit_json).read_text());planner=Planner(circuit)
    nets={r['name']:r for r in circuit if r['type']=='source_net'};root=planner.root(nets['GND']['source_net_id'])
    for region in json.loads(Path(args.power_plan).read_text())['pours']:
        planner.copper.append((planner.root(nets[region['net']]['source_net_id']),region['layer'],Polygon([(p['x'],p['y']) for p in region['outline']])))
    planned_ground=unary_union([Polygon([(p['x'],p['y']) for p in outline]) for outline in json.loads(Path(args.ground_outline).read_text())['top_regions']])
    existing_ground=[]
    for record in circuit:
        if record['type']=='pcb_copper_pour' and record['layer']=='top' and planner.root(record['source_net_id'])==root:
            brep=record['brep_shape'];existing_ground.append(Polygon([(p['x'],p['y']) for p in brep['outer_ring']['vertices']],
                [[(p['x'],p['y']) for p in ring['vertices']] for ring in brep['inner_rings']]))
    ground=unary_union(existing_ground).intersection(planned_ground)
    missing={p for r in circuit if r['type']=='pcb_port_not_connected_error' for p in r['pcb_port_ids']}
    paths,unresolved=[],[]
    for port in planner.ports.values():
        if port['pcb_port_id'] not in missing or planner.root(port['source_port_id'])!=root:
            continue
        source=planner.source_ports[port['source_port_id']]
        if source['source_component_id'] not in planner.source_components:
            continue
        if planner.port_name(port).startswith('.J7 >'):
            continue
        candidates=[port]
        for internal in circuit:
            if internal['type']=='source_component_internal_connection' and port['source_port_id'] in internal['source_port_ids']:
                candidates.extend(p for p in planner.ports.values() if p['source_port_id'] in internal['source_port_ids'] and p!=port)
        for candidate in candidates:
            positions=plan_contact(planner,{'port':candidate,'ground':ground})
            if positions:
                paths.append(record_contact(planner,{'port':candidate,'positions':positions}));break
        else:
            unresolved.append({'port':planner.port_name(port),'reason':'No nonzero 0.3 mm contact beyond pad boundary to an existing ground pour'})
    Path(args.output_json).write_text(json.dumps({'classification':'manual native ground contacts; no zero-length markers','source_circuit_json':args.circuit_json,'paths':paths,'unresolved':unresolved},indent=2)+'\n')
    print(json.dumps({'ground_contacts':len(paths),'unresolved':unresolved}))


if __name__=='__main__':main()
