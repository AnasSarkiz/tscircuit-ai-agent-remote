"""Verify every staged file against anonymous GitHub source at an exact commit."""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
import urllib.error
import urllib.request
from pathlib import Path


def read_public(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={}), timeout=30) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, None
    except (TimeoutError, urllib.error.URLError):
        return None, None


def verify_file(filename, context):
    local = Path(filename).read_bytes()
    stage = (context['stage'] / filename).read_bytes()
    status, remote = read_public(f"https://raw.githubusercontent.com/AnasSarkiz/tscircuit-ai-agent-remote/{context['commit']}/{filename}")
    return {'path': filename, 'anonymous_http_status': status,
            'local_sha256': hashlib.sha256(local).hexdigest(),
            'remote_sha256': hashlib.sha256(remote).hexdigest() if remote is not None else None,
            'matches': local == remote, 'stage_matches_repository': local == stage}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--stage', type=Path, default=Path('.publish/board'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    paths = sorted(str(p.relative_to(args.stage)) for p in args.stage.rglob('*') if p.is_file())
    context = {'commit': args.commit, 'stage': args.stage}
    status, payload = read_public('https://api.github.com/repos/AnasSarkiz/tscircuit-ai-agent-remote')
    repository = json.loads(payload) if payload is not None and status == 200 else {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        records = list(executor.map(verify_file, paths, [context] * len(paths)))
    differences = [r['path'] for r in records if not r['stage_matches_repository']]
    root_package = json.loads(Path('package.json').read_text())
    stage_package = json.loads((args.stage/'package.json').read_text())
    package_identity_and_pins_match = all(root_package[k] == stage_package[k]
        for k in ['name', 'version', 'main', 'author', 'devDependencies', 'overrides'])
    passed = (repository.get('private') is False and all(r['matches'] for r in records)
              and differences == ['package.json'] and package_identity_and_pins_match)
    result = {'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'commit': args.commit, 'anonymous_access': True, 'repository_http_status': status,
              'repository_is_private': repository.get('private'), 'checked_files': len(records),
              'matching_files': sum(r['matches'] for r in records),
              'supported_runtime_package_metadata_differences': differences,
              'runtime_package_identity_and_dependency_pins_match': package_identity_and_pins_match,
              'files': records, 'passed': passed, 'fabrication_ready': False}
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'files'}))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
