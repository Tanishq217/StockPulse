#!/usr/bin/env bash
set -euo pipefail

URL="${URL:-http://localhost:8000/api/inventory}"
REQUESTS="${REQUESTS:-500}"

echo "============================================================"
echo "StockPulse Traffic Generator & Prometheus Scrape Load Test"
echo "Target Endpoint : $URL"
echo "Total Requests  : $REQUESTS"
echo "============================================================"

for i in $(seq 1 "$REQUESTS"); do
  curl -s "$URL" >/dev/null || true
  if (( i % 100 == 0 )); then
    echo "[$i / $REQUESTS] requests transmitted..."
  fi
done

echo "============================================================"
echo "Load test finished successfully! Check /metrics or Grafana."
echo "============================================================"
