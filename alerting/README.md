# Alerting do Projeto 03

## Objetivo

Este diretório existe para concentrar a documentação relacionada à estratégia de alertas da stack de observabilidade, incluindo regras previstas, canais de notificação, critérios de severidade e validação operacional dos disparos.

O foco do projeto é demonstrar resposta automática a incidentes com valor operacional real, e não apenas exibir dashboards.

---

## Estratégia inicial de alertas

A estratégia inicial do projeto prevê dois tipos principais de alerta:

- alerta baseado em erro de aplicação identificado nos logs
- alerta complementar baseado em uso elevado de CPU

Esses alertas foram escolhidos para demonstrar dois caminhos importantes da observabilidade:

- resposta a eventos operacionais vindos dos logs
- resposta a comportamento quantitativo vindo das métricas

---

## Canal previsto

Canal principal de notificação:

- Slack

O Slack será utilizado como destino inicial dos alertas por ser aderente a rotinas modernas de operação e por facilitar demonstração prática do fluxo de incident response.

---

## Regras previstas

### Regra 1 — Erro de aplicação
Disparar alerta quando eventos com nível `error` ultrapassarem o limite definido na janela de avaliação.

### Regra 2 — Uso elevado de CPU
Disparar alerta quando o consumo de CPU permanecer acima do limite definido por uma janela mínima.

---

## Status atual

A estratégia de alertas está documentada, mas a implementação prática das regras e da integração com Slack será realizada em fase posterior do projeto.