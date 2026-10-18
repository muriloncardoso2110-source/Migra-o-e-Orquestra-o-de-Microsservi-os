#!/usr/bin/env bash
set -euo pipefail
PORT="${APP_PORT:-8080}"
for route in /health /api/products /api/customers /api/orders; do
  curl --fail --silent --show-error "http://localhost:${PORT}${route}" >/dev/null
  echo "OK ${route}"
done
