# Arquitetura do Projeto 03 — Observabilidade, Logs e Alertas

## 1. Objetivo da arquitetura

A arquitetura deste projeto foi desenhada para oferecer visibilidade operacional ponta a ponta sobre uma aplicação instrumentada com logs estruturados em JSON e sobre métricas básicas da infraestrutura/container host. O objetivo é transformar sinais dispersos em capacidade real de operação, permitindo que a equipe acompanhe comportamento do ambiente, investigue falhas com rapidez e responda a incidentes por meio de alertas automáticos.

A solução utiliza uma stack composta por **Prometheus**, **Grafana**, **Loki**, **Promtail** e integração com **Slack**, organizada de forma reproduzível em ambiente local/containerizado. Essa combinação foi escolhida para demonstrar, de forma prática e objetiva, um fluxo completo de observabilidade que vai da coleta até a notificação.

---

## 2. Visão arquitetural em alto nível

O fluxo principal da solução segue esta sequência:

1. a aplicação gera logs estruturados em JSON
2. o Promtail coleta esses logs, enriquece os eventos com labels e os envia ao Loki
3. o Loki centraliza e indexa os logs para consulta
4. o Prometheus coleta métricas do ambiente a partir de exporters
5. o Grafana consome tanto o Prometheus quanto o Loki como fontes de dados
6. dashboards e consultas permitem navegação entre métricas e logs
7. regras de alerta avaliam condições críticas e disparam notificações no Slack

Essa arquitetura foi desenhada para ser simples o suficiente para reprodução local, mas suficientemente forte para demonstrar uma dinâmica operacional próxima de cenários reais.

---

## 3. Fluxo completo dos dados

## 3.1 Fluxo de métricas

O fluxo de métricas começa nos componentes monitorados, que expõem dados em formato compatível com scrape do Prometheus. Esses dados são coletados periodicamente e armazenados como séries temporais. A partir disso, o Grafana consulta o Prometheus para construir dashboards e alimentar regras de alerta baseadas em comportamento quantitativo.

Fluxo resumido:

- infraestrutura ou container host expõe métricas
- exporter disponibiliza endpoint de métricas
- Prometheus realiza scrape periódico
- Prometheus armazena séries temporais
- Grafana consulta os dados com PromQL
- dashboards e alertas são atualizados a partir dessas métricas

## 3.2 Fluxo de logs

O fluxo de logs parte da aplicação monitorada, que grava eventos em formato JSON estruturado. Esses arquivos são observados pelo Promtail, que identifica novas linhas, aplica labels para indexação e encaminha os registros ao Loki. O Grafana consulta o Loki com LogQL para exibir logs em tempo real, filtrar erros e correlacionar eventos com sinais de métricas.

Fluxo resumido:

- aplicação gera logs estruturados em JSON
- logs são gravados em arquivo monitorado
- Promtail descobre o arquivo e lê continuamente novos eventos
- Promtail aplica labels de contexto
- Promtail envia os logs ao Loki
- Loki armazena os registros com indexação por labels
- Grafana consulta logs e os exibe em painéis e explorador

## 3.3 Fluxo de alerta

Os alertas poderão ser disparados a partir de métricas ou de consultas sobre logs, dependendo da regra definida. O Grafana avalia essas condições segundo janelas temporais e limites estabelecidos. Quando a regra é satisfeita, a plataforma envia uma notificação ao canal configurado no Slack.

Fluxo resumido:

- Grafana executa a consulta da regra
- a condição ultrapassa o limite definido
- a severidade é classificada
- o contato configurado é acionado
- a notificação é enviada ao Slack

---

## 4. Componentes da arquitetura

## 4.1 Aplicação emissora de logs

A aplicação é a principal fonte de eventos do projeto. Ela será responsável por gerar logs estruturados em JSON contendo informações úteis para investigação operacional, como:

- timestamp
- nível do evento
- nome do serviço
- rota ou operação executada
- código de status
- tempo de resposta
- mensagem descritiva
- contexto adicional para análise

A escolha por logs estruturados foi feita para permitir consultas mais precisas, filtros mais úteis e regras de alerta com maior valor operacional.

## 4.2 Promtail

O Promtail atua como agente coletor de logs. Sua função é descobrir os arquivos monitorados, acompanhar novas linhas registradas, aplicar labels e encaminhar os eventos ao Loki.

Ele será responsável por:

- identificar os arquivos de log da aplicação
- manter leitura contínua dos arquivos
- aplicar labels como `job`, `service`, `level` e `environment`
- enviar os registros ao Loki com eficiência
- preservar contexto suficiente para consulta e filtragem

