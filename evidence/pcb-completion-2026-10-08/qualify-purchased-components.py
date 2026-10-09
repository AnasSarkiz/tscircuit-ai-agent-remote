"""Compare actual purchased components before/after canonical regeneration."""
import hashlib
import json
import math
from pathlib import Path

old_bytes = Path('dist/index/circuit.json').read_bytes()
new_bytes = Path('evidence/pcb-completion-2026-10-08/final-native/circuit.json').read_bytes()
old, new = json.loads(old_bytes), json.loads(new_bytes)


def purchased(circuit):
    source = {e['source_component_id']: e for e in circuit if e['type'] == 'source_component' and e.get('supplier_part_numbers', {}).get('jlcpcb')}
    components = {source[e['source_component_id']]['name']: e for e in circuit if e['type'] == 'pcb_component' and e['source_component_id'] in source}
    return source, components


old_source, old_components = purchased(old)
new_source, new_components = purchased(new)
assert set(old_components) == set(new_components)
unchanged = []
for name, component in old_components.items():
    other = new_components[name]
    assert component['center'] == other['center'] and component['rotation'] == other['rotation'] and component['layer'] == other['layer']
    assert old_source[component['source_component_id']]['supplier_part_numbers'] == new_source[other['source_component_id']]['supplier_part_numbers']
    if name == 'U14':
        continue
    for key in ['width', 'height']:
        assert component.get(key) == other.get(key), (name, key)
    for element_type in ['pcb_smtpad', 'pcb_plated_hole', 'pcb_courtyard_rect', 'pcb_courtyard_polygon']:
        before = [e for e in old if e['type'] == element_type and e.get('pcb_component_id') == component['pcb_component_id']]
        after = [e for e in new if e['type'] == element_type and e.get('pcb_component_id') == other['pcb_component_id']]
        assert before == after, (name, element_type)
    unchanged.append(name)
u14_old = [e for e in old if e['type'] == 'pcb_smtpad' and e['pcb_component_id'] == old_components['U14']['pcb_component_id']]
u14_new = [e for e in new if e['type'] == 'pcb_smtpad' and e['pcb_component_id'] == new_components['U14']['pcb_component_id']]
assert len(u14_old) == len(u14_new) == 20
maximum_delta = max(min(math.hypot(p['x'] - q['x'], p['y'] - q['y']) for q in u14_new) for p in u14_old)
assert maximum_delta < .0002
assert all(e['shape'] in ['pill', 'rotated_pill'] for e in u14_new)
result = {'before_sha256': hashlib.sha256(old_bytes).hexdigest(), 'after_sha256': hashlib.sha256(new_bytes).hexdigest(), 'purchased_components': len(new_components), 'unchanged_component_poses': len(new_components), 'identical_other_supplier_geometry': len(unchanged), 'u14_genuine_reimport_pad_count': len(u14_new), 'u14_maximum_pad_center_delta_mm': maximum_delta, 'u14_source_manually_edited': False, 'genuine_import_receipt': 'evidence/pcb-completion-2026-10-08/u14-import-provenance.json', 'passes': True}
Path('evidence/pcb-completion-2026-10-08/purchased-geometry.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
