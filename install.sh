#!/usr/bin/env bash
# install.sh — Install twat-task locally
# Video processing task utilities using Prefect for workflow management
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing twat-task..."
uv pip install -e . 2>/dev/null || pip install -e .
echo "Done."
