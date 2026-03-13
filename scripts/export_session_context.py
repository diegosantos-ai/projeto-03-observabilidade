#!/usr/bin/env python3
"""
Gera um relatório completo de contexto da sessão atual.

Objetivo:
- Consolidar contexto técnico e operacional do projeto em um único arquivo Markdown.
- Reduzir perda de contexto entre sessões.
- Fornecer material objetivo para retomada de trabalho.

Saída:
- docs/checkpoints/session-context.md
"""

from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "docs" / "checkpoints" / "session-context.md"

FILES_TO_INCLUDE = [
    "README.md",
    "docs/checkpoints/project-status.md",
    "docs/checkpoints/current-session.md",
    "docs/contexto.md",
    "docs/arquitetura.md",
    "docs/troubleshooting.md",
    "docker-compose.yml",
    "prometheus/prometheus.yml",
    "loki/config.yml",
    "promtail/config.yml",
    "scripts/session_start_check.sh",
    "scripts/session_end_check.sh",
    "scripts/check_stack_health.sh",
    "scripts/check_service_connectivity.sh",
]

COMMANDS = [
    ("pwd", ["pwd"]),
    ("git branch --show-current", ["git", "branch", "--show-current"]),
    ("git status --short", ["git", "status", "--short"]),
    ("git log --oneline --decorate -n 10", ["git", "log", "--oneline", "--decorate", "-n", "10"]),
    ("docker compose ps", ["docker", "compose", "ps"]),
    ("docker compose logs --tail=40 promtail", ["docker", "compose", "logs", "--tail=40", "promtail"]),
    ("docker compose logs --tail=30 loki", ["docker", "compose", "logs", "--tail=30", "loki"]),
    ("docker compose logs --tail=30 prometheus", ["docker", "compose", "logs", "--tail=30", "prometheus"]),
    ("docker compose logs --tail=30 grafana", ["docker", "compose", "logs", "--tail=30", "grafana"]),
]


def run_command(command: list[str]) -> str:
    """
    Executa um comando no diretório raiz do projeto.

    Args:
        command: Lista com comando e argumentos.

    Returns:
        Saída padrão ou mensagem de erro formatada.
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
    Lê um arquivo relativo à raiz do projeto.

    Args:
        relative_path: Caminho relativo do arquivo.

    Returns:
        Conteúdo do arquivo ou mensagem indicando ausência/erro.
    """
    file_path = PROJECT_ROOT / relative_path
    if not file_path.exists():
        return "[arquivo não encontrado]"

    if file_path.is_dir():
        return "[caminho é um diretório]"

    try:
        return file_path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        return f"[erro ao ler arquivo]\n{exc}"


def find_optional_files() -> list[str]:
    """
    Descobre arquivos adicionais úteis para contexto.

    Returns:
        Lista de caminhos relativos.
    """
    patterns = [
        "grafana/provisioning/**/*",
        "alerting/**/*",
    ]

    discovered: list[str] = []
    for pattern in patterns:
        for path in PROJECT_ROOT.glob(pattern):
            if path.is_file():
                discovered.append(str(path.relative_to(PROJECT_ROOT)))

    return sorted(set(discovered))


