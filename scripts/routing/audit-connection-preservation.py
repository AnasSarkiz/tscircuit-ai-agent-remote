"""Compare real numbered-port contacts across two untouched native outputs."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def numbered_ports(circuit, audit):
    components={r['source_component_id']:r for r in circuit if r['type']=='source_component'}
    sources={r['source_port_id']:r for r in circuit if r['type']=='source_port'}
    result={}
    for record in circuit:
        if record['type']!='pcb_port':continue
        port=sources[record['source_port_id']];component=components.get(port.get('source_component_id'))
        if component is None:continue
        label=f"{component['name']}.{port.get('pin_number',port['name'])}"
        if label in result:raise ValueError(f'Duplicate numbered terminal {label}')
        result[label]=set(audit['physical_port_groups'][record['pcb_port_id']])
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before_native');parser.add_argument('before_audit');parser.add_argument('after_native');parser.add_argument('after_audit');parser.add_argument('output')
    args=parser.parse_args()
    before=numbered_ports(json.loads(Path(args.before_native).read_text()),json.loads(Path(args.before_audit).read_text()))
    after=numbered_ports(json.loads(Path(args.after_native).read_text()),json.loads(Path(args.after_audit).read_text()))
    missing=sorted(before.keys()-after.keys());lost=[];gained=[];checked=0
    for first,last in itertools.combinations(before,2):
        connected=bool(before[first]&before[last]);now=bool(after.get(first,set())&after.get(last,set()))
        if connected:
            checked+=1
            if not now:lost.append([first,last])
        elif now:gained.append([first,last])
    result={'before_native_sha256':hashlib.sha256(Path(args.before_native).read_bytes()).hexdigest(),
            'after_native_sha256':hashlib.sha256(Path(args.after_native).read_bytes()).hexdigest(),
            'previously_connected_pairs_checked':checked,'lost_pairs':lost,'missing_ports':missing,
            'newly_connected_pair_count':len(gained),'newly_connected_pairs':gained,
            'preserved':not(lost or missing)}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='newly_connected_pairs'}))
    return 0 if result['preserved'] else 1

if __name__=='__main__':raise SystemExit(main())
