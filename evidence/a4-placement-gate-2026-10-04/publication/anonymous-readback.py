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

version = 'AnasSarkiz/tscircuit-ai-agent-remote@0.0.2-wip-a4-placement-review'
stage = Path('.publish/board')
out = Path('evidence/a4-placement-gate-2026-10-04/publication')

def post(endpoint, body):
    request = urllib.request.Request(
        'https://registry-api.tscircuit.com/' + endpoint,
        data=json.dumps(body).encode(),
        headers={'Content-Type': 'application/json'},
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
            headers={},
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
        'local_bytes': (stage / file_path).stat().st_size,
        'remote_sha256': remote_sha256,
        'matches': remote_sha256 == hashlib.sha256((stage / file_path).read_bytes()).hexdigest() if remote_sha256 else None,
    }

release = post('package_releases/get', {'package_name_with_version': version})
package = post('packages/get', {'name': 'AnasSarkiz/tscircuit-ai-agent-remote'})
file_list = post('package_files/list', {'package_name_with_version': version})
manifest = json.loads((out / 'package-manifest.json').read_text())
paths = [entry['path'] for entry in manifest['files']]
remote_paths = sorted(entry['file_path'].lstrip('/') for entry in file_list.get('package_files', []))
record = {
    'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'version': version,
    'ready_to_build': release.get('package_release', {}).get('ready_to_build'),
    'is_private': package.get('package', {}).get('is_private'),
    'is_unlisted': package.get('package', {}).get('is_unlisted'),
    'anonymous_access': True,
    'cloud_build_error': release.get('package_release', {}).get('circuit_json_build_error'),
    'transpilation_error': release.get('package_release', {}).get('transpilation_error'),
    'release_http_status': release.get('http_status'),
    'file_list_http_status': file_list.get('http_status'),
    'remote_file_paths': remote_paths,
    'missing_from_list': sorted(set(paths) - set(remote_paths)),
    'extra_remote_files': sorted(set(remote_paths) - set(paths)),
}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    record['files'] = list(executor.map(read_file, paths))
record['matching_files'] = sum(file['matches'] is True for file in record['files'])
record['missing_files'] = [file['path'] for file in record['files'] if file['http_status'] == 404]
record['unverified_or_mismatched_files'] = [file['path'] for file in record['files'] if file['matches'] is not True and file['http_status'] != 404]
(out / 'remote-receipt.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({key: value for key, value in record.items() if key not in ['files', 'remote_file_paths']}, indent=2))
if record['matching_files'] != len(paths) or record['missing_from_list'] or record['extra_remote_files'] or record['is_private'] is not False:
    raise SystemExit(1)
