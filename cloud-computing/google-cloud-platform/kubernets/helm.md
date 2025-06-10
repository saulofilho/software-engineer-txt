# Guia Completo de Helm

Este guia aborda, em nível avançado, o **Helm**, o gerenciador de pacotes para Kubernetes, cobrindo conceitos, arquitetura, instalação, comandos essenciais, desenvolvimento de charts, repositórios, segurança, pipelines e boas práticas.

---

## 1. O que é Helm?

* Helm é o gerenciador de pacotes para Kubernetes, facilitando deploy, versionamento e atualização de aplicações como **charts**.
* Inspirado em gerenciadores de pacotes tradicionais (apt, yum), mas voltado para objetos Kubernetes.
* Componentes principais:

  * **Helm CLI** (`helm`)
  * **Tiller** (Helm v2; removido no v3)
  * **Charts**: pacotes contendo templates e valores
  * **Repositórios**: armazéns de charts

---

## 2. Arquitetura do Helm v3

* **Cliente-Only**: CLI único, sem servidor no cluster.
* **Helm Activities**:

  1. **Init**: configuração local de repositórios e cache
  2. **Install**: cria um **release** a partir de um chart
  3. **Upgrade**: aplica mudanças a um release existente
  4. **Rollback**: reverte para versão anterior do release
  5. **Uninstall**: remove um release
* **Releases**: instâncias de charts implantadas em um namespace
* **Repository Index**: arquivo `index.yaml` que descreve charts e versões

---

## 3. Instalação e Configuração Inicial

### 3.1 Instalar Helm CLI

* **Linux/macOS** (via script):

  ```bash
  curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
  ```
* **Homebrew** (macOS/Linux):

  ```bash
  brew install helm
  ```
* **Scoop** (Windows):

  ```powershell
  scoop install helm
  ```

### 3.2 Configurar Repositórios Padrão

```bash
helm repo add stable https://charts.helm.sh/stable
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

* Lista de repositórios:

  ```bash
  helm repo list
  ```

---

## 4. Comandos Básicos

| Comando                          | Descrição                                   |
| -------------------------------- | ------------------------------------------- |
| `helm repo add <nome> <url>`     | Adiciona repositório de charts              |
| `helm repo update`               | Atualiza cache local de repositórios        |
| `helm search repo <termo>`       | Busca charts em repositórios                |
| `helm install <nome> <chart>`    | Instala um chart como release               |
| `helm list`                      | Lista releases implantados                  |
| `helm status <release>`          | Exibe status de um release                  |
| `helm upgrade <release> <chart>` | Atualiza um release                         |
| `helm rollback <release> [n]`    | Reverte release para a revisão `n`          |
| `helm uninstall <release>`       | Remove um release                           |
| `helm get values <release>`      | Exibe valores usados no release             |
| `helm template <chart>`          | Renderiza templates localmente (sem deploy) |

---

## 5. Estrutura de um Chart

```
mychart/
├── Chart.yaml       # metadados (nome, versão, dependências)
├── values.yaml      # valores padrão configuráveis
├── charts/          # charts dependentes (subcharts)
├── templates/       # templates Go para objetos Kubernetes
│   ├── deployment.yaml
│   ├── service.yaml
│   └── _helpers.tpl # funções e helpers de template
└── README.md        # documentação do chart
```

### 5.1 `Chart.yaml`

```yaml
apiVersion: v2
name: mychart
version: 1.2.3
appVersion: "1.16.0"
dependencies:
  - name: redis
    version: "14.x.x"
    repository: https://charts.bitnami.com/bitnami
```

### 5.2 `values.yaml`

```yaml
replicaCount: 2
image:
  repository: myapp
  tag: latest
service:
  type: ClusterIP
  port: 80
resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 50m
    memory: 64Mi
