import datetime
import json
import urllib.request
from pathlib import Path

package_name = 'AnasSarkiz/tscircuit-ai-agent-remote'
config = json.loads(Path('/Users/anassarkiz/Library/Preferences/tscircuit-nodejs/config.json').read_text())

def post(endpoint, body):
    request = urllib.request.Request('https://registry-api.tscircuit.com/' + endpoint,
        data=json.dumps(body).encode(),
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + config['sessionToken']})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)

package = post('packages/get', {'name': package_name})['package']
updated = post('packages/update', {'package_id': package['package_id'], 'is_private': False, 'is_unlisted': False, 'public_dist_enabled': True})['package']
record = {'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'package_name': package_name, 'previous_is_private': package.get('is_private'),
    'is_private': updated.get('is_private'), 'is_public': updated.get('is_public'),
    'is_unlisted': updated.get('is_unlisted'), 'public_dist_enabled': updated.get('public_dist_enabled'),
    'official_endpoint_source': 'https://github.com/tscircuit/api.tscircuit.com/blob/main/routes/packages/update.ts'}
Path('evidence/public-board-publication-2026-10-04/visibility-change.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record))
if record['is_private'] is not False or record['is_unlisted'] is not False or record['public_dist_enabled'] is not True:
    raise SystemExit(1)
