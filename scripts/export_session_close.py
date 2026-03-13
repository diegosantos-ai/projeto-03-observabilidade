#!/usr/bin/env python3
"""
Gera checkpoint de fechamento da sessão.

Objetivo:
- Registrar o estado final da sessão.
- Facilitar retomada no próximo dia.
- Atualizar status oficial curto do projeto.

Saídas:
- docs/checkpoints/current-session.md
- docs/checkpoints/project-status.md
"""

from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CURRENT_SESSION_FILE = PROJECT_ROOT / "docs" / "checkpoints" / "current-session.md"
PROJECT_STATUS_FILE = PROJECT_ROOT / "docs" / "checkpoints" / "project-status.md"

COMMANDS = [
    ("pwd", ["pwd"]),
    ("git branch --show-current", ["git", "branch", "--show-current"]),
    ("git status --short", ["git", "status", "--short"]),
    ("git log --oneline --decorate -n 10", ["git", "log", "--oneline", "--decorate", "-n", "10"]),
    ("docker compose ps", ["docker", "compose", "ps"]),
    ("docker compose logs --tail=30 promtail", ["docker", "compose", "logs", "--tail=30", "promtail"]),
    ("docker compose logs --tail=20 loki", ["docker", "compose", "logs", "--tail=20", "loki"]),
    ("docker compose logs --tail=20 prometheus", ["docker", "compose", "logs", "--tail=20", "prometheus"]),
    ("docker compose logs --tail=20 grafana", ["docker", "compose", "logs", "--tail=20", "grafana"]),
]


def run_command(command: list[str]) -> str:
    """
    Executa comando na raiz do projeto.

    Args:
        command: Comando e argumentos.

    Returns:
        Saída formatada.
    """
    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:  # pragma: no cover
        return f"[ERRO AO EXECUTAR COMANDO]\n{exc}"

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    if result.returncode == 0:
        return stdout or "[sem saída]"
    return f"[exit code: {result.returncode}]\nSTDOUT:\n{stdout or '[vazio]'}\n\nSTDERR:\n{stderr or '[vazio]'}"


def read_file(relative_path: str) -> str:
    """
    Lê arquivo relativo ao projeto.

    Args:
        relative_path: Caminho relativo.

    Returns:
        Conteúdo ou mensagem de ausência.
    """
    path = PROJECT_ROOT / relative_path
    if not path.exists():
        return "[arquivo não encontrado]"
    if path.is_dir():
        return "[caminho é um diretório]"

    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        return f"[erro ao ler arquivo]\n{exc}"


def extract_status_fields(project_status_content: str) -> dict[str, str]:
    """
    Extrai campos do arquivo de status oficial.

    Args:
        project_status_content: Conteúdo bruto.

    Returns:
        Dicionário com campos.
    """
    fields = {
        "fase_atual": "Fase não identificada",
        "task_atual": "Task não identificada",
        "objetivo_imediato": "Objetivo não identificado",
        "bloqueio_principal": "Bloqueio não identificado",
        "proxima_acao": "Próxima ação não identificada",
    }

    mapping = {
        "fase atual:": "fase_atual",
        "task atual:": "task_atual",
        "objetivo imediato:": "objetivo_imediato",
        "bloqueio principal:": "bloqueio_principal",
        "próxima ação:": "proxima_acao",
        "proxima ação:": "proxima_acao",
    }

    for raw_line in project_status_content.splitlines():
        line = raw_line.strip()
        lower = line.lower()
        for prefix, key in mapping.items():
            if lower.startswith(prefix):
                fields[key] = line.split(":", 1)[1].strip() if ":" in line else fields[key]

    return fields


def build_section(title: str, content: str, language: str = "") -> str:
    """
    Cria uma seção Markdown com bloco de código.

    Args:
        title: Título.
        content: Conteúdo.
        language: Linguagem opcional.

    Returns:
        Texto formatado.
    """
    fence = f"```{language}".rstrip()
    return f"## {title}\n\n{fence}\n{content.rstrip()}\n```\n"


