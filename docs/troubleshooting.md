# Troubleshooting do Projeto 03

## Objetivo

Este documento existe para registrar problemas encontrados ao longo da implementação e validação da stack de observabilidade, mantendo histórico técnico de erros, hipóteses, validações, correções aplicadas e formas de prevenção.

A proposta é transformar falhas operacionais em conhecimento reutilizável, facilitando troubleshooting futuro e aumentando a maturidade de operação do projeto.

---

## Estrutura padrão de análise

Sempre que ocorrer um problema relevante, o registro deve seguir este modelo:

### Erro observado
Descrever objetivamente o sintoma, mensagem de erro ou comportamento inesperado.

### O que significa
Explicar tecnicamente o erro em linguagem clara.

### Causa provável
Registrar a hipótese principal com base no comportamento observado.

### Como validar
Descrever os comandos, verificações ou evidências usados para confirmar a hipótese.

### Correção aplicada
Registrar a ação executada para resolver o problema.

### Como evitar no futuro
Registrar aprendizado operacional, ajuste estrutural ou hábito de validação que reduz a chance de recorrência.

---

## Histórico de troubleshooting

### Registro 001
**Status:** resolvido

### Erro observado
Promtail apresentava erro recorrente ao gravar o arquivo de posições:
`error writing positions file` com falha de `rename` em `/tmp/positions.yaml` e mensagem `device or resource busy`.

### O que significa
O Promtail não conseguia persistir corretamente o estado de leitura dos logs. Isso comprometia a retomada consistente após reinicializações.

### Causa provável
O `docker-compose.yml` montava um arquivo individual do host diretamente em `/tmp/positions.yaml`, enquanto o Promtail utiliza escrita atômica com arquivo temporário e `rename`, gerando conflito no bind mount de arquivo.

### Como validar
- revisar `docker-compose.yml`
- revisar `promtail/config.yml`
- verificar logs do container `promtail`
- confirmar ausência de novos erros após reinicialização da stack

### Correção aplicada
Foi substituído o bind mount do arquivo `./promtail/positions.yaml:/tmp/positions.yaml` por um bind mount de diretório `./promtail/data:/var/lib/promtail`, e o `positions.filename` foi alterado para `/var/lib/promtail/positions.yaml`.

### Como evitar no futuro
Evitar persistir arquivos de estado internos de containers via bind mount direto em arquivo quando o processo usa escrita atômica com `rename`. Preferir bind mount de diretório persistente.

### Registro 002
**Status:** resolvido

### Erro observado
Ao cadastrar o Loki como data source no Grafana, a conexão falhou com a mensagem:
`Unable to connect with Loki. Please check the server logs for more details.`

### O que significa
O Grafana não conseguiu alcançar a API do Loki usando a URL configurada no data source.

### Causa provável
A URL foi digitada incorretamente no cadastro do data source.

### Como validar
- revisar a URL configurada no Grafana
- testar novamente com `Save & test`
- confirmar sucesso da conexão
- validar consulta no Explore com `{job="app-logs"}`

### Correção aplicada
Foi corrigida a URL do data source Loki no Grafana para o formato correto com hostname do serviço Docker Compose e porta adequada.

### Como evitar no futuro
Sempre validar com atenção hostname e porta ao cadastrar integrações entre containers. Em ambiente Docker Compose, preferir o nome do serviço como hostname interno.

---

## Observação operacional

Nem todo erro precisa virar registro formal. Devem entrar aqui principalmente:

- falhas de integração entre componentes
- problemas de configuração
- erros de comunicação entre serviços
- comportamentos inesperados da stack
- correções que gerem aprendizado reutilizável