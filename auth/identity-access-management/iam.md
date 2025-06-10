# Guia Completo de Gerenciamento de Identidade e Acesso (IAM)

Este guia apresenta, de nível avançado, todos os aspectos de **Identity and Access Management (IAM)**: conceitos, componentes, protocolos, práticas, arquiteturas e ferramentas.

---

## 1. Visão Geral de IAM

* **Definição**: Conjunto de políticas, processos e tecnologias para gerenciar identidades (quem é) e autorizações (o que pode fazer) em sistemas.
* **Objetivos**:

  1. Garantir acesso correto a recursos.
  2. Unificar autenticação e autorização.
  3. Prover auditoria e conformidade.
* **Benefícios**:

  * Segurança reforçada.
  * Experiência de usuário (SSO).
  * Eficiência operacional e governança.

---

## 2. Componentes de um Sistema IAM

1. **Identity Store**: repositório de identidades (LDAP, Active Directory, banco SQL, SCIM service).
2. **Authentication**: confirmação de identidade (senha, MFA, biometria).
3. **Authorization**: controle de acesso (RBAC, ABAC, PBAC).
4. **Directory Services**: diretórios LDAP/AD para consulta de atributos.
5. **Federation**: integração de domínios de confiança (SAML, OIDC).
6. **Lifecycle Management**: criação, modificação e exclusão de contas (provisioning/deprovisioning).
7. **Privileged Access Management**: controle de contas de alto privilégio.
8. **Audit & Compliance**: logs de acesso, relatórios e conformidade regulatória.

---

## 3. Modelos de Autenticação

* **Single Factor**: senha, token estático.
* **Multi-Factor (MFA)**: combinação de algo que você sabe (senha), algo que você tem (token), algo que você é (biometria).
* **Adaptive / Risk-Based**: ajusta requisitos de autenticação conforme contexto (localização, device).

---

## 4. Protocolos e Padrões

| Protocolo/Padronização | Papel em IAM                            | Exemplo de Uso                       |
| ---------------------- | --------------------------------------- | ------------------------------------ |
| **LDAP / AD**          | Diretório de identidades e atributos    | Autenticação interna de corporações  |
| **SAML 2.0**           | Federation e SSO baseado em XML         | SSO entre empresas e aplicações SaaS |
| **OAuth 2.0**          | Autorização de APIs                     | Concessão de tokens a apps clientes  |
| **OIDC**               | Autenticação federada baseada em OAuth2 | Login federado via Google/Microsoft  |
| **SCIM 2.0**           | Provisionamento automático de usuários  | Provisionar contas em SaaS           |
| **Kerberos**           | Autenticação unificada em redes Windows | Ingresso único em redes corporativas |
| **WS-Fed / WS-Trust**  | Serviços SOAP federados                 | Integração legado SOAP               |

---

## 5. Autorização: Modelos de Controle

### 5.1 RBAC (Role-Based Access Control)

* Define permissões baseadas em **papéis** (roles).
* Simples de entender; requer definição de roles e assignment de usuários.

### 5.2 ABAC (Attribute-Based Access Control)

* Avalia **atributos** de usuário, recurso e ambiente para decisão.
* Flexível para cenários dinâmicos.

### 5.3 PBAC (Policy-Based Access Control)

* Políticas escritas em linguagem declarativa (XACML, Rego).
* Permite centralizar regras e avaliações via PDP/PEP.

---

## 6. Arquiteturas IAM

### 6.1 Centralizado

* Um único IdP e PDP; simples gestão, mas ponto único de falha.

### 6.2 Federado

* Vários domínios confiáveis via SAML / OIDC; alta disponibilidade e isolamento.

### 6.3 Zero Trust Identity

* Microsegmentação com autenticação/ autorização contínuas.
* Verifica identidades e contexto a cada solicitação.

---

## 7. Provisionamento e Deprovisionamento

* **SCIM**: protocolo REST/Schemas JSON para CRUD de identidades.
* **Branching Workflows**: onboarding/offboarding via automação (API call, workflows no IdP).
* **Reconciliation**: rotina periódica para alinhar identidade fonte e destinos (SaaS apps).

---

## 8. Privileged Access Management (PAM)

* Controle de contas elevadas (root, domain admin).
* **Vaults**: cofre de senhas (HashiCorp Vault, CyberArk).
* **Sessões elevadas**: gravações, monitoramento de comandos.

---

## 9. Implementação de IdP/SSO

### 9.1 Keycloak

* Open source, suporta OIDC, SAML, Kerberos.
* Componentes: Realm, Client, User Federation, Identity Brokering.

### 9.2 Azure AD

* PaaS Microsoft, integra com Office365, apps custom.
* Suporta SAML, OIDC, SCIM, MFA, Conditional Access.

### 9.3 Okta / Auth0

* SaaS IAM com UI de configuração.
* APIs para integração, pulsos de eventos.

---

## 10. Integração de Aplicações

* **SDKs**:

  * Java: Spring Security SAML/OAuth.
  * .NET: Microsoft.Identity.Web, Sustainsys.Saml2.
  * Node.js: passport-saml, oidc-client.
* **Middleware**: intercepta requests, valida tokens/assertions.
* **Token Translation**: converter SAML → JWT para APIs.

---

## 11. Monitoramento e Auditoria

* **Logs de Acesso**: record login, logout, falhas.
* **SIEM**: coletar e correlacionar eventos de IAM.
* **Métricas**: tempo de login, taxa de falhas de autenticação.

---

## 12. Conformidade e Governança

* **PCI DSS**, **GDPR**, **LGPD**: exigem controle de acesso, registros de auditoria.
* **Privileged Access**: atender requisitos de segregação de funções (SoD).

---

## 13. Boas Práticas

1. **Centralizar gerenciamento de identidade**: reduzir senhas e pontos de controle.
2. **Implementar SSO**: melhorar UX e segurança.
3. **Adotar MFA**: minimizar risco de comprometimento.
4. **Revisão periódica de roles e privilégios**.
5. **Auditoria contínua** e alertas para falhas repetidas.
6. **Automatizar provisioning** e deprovisioning.
7. **Criptografar tokens** em trânsito e repouso.
8. **Educar usuários** em boas práticas de senha e phishing.
9. **Seguir Zero Trust**: nunca confiar implicitamente.
10. **Atualizar protocolos e bibliotecas** para mitigar vulnerabilidades.

---

## 14. Conclusão

IAM é a base da segurança cibernética moderna. Ao implementar autenticação federada, autorização granular, MFA e práticas de governança, organizações fortalecem postura de segurança e melhoram experiência dos usuários.
