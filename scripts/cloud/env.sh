# Source this in cloud task shells after setup; no credentials or machine-specific paths.
cloud_board_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
if [[ -x "$cloud_board_root/.tools/bun/bin/bun" ]]; then
  export PATH="$cloud_board_root/.tools/bun/bin:$PATH"
fi
export PYTHONPATH="$cloud_board_root/.geometry-runtime${PYTHONPATH:+:$PYTHONPATH}"
# Keep CLI configuration and dependency caches in the writable cloud checkout.
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$cloud_board_root/.tools/cache}"
mkdir -p "$XDG_CACHE_HOME"
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$cloud_board_root/.tools/config}"
export BUN_INSTALL_CACHE_DIR="${BUN_INSTALL_CACHE_DIR:-$cloud_board_root/.tools/bun-cache}"
export npm_config_cache="${npm_config_cache:-$cloud_board_root/.tools/npm-cache}"
export PIP_CACHE_DIR="${PIP_CACHE_DIR:-$cloud_board_root/.tools/pip-cache}"
