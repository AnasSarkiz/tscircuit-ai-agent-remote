"""Verify the published source and native anonymously, without CI assumptions."""
import concurrent.futures
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
FOLDER = Path(__file__).resolve().parent
REPOSITORY = 'AnasSarkiz/tscircuit-ai-agent-remote'
VERSION = REPOSITORY + '@0.0.11-wip-generator-qualification'
STAGE = ROOT / '.publish/board'
COMMIT = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
SPEC = importlib.util.spec_from_file_location('registry_verification', ROOT / 'scripts/verify-registry-publication.py')
REGISTRY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REGISTRY)


def get_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={}), timeout=30) as response:
        return json.load(response)


def verify_github_file(filename):
    url = f'https://raw.githubusercontent.com/{REPOSITORY}/{COMMIT}/{filename}'
    with urllib.request.urlopen(urllib.request.Request(url, headers={}), timeout=30) as response:
        payload = response.read()
        status = response.status
    local = (ROOT / filename).read_bytes()
    staged = (STAGE / filename).read_bytes()
    package_metadata_ok = None
    if filename == 'package.json':
        public_package = json.loads(payload)
        staged_package = json.loads(staged)
        package_metadata_ok = all(public_package[field] == staged_package[field]
                                  for field in ['name', 'version', 'devDependencies', 'overrides'])
    return {'path': filename, 'anonymous_http_status': status,
            'local_sha256': hashlib.sha256(local).hexdigest(),
            'remote_sha256': hashlib.sha256(payload).hexdigest(),
            'matches': payload == local,
            'stage_matches_repository': staged == payload,
            'runtime_package_identity_and_dependency_pins_match': package_metadata_ok}


def main():
    paths = sorted(p.relative_to(STAGE).as_posix() for p in STAGE.rglob('*') if p.is_file())
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        files = list(executor.map(verify_github_file, paths))
    repository = get_json('https://api.github.com/repos/' + REPOSITORY)
    main_ref = get_json('https://api.github.com/repos/' + REPOSITORY + '/git/ref/heads/main')
    github = {'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'commit': COMMIT, 'commit_url': f'https://github.com/{REPOSITORY}/commit/{COMMIT}',
              'anonymous_access': True, 'main_matches': main_ref['object']['sha'] == COMMIT,
              'repository_is_private': repository['private'], 'checked_files': len(files),
              'matching_files': sum(r['matches'] for r in files),
              'supported_runtime_package_metadata_differences': ['package.json'], 'files': files}
    (FOLDER / 'github-publication-receipt.json').write_text(json.dumps(github, indent=2) + '\n')
    assert not github['repository_is_private'] and github['main_matches']
    assert all(r['matches'] for r in files)
    assert all(r['stage_matches_repository'] or r['runtime_package_identity_and_dependency_pins_match'] for r in files)
    release = REGISTRY.post('package_releases/get', {'package_name_with_version': VERSION})['package_release']
    release_id = release['package_release_id']
    url = 'https://registry-api.tscircuit.com/package_releases/get_preview_circuit_json?package_release_id=' + release_id
    preview = get_json(url)
    native_payload = (ROOT / 'dist/index/circuit.json').read_bytes()
    native = json.loads(native_payload)
    public_native = preview['preview_circuit_json_response']['circuit_json']
    page_url = f'https://tscircuit.com/{REPOSITORY}/releases/{release_id}/preview'
    with urllib.request.urlopen(urllib.request.Request(page_url, headers={}), timeout=30) as response:
        page_status = response.status
    receipt = {'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'release_id': release_id, 'version': '0.0.11-wip-generator-qualification',
               'preview_endpoint_url': url, 'anonymous_http_status': 200,
               'exact_native_object_equality': public_native == native,
               'local_native_json_sha256': hashlib.sha256(native_payload).hexdigest(),
               'native_elements': len(native), 'preview_page_url': page_url,
               'preview_page_anonymous_http_status': page_status,
               'cloud_CI_success_inferred': False, 'fabrication_ready': False}
    (FOLDER / 'final-public-preview-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'github_commit': COMMIT, 'github_matching_files': github['matching_files'], **receipt}))
    assert receipt['exact_native_object_equality'] and page_status == 200


if __name__ == '__main__':
    main()
