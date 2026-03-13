# **Planejamento completo do Projeto 03 no Trello**

## **Card macro**

**Projeto 03 — Observabilidade, Logs e Alertas**

Descrição sugerida do card macro:

* objetivo principal do projeto

* stack principal

* critérios gerais de aceite

* link para `contexto.md`

* link para `arquitetura.md`

* fases do projeto

* regra de operação: uma task por vez, validar antes de concluir

## FASE ATUAL - Fase 4 — Stack base com Docker Compose

---

# **Fase 1 — Definição estratégica e base documental** (CONCLUIDA)

## **Card macro da fase**

**Projeto 03 — Fase 1 | Definição estratégica e base documental**

### **Objetivo da fase**

Definir o racional do projeto, consolidar contexto, arquitetura e planejamento macro de execução.

### **Critério de conclusão**

A fase só fecha quando:

* `contexto.md` estiver concluído e validado

* `arquitetura.md` estiver concluído e validado

* planejamento do Trello estiver completo

* escopo MVP estiver fechado

* stack e fonte principal de logs estiverem formalmente definidos

### **Riscos**

* começar execução sem fronteira clara

* inflar escopo cedo demais

* documentação ficar genérica demais

### **Tasks**

* `P03-F1-T1 - Definir objetivo principal do projeto`

* `P03-F1-T2 - Definir critério de aceite macro`

* `P03-F1-T3 - Formalizar fonte principal de logs`

* `P03-F1-T4 - Criar contexto.md`

* `P03-F1-T5 - Criar arquitetura.md`

* `P03-F1-T6 - Planejar fases e tasks no Trello`

* `P03-F1-T7 - Definir escopo MVP e escopo evolutivo`

* `P03-F1-T8 - Revisar coerência documental da fase`

---

# **Fase 2 — Estrutura inicial do repositório** (CONCLUIDA)

## **Card macro da fase**

**Projeto 03 — Fase 2 | Estrutura inicial do repositório**

### **Objetivo da fase**

Criar a base física do projeto no repositório, com estrutura clara, documentação inicial útil e organização pronta para execução.

### **Critério de conclusão**

A fase só fecha quando:

* repositório estiver estruturado

* README inicial estiver útil

* `.gitignore` estiver adequado

* diretórios principais estiverem criados

* convenções de organização estiverem definidas

### **Riscos**

* criar estrutura confusa

* misturar documentação com configuração

* fazer primeiro commit cedo demais sem base coerente

### **Tasks**

* `P03-F2-T1 - Definir nome oficial do repositório`

* `P03-F2-T2 - Criar README inicial`

* `P03-F2-T3 - Criar .gitignore`

* `P03-F2-T4 - Criar diretórios base do projeto`

* `P03-F2-T5 - Definir convenção de nomes e arquivos`

* `P03-F2-T6 - Revisar estrutura inicial com tree`

* `P03-F2-T7 - Validar base mínima para primeiro commit`

---

# **Fase 3 — Aplicação emissora de logs JSON** (CONCLUIDA)

## **Card macro da fase**

**Projeto 03 — Fase 3 | Aplicação emissora de logs JSON**

### **Objetivo da fase**

Criar uma aplicação simples que gere logs estruturados em JSON com valor operacional para consulta, filtro e alerta.

### **Critério de conclusão**

A fase só fecha quando:

* a aplicação executar localmente

* os logs forem gerados em JSON

* os campos estiverem consistentes

* houver eventos `info`, `warning` e `error`

* o cenário de erro for reproduzível

### **Riscos**

* logs pobres demais

* estrutura JSON inconsistente

* aplicação gerar logs sem valor operacional

### **Tasks**

* `P03-F3-T1 - Definir stack da aplicação emissora`

* `P03-F3-T2 - Definir modelo do log JSON`

* `P03-F3-T3 - Criar aplicação mínima`

* `P03-F3-T4 - Implementar geração de logs info`

* `P03-F3-T5 - Implementar geração de logs warning`

* `P03-F3-T6 - Implementar geração de logs error`

* `P03-F3-T7 - Definir diretório e arquivo de logs`

* `P03-F3-T8 - Validar execução local da aplicação`

* `P03-F3-T9 - Validar qualidade e consistência dos logs`

---

# **Fase 4 — Stack base com Docker Compose** (EM ANDAMENTO)

