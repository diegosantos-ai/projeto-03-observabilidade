#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "========================================"
echo "EXPORTANDO FECHAMENTO DE SESSÃO"
echo "Projeto: ${PROJECT_ROOT##*/}"
echo "Diretório: ${PROJECT_ROOT}"
echo "========================================"

cd "$PROJECT_ROOT"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "[ERRO] Python não encontrado: $PYTHON_BIN"
  exit 1
fi

mkdir -p docs/checkpoints

"$PYTHON_BIN" scripts/export_session_close.py

echo
echo "[OK] Arquivos atualizados:"
echo " - docs/checkpoints/current-session.md"
echo " - docs/checkpoints/project-status.md"