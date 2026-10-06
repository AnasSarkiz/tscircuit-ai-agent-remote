"""Preserve the full strict-schema failure tree and publish a compact summary."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

FOLDER = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', nargs='?', type=Path, default=FOLDER)
    folder = parser.parse_args().folder
    original = folder / 'schema-audit.json'
    compressed = folder / 'schema-audit.json.gz'
    if compressed.exists():
        raise FileExistsError(compressed)
    original_bytes = original.read_bytes()
    original_sha256 = hashlib.sha256(original_bytes).hexdigest()
    result = json.loads(original_bytes)
    summary = {key: record for key, record in result.items() if key != 'failures'}
    summary['failures'] = [{'index': failure['index'], 'type': failure['type']}
                           for failure in result['failures']]
    summary['full_original_failure_tree'] = compressed.name
    summary['full_original_failure_tree_sha256'] = original_sha256
    (folder / 'schema-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    with gzip.open(compressed, 'wb', compresslevel=5) as stream:
        stream.write(original_bytes)
    with gzip.open(compressed, 'rb') as stream:
        restored_bytes = stream.read()
    if restored_bytes != original_bytes:
        raise ValueError('Schema archive did not preserve exact original bytes')
    receipt = {'original': original.name, 'original_bytes': len(original_bytes),
               'original_sha256': original_sha256, 'archive': compressed.name,
               'archive_bytes': compressed.stat().st_size,
               'archive_sha256': hashlib.sha256(compressed.read_bytes()).hexdigest(),
               'verified_exact_original_bytes_before_removal': True,
               'restore': 'gzip -dk schema-audit.json.gz'}
    (folder / 'schema-archive.json').write_text(json.dumps(receipt, indent=2) + '\n')
    if hashlib.sha256(original.read_bytes()).hexdigest() != original_sha256:
        raise ValueError('Original schema receipt changed before removal')
    original.unlink()
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