## **Card macro da fase**

**Projeto 03 — Fase 4 | Stack base com Docker Compose**

### **Objetivo da fase**

Subir a base da stack de observabilidade de forma reproduzível com Docker Compose.

### **Critério de conclusão**

A fase só fecha quando:

* containers principais subirem corretamente

* rede entre serviços estiver funcional

* volumes e persistência mínima estiverem coerentes

* acesso aos serviços estiver validado

### **Riscos**

* container subir sem integração real

* erro de rede entre componentes

* configuração inicial confusa

### **Tasks**

* `P03-F4-T1 - Criar docker-compose.yml base`

* `P03-F4-T2 - Adicionar serviço da aplicação`

* `P03-F4-T3 - Adicionar Prometheus ao compose`

* `P03-F4-T4 - Adicionar Grafana ao compose`

* `P03-F4-T5 - Adicionar Loki ao compose`

* `P03-F4-T6 - Adicionar Promtail ao compose`

* `P03-F4-T7 - Adicionar Node Exporter ao compose`

* `P03-F4-T8 - Validar health básico dos containers`

* `P03-F4-T9 - Validar comunicação entre os serviços`

---

# **Fase 5 — Coleta e centralização de logs**

## **Card macro da fase**

**Projeto 03 — Fase 5 | Coleta e centralização de logs**

### **Objetivo da fase**

Configurar o pipeline de logs entre aplicação, Promtail e Loki.

### **Critério de conclusão**

A fase só fecha quando:

* Promtail descobrir o arquivo de log corretamente

* labels principais estiverem aplicadas

* Loki receber logs

* Grafana conseguir consultar logs em tempo real

* erros puderem ser filtrados

### **Riscos**

* Promtail não enxergar o arquivo

* labels mal definidas

* Loki receber dados sem contexto útil

### **Tasks**

* `P03-F5-T1 - Criar configuração inicial do Promtail`

* `P03-F5-T2 - Definir path de descoberta dos logs`

* `P03-F5-T3 - Definir labels iniciais`

* `P03-F5-T4 - Configurar Loki para ingestão`

* `P03-F5-T5 - Validar envio de logs do Promtail ao Loki`

* `P03-F5-T6 - Integrar Loki ao Grafana`

* `P03-F5-T7 - Validar consulta de logs em tempo real`

* `P03-F5-T8 - Validar filtro de logs error`

* `P03-F5-T9 - Registrar evidência funcional da camada de logs`

---

# **Fase 6 — Coleta de métricas com Prometheus**

## **Card macro da fase**

**Projeto 03 — Fase 6 | Coleta de métricas com Prometheus**

### **Objetivo da fase**

Configurar a coleta de métricas de infraestrutura com Prometheus e Node Exporter.

### **Critério de conclusão**

A fase só fecha quando:

* Prometheus estiver funcional

* Node Exporter estiver expondo métricas

* target estiver UP

* CPU puder ser consultada com consistência

* Grafana puder consumir essas métricas

### **Riscos**

* target configurado errado

* scrape sem retorno útil

* painel criado sobre dado inconsistente

### **Tasks**

* `P03-F6-T1 - Criar prometheus.yml inicial`

* `P03-F6-T2 - Configurar job do Prometheus`

* `P03-F6-T3 - Configurar target do Node Exporter`

* `P03-F6-T4 - Definir scrape_interval e evaluation_interval`

* `P03-F6-T5 - Validar target UP no Prometheus`

* `P03-F6-T6 - Validar métricas de CPU disponíveis`

* `P03-F6-T7 - Integrar Prometheus ao Grafana`

* `P03-F6-T8 - Registrar evidência funcional da coleta de métricas`

---

# **Fase 7 — Dashboards operacionais no Grafana**

## **Card macro da fase**

**Projeto 03 — Fase 7 | Dashboards operacionais no Grafana**

### **Objetivo da fase**

Construir dashboards claros para leitura operacional de métricas e logs.

### **Critério de conclusão**

A fase só fecha quando:

* dashboard de CPU estiver funcional

* painel de logs em tempo real estiver funcional

* visualização de erros estiver funcional

* variáveis básicas estiverem configuradas

* navegação operacional estiver clara

### **Riscos**

* painel bonito e inútil

* excesso de visual sem valor operacional

* falta de correlação entre métricas e logs

### **Tasks**

