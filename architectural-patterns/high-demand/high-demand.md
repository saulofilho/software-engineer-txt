## 🏗️ Arquitetura de Alta Demanda com Ruby on Rails

### 1. **Separação de Responsabilidades**

- **Monólito bem organizado** OU **Arquitetura modular/Service-Oriented Architecture (SOA)**.
- Ex: `app/services`, `app/workers`, `app/serializers`, `app/interactors`.

---

### 2. **Load Balancing**

- Use um **load balancer** como:
    - **NGINX** ou **HAProxy**.
    - Em nuvem: **AWS ELB**.
- Balanceia requisições entre múltiplos containers/instâncias da aplicação.

---

### 3. **Escalabilidade Horizontal**

- Rodar múltiplas instâncias da aplicação com **Docker** ou em **Kubernetes (k8s)**.
- Usar **Rails server** eficiente (como **Puma**) em modo **cluster**.

```ruby
# config/puma.rb
workers ENV.fetch("WEB_CONCURRENCY") { 4 }
threads_count = ENV.fetch("RAILS_MAX_THREADS") { 5 }
threads threads_count, threads_count

```

---

### 4. **Banco de Dados Otimizado**

- PostgreSQL (com réplicas de leitura se necessário).
- **Read/Write split**.
- **Connection Pooling** com PgBouncer.
- Indexes bem planejados.
- Query caching e uso de `includes`, `select`, `pluck` etc.

---

### 5. **Fila de Processamento Assíncrono**

- Sidekiq + Redis para background jobs.
- Ex: envio de e-mails, geração de PDFs, processamento de imagens, etc.

---

### 6. **Cache Estratégico**

- **Fragment caching** no Rails (ex: `cache do ... end`).
- **Russian doll caching**.
- Usar **Redis** ou **Memcached** para:
    - Cache de páginas, dados comuns, sessões.
    - Cache de consultas caras com `Rails.cache.fetch`.

---

### 7. **CDN + Asset Pipeline**

- Servir assets estáticos via **CDN** (Cloudflare, Fastly, AWS CloudFront).
- Usar `asset_sync` para mandar assets para o S3.
- Pré-compilação eficiente com Webpacker ou Propshaft (Rails 7).

---

### 8. **Observabilidade e Monitoramento**

- Logging estruturado com Lograge.
- APMs como:
    - New Relic
    - Datadog
    - Scout APM
- Dashboards com Prometheus + Grafana.
- Alertas com Sentry ou Honeybadger.

---

### 9. **Feature Flags / Toggle**

- Permite ativar/desativar recursos sem precisar deployar.
- Gems: `flipper`, `rollout`.

---

### 10. **CD/CI**

- Deploys contínuos com GitHub Actions, GitLab CI ou CircleCI.
- Releases pequenos e reversíveis (Blue/Green deploys, canary).

---

### Exemplo em Infraestrutura (Kubernetes)

```bash
Users -> Cloudflare CDN
      -> AWS Load Balancer
         -> NGINX (Ingress Controller)
            -> Rails App (Puma) x N pods
               -> Redis (Sidekiq) x N workers
               -> PostgreSQL (RDS) + Read Replicas
               -> Redis (Cache)

```

---

## ☁️ Arquitetura Adaptada para **AWS**

### 🔹 Componentes:

| Função | Serviço AWS |
| --- | --- |
| Load Balancer | **Elastic Load Balancer (ALB)** |
| App Containers | **ECS (Fargate)** ou **EKS (Kubernetes)** |
| Banco de Dados | **RDS (PostgreSQL)** com Read Replicas |
| Cache / Session Store | **ElastiCache (Redis/Memcached)** |
| Background Jobs | **Sidekiq em ECS/EKS** |
| Armazenamento de Arquivos | **S3** |
| Assets estáticos | **CloudFront** (CDN) + S3 |
| Monitoramento | **CloudWatch**, **X-Ray**, **Sentry** |
| CI/CD | **CodePipeline** ou GitHub Actions |
| Secrets | **AWS Secrets Manager** ou **SSM Parameter Store** |

---

## ☁️ Arquitetura Adaptada para **GCP**

### 🔹 Componentes:

| Função | Serviço GCP |
| --- | --- |
| Load Balancer | **Cloud Load Balancing** |
| App Containers | **Cloud Run** (serverless) ou **GKE (Kubernetes)** |
| Banco de Dados | **Cloud SQL (PostgreSQL)** com réplicas |
| Cache / Session Store | **MemoryStore (Redis)** |
| Background Jobs | Sidekiq em GKE ou Cloud Run Jobs |
| Armazenamento de Arquivos | **Cloud Storage** |
| Assets estáticos | **Cloud CDN** + Cloud Storage |
| Monitoramento | **Cloud Monitoring** + **Error Reporting** |
| CI/CD | **Cloud Build**, GitHub Actions, GitLab CI |
| Secrets | **Secret Manager** |

---

## 🔁 Infraestrutura Comparada (Simplificada)

| Camada | AWS | GCP |
| --- | --- | --- |
| **Load Balancer** | Application Load Balancer (ALB) | Cloud Load Balancer |
| **App Layer** | ECS (Fargate) ou EKS (k8s) + Puma | Cloud Run (serverless) ou GKE (k8s) |
| **DB** | RDS (PostgreSQL) + Read Replicas | Cloud SQL (PostgreSQL) + Read Replicas |
| **Jobs** | Sidekiq via ECS/EKS | Sidekiq via GKE ou Cloud Run Jobs |
| **Cache** | ElastiCache (Redis) | MemoryStore (Redis) |
| **Armazenamento** | S3 | Cloud Storage |
| **CDN** | CloudFront | Cloud CDN |
| **Monitoring** | CloudWatch + X-Ray | Cloud Monitoring + Error Reporting |
| **Secrets** | Secrets Manager / SSM | Secret Manager |
