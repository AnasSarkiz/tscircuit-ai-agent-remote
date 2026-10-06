"""Integrate a complete authored proposal without changing original solver output."""
import hashlib
import json
from pathlib import Path

evidence = Path(__file__).parent
proposal_path = evidence/'speaker-vsys-fixed-right-bridge.json'
proposal = json.loads(proposal_path.read_text())
native = evidence/'microphone-native/circuit.json'
assert hashlib.sha256(native.read_bytes()).hexdigest() == proposal['native_sha256']
assert not proposal['unresolved'] and proposal.get('status') != 'INCOMPLETE power restoration'
sources = {}
before = {}
for filename in ('src/board/connection-copper.json', 'src/board/manual-power-copper.json'):
    path = Path(filename)
    assert path.read_bytes() == (evidence/'before-speaker'/f'{path.name}.txt').read_bytes()
    before[filename] = hashlib.sha256(path.read_bytes()).hexdigest()
    sources[filename] = json.loads(path.read_text())
for filename, source in sources.items():
    retired = {record['index'] for record in proposal['retired_authored_regions'] if record['source'] == filename}
    for index in retired:
        region = source['pours'][index]
        assert region['net'] == 'VSYS' and region['layer'] in ('top', 'bottom') and region['nominal_width_mm'] == 1.
    source['pours'] = [region for index, region in enumerate(source['pours']) if index not in retired]
connection = sources['src/board/connection-copper.json']
offset = len(connection['vias'])
connection['vias'].extend(proposal['vias'])
for path in proposal['paths']:
    if 'from_proposal_via_index' in path:
        path['from'] = f".CONNECTION_VIA_{offset+path.pop('from_proposal_via_index')} > .{path.pop('from_layer')}"
    if 'to_proposal_via_index' in path:
        path['to'] = f".CONNECTION_VIA_{offset+path.pop('to_proposal_via_index')} > .top"
    assert path['from'] and path['to']
    connection['paths'].append(path)
connection['pours'].extend(proposal['pours'])
connection.setdefault('pad_necks', []).extend(proposal['pad_necks'])
connection['speaker_vsys_repair'] = {
    'classification': 'Manual native copper, not an autorouter cache; native qualification pending',
    'proposal': str(proposal_path), 'native_sha256_before': proposal['native_sha256'],
    'retired_authored_regions': proposal['retired_authored_regions'],
    'preserved_original_vsys_anchors_mm': proposal['original_vsys_anchors_mm'],
    'new_standalone_via_offset': offset,
    'nominal_speaker_trunk_mm': .6, 'nominal_vsys_trunk_mm': 1.,
}
for filename, source in sources.items():
    Path(filename).write_text(json.dumps(source, indent=2)+'\n')
(evidence/'speaker-integration-receipt.json').write_text(json.dumps({
    'classification': 'Authored source candidate; not yet native qualified',
    'before_source_sha256': before, 'proposal_sha256': hashlib.sha256(proposal_path.read_bytes()).hexdigest(),
    'replaced_vsys_regions': len(proposal['retired_authored_regions']),
    'added_vsys_regions': len(proposal['pours']), 'added_paths': len(proposal['paths']),
    'added_standalone_vias': len(proposal['vias']),
}, indent=2)+'\n')
print(json.dumps({'paths': len(connection['paths']), 'regions': len(connection['pours']),
                  'vias': len(connection['vias']), 'new_via_offset': offset}))