* `P03-F7-T1 - Criar dashboard de infraestrutura`

* `P03-F7-T2 - Criar painel de CPU`

* `P03-F7-T3 - Criar dashboard de logs da aplicação`

* `P03-F7-T4 - Criar painel de logs em tempo real`

* `P03-F7-T5 - Criar painel de erros`

* `P03-F7-T6 - Definir variáveis de ambiente e serviço`

* `P03-F7-T7 - Validar navegação entre métricas e logs`

* `P03-F7-T8 - Revisar legibilidade dos dashboards`

---

# **Fase 8 — Alertas automáticos no Slack**

## **Card macro da fase**

**Projeto 03 — Fase 8 | Alertas automáticos no Slack**

### **Objetivo da fase**

Implementar resposta automática a incidentes com alerta via Slack.

### **Critério de conclusão**

A fase só fecha quando:

* contato Slack estiver configurado

* regra principal de erro em log estiver criada

* regra complementar de CPU estiver criada

* teste de disparo funcionar

* mensagem chegar ao Slack com contexto útil

### **Riscos**

* webhook mal configurado

* regra gerar ruído demais

* alerta sem contexto operacional

### **Tasks**

* `P03-F8-T1 - Definir canal e estratégia de notificação`

* `P03-F8-T2 - Configurar integração do Grafana com Slack`

* `P03-F8-T3 - Criar regra de alerta para erro em log`

* `P03-F8-T4 - Criar regra complementar de CPU`

* `P03-F8-T5 - Definir severidade dos alertas`

* `P03-F8-T6 - Validar disparo controlado de erro`

* `P03-F8-T7 - Validar recebimento do alerta no Slack`

* `P03-F8-T8 - Revisar ruído e qualidade da notificação`

---

# **Fase 9 — Simulação operacional e troubleshooting**

## **Card macro da fase**

**Projeto 03 — Fase 9 | Simulação operacional e troubleshooting**

### **Objetivo da fase**

Executar o fluxo completo de operação para provar que a stack funciona ponta a ponta.

### **Critério de conclusão**

A fase só fecha quando:

* for possível gerar evento normal

* for possível gerar warning

* for possível gerar error

* logs e métricas refletirem o comportamento

* alerta disparar corretamente

* troubleshooting básico estiver documentado

### **Riscos**

* validar partes isoladas sem validar o fluxo completo

* erro não ser reproduzível

* stack funcionar só parcialmente

### **Tasks**

* `P03-F9-T1 - Definir cenário de simulação operacional`

* `P03-F9-T2 - Executar fluxo de evento normal`

* `P03-F9-T3 - Executar fluxo de warning`

* `P03-F9-T4 - Executar fluxo de error`

* `P03-F9-T5 - Validar correlação entre evento e log`

* `P03-F9-T6 - Validar correlação entre métrica e contexto`

* `P03-F9-T7 - Validar disparo ponta a ponta do alerta`

* `P03-F9-T8 - Registrar troubleshooting da operação`

---

# **Fase 10 — Documentação final, evidências e fechamento**

## **Card macro da fase**

**Projeto 03 — Fase 10 | Documentação final, evidências e fechamento**

### **Objetivo da fase**

Consolidar a apresentação profissional do projeto como item de portfólio.

### **Critério de conclusão**

A fase só fecha quando:

* README final estiver consolidado

* arquitetura e contexto estiverem coerentes com a implementação real

* evidências estiverem registradas

* validação final estiver documentada

* narrativa do projeto estiver pronta para portfólio e entrevista

### **Riscos**

* documentação prometer mais do que foi implementado

* fechar projeto sem evidências

* perder a história das decisões

### **Tasks**

* `P03-F10-T1 - Revisar README final`

* `P03-F10-T2 - Revisar contexto.md com base na execução real`

* `P03-F10-T3 - Revisar arquitetura.md com base na execução real`

* `P03-F10-T4 - Registrar evidências técnicas`

* `P03-F10-T5 - Registrar critérios finais de validação`

* `P03-F10-T6 - Documentar decisões e trade-offs`

* `P03-F10-T7 - Preparar resumo técnico do projeto`

* `P03-F10-T8 - Preparar resumo executivo do projeto`

* `P03-F10-T9 - Registrar próximos passos evolutivos`

* `P03-F10-T10 - Encerrar formalmente o projeto`

