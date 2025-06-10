# Guia Completo de OpenID Connect (OIDC)

Este guia aborda, em nível avançado, o **OpenID Connect (OIDC)** — uma camada de identidade construída sobre OAuth 2.0 — incluindo conceitos, fluxos, componentes, segurança, exemplos práticos e implementação de servidores e clientes.

---

## 1. Visão Geral

* **OpenID Connect** é um protocolo de autenticação federada que estende OAuth 2.0 para fornecer informações de identidade do usuário (ID Token) de forma segura.
* **Pilares**:

  * Baseado em **OAuth 2.0** para autorização.
  * Usa **JWT** para ID Tokens.
  * Padrões definidos pelo **OIDC** e **OpenID Foundation**.
* **Objetivos**:

  1. Autenticar usuários (quem eles são).
  2. Obter perfil de usuário (claims).
  3. Integrar login único (SSO) em múltiplas aplicações.

---

## 2. Componentes Principais

* **Relying Party (RP)**: aplicação cliente que confia no provedor OIDC.
* **OpenID Provider (OP)**: servidor de autorização que implementa OIDC (ex: Keycloak, Auth0, Azure AD).
* **Discovery Endpoint**: `/.well-known/openid-configuration` fornece metadados do OP.
* **Authorization Endpoint**: inicia fluxo de autorização.
* **Token Endpoint**: troca código por tokens.
* **UserInfo Endpoint**: retorna informações adicionais do usuário.
* **JWKS Endpoint**: expõe chaves públicas para verificar tokens.

---

## 3. Fluxos de Autenticação

### 3.1 Authorization Code Flow (Recomendado)

1. RP redireciona usuário:

   ```text
   GET /authorize?
     response_type=code
     &client_id={client_id}
     &redirect_uri={redirect_uri}
     &scope=openid profile email
     &state={state}
     &nonce={nonce}
   ```
2. OP autentica usuário e obtém consentimento.
3. OP redireciona para `redirect_uri?code={code}&state={state}`.
4. RP faz POST a `/token`:

   ```http
   POST /token
   grant_type=authorization_code
   &code={code}
   &redirect_uri={redirect_uri}
   Authorization: Basic base64(client_id:client_secret)
   ```
5. OP retorna JSON com `access_token`, `id_token`, `refresh_token`.
6. RP valida `id_token` (signature, `iss`, `aud`, `nonce`, `exp`).
7. RP opcionalmente chama `/userinfo` com `access_token` para claims adicionais.

### 3.2 Hybrid Flow

* Combina código e tokens flow: `response_type=code id_token token`.
* Permite obter tokens sem chamada a `/token`, mas menos recomendado.

### 3.3 Implicit Flow *\[Depreciado]*

* Fluxo antigo para SPAs: `response_type=id_token token`, mas não recomendado — prefira Code+PKCE.

---

## 4. Tokens e Claims

### 4.1 ID Token (JWT)

* **Campos (claims) básicos**:

  * `iss`: issuer.
  * `sub`: subject (identifier do usuário).
  * `aud`: audience (client\_id).
  * `exp`, `iat`, `auth_time`.
  * `nonce`: prevenção de replay.
* **Scope `openid`** é obrigatório.
* **Claims opcionais**: `name`, `email`, `picture`, `updated_at`, definidos em `profile`, `email` scopes.

### 4.2 Access Token

* Credencial para acessar recursos (Resource Server/API).
* Formato tipicamente **opaque** ou **JWT** (depende do OP).

### 4.3 Refresh Token

* Usado para obter novos access e id tokens sem reautenticar o usuário.
* Deve ser armazenado com segurança (HttpOnly cookie ou secure storage).

---

## 5. Inline OIDC (Discovery & JWKS)

* **Discovery**: RP obtém configurações automaticamente:

  ```json
  GET /.well-known/openid-configuration
  ```

* Importante campos:

  * `authorization_endpoint`, `token_endpoint`, `userinfo_endpoint`, `jwks_uri`.
  * Algoritmos suportados (`id_token_signing_alg_values_supported`).

* **JWKS**: JSON Web Key Set para validar signatures:

  ```json
  GET /.well-known/jwks.json
  ```

