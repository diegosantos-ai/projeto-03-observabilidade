# Contexto do Projeto 03 — Observabilidade, Logs e Alertas

## 1. Visão geral do cenário atual

Em ambientes modernos de aplicações e serviços, a disponibilidade e a confiabilidade operacional dependem não apenas da execução correta dos sistemas, mas também da capacidade de observá-los de forma contínua. Quando uma aplicação apresenta falhas, lentidão ou comportamento anômalo, a resposta da equipe depende diretamente da existência de métricas, logs centralizados e mecanismos de alerta que permitam identificar o problema com rapidez e precisão.

No cenário atual deste projeto, parte-se de uma operação com baixa maturidade de observabilidade. Existe a possibilidade de executar serviços e validar seu funcionamento básico, porém a visibilidade operacional ainda é limitada. Em um contexto assim, falhas de aplicação tendem a ser percebidas tarde demais, logs ficam dispersos ou dependentes de acesso manual ao ambiente, e a análise de incidentes se torna reativa, lenta e sujeita a erro humano.

Essa ausência de uma stack de observabilidade integrada gera um problema clássico: a equipe consegue colocar serviços em funcionamento, mas não possui instrumentos suficientes para entender com clareza o que está acontecendo durante a operação. Isso reduz a capacidade de diagnóstico, dificulta a investigação de incidentes e aumenta o esforço necessário para manter confiabilidade em produção.

Este projeto nasce para endereçar exatamente essa lacuna, estruturando uma stack composta por Prometheus, Loki e Grafana, com foco em métricas operacionais, centralização de logs estruturados em JSON e alertas automáticos para resposta a eventos críticos.

---

## 2. Problemas observados no modelo sem observabilidade estruturada

Sem uma camada de observabilidade bem definida, a operação sofre com limitações importantes:

### 2.1 Falta de visibilidade em tempo real
Sem dashboards e consultas centralizadas, a equipe depende de verificações manuais, acesso a arquivos locais e testes pontuais para entender o estado do ambiente. Isso dificulta a percepção rápida de degradações, aumentos de consumo de recursos e falhas intermitentes.

### 2.2 Diagnóstico lento de incidentes
Quando ocorre um erro, a investigação tende a começar do zero. Em vez de navegar por métricas e logs centralizados, o operador precisa buscar evidências manualmente, correlacionar sinais dispersos e reconstruir o contexto do problema com baixa velocidade.

### 2.3 Aumento do MTTR
A falta de observabilidade impacta diretamente o **MTTR (Mean Time to Resolution)**, ou tempo médio de resolução de incidentes. Quanto menor a capacidade de identificar a origem, a natureza e o impacto de uma falha, maior tende a ser o tempo necessário para restaurar o serviço.

### 2.4 Dependência excessiva de esforço humano
Sem automação de coleta, consulta e alerta, a operação fica dependente de atenção manual. Isso aumenta o risco de erro, reduz previsibilidade e dificulta escalar a rotina operacional de forma consistente.

### 2.5 Falta de evidência para tomada de decisão
Sem métricas e logs organizados, decisões técnicas passam a depender mais de percepção do que de dados. Isso enfraquece tanto a resposta a incidentes quanto a capacidade de melhorar a arquitetura e otimizar custos operacionais.

---

## 3. Impactos operacionais e de negócio

A ausência de visibilidade não é apenas um problema técnico. Ela também gera consequências diretas no negócio e na gestão da operação.

### 3.1 Impacto na confiabilidade dos serviços
Quando a equipe não consegue identificar rapidamente erros, gargalos ou degradações, a confiabilidade percebida do serviço cai. Pequenos incidentes podem se prolongar ou se repetir porque a causa raiz não foi observada com clareza.

### 3.2 Impacto no tempo de resposta a incidentes
Sem alertas automáticos e sem contexto centralizado, a resposta tende a ser mais lenta. Isso eleva o MTTR e reduz a capacidade da equipe de agir antes que uma falha se torne visível para o usuário final.

### 3.3 Impacto na produtividade operacional
Horas que poderiam ser dedicadas a melhoria contínua passam a ser consumidas em investigação manual, coleta de evidências dispersas e reexecução de testes para tentar reproduzir problemas.

