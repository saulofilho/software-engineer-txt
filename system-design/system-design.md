# Guia Completo de System Design

Este guia aborda, de forma avançada e prática, os princípios, padrões e melhores práticas para projetar sistemas de software escaláveis, resilientes e manuteníveis.

---

## 1. Introdução ao System Design

* **Objetivo**: traduzir requisitos funcionais e não funcionais em arquiteturas de alto nível.
* **Requisitos Não Funcionais (NFRs)**: escalabilidade, disponibilidade, performance, segurança, manutenibilidade.
* **Abordagem**: top-down — comece pelo panorama geral, depois detalhe componentes.

---

## 2. Etapas do System Design

1. **Coleta de Requisitos**

   * Funcionais: fluxos de usuários, operações suportadas.
   * Não Funcionais: picos de tráfego, latência aceitável, SLAs, restrições geográficas.
2. **Capacidade e Dimensionamento**

   * Estimar QPS (queries por segundo), tamanho de payload, crescimento projetado.
   * Calcular latência e throughput necessários.
3. **High-Level Architecture**

   * Definir clientes, API Gateway/Load Balancer, serviço, banco de dados, cache, fila, CDN.
4. **Component Breakdown**

   * Detalhar subdivisão em microserviços ou módulos, definir contratos, protocolos (REST/gRPC).
5. **Detalhamento de Dados**

   * Modelagem de dados: SQL vs NoSQL, esquemas, normalização, denormalização, sharding.
6. **Design de Escalabilidade**

   * Horizontal vs Vertical, Particionamento, Replicação, Caching.
7. **Alta Disponibilidade e Resiliência**

   * Failover, Health Checks, Retry Patterns, Circuit Breaker.
8. **Observabilidade e Monitoramento**

   * Logs estruturados, métricas (Prometheus), tracing distribuído (Jaeger), alertas.
9. **Segurança**

   * Autenticação, Autorização, Proteção contra DDoS, TLS, regras de firewall.
10. **Deploy e Operações**

* CI/CD, Blue/Green, Canary Releases, Infraestrutura como Código (Terraform).

---

## 3. Padrões Arquiteturais Comuns

| Padrão                | Descrição                                          | Quando usar                             |
| --------------------- | -------------------------------------------------- | --------------------------------------- |
| Monolito              | Aplicação única                                    | MVP, baixo tráfego                      |
| Microservices         | Serviços pequenos e independentes                  | Escalar componentes isoladamente        |
| Serverless            | Funções FaaS sob demanda                           | Carga variável, event-driven            |
| Event-Driven          | Sistema baseado em eventos e mensagens             | Alta desacoplagem e extensibilidade     |
| CQRS + Event Sourcing | Separação de leitura/escrita, histórico de eventos | Complexidade na consistência, auditoria |

---

## 4. Componentes Fundamentais

### 4.1 Load Balancer

* Distribui tráfego entre instâncias.
* Algoritmos: Round Robin, Least Connections, IP Hash.

### 4.2 Banco de Dados

* **Relacional**: forte consistência, ACID.
* **NoSQL**: chave-valor, documentos, wide-column, grafo.
* **Sharding**: particionar dados horizontalmente.
* **Replicação**: master-slave, master-master.

### 4.3 Cache

* **In-Memory**: Redis, Memcached.
* **CDN**: conteúdo estático georreferenciado.
* **Cache Aside** vs **Write-Through** vs **Write-Back**.

### 4.4 Filas e Mensageria

* Desacoplar produtores e consumidores.
* Garantias: at-least-once, at-most-once, exactly-once.

### 4.5 API Gateway

* Unified entrypoint, roteamento, autenticação, rate limiting.

### 4.6 CDN (Content Delivery Network)

* Acelera entrega de recursos estáticos, reduz latência geográfica.

---

## 5. Escalabilidade e Performance

* **Escalabilidade Horizontal**: adicionar instâncias.
* **Particionamento de Dados**: hash, range, geográfico.
* **Consistência vs Disponibilidade**: teorema CAP.
* **Bulkhead**: isola falhas em subsistemas.
* **Backpressure**: controlar sobrecarga (circuit breaker, rate limiter).

---

## 6. Alta Disponibilidade e Resiliência

* **Failover Automático**: múltiplas zonas/\_regions.
* **Health Checks e Auto-Healing**: Kubernetes Liveness/Readiness.
* **Retry, Timeout, Circuit Breaker** (padrões do resiliency4j).
* **Disaster Recovery**: backups, replicação assíncrona, RTO/RPO.

---

## 7. Observabilidade

* **Logging**: Correlation ID, JSON logs.
* **Métricas**: latência, erros, throughput (Prometheus).
* **Tracing Distribuído**: context propagation, Jaeger/Zipkin.
* **Alerting**: thresholds, anomalias (Grafana).

---

## 8. Segurança

* **Autenticação**: OAuth2, JWT, mTLS.
* **Autorização**: RBAC, ABAC.
* **Proteção**: WAF, Rate Limiting, Input Validation.
* **Criptografia**: TLS em trânsito, AES em repouso.

---

## 9. Casos de Estudo Exemplares

### 9.1 Design do Instagram

* Upload de fotos: uso de CDN, serviços de processamento de mídia.
* Feed: geração offline (batch) vs online, cache hierarchical.

### 9.2 Design do Twitter

* Timeline: fan-out vs fan-in, sharding de fanout service.
* Tweets: armazenamento em HBase, cache em Redis.

---

## 10. Boas Práticas e Pitfalls

* **YAGNI e KISS**: evite complexidade prematura.
* **Observabilidade desde o início**.
* **Testes de carga e caos engineering** (Chaos Monkey).
* **Documentação**: diagramas C4, API specs (OpenAPI).
* **Revisões de arquitetura**: Architecture Review Boards.

---

## 11. Conclusão

System Design é uma habilidade essencial para engenheiros de software sêniores. Pratique projetando sistemas variados, valide trade-offs e refine soluções com base em métricas reais.