---

## 6. Segurança e Melhores Práticas

1. **TLS obrigatório** para todos endpoints.
2. **Validation de ID Token**: verificar assinatura, `iss`, `aud`, `nonce` e tempo de expiração.
3. **PKCE** para Authorization Code Flow em SPAs e clientes públicos.
4. **Param `state`** para proteção CSRF.
5. **Scope Mínimo**: solicitar apenas scopes necessários.
6. **Proteção de Refresh Tokens**: revogação e rotação periódica.
7. **Token Revocation & Introspection**: implementar endpoints RFC 7009 e 7662.

---

## 7. Exemplo de Implementação de OP com Keycloak

1. **Instalar Keycloak** via Docker:

   ```bash
   docker run -p 8080:8080 -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin quay.io/keycloak/keycloak:latest start-dev
   ```
2. **Criar Realm** e **Client** no Console Admin.
3. **Configurar Client**:

   * Access Type: `confidential` para apps server-side (com client secret), `public` para SPAs.
   * Valid Redirect URIs.
   * Scopes: `openid`, `profile`, `email`.
4. **Endpoints** disponíveis:

   * `http://localhost:8080/realms/{realm}/.well-known/openid-configuration`

---

## 8. Exemplo de Cliente OIDC em ASP.NET Core

```csharp
// appsettings.json
"OIDC": {
  "Authority": "https://auth.example.com/realms/demo",
  "ClientId": "myclient",
  "ClientSecret": "secret",
  "ResponseType": "code",
  "SaveTokens": true,
  "Scope": ["openid", "profile", "email", "api.read"]
}

// Program.cs
builder.Services.AddAuthentication(options => {
    options.DefaultScheme = CookieAuthenticationDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = OpenIdConnectDefaults.AuthenticationScheme;
})
.AddCookie()
.AddOpenIdConnect(options => {
    var oidc = builder.Configuration.GetSection("OIDC");
    options.Authority = oidc["Authority"];
    options.ClientId = oidc["ClientId"];
    options.ClientSecret = oidc["ClientSecret"];
    options.ResponseType = oidc["ResponseType"];
    options.SaveTokens = true;
    options.Scope.Clear();
    foreach (var scope in builder.Configuration.GetSection("OIDC:Scope").Get<string[]>())
        options.Scope.Add(scope);
});

app.UseAuthentication();
app.UseAuthorization();

app.MapGet("/secure", [Authorize] () => Results.Ok("Olá, usuário autenticado!"));
```

---

## 9. Exemplo de Cliente OIDC em React (OIDC-client)

```bash
npm install oidc-client
```

```js
import { UserManager } from 'oidc-client';

const config = {
  authority: 'https://auth.example.com/realms/demo',
  client_id: 'spa-client',
  redirect_uri: 'http://localhost:3000/callback',
  response_type: 'code',
  scope: 'openid profile email api.read',
  post_logout_redirect_uri: 'http://localhost:3000/',
};

const userManager = new UserManager(config);

// Iniciar login
document.getElementById('login').onclick = () => userManager.signinRedirect();

// Callback Handling
userManager.signinRedirectCallback().then(user => {
  console.log('Usuário:', user.profile);
});
```

---

## 10. Integração com OpenID Connect Profiles

* **OIDC Discovery** em clientes: `userManager.getSettings()` usa discovery.
* **Dynamic Client Registration** (RFC 7591) para registrar clientes em runtime.
* **Back-Channel Logout** (RFC 7009) e **Front-Channel Logout** (OIDC RP-Initiated Logout).

---

## 11. Testes e Ferramentas

* **Testes de Compliance**: OpenID Conformance Test Suite.
* **OIDC Debuggers**: jwt.io, Postman.
* **Bibliotecas**: `oidc-provider` (Node.js), `Authlib` (Python), `Microsoft.Identity` (.NET).

---

## 12. Conclusão

OpenID Connect é o padrão de autenticação federada para aplicações modernas, oferecendo um protocolo leve, extensível e seguro para login único e gerenciamento de identidade. Dominar seus fluxos, endpoints e práticas de segurança garante integrações consistentes e proteções robustas em arquiteturas distribuídas.