### 3.4 Impacto no custo operacional
Ambientes sem observabilidade tendem a operar com mais retrabalho, mais esforço humano e menor eficiência na análise de incidentes. Isso pode representar custo indireto elevado, tanto pelo tempo investido quanto pelo risco de manter recursos subutilizados ou sobrecarregados sem percepção clara.

### 3.5 Impacto na governança técnica
Sem uma visão consolidada do comportamento da aplicação e da infraestrutura, torna-se mais difícil sustentar padrões operacionais, justificar decisões técnicas e construir uma rotina madura de operação.

---

## 4. Relação entre observabilidade, MTTR e confiabilidade

Este projeto considera a observabilidade como um componente central da maturidade DevOps/SRE. O objetivo não é apenas “monitorar por monitorar”, mas reduzir atrito operacional e aumentar a capacidade de resposta.

A relação prática é direta:

- **mais visibilidade** reduz o tempo para detectar incidentes
- **logs centralizados** reduzem o tempo para diagnosticar
- **dashboards operacionais** reduzem o tempo para entender contexto
- **alertas automáticos** reduzem o tempo para reagir
- **dados históricos** aumentam a qualidade das decisões corretivas

Com isso, a stack proposta contribui para dois resultados operacionais centrais:

### Redução do MTTR
Ao permitir que métricas, logs e alertas sejam acessados de forma integrada, a equipe consegue sair de uma investigação manual e lenta para um processo mais guiado e objetivo.

### Aumento da confiabilidade
Uma operação que observa melhor seus serviços responde mais rápido, aprende mais rápido com falhas e consegue atuar preventivamente com mais eficiência.

---

## 5. Fronteiras do projeto

Para manter clareza e foco, este projeto define fronteiras explícitas.

### 5.1 O que está dentro do escopo
O projeto contempla:

- uma stack de observabilidade executada em ambiente local/containerizado
- coleta de métricas operacionais do host e/ou containers
- centralização de logs de aplicação estruturados em JSON
- visualização de métricas e logs no Grafana
- criação de dashboards operacionais
- filtragem e análise de erros em tempo real
- configuração de alertas automáticos no Slack
- documentação técnica e fluxo reproduzível de validação

### 5.2 O que está fora do escopo
Neste momento, não fazem parte do escopo principal:

- observabilidade distribuída multiambiente
- tracing distribuído entre múltiplos serviços
- alta disponibilidade da stack de observabilidade
- retenção de longo prazo em ambiente produtivo real
- integração com múltiplos canais corporativos de incident management
- controle avançado de acesso com identidade centralizada
- operação em Kubernetes ou cloud como requisito obrigatório inicial

Essas possibilidades podem ser tratadas como evolução futura, mas não são necessárias para que o projeto cumpra seu objetivo principal de portfólio com valor operacional real.

---

## 6. Sistemas contemplados no monitoramento

A solução será desenhada para observar um conjunto controlado e reproduzível de componentes, permitindo validação ponta a ponta.

### 6.1 Aplicação emissora de logs
O principal sistema monitorado será uma aplicação simples capaz de gerar logs estruturados em JSON. Essa aplicação funcionará como fonte principal de eventos operacionais, incluindo:

- logs informativos de fluxo normal
- logs de aviso para condições anômalas
- logs de erro para simulação de incidentes
- eventos com campos úteis para consulta, filtro e alerta

### 6.2 Infraestrutura/container host
Também serão observadas métricas básicas de infraestrutura, como uso de CPU, com o objetivo de compor dashboards operacionais e demonstrar monitoramento de recursos.

### 6.3 Stack de observabilidade
Os próprios componentes da solução também fazem parte do contexto operacional, incluindo:

- Prometheus, responsável pela coleta de métricas
- Loki, responsável pela centralização de logs
- Grafana, responsável pela visualização e alertas
- Promtail, responsável pela coleta e envio de logs

---

## 7. Usuários finais da plataforma

A plataforma de observabilidade proposta neste projeto atende diferentes perfis de usuário, cada um com necessidades específicas.