def detect_blocker(promtail_logs: str) -> tuple[str, str, str]:
    """
    Detecta bloqueio principal com base nos logs do Promtail.

    Args:
        promtail_logs: Logs recentes do Promtail.

    Returns:
        Tupla com erro observado, impacto e causa provável.
    """
    if "error writing positions file" in promtail_logs and "device or resource busy" in promtail_logs:
        return (
            "Promtail falha recorrentemente ao gravar o arquivo de posições.",
            "Impede considerar coerente a persistência mínima da stack na Fase 4.",
            "Conflito provável entre escrita atômica do Promtail e estratégia de volume montado para positions.yaml.",
        )

    return (
        "Nenhum bloqueio principal foi detectado automaticamente nos logs do Promtail.",
        "Sem impacto principal definido automaticamente.",
        "Causa provável não identificada automaticamente.",
    )


def update_project_status(
    current_fields: dict[str, str],
    blocker_error: str,
    blocker_cause: str,
) -> None:
    """
    Atualiza o arquivo de status oficial curto do projeto.

    Args:
        current_fields: Campos atuais extraídos.
        blocker_error: Erro observado.
        blocker_cause: Causa provável.
    """
    next_action = current_fields["proxima_acao"]
    if "Promtail" in blocker_error:
        next_action = "Revisar volume do Promtail, corrigir persistência do positions.yaml e revalidar a Fase 4."

    new_content = "\n".join(
        [
            "# Status Atual do Projeto 03",
            "",
            "## Projeto",
            "Projeto 03 — Observabilidade, Logs e Alertas",
            "",
            f"Fase atual: {current_fields['fase_atual']}",
            f"Task atual: {current_fields['task_atual']}",
            f"Objetivo imediato: {current_fields['objetivo_imediato']}",
            f"Bloqueio principal: {blocker_error} Causa provável: {blocker_cause}",
            f"Próxima ação: {next_action}",
            "",
        ]
    )
    PROJECT_STATUS_FILE.write_text(new_content, encoding="utf-8")


