#!/usr/bin/env bash
set -euo pipefail
# Keep the verified lockfile/test runtime separate from the completed native-build runtime.
board_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
if [[ "$(uname -s)" != Linux || "$(uname -m)" != x86_64 ]]; then
  echo "The qualified generation runtime requires Linux x86_64." >&2
  exit 2
fi
runtime_dir="$board_root/.tools/bun-1.4.0"
archive_sha="2d03fb5fb83ac8b567aca0a281b2ce1a1a19d488f56c2968d88c3f25e92fe452"
mkdir -p "$runtime_dir"
if [[ ! -f "$runtime_dir/bun.zip" ]] || ! echo "$archive_sha  $runtime_dir/bun.zip" | sha256sum --check --status; then
  curl --fail --silent --show-error --location \
    https://github.com/oven-sh/bun/releases/download/bun-v1.4.0/bun-linux-x64.zip \
    --output "$runtime_dir/bun.zip"
fi
echo "$archive_sha  $runtime_dir/bun.zip" | sha256sum --check --status
python3 - "$runtime_dir" <<'PY'
import pathlib, sys, zipfile
directory = pathlib.Path(sys.argv[1])
with zipfile.ZipFile(directory / "bun.zip") as archive:
    archive.extract("bun-linux-x64/bun", directory)
(directory / "bun-linux-x64/bun").chmod(0o755)
PY
[[ "$("$runtime_dir/bun-linux-x64/bun" --version)" == 1.4.0 ]]
echo "Qualified native generation runtime: Bun 1.4.0; lockfile/test runtime unchanged."
