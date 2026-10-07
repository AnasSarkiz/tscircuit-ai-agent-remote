"""Read the official preview anonymously; require the exact published native object."""
import argparse
import datetime
import hashlib
import json
import urllib.request
from pathlib import Path


def matching_paths(node, context):
    if isinstance(node, list) and node == context['native']:
        return [context['path']]
    children = node.items() if isinstance(node, dict) else enumerate(node) if isinstance(node, list) else []
    results = []
    for key, child in children:
        results.extend(matching_paths(child, {**context, 'path': [*context['path'], key]}))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-id', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    local = Path('dist/index/circuit.json').read_bytes()
    native = json.loads(local)
    url = f'https://registry-api.tscircuit.com/package_releases/get_preview_circuit_json?package_release_id={args.release_id}'
    with urllib.request.urlopen(urllib.request.Request(url, headers={}), timeout=45) as response:
        status, payload = response.status, json.load(response)
    paths = matching_paths(payload, {'native': native, 'path': ['$']})
    page = f'https://tscircuit.com/AnasSarkiz/tscircuit-ai-agent-remote/releases/{args.release_id}/preview'
    with urllib.request.urlopen(urllib.request.Request(page, headers={}), timeout=30) as response:
        page_status = response.status
    result = {'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'release_id': args.release_id, 'version': '0.0.8-wip-speaker-routing',
              'preview_endpoint_url': url, 'anonymous_http_status': status,
              'exact_native_object_equality': bool(paths), 'matching_native_paths': paths,
              'local_native_json_sha256': hashlib.sha256(local).hexdigest(),
              'native_elements': len(native), 'schematic_sheet_count': sum(r['type'] == 'schematic_sheet' for r in native),
              'preview_page_url': page, 'preview_page_anonymous_http_status': page_status,
              'cloud_CI_success_inferred': False, 'fabrication_ready': False}
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))
    return 0 if paths and page_status == 200 else 1


if __name__ == '__main__':
    raise SystemExit(main())
