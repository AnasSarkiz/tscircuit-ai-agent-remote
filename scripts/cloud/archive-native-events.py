"""Losslessly archive large native event captures and verify every original byte."""
import argparse
import hashlib
import json
import tarfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capture_root')
    args = parser.parse_args()
    for directory in sorted(Path(args.capture_root).iterdir()):
        if not directory.is_dir():
            continue
        files = sorted([*directory.glob('event-*.json'), *directory.glob('start-*.json')])
        if not files:
            continue
        archive_path = directory/'native-events.tar.gz'
        receipt_path = directory/'native-event-archive.json'
        if archive_path.exists() or receipt_path.exists():
            raise FileExistsError(f'Refusing to replace an existing archive: {directory}')
        originals = {path.name: {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for path in files}
        temporary_archive = directory/'.native-events.tar.gz.inprogress'
        # A budget stop retains originals; an interrupted temporary archive can
        # be rewritten without replacing any verified capture or receipt.
        with tarfile.open(temporary_archive, 'w:gz', compresslevel=5) as archive:
            for path in files:
                archive.add(path, arcname=path.name)
        with tarfile.open(temporary_archive, 'r:gz') as archive:
            assert set(archive.getnames()) == set(originals)
            for name, expected in originals.items():
                content = archive.extractfile(name).read()
                assert len(content) == expected['bytes']
                assert hashlib.sha256(content).hexdigest() == expected['sha256']
        temporary_archive.rename(archive_path)
        receipt_path.write_text(json.dumps({'classification': 'lossless original native event archive; not a solver cache',
            'archive': archive_path.name, 'archive_sha256': hashlib.sha256(archive_path.read_bytes()).hexdigest(),
            'verified_exact_original_bytes_before_removal': True, 'files': originals,
            'restore': 'tar -xzf native-events.tar.gz (run inside this capture directory)'}, indent=2)+'\n')
        for path in files:
            assert hashlib.sha256(path.read_bytes()).hexdigest() == originals[path.name]['sha256']
            path.unlink()
        print(json.dumps({'directory': str(directory), 'files': len(files),
            'original_bytes': sum(record['bytes'] for record in originals.values()), 'archive_bytes': archive_path.stat().st_size}), flush=True)


if __name__ == '__main__':
    main()
