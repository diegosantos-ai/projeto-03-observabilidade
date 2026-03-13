#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo "FECHAMENTO DE SESSÃO — PROJETO 03"
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
echo "[3] STATUS FINAL DO GIT"
git status || true

echo
echo "[4] DIFF RESUMIDO"
git diff --stat || true

echo
echo "[5] ÚLTIMOS COMMITS"
git log --oneline --decorate -n 5 || true

echo
echo "[6] STATUS FINAL DA STACK"
docker compose ps || true

echo
echo "[7] LOGS FINAIS DA STACK"
docker compose logs --tail=80 || true

echo
echo "[8] PENDÊNCIAS MANUAIS SUGERIDAS"
echo "- Confirmar fase atual"
echo "- Confirmar task atual"
echo "- Confirmar se houve mudança relevante que exige commit"
echo "- Confirmar se a stack precisa continuar ligada ou pode ser derrubada"
echo "- Registrar mini relatório no Trello ao encerrar fase"

echo
echo "=================================================="
echo "FIM DO FECHAMENTO DE SESSÃO"
echo "=================================================="
