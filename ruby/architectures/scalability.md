### Load Balancer

- Sim, quase sempre tem. Pode ser um ELB (AWS), NGINX, HAProxy ou outro.
- Ele é quem faz o roteamento das requisições externas para os serviços internos.
- Normalmente usado junto de um proxy reverso para balancear e proteger APIs.

---

### ✅ Proxy Reverso

- Pode ser o próprio Load Balancer ou um componente à parte (NGINX, Traefik, Envoy).
- Faz terminação de SSL, autenticação de requests, controle de rate limit, e roteamento inteligente.
- Em Kubernetes é comum usar um **Ingress Controller** (que é basicamente um proxy reverso gerenciado).

---

### ✅ Redundância de Banco de Dados

- Sempre recomendado, principalmente com clusters (Postgres com Patroni, MySQL com Group Replication, MongoDB ReplicaSet, etc.).
- Replicação síncrona ou assíncrona, dependendo do caso.
- Alta disponibilidade via failover automático ou manual.

---

### ✅ Auto-scaling

- Kubernetes faz auto-scaling de pods automaticamente (HPA - Horizontal Pod Autoscaler).
- Infraestrutura (máquinas virtuais ou nodes) geralmente escalada com Terraform + auto-scaling groups (AWS, GCP).
- Pode ser baseado em CPU, memória, filas, ou métricas customizadas (como latência ou throughput).

---

### ✅ Kubernetes + Skaffold + Terraform

- **Terraform** provisiona a infra (rede, VPC, clusters, bancos, balancers).
- **Kubernetes** orquestra os containers e mantém os serviços funcionando.
- **Skaffold** facilita o ciclo de desenvolvimento (build, deploy e teste local e em clusters).

---

### ✅ Comunicação entre as peças

Pode ter uma combinação de:

1. **HTTP/REST** - Clássico, simples, direto.
2. **gRPC** - Se precisar de performance e comunicação binária.
3. **Mensageria** - Se for desacoplado ou assíncrono:
    - **Kafka** para *event streaming*.
    - **RabbitMQ** para filas tradicionais.
    - **SNS/SQS** (AWS) para pub/sub e filas simples.
4. **Service Mesh** - (opcional) Istio ou Linkerd para gerenciar comunicações internas, segurança e observabilidade.
