import base64
import concurrent.futures
import datetime
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

config = json.loads(Path('/Users/anassarkiz/Library/Preferences/tscircuit-nodejs/config.json').read_text())
version = 'AnasSarkiz/tscircuit-ai-agent-remote@0.0.2-wip-a0-fabrication-review'

def post(endpoint, body):
    request = urllib.request.Request(
        'https://registry-api.tscircuit.com/' + endpoint,
        data=json.dumps(body).encode(),
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + config['sessionToken']},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        return {'http_status': error.code}
    except (TimeoutError, urllib.error.URLError) as error:
        return {'network_error': type(error).__name__}

def read_file(file_path):
    response = post('package_files/get', {'package_name_with_version': version, 'file_path': '/' + file_path})
    remote = response.get('package_file', {})
    content = remote.get('content_text')
    payload = content.encode() if isinstance(content, str) else base64.b64decode(remote['content_base64']) if remote.get('content_base64') else None
    download_http_status = None
    download_error = None
    if payload is None and remote.get('package_file_id'):
        query = urllib.parse.urlencode({'package_name_with_version': version, 'file_path': '/' + file_path})
        request = urllib.request.Request(
            'https://registry-api.tscircuit.com/package_files/download?' + query,
            headers={'Authorization': 'Bearer ' + config['sessionToken']},
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as download_response:
                payload = download_response.read()
        except urllib.error.HTTPError as error:
            download_http_status = error.code
        except (TimeoutError, urllib.error.URLError) as error:
            download_error = type(error).__name__
    remote_sha256 = hashlib.sha256(payload).hexdigest() if payload is not None else None
    return {
        'path': file_path,
        'http_status': response.get('http_status'),
        'network_error': response.get('network_error'),
        'download_http_status': download_http_status,
        'download_error': download_error,
        'local_bytes': Path(file_path).stat().st_size,
        'remote_sha256': remote_sha256,
        'matches': remote_sha256 == hashlib.sha256(Path(file_path).read_bytes()).hexdigest() if remote_sha256 else None,
    }

release = post('package_releases/get', {'package_name_with_version': version})
package = post('packages/get', {'name': 'AnasSarkiz/tscircuit-ai-agent-remote'})
log = Path('evidence/hold-readback-review-2026-10-03/fabrication-review-native-push.log').read_text()
paths = re.findall(r'^    - (.+)$', log, re.M)
record = {
    'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'source_revision': 'fa90b5420f8e567270697c68132f311444a42424',
    'version': version,
    'publisher_exit_code': 1,
    'reported_successes': int(re.search(r'Succeeded: ([0-9]+) files', log).group(1)),
    'reported_failures': int(re.search(r'Failed: ([0-9]+) files', log).group(1)),
    'ready_to_build': release.get('package_release', {}).get('ready_to_build'),
    'is_private': package.get('package', {}).get('is_private'),
}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    record['files'] = list(executor.map(read_file, paths))
Path('evidence/hold-readback-review-2026-10-03/fabrication-review-publication-failure-receipt.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({key: value for key, value in record.items() if key != 'files'}, indent=2))
print(json.dumps({'matching_files': sum(file['matches'] is True for file in record['files']), 'missing_files': [file['path'] for file in record['files'] if file['http_status'] == 404], 'unverified_files': [file['path'] for file in record['files'] if file['matches'] is None and file['http_status'] != 404]}, indent=2))
