#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo "ABERTURA DE SESSÃO — PROJETO 03"
echo "=================================================="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo
echo "[1] DIRETÓRIO ATUAL"
pwd

echo
echo "[2] BRANCH ATUAL"
git branch --show-current

echo
echo "[3] STATUS DO GIT"
git status --short || true

echo
echo "[4] ÚLTIMOS COMMITS"
git log --oneline --decorate -n 5 || true

echo
echo "[5] ESTRUTURA PRINCIPAL"
find . -maxdepth 2 \( -type f -o -type d \) \
  ! -path "./.git*" \
  ! -path "./grafana/data*" \
  ! -path "./loki/data*" \
  ! -path "./prometheus/data*" \
  | sort

echo
echo "[6] ARQUIVOS CRÍTICOS"

for file in \
  "docker-compose.yml" \
  "promtail/config.yml" \
  "prometheus/prometheus.yml" \
  "loki/config.yml" \
  "README.md" \
  "docs/contexto.md" \
  "docs/arquitetura.md" \
  "docs/troubleshooting.md"
do
  if [[ -f "$file" ]]; then
    echo
    echo "----- $file -----"
    sed -n '1,220p' "$file"
  else
    echo
    echo "----- $file -----"
    echo "ARQUIVO NÃO ENCONTRADO"
  fi
done

echo
echo "[7] STATUS DA STACK"
docker compose ps || true

echo
echo "[8] LOGS RECENTES DA STACK"
docker compose logs --tail=80 || true

echo
echo "=================================================="
echo "FIM DA ABERTURA DE SESSÃO"
echo "=================================================="
