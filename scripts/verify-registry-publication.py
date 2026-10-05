"""Read a public tscircuit release anonymously and compare every staged file."""

import argparse
import base64
import concurrent.futures
import datetime
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


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


def read_file(file_path, context):
    response = post('package_files/get', {
        'package_name_with_version': context['version'],
        'file_path': '/' + file_path,
    })
    remote = response.get('package_file', {})
    content = remote.get('content_text')
    payload = None
    if isinstance(content, str):
        payload = content.encode()
    elif remote.get('content_base64'):
        payload = base64.b64decode(remote['content_base64'])
    download_http_status = None
    download_error = None
    if payload is None and remote.get('package_file_id'):
        query = urllib.parse.urlencode({
            'package_name_with_version': context['version'],
            'file_path': '/' + file_path,
        })
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
    local = (context['stage'] / file_path).read_bytes()
    return {
        'path': file_path,
        'http_status': response.get('http_status'),
        'network_error': response.get('network_error'),
        'download_http_status': download_http_status,
        'download_error': download_error,
        'local_bytes': len(local),
        'local_sha256': hashlib.sha256(local).hexdigest(),
        'remote_sha256': remote_sha256,
        'matches': remote_sha256 == hashlib.sha256(local).hexdigest()
        if remote_sha256 is not None else None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', required=True)
    parser.add_argument('--stage', type=Path, default=Path('.publish/board'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    package_name, version_tag = args.version.rsplit('@', 1)
    context = {'version': args.version, 'stage': args.stage}
    paths = sorted(p.relative_to(args.stage).as_posix()
                   for p in args.stage.rglob('*') if p.is_file())
    release_response = post('package_releases/get', {
        'package_name_with_version': args.version,
    })
    package_response = post('packages/get', {'name': package_name})
    list_response = post('package_files/list', {
        'package_name_with_version': args.version,
    })
    release = release_response.get('package_release', {})
    package = package_response.get('package', {})
    remote_paths = sorted(entry['file_path'].lstrip('/')
                          for entry in list_response.get('package_files', []))
    record = {
        'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'version': args.version,
        'public_url': f'https://tscircuit.com/{package_name}?version={version_tag}#files',
        'anonymous_access': True,
        'ready_to_build': release.get('ready_to_build'),
        'is_private': package.get('is_private'),
        'is_unlisted': package.get('is_unlisted'),
        'cloud_build_error': release.get('circuit_json_build_error'),
        'transpilation_error': release.get('transpilation_error'),
        'release_http_status': release_response.get('http_status'),
        'package_http_status': package_response.get('http_status'),
        'file_list_http_status': list_response.get('http_status'),
        'remote_file_paths': remote_paths,
        'missing_from_list': sorted(set(paths) - set(remote_paths)),
        'extra_remote_files': sorted(set(remote_paths) - set(paths)),
    }
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        record['files'] = list(executor.map(read_file, paths, [context] * len(paths)))
    record['matching_files'] = sum(f['matches'] is True for f in record['files'])
    record['expected_files'] = len(paths)
    record['missing_files'] = [f['path'] for f in record['files'] if f['http_status'] == 404]
    record['unverified_or_mismatched_files'] = [
        f['path'] for f in record['files']
        if f['matches'] is not True and f['http_status'] != 404
    ]
    record['complete_public_upload'] = (
        record['matching_files'] == len(paths)
        and not record['missing_from_list']
        and not record['extra_remote_files']
        and record['is_private'] is False
        and record['is_unlisted'] is False
        and record['ready_to_build'] is True
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: v for k, v in record.items()
                      if k not in ['files', 'remote_file_paths']}, indent=2))
    return 0 if record['complete_public_upload'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