```

### 5.3 Templates Go

* Helpers em `_helpers.tpl`: funções reutilizáveis, nomenclatura de recursos.
* Utilização de sintaxe `{{ .Values.image.repository }}` para injeção de valores.
* Condicionais e loops: `{{ if .Values.service.enabled }}` e `{{ range .Values.ports }}`.

---

## 6. Desenvolvimento Avançado de Charts

### 6.1 Dependências de Charts

```bash
helm dependency update mychart/
helm dependency build mychart/
```

* `charts/` conterá os dependentes.

### 6.2 Chart Hooks

* Permitem executar tarefas antes/depois de install/upgrade/uninstall.
* Exemplos:

  * `pre-install`, `post-install`
  * `pre-upgrade`, `post-upgrade`
  * `pre-delete`, `post-delete`
* Exemplo de hook em `templates/hooks.yaml`:

  ```yaml
  apiVersion: batch/v1
  kind: Job
  metadata:
    name: "{{ include "mychart.fullname" . }}-migrate"
    annotations:
      "helm.sh/hook": pre-upgrade
  spec:
    template:
      spec:
        containers:
          - name: migrate
            image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
            command: ["/scripts/migrate.sh"]
        restartPolicy: OnFailure
  ```

### 6.3 Testes de Chart

* Definir testes em `templates/tests/` com `helm.sh/hook: test`
* Executar:

  ```bash
  helm test <release>
  ```

### 6.4 Lint e Validação

```bash
helm lint mychart/
```

* Detecta erros de sintaxe, valores ausentes e práticas incorretas.

---

## 7. Repositórios de Charts

### 7.1 Criar e Hospedar

1. Empacotar chart:

   ```bash
   helm package mychart/
   ```
2. Atualizar `index.yaml`:

   ```bash
   helm repo index . --url https://meus-charts.example.com/
   ```
3. Servir `index.yaml` e arquivos `.tgz` via HTTP (Nginx, S3).

### 7.2 Gerenciamento de Versões

* Use **SemVer** (`MAJOR.MINOR.PATCH`) no `Chart.yaml`.
* Publique cada alteração de chart como nova versão.
* Remova versões obsoletas e atualize `index.yaml`.

---

## 8. Integração CI/CD

* **GitOps** com ArgoCD ou Flux:

  * Armazenar charts ou `values.yaml` em repositório Git.
  * Sincronização automática de releases.
* **Pipelines** (Jenkins, GitLab CI, GitHub Actions):

  1. Lint e teste de charts
  2. Build do chart (`helm package`)
  3. Publicação em repositório (S3, ChartMuseum)
  4. Deploy em cluster de homologação/produção

```yaml
# Exemplo GitHub Actions snippet
- name: Lint Chart
  run: helm lint mychart/
- name: Package Chart
  run: helm package mychart/ --destination charts/
- name: Publish to S3
  run: aws s3 sync charts/ s3://meu-bucket/charts --acl public-read
```

---

## 9. Segurança de Charts e Releases

* **Assinatura**:

  * Chave GPG para assinar charts:`helm package --sign --key mykey --keyring /path/to/keyring.gpg`
  * Configurar `--verify` no `helm install`.
* **Segurança de Valores**:

  * Não versionar segredos em `values.yaml`; usar **SealedSecrets**, **ExternalSecrets** ou **Vault**.
  * Integrar com **helm-secrets** plugin para criptografia.

---

## 10. Boas Práticas e Considerações Finais

1. **Manter templates simples**: evitar lógicas complexas em templates.
2. **Valores sensíveis**: use mecanismos de segredo externos.
3. **Documentação**: incluir exemplos e descrições em `README.md`.
4. **Versão Semântica**: evolua charts de forma estável.
5. **Automação**: pipelines para lint, testes e deploy.
6. **Monitore releases**: use `helm status` e alertas.
7. **Evite Tiller** (Helm v2); claro adote Helm v3.

---

## Conclusão

Helm transforma a experiência de gerenciamento de aplicações em Kubernetes, provendo estrutura, versionamento e automação. Domine a criação de charts, repositórios e pipelines para operar ambientes em larga escala com segurança e eficiência.