### 7.1 SRE / DevOps
Esse público utiliza a plataforma para:

- acompanhar saúde operacional do ambiente
- investigar falhas
- analisar comportamento anômalo
- responder a alertas
- reduzir tempo de diagnóstico

### 7.2 Desenvolvedores
Esse público utiliza a plataforma para:

- inspecionar erros da aplicação
- entender comportamento em execução
- validar eventos de falha
- apoiar troubleshooting sem depender apenas de acesso local à aplicação

### 7.3 Gestores técnicos ou liderança operacional
Esse público utiliza a solução de forma mais estratégica, buscando:

- visibilidade sobre estabilidade do ambiente
- evidência da capacidade operacional da equipe
- redução de incidentes recorrentes
- maior previsibilidade na sustentação dos serviços

---

## 8. Resultados esperados

O projeto deve entregar resultados técnicos e operacionais claros.

### 8.1 Resultados técnicos
- centralização dos logs da aplicação em um repositório consultável
- coleta de métricas com atualização contínua
- dashboards funcionais para leitura operacional
- filtros e consultas para identificação rápida de erro
- integração de alerta automático com Slack

### 8.2 Resultados operacionais
- menor tempo para detectar e investigar falhas
- maior clareza sobre o comportamento da aplicação
- rotina de troubleshooting mais objetiva
- redução do esforço manual para identificar incidentes

### 8.3 Resultados estratégicos
- demonstração prática de maturidade em observabilidade
- fortalecimento do portfólio DevOps com foco em operação real
- evidência de capacidade de integrar coleta, visualização e resposta
- base reutilizável para evoluções futuras em monitoramento e confiabilidade

---

## 9. Valor estratégico da stack Prometheus + Loki + Grafana

A escolha da stack não é apenas técnica; ela também é estratégica.

### 9.1 Prometheus
Responsável pela coleta e consulta de métricas, permite acompanhar sinais quantitativos do ambiente, como CPU, disponibilidade e comportamento temporal de indicadores operacionais.

### 9.2 Loki
Responsável pela centralização e indexação eficiente de logs, permite armazenar e consultar eventos da aplicação de forma integrada ao Grafana, com menor complexidade do que stacks mais pesadas.

### 9.3 Grafana
Atua como camada de visualização e resposta, unificando painéis, consultas, exploração operacional e alertas em uma única interface.

### 9.4 Integração entre os componentes
O valor estratégico da solução está justamente na combinação dessas ferramentas:

- métricas mostram **que há um problema**
- logs ajudam a entender **qual problema ocorreu**
- dashboards ajudam a enxergar **o contexto operacional**
- alertas ajudam a agir **no momento certo**

Essa integração transforma sinais isolados em capacidade operacional utilizável.

---

## 10. Justificativa do recorte técnico adotado

O projeto adota como fonte principal de logs a aplicação com logs estruturados em JSON. Essa decisão foi tomada porque esse modelo oferece melhor equilíbrio entre:

- clareza para consulta e filtragem
- valor demonstrável em portfólio
- capacidade de gerar alertas mais inteligentes
- previsibilidade de implementação
- controle do cenário de validação

Ao escolher logs estruturados como núcleo do projeto, a solução passa a demonstrar não apenas coleta de arquivos, mas observabilidade orientada a eventos operacionais relevantes.

---

## 11. Síntese executiva

O Projeto 03 foi concebido para resolver um problema concreto de operação: a falta de visibilidade sobre o comportamento de aplicações e serviços, que aumenta o MTTR, dificulta a investigação de incidentes e reduz a confiabilidade do ambiente.

A proposta do projeto é construir uma stack de observabilidade reproduzível com Prometheus, Loki, Grafana e Promtail, complementada por alertas automáticos no Slack. Essa stack permitirá observar métricas, centralizar logs estruturados em JSON, analisar erros em tempo real e apoiar uma resposta operacional mais rápida e orientada por dados.

Mais do que apresentar ferramentas, o projeto busca demonstrar maturidade prática em observabilidade, conectando necessidade técnica, impacto operacional e valor estratégico para a sustentação de serviços.
