# Source this in cloud task shells after setup; no credentials or machine-specific paths.
cloud_board_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
if [[ -x "$cloud_board_root/.tools/bun/bin/bun" ]]; then
  export PATH="$cloud_board_root/.tools/bun/bin:$PATH"
fi
export PYTHONPATH="$cloud_board_root/.geometry-runtime${PYTHONPATH:+:$PYTHONPATH}"
