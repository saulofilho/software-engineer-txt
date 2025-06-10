# Guia Completo de Backstage

Este guia apresenta, de forma avançada, o **Backstage**, plataforma de desenvolvedor open source criada pela Spotify para gerenciar serviços, componentes e documentação em um portal unificado.

---

## 1. O que é Backstage?

* **Backstage** é uma plataforma de developer portal baseada em microsserviços e plugins, construída em Node.js e React.
* **Objetivos**:

  1. **Catálogo unificado** de serviços, bibliotecas e documentação.
  2. **Automação** de scaffolding (boilerplates) via Scaffolder.
  3. **Observabilidade** integrada (monitoramento, logs, métricas).
  4. **Extensibilidade** por meio de plugins oficiais e customizados.

---

## 2. Arquitetura e Componentes Principais

* **Backstage App**: aplicação front-end React + API backend em Node.js (Framework Express).
* **Plugins**: funcionalidades modulares (Catalog, Scaffolder, TechDocs, CI/CD, Auth).
* **Catalog**: armazena metadados de entidades (Component, API, Resource) via arquivos YAML ou integração com Git.
* **Scaffolder**: gera projetos e recursos usando templates declarativos (Handlebars).
* **TechDocs**: exibe documentação Markdown/MDX renderizada via MkDocs.
* **Identity & Auth**: integra com OAuth2, LDAP, SAML ou JWT.
* **Proxy**: back-end inclui proxy para acessos a APIs internas seguras.

---

## 3. Requisitos e Pré-requisitos

* **Node.js** v14 ou superior.
* **Yarn** ou npm.
* **Docker** (opcional, para desenvolvimento com containers).
* **Git** para versionamento e ingestão de metadados.
* Acesso a **GitHub/GitLab/Bitbucket** via tokens API para integração.

---

## 4. Criação de um Backstage App

1. Instale o CLI:

   ```bash
   npm install -g @backstage/create-app
   ```
2. Crie o projeto:

   ```bash
   npx @backstage/create-app
   # Preencha nome, pacote, rota base
   ```
3. Estrutura gerada:

   ```text
   my-backstage/
   ├── packages/
   │   ├── app/           # aplicação front-end
   │   └── backend/       # API backend
   ├── plugins/          # plugins customizados
   ├── catalog-info.yaml # metadados iniciais
   ├── scaffolder/       # templates de scaffolding
   ├── techdocs/         # config de documentação
   └── app-config.yaml   # configurações globais
   ```
4. Executar localmente:

   ```bash
   yarn dev
   ```

   * Acesse `http://localhost:3000`

---

## 5. Configuração do Catálogo

* Adicione entidades criando `catalog-info.yaml` em cada repositório:

  ```yaml
  apiVersion: backstage.io/v1alpha1
  kind: Component
  metadata:
    name: my-service
    description: "Serviço de exemplo"
  spec:
    type: service
    lifecycle: production
    owner: team@example.com
    implementsApis:
      - example-api
  ```
* No `app-config.yaml`, configure o `catalog` e `locations`:

  ```yaml
  catalog:
    locations:
      - type: url
        target: https://raw.githubusercontent.com/org/repo/master/catalog-info.yaml
  ```
* Configure introspeção via GitHub org:

  ```yaml
  catalog:
    providers:
      github:
        orgs:
          - target: github.com/my-org
            branch: main
  ```

---

## 6. Desenvolvimento de Plugins

1. Gere um plugin:

   ```bash
   yarn backstage-cli plugin:generate
   # Escolha nome e rotas
   ```
2. Estrutura do plugin:

   ```text
   plugins/my-plugin/
   ├── src/
   │   ├── components/
   │   ├── routes.ts
   │   └── index.ts
   ├── package.json
   └── README.md
   ```
3. Adicione ao `app/package.json` e `backend/package.json` conforme necessário.
4. Registre no App:

   ```ts
   // packages/app/src/App.tsx
   import { MyPluginPage } from '@backstage/plugin-my-plugin';
   routes.push(<Route path="/my-plugin" element={<MyPluginPage />} />);
   ```
5. Importe no menú e personalize ícones.

---

## 7. Scaffolder Templates

* Defina templates YAML em `scaffolder/templates/my-template/template.yaml`:

  ```yaml
  apiVersion: scaffolder.backstage.io/v1beta3
  kind: Template
  metadata:
    name: node-service
    title: New Node Service
  spec:
    parameters:
      - title: Name
        required: true
        type: string
        name: name
    steps:
      - id: fetch
        name: Fetch skeleton
        action: fetch:template
        input:
          url: ./template
      - id: publish
        name: Publish
        action: publish:github
        input:
          path: ${{ steps.fetch.output.directory }}
          repoUrl: https://github.com/org/${{ parameters.name }}
  ```
* Acesse em **Create...** no UI.

---

## 8. TechDocs (Documentação)

* Configure MkDocs no `techdocs` plugin:

  ```yaml
  techdocs:
    builder: 'local'
    generators:
      techdocs: '@backstage/techdocs-cli'
  ```
* Em cada repositório, adicione `docs/` com `mkdocs.yml`.
* Executar:

  ```bash
  yarn build-techdocs
  yarn start
  ```

---

## 9. Autenticação e Autorização

* Suporta **OAuth2**, **OIDC**, **SAML**, **LDAP**.
* Exemplo GitHub OAuth:

  ```yaml
  auth:
    environment:
      global:
        providers:
          github:
            development:
              clientId: ${GITHUB_CLIENT_ID}
              clientSecret: ${GITHUB_CLIENT_SECRET}
              callbackUrl: http://localhost:7007/auth/github/handler/frame
  ```
* Defina permissões de rota com `@requiresPermission` nos plugins.

---

## 10. Deploy em Produção

### 10.1 Docker

* Dockerfile padrão em `packages/backend/Dockerfile` e `packages/app/Dockerfile`.
* Compose para desenvolvimento:

  ```yaml
  version: '3'
  services:
    backend:
      build: ./packages/backend
      ports:
        - 7007:7007
    app:
      build: ./packages/app
      ports:
        - 3000:3000
      environment:
        APP_CONFIG_app_baseUrl: http://localhost:3000
  ```

### 10.2 Kubernetes (Helm)

* Use **Helm chart** oficial ou **kustomize**:

  ```bash
  helm repo add backstage https://backstage.github.io/charts
  helm install backstage backstage/backstage \
    --set app.baseUrl=https://backstage.example.com \
    --set auth.github.clientId=... \
    --set auth.github.clientSecret=...
  ```

---

## 11. Observabilidade

* **Logging** e **Tracing** via **OpenTelemetry**.
* Integração com **Prometheus**, **Grafana**, **Loki** e **Tempo**.
* Exponha endpoints `/metrics` e **Health Checks**.

---

## 12. Boas Práticas e Dicas

1. **Mantenha App Config Seguro**: use Vault ou Kubernetes Secrets.
2. **Versione Entidades** no catálogo para rastreabilidade.
3. **Automatize** publicação de templates e documentação.
4. **Teste** plugins isoladamente com Jest e React Testing Library.
5. **Atualize** dependências e Backstage LTS regularmente.
6. **Reutilize** plugins oficiais e da comunidade antes de criar novos.
7. **Implemente** monitoramento de performance (Web Vitals).

---

## Conclusão

O Backstage facilita a descoberta, criação e operação de serviços em larga escala, centralizando informações e automação. Com sua arquitetura de plugins, é possível estender e personalizar para atender às necessidades de qualquer organização.