## 4.3 Loki

O Loki será utilizado como sistema de centralização de logs. Diferente de stacks mais pesadas, ele foi escolhido por oferecer integração natural com o Grafana e por trabalhar com indexação baseada em labels, o que simplifica a operação e mantém o foco do projeto no valor observável dos eventos.

Suas responsabilidades no projeto são:

- receber os logs enviados pelo Promtail
- armazenar os registros de forma consultável
- indexar os eventos com base nos labels definidos
- responder a consultas LogQL realizadas pelo Grafana

## 4.4 Prometheus

O Prometheus será responsável pela coleta e armazenamento de métricas em séries temporais. Ele fará scrape dos targets configurados em intervalos regulares, permitindo acompanhar comportamento do ambiente e alimentar dashboards e alertas.

Suas responsabilidades no projeto são:

- realizar scraping periódico de exporters
- armazenar métricas temporais
- responder consultas PromQL
- sustentar painéis operacionais e regras de alerta

## 4.5 Exporters

A arquitetura utilizará exporters para extrair métricas da infraestrutura e/ou do ambiente containerizado.

### Exporter principal recomendado
- **Node Exporter**

O Node Exporter será usado para expor métricas do host ou do ambiente monitorado, com foco inicial em:

- uso de CPU
- memória
- sistema de arquivos
- carga do sistema
- estatísticas básicas de rede

Caso o ambiente de execução exija adaptação, poderá ser considerado um exporter alternativo voltado ao universo de containers, mas o desenho inicial considera Node Exporter como ponto de partida principal.

## 4.6 Grafana

O Grafana será a camada de visualização, exploração e resposta. Ele centralizará os dados provenientes do Prometheus e do Loki em uma mesma interface, permitindo:

- dashboards operacionais
- consulta de logs em tempo real
- investigação de incidentes
- criação de alertas
- envio de notificações ao Slack

---

## 5. Estratégia de coleta de métricas

## 5.1 Fonte de métricas

A coleta de métricas será concentrada inicialmente em indicadores básicos de infraestrutura, especialmente consumo de CPU, que é um dos requisitos mínimos do projeto. Outros indicadores poderão ser adicionados como evolução, desde que não comprometam a clareza do MVP.

## 5.2 Exporters utilizados

O exporter principal previsto é:

- **Node Exporter** para métricas de host e sistema

Essa escolha garante aderência a cenários reais de operação e permite montar dashboards com valor operacional imediato.

## 5.3 Targets monitorados

Os targets previstos são:

- o endpoint exposto pelo Node Exporter
- o próprio Prometheus, para saúde da coleta
- eventualmente outros endpoints internos da stack, caso seja útil para visibilidade operacional

## 5.4 Intervalos de scrape

Como diretriz inicial, o Prometheus deve operar com intervalos de coleta consistentes com um ambiente de laboratório realista, equilibrando atualidade dos dados e custo de processamento.

Recomendação inicial:

- `scrape_interval`: **15s**
- `evaluation_interval`: **15s**

Esse intervalo oferece boa responsividade para dashboards e alertas sem gerar ruído excessivo no contexto do projeto.

## 5.5 Estratégia de naming e organização

As configurações de scrape devem manter consistência de nomenclatura para facilitar leitura e troubleshooting. Os jobs devem ser nomeados de forma explícita, por exemplo:

- `prometheus`
- `node-exporter`
- `app-logs` para o lado de logs, quando necessário em documentação cruzada

A clareza na nomeação reduz confusão durante a investigação.

---

## 6. Estratégia de coleta e centralização de logs

## 6.1 Origem dos logs

A origem principal dos logs será uma aplicação simples, instrumentada para escrever eventos em **JSON estruturado**. Essa decisão foi tomada para maximizar utilidade de consulta, clareza de contexto e valor de portfólio.

## 6.2 Descoberta dos arquivos pelo Promtail

O Promtail será configurado para descobrir arquivos de log específicos da aplicação. Essa descoberta deve ser explícita e controlada, evitando leitura ampla e desnecessária de diretórios inteiros sem critério.

A estratégia recomendada é:

- definir um diretório conhecido para os logs da aplicação
- apontar o Promtail para esse diretório
- usar padrões de caminho previsíveis
- garantir persistência e permissões adequadas no ambiente containerizado

## 6.3 Aplicação de labels

Os labels são centrais para a eficiência do Loki. Eles devem ser definidos com equilíbrio: suficientes para consulta útil, mas sem explosão desnecessária de cardinalidade.

Labels iniciais recomendados:

