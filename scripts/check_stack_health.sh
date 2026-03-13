#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo "CHECK DE HEALTH DA STACK"
echo "=================================================="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo
echo "[1] CONTAINERS"
docker compose ps

echo
echo "[2] LOGS RECENTES"
docker compose logs --tail=100 || true

echo
echo "[3] PORTAS ESPERADAS"
echo "- Grafana:    http://localhost:3000"
echo "- Loki:       http://localhost:3100"
echo "- Prometheus: http://localhost:9090"
echo "- Node Exporter: http://localhost:9100"

echo
echo "=================================================="
echo "FIM DO CHECK DE HEALTH"
echo "=================================================="