def extract_status_fields(project_status_content: str) -> dict[str, str]:
    """
    Extrai campos simples do arquivo de status oficial.

    Args:
        project_status_content: Conteúdo bruto do project-status.md.

    Returns:
        Dicionário com campos principais.
    """
    fields = {
        "fase_atual": "[não identificado]",
        "task_atual": "[não identificado]",
        "objetivo_imediato": "[não identificado]",
        "bloqueio_principal": "[não identificado]",
        "proxima_acao": "[não identificado]",
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
                fields[key] = line.split(":", 1)[1].strip() if ":" in line else "[não identificado]"

    return fields


def summarize_observed_issues(command_outputs: dict[str, str]) -> list[str]:
    """
    Resume problemas observados com base nas saídas coletadas.

    Args:
        command_outputs: Mapeamento comando -> saída.

    Returns:
        Lista de observações objetivas.
    """
    issues: list[str] = []

    promtail_logs = command_outputs.get("docker compose logs --tail=40 promtail", "")
    if "error writing positions file" in promtail_logs:
        issues.append(
            "Promtail apresenta erro recorrente ao gravar positions.yaml, com falha de rename em /tmp/positions.yaml."
        )

    if "device or resource busy" in promtail_logs:
        issues.append(
            "Há evidência de conflito no volume/arquivo de estado do Promtail ('device or resource busy')."
        )

    grafana_logs = command_outputs.get("docker compose logs --tail=30 grafana", "")
    if "can't read datasource provisioning files" in grafana_logs:
        issues.append(
            "Grafana está subindo sem estrutura completa de provisioning de datasources."
        )
    if "can't read dashboard provisioning files" in grafana_logs:
        issues.append(
            "Grafana está subindo sem estrutura completa de provisioning de dashboards."
        )

    prometheus_logs = command_outputs.get("docker compose logs --tail=30 prometheus", "")
    if "A lockfile from a previous execution already existed" in prometheus_logs:
        issues.append(
            "Prometheus registrou lockfile de execução anterior, mas continuou inicialização normalmente."
        )

    if not issues:
        issues.append("Nenhum erro recorrente evidente foi detectado automaticamente nas saídas analisadas.")

    return issues


def build_markdown_section(title: str, content: str, language: str = "") -> str:
    """
    Monta uma seção Markdown com bloco de código.

    Args:
        title: Título da seção.
        content: Conteúdo da seção.
        language: Linguagem opcional do bloco.

    Returns:
        Texto Markdown formatado.
    """
    fence = f"```{language}".rstrip()
    return f"## {title}\n\n{fence}\n{content.rstrip()}\n```\n"


def build_markdown_list(items: Iterable[str]) -> str:
    """
    Constrói lista Markdown simples.

    Args:
        items: Itens da lista.

    Returns:
        Lista formatada.
    """
    return "\n".join(f"- {item}" for item in items)


def main() -> None:
    """
    Executa a geração do arquivo de contexto da sessão.
    """
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    project_status_content = read_file("docs/checkpoints/project-status.md")
    status_fields = extract_status_fields(project_status_content)

    command_outputs = {label: run_command(cmd) for label, cmd in COMMANDS}

    discovered_files = find_optional_files()
    files_to_render = FILES_TO_INCLUDE + [f for f in discovered_files if f not in FILES_TO_INCLUDE]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    observed_issues = summarize_observed_issues(command_outputs)

    parts: list[str] = []
    parts.append("# Session Context\n")
    parts.append("## 1. Identificação da sessão\n")
    parts.append(f"- Data e hora: {now}")
    parts.append(f"- Projeto: {PROJECT_ROOT.name}")
    parts.append(f"- Diretório atual: {command_outputs['pwd']}")
    parts.append(f"- Branch atual: {command_outputs['git branch --show-current']}\n")

    parts.append("## 2. Estado oficial atual do projeto\n")
    parts.append(f"- Fase atual: {status_fields['fase_atual']}")
    parts.append(f"- Task atual: {status_fields['task_atual']}")
    parts.append(f"- Objetivo imediato: {status_fields['objetivo_imediato']}")
    parts.append(f"- Bloqueio principal: {status_fields['bloqueio_principal']}")
    parts.append(f"- Próxima ação: {status_fields['proxima_acao']}\n")

    parts.append("## 3. Estado do repositório\n")
    for label in [
        "pwd",
        "git branch --show-current",
        "git status --short",
        "git log --oneline --decorate -n 10",
    ]:
        parts.append(build_markdown_section(label, command_outputs[label], "bash"))

    parts.append("## 4. Arquivos incluídos no relatório\n")
    parts.append(build_markdown_list(files_to_render) + "\n")

    parts.append("## 5. Conteúdo completo dos arquivos críticos\n")
    for file_path in files_to_render:
        content = read_file(file_path)
        language = "yaml" if file_path.endswith((".yml", ".yaml")) else "markdown"
        if file_path.endswith(".py"):
            language = "python"
        elif file_path.endswith(".sh"):
            language = "bash"
        elif file_path.endswith(".md"):
            language = "markdown"
        parts.append(build_markdown_section(file_path, content, language))

    parts.append("## 6. Estado atual da stack\n")
    parts.append(build_markdown_section("docker compose ps", command_outputs["docker compose ps"], "bash"))

    parts.append("## 7. Logs recentes\n")
    for label in [
        "docker compose logs --tail=40 promtail",
        "docker compose logs --tail=30 loki",
        "docker compose logs --tail=30 prometheus",
        "docker compose logs --tail=30 grafana",
    ]:
        parts.append(build_markdown_section(label, command_outputs[label], "bash"))

    parts.append("## 8. Problemas observados automaticamente\n")
    parts.append(build_markdown_list(observed_issues) + "\n")

    parts.append("## 9. Hipótese operacional atual\n")
    if any("Promtail" in issue for issue in observed_issues):
        parts.append(
            "- O principal bloqueio atual parece estar relacionado à persistência do arquivo de posições do Promtail, "
            "com indício forte de conflito entre estratégia de escrita do processo e o tipo de volume montado.\n"
        )
    else:
        parts.append("- Não foi possível identificar uma hipótese principal forte apenas com base na coleta automática.\n")

    parts.append("## 10. Próxima ação recomendada para revisão humana\n")
    if any("Promtail" in issue for issue in observed_issues):
        parts.append(
            "- Revisar o volume do Promtail responsável por `positions.yaml`, validar a estratégia de persistência "
            "e reexecutar a validação da Fase 4.\n"
        )
    else:
        parts.append("- Revisar manualmente os logs e o estado da stack para definir a próxima ação.\n")

    OUTPUT_FILE.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Arquivo gerado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()