- `job`: identifica a origem lógica do log
- `service`: identifica a aplicação monitorada
- `environment`: identifica o ambiente
- `level`: identifica severidade do evento
- `source`: identifica a origem do arquivo ou componente

A adoção desses labels permitirá consultas objetivas e painéis mais úteis no Grafana.

## 6.4 Transporte dos logs

O transporte entre Promtail e Loki deve ser contínuo e eficiente, priorizando simplicidade e previsibilidade no ambiente do projeto. O Promtail atuará como agente leve, enviando novos eventos à medida que forem registrados.

## 6.5 Qualidade dos logs

Para que a camada de observabilidade tenha valor real, os logs devem ser pensados como eventos operacionais e não apenas como mensagens de debug soltas. Isso significa que a aplicação deve gerar registros com consistência de campos, semântica clara de severidade e contexto suficiente para análise.

Campos recomendados no payload JSON:

- `timestamp`
- `level`
- `service`
- `event`
- `message`
- `endpoint` ou `operation`
- `status_code`
- `response_time_ms`

---

## 7. Organização dos dashboards no Grafana

## 7.1 Princípios de organização

Os dashboards devem ser organizados para apoiar leitura operacional rápida. O operador precisa bater o olho e entender:

- saúde básica do ambiente
- existência de erro recente
- comportamento dos logs
- contexto suficiente para investigação

A recomendação é organizar o Grafana por finalidade, não apenas por ferramenta.

## 7.2 Dashboards mínimos do projeto

### Dashboard 1 — Visão de infraestrutura
Painel focado em métricas de CPU e sinais básicos de host.

Objetivos:
- visualizar consumo de CPU
- identificar picos ou comportamento anômalo
- servir como ponto inicial de leitura operacional

### Dashboard 2 — Visão de logs da aplicação
Painel focado em fluxo de eventos e consulta em tempo real.

Objetivos:
- acompanhar logs recentes
- filtrar por nível
- visualizar sequência operacional da aplicação

### Dashboard 3 — Visão de erros
Painel ou seção dedicada a eventos de erro.

Objetivos:
- filtrar apenas eventos `error`
- observar frequência e tendência
- apoiar diagnóstico rápido

## 7.3 Uso de variáveis e filtros dinâmicos

Os dashboards devem utilizar variáveis para facilitar navegação sem duplicação de painel. Variáveis recomendadas:

- ambiente
- serviço
- nível do log
- janela temporal

Isso melhora usabilidade e aproxima a solução de um padrão profissional de operação.

## 7.4 Integração entre métricas e logs

Um dos pontos mais importantes da arquitetura é permitir que o operador navegue entre métricas e logs como partes do mesmo contexto operacional.

A integração desejada é:

- identificar um pico ou comportamento anômalo em métrica
- usar o mesmo intervalo temporal para consultar logs
- filtrar eventos do serviço relacionado
- localizar erros ou warnings associados ao comportamento observado

Essa correlação não precisa ser extremamente sofisticada no MVP, mas precisa ser clara e funcional.

---

## 8. Estratégia de consultas e inteligência operacional

## 8.1 Consultas PromQL

As consultas PromQL serão utilizadas para:

- medir uso de CPU
- avaliar comportamento ao longo do tempo
- identificar condição anômala para dashboards ou alertas

Exemplos de uso esperado:

- percentual de uso de CPU
- taxa de uso ao longo da janela
- comparação entre intervalos recentes

## 8.2 Consultas LogQL

As consultas LogQL serão utilizadas para:

- visualizar logs em tempo real
- filtrar por severidade
- localizar erros
- agrupar eventos por nível ou tipo

Exemplos de uso esperado:

- logs do serviço principal
- apenas eventos com `level="error"`
- contagem de erros por janela de tempo
- busca por mensagem ou evento específico

## 8.3 Objetivo da camada de consulta

O objetivo não é apenas “consultar dados”, mas transformar consultas em leitura operacional útil. Tanto PromQL quanto LogQL devem sustentar:

- dashboards legíveis
- troubleshooting objetivo
- alertas justificáveis
- demonstração forte de portfólio

---

## 9. Estratégia de alertas

## 9.1 Princípios de alerta

Os alertas devem seguir alguns princípios:

- representar condição relevante de operação
- ter lógica simples e compreensível
- evitar ruído excessivo
- apoiar resposta rápida
- ter severidade explícita

No contexto do projeto, o foco é demonstrar uma trilha completa de resposta a incidente: evento ocorre, stack identifica, alerta é disparado.

## 9.2 Fonte principal de alerta

