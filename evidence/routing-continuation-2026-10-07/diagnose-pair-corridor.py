"""Plot actual fixed obstacles and paired-corridor free components."""
import json,runpy
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point

module=runpy.run_path('scripts/routing/plan-coupled-speaker.py')
planner,specification=module['planning_scene'](Path('dist/index/circuit.json'))
clock=module['relocate_clock_star'](planner,specification)
planner.pads=[(record,shape) for record,shape in planner.pads if not (
    record.get('pcb_port_id') in planner.ports and
    planner.root(planner.ports[record['pcb_port_id']]['source_port_id']) in specification['pair_roots'])]
figure,axes=plt.subplots(1,2,figsize=(12,8),constrained_layout=True)
receipt=[]
for layer,axis in zip(('bottom','top'),axes):
    obstacles=planner.obstacles('speaker_bundle_space_only',layer,1.402)
    blocked,labels=planner.grid_data(obstacles)
    starts=planner.grid_anchor_options(((-16.25,6.35),),(blocked,obstacles))[0]
    ends=planner.grid_anchor_options(((22.02499995,10.5),),(blocked,obstacles))[0]
    start_labels=sorted({int(labels[node]) for node,_ in starts})
    end_labels=sorted({int(labels[node]) for node,_ in ends})
    image=np.zeros((*blocked.shape,3));image[blocked]=(.12,.12,.12);image[~blocked]=(.85,.85,.85)
    for identifier in start_labels:image[labels==identifier]=(.22,.68,.9)
    for identifier in end_labels:image[labels==identifier]=(.95,.7,.25)
    axis.imshow(image,origin='lower',extent=(-24.5,24.5,-32,32))
    axis.scatter([-16.25,22.025],[6.35,10.5],c=['blue','red'],s=35)
    axis.set_title(layer+' — blue: start space; orange: destination space');axis.set_aspect('equal')
    axis.set_xlabel('x (mm)');axis.set_ylabel('y (mm)')
    nearby=[]
    for record in planner.circuit:
        if record['type']=='pcb_via' and -20<record['x']<-8 and 2<record['y']<15:
            axis.annotate(record['pcb_via_id'].replace('pcb_via_',''),(record['x'],record['y']),fontsize=5,color='crimson')
            nearby.append({key:record[key] for key in ('pcb_via_id','x','y')})
    receipt.append({'layer':layer,'start_component_ids':start_labels,'destination_component_ids':end_labels,
                    'same_component':bool(set(start_labels)&set(end_labels)),
                    'nearby_native_vias':nearby})
figure.savefig('evidence/routing-continuation-2026-10-07/pair-corridor-components.png',dpi=140)
Path('evidence/routing-continuation-2026-10-07/pair-corridor-components.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
