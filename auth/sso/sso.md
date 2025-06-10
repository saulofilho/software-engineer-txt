# Guia Completo de Single Sign‑On (SSO)

Este guia aborda, em nível avançado, o **SSO (Single Sign‑On)**: conceitos, arquiteturas, protocolos (SAML, OAuth2/OIDC, Kerberos, CAS), componentes, fluxos, implementação em aplicações e boas práticas.

---

## 1. O que é SSO?

* **Single Sign‑On** permite que um usuário se autentique uma única vez (login) e obtenha acesso a múltiplos sistemas sem nova autenticação.
* **Benefícios**:

  * Reduz fricção de login e melhora experiência do usuário.
  * Centraliza controle de identidade e políticas de segurança.
  * Facilita gerenciamento de credenciais e auditoria.

---

## 2. Componentes Principais

* **Identity Provider (IdP)**: serviço que autentica usuários e emite tokens/assertions.
* **Service Provider (SP)** / **Relying Party (RP)**: aplicações que confiam no IdP para autenticar.
* **User Agent**: normalmente um navegador ou cliente que transita tokens/assertions.
* **Tokens/Assertions**: credenciais de SSO (JWT, SAML assertion, Kerberos ticket).

---

## 3. Protocolos de SSO

### 3.1 SAML 2.0 (Security Assertion Markup Language)

* **XML‑based** para troca de autenticação/atributos.
* **Fluxo básico (Web Browser SSO)**:

  1. Usuário tenta acessar SP.
  2. SP redireciona para IdP `/SAML2/SSO/Redirect?SAMLRequest=…`.
  3. IdP autentica usuário, gera `<Assertion>` e envia ao SP via POST form.
  4. SP valida assinatura, extrai atributos e cria sessão.
* **Perfis**: Web Browser SSO, Single Logout.

### 3.2 OAuth2 + OpenID Connect

* **OIDC** adiciona autenticação ao OAuth2.
* **Authorization Code Flow** (com PKCE em SPAs): recomendado para SSO moderno.
* **JWT ID Token** carrega claims de identidade.

### 3.3 Kerberos (SPNEGO)

* **Ticket‑Granting Ticket (TGT)** e **Service Tickets**.
* **SPNEGO/GSSAPI** para SSO em ambientes corporativos (Windows AD).
* Integrado a HTTP via **Negotiate** header no navegador.

### 3.4 CAS (Central Authentication Service)

* Protocolo simples baseado em tickets.
* **Fluxo**:

  1. SP redireciona para `/cas/login?service=…`.
  2. IdP CAS autentica e gera `TGT`, depois `ST` (Service Ticket).
  3. SP valida `ST` em `/cas/serviceValidate`.

---

## 4. Fluxos de Autenticação SSO

| Protocolo       | Perfil / Flow                   | Token / Assertion            |
| --------------- | ------------------------------- | ---------------------------- |
| SAML 2.0        | Web Browser SSO                 | SAML Assertion (XML), signed |
| OAuth2 + OIDC   | Authorization Code + PKCE       | JWT ID Token + Access Token  |
| Kerberos SPNEGO | Negotiate HTTP Challenge        | Kerberos Service Ticket      |
| CAS             | Ticket‑Granting, Service Ticket | CAS Ticket                   |

---

## 5. Implementação de IdP

### 5.1 Keycloak (Open Source)

* Suporta SAML, OIDC, LDAP, Kerberos.
* **Instalação rápida via Docker**:

  ```bash
  docker run -p 8080:8080 quay.io/keycloak/keycloak:latest start-dev
  ```
* **Configurar Realm, Clients, Mappers** no console admin.

### 5.2 Okta / Auth0 / Azure AD

* Serviços SaaS com suporte SAML, OIDC.
* Configuração via dashboards para aplicativos (SP/RP).
* Gerenciamento de usuários, grupos e políticas de acesso.

---

## 6. Integração em Aplicações

### 6.1 Java (Spring Security)

#### SAML

```java
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
  @Override
  protected void configure(HttpSecurity http) throws Exception {
    http
      .authorizeRequests(a -> a.anyRequest().authenticated())
      .saml2Login();
  }
}
```

#### OIDC

```java
@Configuration
public class SecurityConfig {
  @Bean
  SecurityFilterChain springSecurityFilterChain(HttpSecurity http) throws Exception {
    http
      .authorizeRequests(a -> a.anyRequest().authenticated())
      .oauth2Login();
    return http.build();
  }
}
```

### 6.2 .NET (ASP.NET Core)

```csharp
builder.Services.AddAuthentication(options => {
  options.DefaultScheme = CookieAuthenticationDefaults.AuthenticationScheme;
  options.DefaultChallengeScheme = OpenIdConnectDefaults.AuthenticationScheme;
})
.AddCookie()
.AddOpenIdConnect();

app.UseAuthentication();
app.UseAuthorization();
```

### 6.3 Node.js (Passport.js)

```js
const passport = require('passport');
const SamlStrategy = require('passport-saml').Strategy;
passport.use(new SamlStrategy({
  path: '/login/callback',
  entryPoint: 'https://idp.example.com/sso',
  issuer: 'my-app-issuer',
  cert: fs.readFileSync('idp-public.cert', 'utf-8'),
}, (profile, done) => done(null, profile)));
```

### 6.4 JavaScript SPA (OIDC-client)

```js
import { UserManager } from 'oidc-client';
const mgr = new UserManager({
  authority: 'https://idp/', client_id: 'spa', redirect_uri: 'https://app/callback', response_type: 'code', scope: 'openid profile'
});
mgr.signinRedirect();
```

---

## 7. Single Logout (SLO)

* **SAML SLO** via redirect/POST para `/slo` endpoints.
* **OIDC RP-Initiated Logout**: RP chama `/logout?post_logout_redirect_uri=…&id_token_hint=…`.
* **CAS Logout**: `/cas/logout?service=…` para limpar sessão no SP.

---

## 8. Segurança e Considerações

1. **Validate Assertions/Tokens**: assinatura, timestamps, audience.
2. **Use HTTPS** sempre.
3. **Proteja Endpoints de Logout** contra CSRF.
4. **Gerencie Sessões**: back‑channel logout e limpeza de cookies.
5. **Configure Time Skew** mínimo para validação de timestamps.

---

## 9. Boas Práticas

1. **Escolha o protocolo** adequado ao caso de uso (SAML vs OIDC).
2. **Centralize autenticação** em um IdP confiável.
3. **Implante redundância** no IdP (cluster, alta disponibilidade).
4. **Monitore** métricas de autenticação e falhas.
5. **Audite** logs de login e SLO.
6. **Eduque** equipes sobre fluxos e segurança de SSO.

---

## 10. Conclusão

SSO melhora a experiência do usuário e consolida políticas de segurança em aplicações federadas. Dominar protocolos como SAML, OIDC e Kerberos e suas implementações garante integrações seguras e escaláveis em ambientes corporativos.
