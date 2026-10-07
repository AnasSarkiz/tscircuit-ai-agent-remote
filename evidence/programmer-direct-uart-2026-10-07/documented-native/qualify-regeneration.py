"""Accept a completed documentation-only regeneration by exact native comparison."""
from pathlib import Path
import gzip
import hashlib
import json
import tarfile

ROOT = Path(__file__).resolve().parents[3]
FOLDER = Path(__file__).resolve().parent
EVIDENCE = FOLDER.parent
STAGE = ROOT / '.publish/board'


def sha256(payload):
    return hashlib.sha256(payload).hexdigest()


def main():
    outcome = json.loads((EVIDENCE / 'documented-native-linked-build.log.outcome.json').read_text())
    assert outcome['completed_command'] and outcome['exit_code'] == 1
    previous_payload = gzip.decompress((EVIDENCE / 'final-native/circuit.json.gz').read_bytes())
    new_payload = (STAGE / 'dist/index/circuit.json').read_bytes()
    previous = json.loads(previous_payload)
    new = json.loads(new_payload)
    previous_records = [r for r in previous if r['type'] != 'source_project_metadata']
    new_records = [r for r in new if r['type'] != 'source_project_metadata']
    previous_metadata = [r for r in previous if r['type'] == 'source_project_metadata']
    new_metadata = [r for r in new if r['type'] == 'source_project_metadata']
    strip_hash = lambda rows: [{k: v for k, v in r.items() if k != 'source_filesystem_md5_hash'} for r in rows]
    expected_source = json.loads((FOLDER / 'source-manifest.json').read_text())
    changed_sources = [p for p, binding in expected_source.items()
                       if sha256((STAGE / p).read_bytes()) != binding['sha256']]
    receipt = {'previous_native_sha256': sha256(previous_payload),
               'new_native_sha256': sha256(new_payload), 'new_native_bytes': len(new_payload),
               'completed_regeneration': outcome['completed_command'],
               'build_outcome': '../documented-native-linked-build.log.outcome.json',
               'all_non_metadata_records_exactly_identical': previous_records == new_records,
               'all_other_metadata_fields_exactly_identical': strip_hash(previous_metadata) == strip_hash(new_metadata),
               'previous_source_filesystem_md5': previous_metadata[0]['source_filesystem_md5_hash'],
               'new_source_filesystem_md5': new_metadata[0]['source_filesystem_md5_hash'],
               'changed_runtime_source_files_during_generation': changed_sources,
               'qualification_reuse_scope': 'Exact unchanged circuit/geometry/errors/schema/annotations justify retaining previous native copper, width, continuity, UI, visual and snapshot receipts. Only source filesystem metadata changes for corrected documentation. Raw prior receipt hashes are retained, not rewritten.',
               'fabrication_ready': False}
    (FOLDER / 'comparison.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt), flush=True)
    assert receipt['all_non_metadata_records_exactly_identical']
    assert receipt['all_other_metadata_fields_exactly_identical'] and not changed_sources
    assert receipt['new_source_filesystem_md5'] != receipt['previous_source_filesystem_md5']
    (FOLDER / 'circuit.json.gz').write_bytes(gzip.compress(new_payload, mtime=0))
    manifest = {}
    with tarfile.open(FOLDER / 'completed-source-and-events.tar.gz', 'w:gz') as archive:
        for path in sorted(STAGE.rglob('*')):
            if not path.is_file() or 'node_modules' in path.parts:
                continue
            if 'dist' in path.parts and 'autorouter-debug' not in path.parts:
                continue
            relative = path.relative_to(STAGE).as_posix()
            payload = path.read_bytes()
            manifest[relative] = {'sha256': sha256(payload), 'bytes': len(payload)}
            archive.add(path, arcname=relative, recursive=False)
    (FOLDER / 'completed-source-and-events-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (ROOT / 'dist/index/circuit.json').write_bytes(new_payload)
    summary_path = EVIDENCE / 'final-qualification-summary.json'
    summary = json.loads(summary_path.read_text())
    summary.update(native_sha256=sha256(new_payload), native_bytes=len(new_payload),
                   native_source_filesystem_md5=new_metadata[0]['source_filesystem_md5_hash'],
                   qualification_native_sha256=sha256(previous_payload),
                   documentation_regeneration_comparison='documented-native/comparison.json',
                   all_non_metadata_native_records_exactly_identical=True)
    summary_path.write_text(json.dumps(summary, indent=2) + '\n')
    checkpoint_path = ROOT / 'context/build-checkpoint.json'
    checkpoint = json.loads(checkpoint_path.read_text())
    checkpoint.update(sha256=sha256(new_payload), size_bytes=len(new_payload),
                      native_build='evidence/programmer-direct-uart-2026-10-07/documented-native/circuit.json.gz',
                      publication_runtime_cli_build_seconds=outcome['elapsed_seconds'],
                      accepted_source_snapshot='evidence/programmer-direct-uart-2026-10-07/documented-native/completed-source-and-events.tar.gz',
                      documentation_regeneration_comparison='evidence/programmer-direct-uart-2026-10-07/documented-native/comparison.json')
    checkpoint_path.write_text(json.dumps(checkpoint, indent=2) + '\n')
    handoff = ROOT / 'CLOUD_HANDOFF.md'
    handoff.write_text(handoff.read_text().replace(sha256(previous_payload), sha256(new_payload), 1))


if __name__ == '__main__':
    main()
