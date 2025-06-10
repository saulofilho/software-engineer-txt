# Guia Completo de OpenShift

Este guia apresenta, de forma detalhada e avançada, o **Red Hat OpenShift**, plataforma de containers corporativa baseada em Kubernetes, cobrindo arquitetura, instalação, operações, segurança, CI/CD e boas práticas.

---

## 1. O que é OpenShift?

* Plataforma de containers empresarial, desenvolvida pela Red Hat, que estende o Kubernetes com funcionalidades de PaaS (Platform as a Service).
* Inclui:

  * **OKD** (Origin Community Distribution) versão comunitária.
  * **OpenShift Container Platform** (OCP) versão suportada pela Red Hat.
* Objetivos:

  1. Simplificar deploy e gerenciamento de aplicações em containers.
  2. Integrar pipelines de build, deploy e observabilidade.
  3. Garantir segurança e governança corporativa.

---

## 2. Arquitetura

### 2.1 Componentes Principais

* **Control Plane (Masters)**:

  * API Server, Controller Manager, Scheduler, etcd.
* **Worker Nodes**:

  * kubelet, CRI-O/Docker, SDN (Open vSwitch), conectados ao schedulers.
* **Ingress & Routers**:

  * HAProxy ou Routes para expor serviços externamente.
* **Registry Interno**:

  * Armazena imagens de containers construídas.
* **Operators**:

  * Gerenciam ciclo de vida de componentes (Prometheus, Kafka, etc.).
* **Pipelines (Tekton)**:

  * Integração com CI/CD.

### 2.2 SDN e NetworkPolicies

* **OpenShift SDN**: plugin CNI padrão, suporta multitenancy via NetworkPolicy.
* **OpenShift OVN-Kubernetes**: alternativa que utiliza OVN para redes avançadas.

---

## 3. Instalação e Provisionamento

### 3.1 Modos de Instalação

1. **IPI (Installer Provisioned Infrastructure)**:

   * Provisiona automaticamente infra em AWS, Azure, GCP, VMware.
2. **UPI (User Provisioned Infrastructure)**:

   * O usuário configura rede, DNS, storage, depois instala.

### 3.2 Requisitos

* **Hardware**:

  * Mínimo 3 masters (2 CPU, 8 GB RAM) e 3 workers (4 CPU, 16 GB RAM).
* **Rede**:

  * DNS wildcard, load balancer para API e ingress.
* **Armazenamento**:

  * NFS, GlusterFS, Ceph, ou provedor CSI.

### 3.3 Passos Básicos (IPI em AWS)

1. **Pré-requisitos**: AWS CLI configurado, domínio configurado no Route 53.
2. **Download do instalador**:

   ```bash
   ocp-install-linux-amd64
   ```
3. **Criar arquivo install-config.yaml** com credenciais e configurações.
4. **Executar**:

   ```bash
   ./openshift-install create cluster
   ```
5. **Acessar Console**: [https://console-openshift-console.apps](https://console-openshift-console.apps).\<domínio>

---

## 4. Gerenciamento de Recursos

### 4.1 `oc` CLI

* Comandos essenciais:

  * `oc login`, `oc get pods|svc|routes|projects`.
  * `oc new-project`, `oc adm policy`.
  * `oc apply -f` para manifests YAML.

### 4.2 Projetos e Quotas

* **Namespaces** isolados por projeto.
* **ResourceQuota** e **LimitRange** para cota de CPU/memória.

### 4.3 Templates e Operators

* **Templates**: definem objetos Kubernetes via parâmetros.

  ```bash
  oc create -f template.yaml
  oc new-app mytemplate -p PARAM=value
  ```
* **Operators**: instalados via Operator Hub, gerenciam StatefulSets, etc.

---

## 5. Build e Deploy

### 5.1 BuildConfigs e ImageStreams

* **BuildConfig**: define pipeline de build (Source, Docker, S2I).
* **ImageStream**: rastreamento de tags e triggers.

### 5.2 Source-to-Image (S2I)

* Constrói imagens a partir de código-fonte e builder images.

  ```bash
  oc new-app registry.redhat.io/openshift4/jenkins-2-rhel7~https://github.com/my/repo.git
  ```

### 5.3 DeployConfigs e Rollouts

* **DeploymentConfig**: objeto OpenShift com triggers automáticos.
* **Rollout strategies**: Recreate, Rolling, Custom.

---

## 6. CI/CD com Pipelines (Tekton)

* **OpenShift Pipelines** usa Tekton.

  * **Tasks**, **Pipelines**, **PipelineRuns**.
* Integre com **GitHub Actions** ou **Jenkins**.

---

## 7. Observabilidade e Logging

### 7.1 Monitoramento

* **Prometheus Operator** e **Grafana**.
* Métricas de cluster e aplicações.

### 7.2 Logging Centralizado

* **EFK Stack**: Elasticsearch, Fluentd, Kibana.
* Visualização via Kibana ou Kibana integrado em Console.

---

## 8. Segurança e Compliance

### 8.1 SecurityContextConstraints (SCC)

* Define permissões de pods (RunAsUser, SELinux).
* Configurar SCC customizadas via `oc adm`.

### 8.2 RBAC e OAuth

* **RoleBindings** e **ClusterRoleBindings**.
* Usuários federados via **LDAP**, **GitHub**, **OIDC**.

### 8.3 NetworkPolicy e Quotas

* **NetworkPolicy** para isolar tráfego.
* Quotas para limitar recursos.

---

## 9. Storage

* **PersistentVolumeClaims** com provisionamento dinâmico.
* Drivers CSI: AWS EBS, Azure Disk, CephFS, NFS.
* **OpenShift Data Foundation** para armazenamento de alto desempenho.

---

## 10. Troubleshooting e Recuperação

* **Diagnóstico**: `oc adm must-gather`, logs do API Server e kubelet.
* **Upgrade**: via `oc adm upgrade` sem downtime.
* **Backups**: etcd snapshots e snapshots de PV.

---

## 11. Boas Práticas

1. **Automatizar** deploy e upgrade via GitOps (ArgoCD, Flux).
2. **Definir Quotas** para evitar negação de serviço.
3. **Usar Operators** oficiais para serviços críticos.
4. **Implementar Zero Trust**: autenticação forte e NetworkPolicy.
5. **Monitorar** SLA de aplicações e tempo de resposta.
6. **Testar DR** com restauração de etcd e PV.

---

## Conclusão

O OpenShift adiciona automação, segurança e integração a um cluster Kubernetes padrão, habilitando DevOps em grande escala. Dominar seus componentes e práticas garante operações resilientes e seguras em ambientes corporativos.
