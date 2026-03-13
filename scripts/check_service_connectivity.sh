#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo "CHECK DE COMUNICAÇÃO ENTRE SERVIÇOS"
echo "=================================================="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo
echo "[1] PROMTAIL -> LOKI (evidência por logs)"
docker compose logs --tail=50 loki promtail | grep -E "flushing stream|Adding target|tail routine: started" || true

echo
echo "[2] PROMETHEUS -> NODE EXPORTER"
docker compose exec prometheus sh -c 'wget -qO- http://node-exporter:9100/metrics | head' || true

echo
echo "[3] PROMTAIL -> APP LOG FILE"
docker compose exec promtail sh -c 'ls -l /app/logs && tail -n 5 /app/logs/app.log' || true

echo
echo "=================================================="
echo "FIM DO CHECK DE COMUNICAÇÃO"
echo "=================================================="