"""Verify the migration checkpoint bytes before cloud continuation changes."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
manifest = json.loads((root / "context/checkpoint-sha256.json").read_text())
failures = []
for filename, expected in manifest["files"].items():
    path = root / filename
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        failures.append(filename)
print(json.dumps({"verified_files": len(manifest["files"]), "mismatched_or_missing": failures,
                  "fabrication_approval_inferred": False}, indent=2))
raise SystemExit(1 if failures else 0)