def main() -> None:
    """
    Executa geração do checkpoint de fechamento.
    """
    CURRENT_SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROJECT_STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)

    project_status_content = read_file("docs/checkpoints/project-status.md")
    status_fields = extract_status_fields(project_status_content)

    outputs = {label: run_command(cmd) for label, cmd in COMMANDS}
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    promtail_logs = outputs["docker compose logs --tail=30 promtail"]
    blocker_error, blocker_impact, blocker_cause = detect_blocker(promtail_logs)

    next_action = status_fields["proxima_acao"]
    if "Promtail" in blocker_error:
        next_action = "Corrigir persistência do Promtail e revalidar T8/T9 da Fase 4."

    content_parts: list[str] = []
    content_parts.append("# Checkpoint de Fechamento de Sessão\n")
    content_parts.append("## 1. Identificação\n")
    content_parts.append(f"- Data e hora: {now}")
    content_parts.append(f"- Projeto: {PROJECT_ROOT.name}")
    content_parts.append(f"- Diretório atual: {outputs['pwd']}")
    content_parts.append(f"- Branch atual: {outputs['git branch --show-current']}\n")

    content_parts.append("## 2. Fase atual\n")
    content_parts.append(f"- {status_fields['fase_atual']}\n")

    content_parts.append("## 3. Task atual\n")
    content_parts.append(f"- {status_fields['task_atual']}\n")

    content_parts.append("## 4. Objetivo da sessão\n")
    content_parts.append(f"- {status_fields['objetivo_imediato']}\n")

    content_parts.append("## 5. O que foi feito hoje\n")
    content_parts.append("- Coleta de estado atual do repositório e da stack.")
    content_parts.append("- Consolidação de contexto técnico e operacional.")
    content_parts.append("- Registro de logs recentes dos serviços principais.")
    content_parts.append("- Atualização de checkpoint para retomada futura.\n")

    content_parts.append("## 6. O que foi validado\n")
    content_parts.append("- Estado atual dos containers via `docker compose ps`.")
    content_parts.append("- Logs recentes de Promtail, Loki, Prometheus e Grafana.")
    content_parts.append("- Branch atual e status do repositório.")
    if "Promtail" in blocker_error:
        content_parts.append("- Foi confirmado bloqueio recorrente na persistência do arquivo de posições do Promtail.\n")
    else:
        content_parts.append("- Nenhum bloqueio recorrente principal foi detectado automaticamente.\n")

    content_parts.append("## 7. Pendências abertas\n")
    if "Promtail" in blocker_error:
        content_parts.append("- Corrigir persistência do `positions.yaml` do Promtail.")
        content_parts.append("- Revalidar health básico dos containers.")
        content_parts.append("- Revalidar comunicação entre serviços.")
        content_parts.append("- Confirmar fechamento formal da Fase 4.\n")
    else:
        content_parts.append("- Revisão manual das pendências da fase atual.\n")

    content_parts.append("## 8. Bloqueio atual\n")
    content_parts.append(f"- Erro observado: {blocker_error}")
    content_parts.append(f"- Impacto: {blocker_impact}")
    content_parts.append(f"- Causa provável: {blocker_cause}")
    content_parts.append(f"- Como retomar amanhã: {next_action}\n")

    content_parts.append("## 9. Decisões técnicas tomadas\n")
    content_parts.append(f"- Fase atual preservada como: {status_fields['fase_atual']}")
    content_parts.append(f"- Task atual preservada como: {status_fields['task_atual']}")
    content_parts.append("- O status oficial do projeto foi atualizado sem alterar arquitetura ou configs automaticamente.\n")

    content_parts.append("## 10. Arquivos relevantes alterados\n")
    content_parts.append("- `docs/checkpoints/current-session.md`")
    content_parts.append("- `docs/checkpoints/project-status.md`\n")

    content_parts.append("## 11. Estado atual do git\n")
    content_parts.append(build_section("git status --short", outputs["git status --short"], "bash"))
    content_parts.append(build_section("git log --oneline --decorate -n 10", outputs["git log --oneline --decorate -n 10"], "bash"))

    content_parts.append("## 12. Estado atual da stack\n")
    content_parts.append(build_section("docker compose ps", outputs["docker compose ps"], "bash"))
    content_parts.append(build_section("docker compose logs --tail=30 promtail", outputs["docker compose logs --tail=30 promtail"], "bash"))
    content_parts.append(build_section("docker compose logs --tail=20 loki", outputs["docker compose logs --tail=20 loki"], "bash"))
    content_parts.append(build_section("docker compose logs --tail=20 prometheus", outputs["docker compose logs --tail=20 prometheus"], "bash"))
    content_parts.append(build_section("docker compose logs --tail=20 grafana", outputs["docker compose logs --tail=20 grafana"], "bash"))

    content_parts.append("## 13. Próxima ação recomendada\n")
    content_parts.append(f"- {next_action}\n")

    content_parts.append("## 14. Prompt de retomada\n")
    prompt = (
        f"Retomada do {PROJECT_ROOT.name}. "
        f"Fase atual: {status_fields['fase_atual']}. "
        f"Task atual: {status_fields['task_atual']}. "
        f"Status: stack em andamento com checkpoint atualizado. "
        f"Bloqueio principal: {blocker_error} "
        f"Objetivo da próxima sessão: {next_action} "
        f"Leia primeiro `docs/checkpoints/project-status.md` e `docs/checkpoints/current-session.md`."
    )
    content_parts.append(f"```text\n{prompt}\n```\n")

    CURRENT_SESSION_FILE.write_text("\n".join(content_parts).rstrip() + "\n", encoding="utf-8")
    update_project_status(status_fields, blocker_error, blocker_cause)

    print(f"Arquivo atualizado: {CURRENT_SESSION_FILE}")
    print(f"Arquivo atualizado: {PROJECT_STATUS_FILE}")


if __name__ == "__main__":
    main()