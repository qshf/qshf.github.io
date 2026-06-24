#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-1313}"

echo "Starting Hugo preview at http://${HOST}:${PORT}/"
exec hugo server \
  --bind "$HOST" \
  --port "$PORT" \
  --disableFastRender
