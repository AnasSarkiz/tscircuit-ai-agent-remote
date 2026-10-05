#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "Cloud setup is Linux-only. Do not start routing on the Mac." >&2
  exit 2
fi
board_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$board_root"
python3 scripts/cloud/verify_checkpoint.py
mkdir -p .tools
if ! command -v bun >/dev/null || [[ "$(bun --version)" != "1.3.9" ]]; then
  curl --fail --silent --show-error --location https://bun.sh/install --output .tools/install-bun.sh
  BUN_INSTALL="$board_root/.tools/bun" bash .tools/install-bun.sh bun-v1.3.9
  cloud_bun="$board_root/.tools/bun/bin/bun"
else
  cloud_bun="$(command -v bun)"
fi
"$cloud_bun" install --frozen-lockfile
python3 -m pip install --target .geometry-runtime -r scripts/cloud/requirements.txt
"$cloud_bun" --version
python3 --version
python3 scripts/cloud/smoke_test.py
echo "Dependencies installed. Routing and heavy board builds were not started."
