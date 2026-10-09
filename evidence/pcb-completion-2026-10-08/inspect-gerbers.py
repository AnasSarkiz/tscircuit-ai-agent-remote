"""Independently parse the real exports, including plated layer spans and via hits."""
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, '.gerber-runtime')
from gerbonara.rs274x import GerberFile
from gerbonara.excellon import ExcellonFile
from gerbonara.utils import MM

folder = Path('evidence/pcb-completion-2026-10-08/NOT-FOR-FABRICATION-gerbers')
records = []
for path in sorted(folder.glob('*.gbr')):
    parsed = GerberFile.open(path)
    records.append({'name': path.name, 'object_count': len(parsed.objects), 'bounds_mm': parsed.bounding_box(unit=MM), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
for path in sorted(folder.glob('*.drl')):
    parsed = ExcellonFile.open(path)
    diameters = sorted({round(obj.tool.diameter, 6) for obj in parsed.objects})
    records.append({'name': path.name, 'object_count': len(parsed.objects), 'tool_diameters_mm': diameters, 'bounds_mm': parsed.bounding_box(unit=MM), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    if path.name == 'drill-L1-L4.drl':
        native = json.loads(Path('evidence/pcb-completion-2026-10-08/final-native/circuit.json').read_text())
        vias = [e for e in native if e['type'] == 'pcb_via']
        assert all(e['hole_diameter'] == .3 and e['outer_diameter'] == .45 and set(e['layers']) == {'top', 'inner1', 'inner2', 'bottom'} for e in vias)
        via_hits = [obj for obj in parsed.objects if abs(obj.tool.diameter - .3) < 1e-8]
        assert len(via_hits) == len(vias)
        assert 'TF.FileFunction,Plated,1,4,PTH' in path.read_text()
        records[-1]['verified_full_span_via_count'] = len(via_hits)
assert len(records) == 14
assert {e['name'] for e in records if e['name'].endswith('.drl')} == {'drill-L1-L4.drl', 'drill_npth.drl'}
result = {'independent_parser': 'gerbonara@1.5.0', 'parsed_files': records, 'blind_or_buried_drill_files': 0, 'fabrication_ready': False}
Path('evidence/pcb-completion-2026-10-08/independent-gerber-inspection.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
