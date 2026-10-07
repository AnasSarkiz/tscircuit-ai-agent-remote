"""Check every original contact except the three deliberately removed UART service roles.

The unchanged general preservation checker remains separate and records its raw
failure on renumbered/removed J6 contacts. This interface-specific qualification
maps the five retained roles and still rejects losses anywhere else on the board.
"""
import argparse
import gzip
import hashlib
import itertools
import json
import runpy
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('after_native')
parser.add_argument('after_audit')
parser.add_argument('output')
args = parser.parse_args()
base = Path(__file__).resolve().parent
before_payload = gzip.decompress((base/'before/circuit.json.gz').read_bytes())
before_native = json.loads(before_payload)
after_payload = Path(args.after_native).read_bytes()
after_native = json.loads(after_payload)
before_audit = json.loads(Path('evidence/routing-continuation-2026-10-07/final-cli-copper-audit.json').read_text())
after_audit = json.loads(Path(args.after_audit).read_text())
assert hashlib.sha256(before_payload).hexdigest() == before_audit['source_sha256']
assert hashlib.sha256(after_payload).hexdigest() == after_audit['source_sha256']
for native, part in [(before_native, 'C160405'), (after_native, 'C160389')]:
    connector = next(record for record in native if record['type']=='source_component' and record['name']=='J6')
    assert connector['supplier_part_numbers']['jlcpcb'] == [part]
numbered_ports = runpy.run_path('scripts/routing/audit-connection-preservation.py')['numbered_ports']
before = numbered_ports(before_native, before_audit)
after = numbered_ports(after_native, after_audit)
contact_migration = {'J6.1':'J6.2', 'J6.5':'J6.3', 'J6.6':'J6.1', 'J6.7':'J6.4', 'J6.8':'J6.5'}
removed_service_contacts = {'J6.2':'V3V3', 'J6.3':'MCU_EN', 'J6.4':'MCU_BOOT_N'}
original_contacts = [terminal for terminal in before if terminal not in removed_service_contacts]
missing = [terminal for terminal in original_contacts if contact_migration.get(terminal,terminal) not in after]
checked = 0
lost = []
for first, last in itertools.combinations(original_contacts,2):
    if not before[first].intersection(before[last]):
        continue
    checked += 1
    mapped_first, mapped_last = contact_migration.get(first,first), contact_migration.get(last,last)
    if not after.get(mapped_first,set()).intersection(after.get(mapped_last,set())):
        lost.append({'before':[first,last], 'after':[mapped_first,mapped_last]})
result = {
    'scope':'Every previously connected numbered contact pair after explicitly removing only J6 power/EN/BOOT contacts and mapping the five retained genuine connector roles. All non-J6 contacts are unchanged and fully checked.',
    'before_native_sha256':hashlib.sha256(before_payload).hexdigest(),
    'after_native_sha256':hashlib.sha256(after_payload).hexdigest(),
    'original_connected_pairs':sum(bool(before[first].intersection(before[last])) for first,last in itertools.combinations(before,2)),
    'removed_service_contacts':removed_service_contacts,
    'retained_contact_migration':contact_migration,
    'connected_pairs_checked':checked,
    'missing_original_roles':missing,
    'lost_connections':lost,
    'preserved_under_explicit_interface_migration':not (missing or lost),
    'fabrication_ready':False,
}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
raise SystemExit(0 if result['preserved_under_explicit_interface_migration'] else 1)
