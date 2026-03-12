# Projeto 03 — Observabilidade, Logs e Alertas com Grafana, Prometheus e Loki

Stack de observabilidade voltada para coleta de métricas, centralização de logs estruturados em JSON, visualização operacional em dashboards e alertas automáticos no Slack, com foco em operação real, troubleshooting e resposta a incidentes.

![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-M%C3%A9tricas-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Loki](https://img.shields.io/badge/Loki-Logs-2F3136?style=for-the-badge&logo=grafana&logoColor=white)
![Promtail](https://img.shields.io/badge/Promtail-Coleta%20de%20logs-2F3136?style=for-the-badge&logo=grafana&logoColor=white)
![Node Exporter](https://img.shields.io/badge/Node_Exporter-Infraestrutura-3EAAAF?style=for-the-badge&logo=prometheus&logoColor=white)
![Slack](https://img.shields.io/badge/Slack-Alertas-4A154B?style=for-the-badge&logo=slack&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-Orquestra%C3%A7%C3%A3o-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/status-em%20estrutura%C3%A7%C3%A3o-blue?style=for-the-badge)

## Visão geral

Este projeto foi concebido como o terceiro passo de uma trilha prática de portfólio DevOps. Após consolidar base de aplicação, testes, containerização e CI/CD no Projeto 01, e infraestrutura como código, modularização, backend remoto e automação controlada na AWS no Projeto 02, o foco agora evolui para maturidade operacional: observar, diagnosticar e reagir.

A proposta é construir uma stack de observabilidade reproduzível em ambiente local/containerizado, capaz de:

- coletar métricas operacionais
- centralizar logs de aplicação estruturados em JSON
- exibir dashboards operacionais
- filtrar erros em tempo real
- disparar alertas automáticos no Slack

Mais do que subir ferramentas, este projeto busca demonstrar capacidade prática de organizar uma solução de observabilidade com valor operacional real.

---

## Objetivo principal

Construir uma stack de observabilidade com Grafana, Prometheus, Loki, Promtail, Node Exporter e Slack, capaz de coletar métricas, centralizar logs estruturados em JSON, exibir dashboards operacionais e disparar alertas automáticos com base em eventos relevantes da aplicação.

---

## Case do projeto

Em muitos ambientes, aplicações e serviços são colocados em funcionamento sem uma camada adequada de visibilidade operacional. Quando ocorre erro, lentidão ou comportamento anômalo, a equipe depende de leitura manual de logs, verificações pontuais e investigação lenta.

Este projeto simula esse contexto e propõe uma resposta prática: uma stack de observabilidade que integra métricas, logs, dashboards e alertas, reduzindo atrito operacional, melhorando a capacidade de diagnóstico e fortalecendo a confiabilidade do ambiente.

---

## Escopo do projeto

O projeto contempla:

- aplicação simples emissora de logs estruturados em JSON
- coleta de métricas de infraestrutura com Node Exporter
- coleta e envio de logs com Promtail
- centralização de logs no Loki
- visualização unificada no Grafana
- painel com consumo de CPU
- visualização de logs em tempo real
- filtragem de erros operacionais
- alerta automático no Slack
- documentação técnica e fluxo reproduzível de execução e validação

Neste momento, o projeto está sendo estruturado com foco em clareza arquitetural, base documental forte e planejamento controlado por fases.

---

## Tecnologias utilizadas

- Grafana
- Prometheus
- Loki
- Promtail
- Node Exporter
- Slack
- Docker
- Docker Compose
- YAML
- Markdown
- Git
- GitHub

---

## Fonte principal de logs

A fonte principal de logs adotada neste projeto é uma **aplicação com logs estruturados em JSON**.

Essa decisão foi tomada para garantir:

- melhor capacidade de filtro e consulta
- maior valor operacional para dashboards
- alertas mais inteligentes e explicáveis
- melhor narrativa técnica de portfólio
- maior controle sobre o cenário de validação

Em vez de depender inicialmente de logs de sistema ou de servidor web como base principal, o projeto parte de eventos estruturados da aplicação, permitindo uma observabilidade mais clara e orientada a operação.

---

## Arquitetura da solução

A arquitetura do projeto foi desenhada para demonstrar um fluxo ponta a ponta de observabilidade.

### Fluxo resumido

1. a aplicação gera logs estruturados em JSON
2. o Promtail coleta esses logs e aplica labels
3. o Loki centraliza e indexa os eventos
4. o Node Exporter expõe métricas de infraestrutura
5. o Prometheus realiza scrape periódico dessas métricas
6. o Grafana consome Prometheus e Loki como fontes de dados
7. dashboards operacionais exibem métricas e logs
8. regras de alerta disparam notificações no Slack quando condições críticas são atendidas

### Visão arquitetural em alto nível

```
[Aplicação]
    └─ gera logs JSON
                │
                v
         [Promtail]
                │
                v
            [Loki] <────────────┐
                                        │
                                 [Grafana]
                                        │
                                        │ alertas
                                        v
                                    [Slack]

[Node Exporter]
        │
        v
[Prometheus] ────────────────┘
```

---

## Estrutura atual do projeto

```
.
├── alerting/
│   └── README.md
├── app/
│   └── logs/
├── docker-compose.yml
├── docs/
│   ├── arquitetura.md
│   ├── contexto.md
│   └── troubleshooting.md
├── grafana/
│   └── provisioning/
├── loki/
│   └── config.yml
├── prometheus/
│   └── prometheus.yml
├── promtail/
│   └── config.yml
├── .gitignore
└── README.md
```

## Responsabilidade dos diretórios e arquivos

| Arquivo/Diretório           | Descrição                                                                     |
| --------------------------- | ----------------------------------------------------------------------------- |
| `alerting/README.md`        | Documento previsto para registrar a estratégia de alertas e integrações da stack. |
| `app/logs/`                 | Diretório previsto para os logs estruturados emitidos pela aplicação.         |
| `docker-compose.yml`        | Orquestração local da stack de observabilidade.                               |
| `docs/contexto.md`          | Contexto operacional e estratégico do projeto.                                |
| `docs/arquitetura.md`       | Desenho técnico da solução e fluxo completo dos dados.                        |
| `docs/troubleshooting.md`   | Documento previsto para registrar erros, causas, validações, correções e prevenção ao longo da execução do projeto. |
| `grafana/provisioning/`     | Provisionamento futuro de datasources, dashboards e configurações do Grafana. |
| `loki/config.yml`           | Configuração do Loki.                                                         |
| `prometheus/prometheus.yml` | Configuração do Prometheus e seus targets.                                    |
| `promtail/config.yml`       | Configuração de descoberta e envio de logs para o Loki.                       |
| `.gitignore`                | Regras de exclusão de arquivos locais e temporários.                          |
| `README.md`                 | Documentação principal do projeto.                                            |

---

## Status do projeto

### Fases concluídas

- Fase 1 — Definição estratégica e base documental

### Fase atual

- Fase 2 — Estrutura inicial do repositório

### Próxima evolução prevista

- criação da base mínima funcional da stack
- preenchimento das configurações iniciais
- preparação da aplicação emissora de logs JSON
- início da integração entre Promtail, Loki, Prometheus e Grafana

---

## Planejamento macro por fases

O projeto foi planejado do começo ao fim antes da execução técnica, com gestão por fases no Trello.

### Fase 1 — Definição estratégica e base documental

- objetivo macro
- critério de aceite
- contexto do projeto
- arquitetura da solução
- planejamento completo das fases

### Fase 2 — Estrutura inicial do repositório

- README inicial
- `.gitignore`
- diretórios e arquivos base
- revisão da estrutura do projeto

### Fase 3 — Aplicação emissora de logs JSON

- definição da aplicação
- modelo do log
- geração de eventos `info`, `warning` e `error`

### Fase 4 — Stack base com Docker Compose

- definição e subida inicial dos serviços
- integração de rede e volumes
- validação básica dos containers

### Fase 5 — Coleta e centralização de logs

- Promtail
- Loki
- consulta em tempo real no Grafana

### Fase 6 — Coleta de métricas com Prometheus

- Node Exporter
- Prometheus
- consulta de CPU

### Fase 7 — Dashboards operacionais

- painel de CPU
- painel de logs
- painel de erros

### Fase 8 — Alertas automáticos no Slack

- integração com Slack
- regra de erro
- regra complementar de CPU

### Fase 9 — Simulação operacional e troubleshooting

- geração controlada de eventos
- validação ponta a ponta
- documentação de troubleshooting

### Fase 10 — Documentação final e fechamento

- consolidação do README
- evidências
- revisão técnica
- encerramento formal do projeto

---

## Critério de aceite do projeto

O projeto será considerado concluído quando houver evidência funcional e técnica de que:

- métricas estão sendo coletadas corretamente
- há painel funcional de CPU
- logs estruturados estão centralizados no Loki
- logs podem ser consultados em tempo real no Grafana
- erros podem ser filtrados com clareza
- uma condição crítica dispara alerta automático no Slack
- a documentação está coerente com a implementação real
- o fluxo de execução e validação está reproduzível

---

## Fluxo operacional recomendado

### Antes de alterar

- revisar a fase atual no Trello
- revisar a task em andamento
- confirmar branch correta
- verificar `git status`
- revisar o contexto e a arquitetura do projeto
- entender o impacto da mudança antes de editar qualquer arquivo

### Durante a execução

- alterar um bloco coerente por vez
- validar antes de empilhar novas mudanças
- revisar estrutura com `tree`
- revisar alterações com `git diff`

### Após a execução

- validar comportamento esperado
- atualizar documentação mínima, se necessário
- mover a task para **Em validação**
- só marcar como **Concluído** depois de validação real

---

## Documentação complementar

A documentação principal do projeto está sendo separada em arquivos específicos para manter clareza entre contexto, arquitetura e troubleshooting:

- `docs/contexto.md`
- `docs/arquitetura.md`
- `docs/troubleshooting.md`

Essa separação foi adotada para evitar que o README fique inchado demais e, ao mesmo tempo, preservar profundidade técnica adequada.

---

## Boas práticas aplicadas

- definição de escopo antes da implementação
- planejamento completo por fases e tasks
- documentação técnica antes da execução
- separação entre contexto, arquitetura e troubleshooting
- foco em logs estruturados como fonte principal de observabilidade
- estrutura de projeto organizada por componente
- validação antes de marcar qualquer entrega como concluída
- preocupação com retenção, rastreabilidade e resposta a incidentes

---

## Cuidados importantes

- não versionar segredos ou webhooks do Slack
- não expor credenciais em arquivos do projeto
- evitar inflar o escopo antes de consolidar o MVP
- validar integração real entre os componentes antes de considerar a stack pronta
- manter a documentação coerente com o comportamento implementado
- não tratar container "UP" como sinônimo de observabilidade funcionando

---

## Próximos passos

A próxima etapa formal do projeto é consolidar a **Fase 2 — Estrutura inicial do repositório**, com foco em:

- preencher `README.md`
- preencher `.gitignore`
- definir a base mínima dos arquivos de configuração
- revisar a coerência da estrutura física do projeto
- preparar o repositório para o primeiro ciclo real de implementação

---

## Autor

**Diego Santos**

Projeto desenvolvido como prática de portfólio com foco em observabilidade, operação, troubleshooting, alertas e maturidade DevOps.
````
