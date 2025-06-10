# Guia Completo de OAuth 2.0

Este documento apresenta, em nível avançado, todos os aspectos essenciais do **OAuth 2.0**: conceitos, fluxos de autorização, componentes, segurança, exemplos práticos e implementação de servidor e cliente.

---

## 1. Conceitos Fundamentais

* **OAuth 2.0** é um protocolo de autorização que permite que aplicações de terceiros obtenham acesso limitado a recursos protegidos em nome de um usuário, sem expor credenciais (usuário/senha).
* **Terminologia**:

  * **Resource Owner**: usuário que possui dados.
  * **Client**: aplicação que solicita autorização.
  * **Authorization Server**: emite tokens após autenticação e consentimento.
  * **Resource Server**: API que protege recursos e valida tokens.
  * **Access Token**: credencial de acesso a recursos.
  * **Refresh Token**: usado para obter novos access tokens sem intervenção do usuário.
  * **Scopes**: delimitam permissões solicitadas.

---

## 2. Fluxos (Grant Types)

### 2.1 Authorization Code (com PKCE para clientes públicos)

1. Cliente redireciona Resource Owner para `/authorize?response_type=code&client_id=...&redirect_uri=...&scope=...&code_challenge=...&code_challenge_method=S256`.
2. Usuário autentica e consente.
3. Authorization Server redireciona para `redirect_uri?code=...`.
4. Cliente troca código por token em `/token` com `grant_type=authorization_code`, incluindo `code_verifier` (PKCE).

**PKCE** (Proof Key for Code Exchange) previne interceptação de código em clientes móveis/SPAs públicos.

### 2.2 Client Credentials

* Fluxo máquina-a-máquina.
* Cliente usa `grant_type=client_credentials` em `/token`.
* Obtém access token sem usuário.

### 2.3 Resource Owner Password Credentials (ROPC) *\[Desencorajado]*

* Cliente obtém nome e senha do usuário e envia a `/token` com `grant_type=password`.
* Deve ser evitado, pois expõe credenciais.

### 2.4 Implicit Flow *\[Obsoleto]*

* Sem code exchange (uso direto de token no redirect).
* Substituído por Authorization Code + PKCE.

### 2.5 Device Authorization Grant (Device Flow)

* Para dispositivos sem browser: cliente apresenta `user_code` e `verification_uri`.
* Usuário autoriza em outro dispositivo; cliente polled `/token` com `grant_type=urn:ietf:params:oauth:grant-type:device_code`.

---

## 3. Endpoints Padrão

* **Authorization Endpoint**: recebe requests de autorização (`/authorize`).
* **Token Endpoint**: troca código por token e renova tokens (`/token`).
* **Revocation Endpoint** (RFC 7009): revoga tokens (`/revoke`).
* **Introspection Endpoint** (RFC 7662): validação de token (`/introspect`).
* **UserInfo Endpoint** (OpenID Connect): fornece dados do usuário autenticado.

---

## 4. Access Tokens e Formatos

* **Bearer Tokens**: formato simples, enviado no header: `Authorization: Bearer <token>`.
* **JWT Access Tokens**:

  * Contêm `iss`, `sub`, `aud`, `exp`, `iat`, `scope`.
  * Assinados (HS256, RS256).

**Exemplo de JWT payload**:

```json
{
  "iss":"https://auth.example.com/",  
  "sub":"user123",               
  "aud":"api.example.com",       
  "exp":1700000000,               
  "scope":"read write"
}
```

---

## 5. Segurança e Melhores Práticas

1. **Usar TLS** para todos endpoints.
2. **Implementar PKCE** para Authorization Code.
3. **Configurar `redirect_uri` exatas** (não curingas).
4. **Escopos mínimos necessários** (princípio de menor privilégio).
5. **Short-lived tokens** e uso de **refresh tokens** com revogação.
6. **Revoke** e **introspect** tokens inválidos ou comprometidos.
7. **Proteção contra CSRF** no fluxo de autorização (`state` parameter).
8. **Armazenar tokens** com segurança no cliente (HttpOnly cookies para web apps, armazenamento protegido em mobile).

---

## 6. Exemplo de Servidor OAuth 2.0 com Node.js (Express)

```js
const express = require('express');
const OAuth2Server = require('oauth2-server');
const app = express();

app.oauth = new OAuth2Server({
  model: require('./model.js'),
  allowBearerTokensInQueryString: true,
  accessTokenLifetime: 3600,
});

app.post('/token', app.oauth.token());
app.get('/secure', app.oauth.authenticate(), (req, res) => {
  res.json({ message: 'Acesso liberado', user: req.user });
});

app.listen(3000);
```

* **Model.js** implementa interface para `getClient`, `saveToken`, `getAccessToken`, `getUser`.

---

## 7. Exemplo de Cliente OAuth 2.0 em Python (Requests)

```python
import requests
from urllib.parse import urlencode

# Parâmetros
client_id = 'my-client'
redirect_uri = 'https://app.example.com/callback'
auth_endpoint = 'https://auth.example.com/authorize'
token_endpoint = 'https://auth.example.com/token'

# 1. Redirect user to authorization URL
auth_url = f"{auth_endpoint}?{urlencode({'response_type':'code','client_id':client_id,'redirect_uri':redirect_uri,'scope':'read write','state':'xyz'})}"
print('Visite:', auth_url)

# 2. After redirect with code, exchange for token
code = input('Digite o code: ')
resp = requests.post(token_endpoint, data={
    'grant_type':'authorization_code', 'code':code,
    'redirect_uri':redirect_uri,
}, auth=(client_id, 'client-secret'))
print('Token:', resp.json())
```

---

## 8. Frameworks e Bibliotecas

| Plataforma  | Servidor OAuth 2.0           | Cliente OAuth 2.0              |
| ----------- | ---------------------------- | ------------------------------ |
| **Node.js** | oauth2-server, oidc-provider | simple-oauth2, passport-oauth2 |
| **Python**  | oauthlib, Authlib            | requests-oauthlib, Authlib     |
| **Java**    | Spring Authorization Server  | Spring Security OAuth          |
| **.NET**    | IdentityServer4, OpenIddict  | Microsoft.Identity.Web         |
| **Go**      | go-oauth2                    | oauth2 (golang.org/x/oauth2)   |

---

## 9. Integração com OpenID Connect

* **OIDC** estende OAuth 2.0 para autenticação (login).
* Usa **ID Token** (JWT) com claims `iss`, `sub`, `aud`, `exp`, `nonce`.
* Define endpoints adicionais: `/userinfo`, `/.well-known/openid-configuration`.

---

## 10. Testes e Ferramentas

* **Fuzzers**: testam endpoints de OAuth (e.g., Hydra Fuzzer).
* **Postman / Insomnia**: suporte a OAuth 2.0 flows para testes manuais.
* **Compliance Tools**: OAuth2.0 RFC Compliance Tester.

---

## Conclusão

OAuth 2.0 é o padrão de fato para autorização em aplicações modernas. Compreender seus fluxos, endpoints e melhores práticas de segurança (PKCE, TLS, scoping) é essencial para proteger APIs e experiências de usuário seguras em diversos clientes e plataformas.
