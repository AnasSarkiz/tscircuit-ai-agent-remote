"""Install verified official Freerouting and Java releases in the ignored cache."""
import hashlib
import json
import subprocess
import tarfile
from pathlib import Path

ARTIFACTS = [
    ('freerouting-2.5.0.jar',
     'https://github.com/freerouting/freerouting/releases/download/v2.5.0/freerouting-2.5.0.jar',
     'f6f51bb02245e8e717f9359bd260cc9c5c0b1bc0acc8b7cb2cd5b8ffeb5de3c7'),
    ('OpenJDK25U-jdk_x64_linux_hotspot_25.0.4.1_1.tar.gz',
     'https://github.com/adoptium/temurin25-binaries/releases/download/jdk-25.0.4.1%2B1/OpenJDK25U-jdk_x64_linux_hotspot_25.0.4.1_1.tar.gz',
     'dbb698396d478e7fa2b1e50f4103324b2a99b90569ee27c33f2261f9215cf41e'),
]


def main():
    root = Path(__file__).resolve().parents[2]
    target = root / '.tools' / 'freerouting'
    target.mkdir(parents=True, exist_ok=True)
    receipts = []
    for filename, url, expected_sha256 in ARTIFACTS:
        artifact = target / filename
        if not artifact.exists():
            pending = artifact.with_suffix(artifact.suffix + '.download')
            subprocess.run(['curl', '--fail', '--silent', '--show-error', '--location',
                            '--max-time', '180', url, '--output', str(pending)], check=True)
            if hashlib.sha256(pending.read_bytes()).hexdigest() != expected_sha256:
                raise ValueError(f'Official release checksum mismatch: {filename}')
            pending.rename(artifact)
        actual_sha256 = hashlib.sha256(artifact.read_bytes()).hexdigest()
        if actual_sha256 != expected_sha256:
            raise ValueError(f'Cached artifact checksum mismatch: {filename}')
        receipts.append({'filename': filename, 'official_release_url': url,
                         'sha256': actual_sha256, 'bytes': artifact.stat().st_size})
    with tarfile.open(target / ARTIFACTS[1][0]) as archive:
        archive.extractall(target, filter='data')
    java = target / 'jdk-25.0.4.1+1' / 'bin' / 'java'
    subprocess.run([str(java), '-version'], check=True)
    print(json.dumps({'verified_artifacts': receipts, 'java': str(java),
                      'jar': str(target / ARTIFACTS[0][0]), 'routing_started': False}))


if __name__ == '__main__':
    main()