A fonte principal de alerta deste projeto será a camada de logs da aplicação, com base em eventos de erro estruturados. Essa escolha reforça o valor do recorte técnico adotado e cria um fluxo coerente entre geração de log, centralização, visualização e notificação.

## 9.3 Regras de alerta previstas

### Regra 1 — Erro de aplicação detectado
Condição:
- ocorrência de eventos com nível `error` acima de um limite definido em janela curta

Objetivo:
- detectar falha operacional de forma imediata

### Regra 2 — Uso elevado de CPU
Condição:
- consumo de CPU acima de um limite definido por uma janela mínima

Objetivo:
- demonstrar alerta orientado a métrica, complementando a visão por logs

Essas duas regras já oferecem um bom equilíbrio entre valor didático, valor técnico e narrativa operacional.

## 9.4 Matriz de severidade

Sugestão inicial de severidade:

- **info**: sem ação, apenas observação
- **warning**: comportamento anômalo que merece atenção
- **critical**: condição que exige reação operacional imediata

No projeto, os alertas enviados ao Slack devem pelo menos distinguir entre níveis de atenção e criticidade.

## 9.5 Canais de notificação

Canal principal previsto:
- **Slack**

Canal alternativo documentável para evolução:
- e-mail

O uso do Slack foi escolhido por ser aderente a rotinas modernas de operação e por facilitar demonstração prática de incident response.

---

## 10. Políticas de retenção e controle de custos

## 10.1 Retenção de métricas

Como o projeto é reproduzido em ambiente local e orientado a portfólio, a retenção deve ser suficiente para demonstração e validação, sem exagero de armazenamento.

Diretriz inicial:
- retenção enxuta, compatível com laboratório e testes controlados

O objetivo é demonstrar consciência operacional de custo, mesmo em ambiente não produtivo.

## 10.2 Retenção de logs

A retenção de logs no Loki deve seguir o mesmo princípio: preservar o suficiente para investigação e demonstração, evitando acúmulo desnecessário.

Diretriz inicial:
- retenção curta a moderada, adequada ao ciclo de testes do projeto

## 10.3 Princípio de sustentabilidade

Mesmo em um projeto de portfólio, é importante registrar que observabilidade sem política de retenção vira fonte de custo e desorganização. A arquitetura deve deixar claro que dados observacionais têm valor, mas também têm custo de armazenamento e processamento.

---

## 11. Controle de acesso e segurança

## 11.1 Princípios de segurança

A solução deve considerar boas práticas mínimas de segurança, mesmo em ambiente de laboratório:

- exposição controlada das interfaces
- separação clara de responsabilidades entre componentes
- não versionamento de segredos
- configuração segura de integrações externas, como webhook do Slack

## 11.2 Acesso ao Grafana

O Grafana deve ser tratado como a principal interface operacional. Mesmo em ambiente local, recomenda-se:

- uso de autenticação
- definição de credenciais fora de arquivos versionados, quando aplicável
- cuidado com exposição de portas além do necessário

## 11.3 Segredos e integrações

Segredos como webhook de Slack ou senhas não devem ser mantidos em arquivos versionados. O projeto deve prever mecanismo apropriado para injeção segura dessas informações, mesmo que de forma simples no contexto do laboratório.

---

## 12. Decisões arquiteturais principais

As principais decisões desta arquitetura são:

### 12.1 Logs estruturados em JSON como fonte principal
Essa decisão foi tomada porque maximiza valor de consulta, clareza de contexto e qualidade dos alertas.

### 12.2 Docker Compose como base de execução
Essa escolha garante reproduzibilidade, simplicidade operacional e menor atrito para validação.

### 12.3 Grafana como ponto central de operação
Essa decisão concentra visualização, exploração e resposta em uma mesma interface, fortalecendo a narrativa operacional do projeto.

### 12.4 Foco inicial em CPU e erro de aplicação
Esse recorte garante um MVP forte e bem delimitado, cobrindo métrica, log e alerta sem inflar escopo cedo demais.

---

## 13. Resumo arquitetural

A arquitetura do Projeto 03 foi desenhada para demonstrar uma jornada completa de observabilidade:

- métricas são coletadas via exporter pelo Prometheus
- logs estruturados em JSON são coletados pelo Promtail e enviados ao Loki
- Grafana centraliza dashboards, exploração e alertas
- o operador consegue navegar entre sinais quantitativos e eventos textuais
- condições críticas disparam notificações no Slack

O resultado esperado é uma stack reproduzível, clara e com valor operacional real, capaz de reduzir atrito no diagnóstico, apoiar troubleshooting e demonstrar maturidade prática em observabilidade.