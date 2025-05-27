# Guia Completo de JSON Web Tokens (JWT)

Este documento aborda, em nível avançado, todos os aspectos essenciais de JSON Web Tokens (JWT): definição, estrutura, algoritmos, fluxos de uso, exemplos práticos, práticas de segurança e considerações avançadas.

---

## 1. O que é JWT?

JSON Web Token (JWT) é um padrão aberto (RFC 7519) que define um método compacto e auto-contido para representar informações transferidas entre partes como um objeto JSON. Essas informações podem ser verificadas e confiáveis porque são digitalmente assinadas.

* **Compacto**: cabe em URLs, parâmetros POST ou dentro de cabeçalhos HTTP.
* **Auto-contido**: contém todas as informações necessárias sobre o usuário (claims), evitando consultas adicionais ao banco de dados.

Usos comuns:

* Autenticação sem estado (stateless) em APIs RESTful.
* Autorização: controle de acesso baseado em roles e permissões.

---

## 2. Estrutura de um JWT

Um JWT é composto por três partes separadas por pontos (`.`):

```
<header>.<payload>.<signature>
```

1. **Header** (Cabeçalho)
2. **Payload** (Corpo / Claims)
3. **Signature** (Assinatura)

### 2.1 Header

* Declara o tipo do token (JWT) e o algoritmo de assinatura usado (p.ex. HMAC SHA256 ou RSA).

```json
{
  "alg": "HS256",  
  "typ": "JWT"
}
```

* Serializado em JSON e codificado em Base64Url.

### 2.2 Payload (Claims)

Contém as declarações (claims) — pares chave-valor — que carregam informações sobre a entidade (usuário) e outros metadados.

**Tipos de Claims**:

* **Registered** (padrão): `iss`, `sub`, `aud`, `exp`, `nbf`, `iat`, `jti`.
* **Public**: registrado em IANA JSON Web Token Claims Registry ou acordado entre sistemas. Ex: `email`, `role`.
* **Private**: customizadas entre emissor e consumidor.

```json
{
  "sub": "1234567890",
  "name": "Guilherme Prado",
  "admin": true,
  "iat": 1615159072,
  "exp": 1615162672
}
```

* Codificado em Base64Url.

### 2.3 Signature

Calculada para verificar a integridade do token:

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

Para RSA/ECDSA:

```text
RSASHA256(
  data, privateKey
)
```

* A assinatura garante que o token não foi alterado e, no caso de algoritmos assimétricos, que vem de uma fonte confiável.

---

## 3. Algoritmos de Assinatura

| Sigla | Tipo                 | Descrição                                                            |
| ----- | -------------------- | -------------------------------------------------------------------- |
| HS256 | Symmetric (HMAC)     | HMAC + SHA-256. Rápido, usa segredo compartilhado.                   |
| HS384 | Symmetric (HMAC)     | HMAC + SHA-384.                                                      |
| HS512 | Symmetric (HMAC)     | HMAC + SHA-512.                                                      |
| RS256 | Asymmetric (RSA)     | SHA-256 com RSA. Usa par chave pública/privada.                      |
| RS384 | Asymmetric (RSA)     | SHA-384 com RSA.                                                     |
| RS512 | Asymmetric (RSA)     | SHA-512 com RSA.                                                     |
| ES256 | Asymmetric (ECDSA)   | SHA-256 com ECDSA. Chaves menores, eficiente em dispositivos móveis. |
| PS256 | Asymmetric (RSA-PSS) | RSA-PSS + SHA-256. Segurança adicional contra certos ataques em RSA. |

---

## 4. Fluxos de Autenticação com JWT

### 4.1 Login / Emissão do Token

1. Usuário envia credenciais (usuário/senha) para `/login`.
2. Servidor valida credenciais.
3. Em caso de sucesso, servidor gera um JWT com claims apropriados (
   `sub`, `iat`, `exp`, roles, etc.).
4. Retorna o token ao cliente (JSON response ou cookie HTTP-only).

```json
// Exemplo de resposta JSON
{
  "access_token": "eyJhbGci...",
  "token_type": "Bearer"
}
```

### 4.2 Armazenamento no Cliente

* **LocalStorage / SessionStorage**: fácil acesso no frontend, mas vulnerável a XSS.
* **Cookies HTTP-only**: mais seguro contra XSS, mas vulnerável a CSRF sem medidas adicionais (SameSite).

### 4.3 Autorização em Requisições

* Cliente inclui o JWT no cabeçalho `Authorization`:

```
Authorization: Bearer <token>
```

* Servidor extrai e valida a assinatura, checa `exp` e outros claims (`aud`, `iss`).
* Concede ou nega acesso com base nas permissões no `payload`.

### 4.4 Refresh Tokens

Para manter sessões longas sem expor o access token:

1. Emite `access_token` (curta validade) e `refresh_token` (longa validade).
2. Quando `access_token` expira, cliente faz requisição a `/refresh` enviando o `refresh_token`.
3. Servidor valida o `refresh_token` e emite novos tokens.

* **Armazenamento**: `refresh_token` deve ser guardado com segurança (cookie HTTP-only).
* **Regras**: usar blacklist/revogar se for necessário encerrar sessão.

---

## 5. Exemplos Práticos

### 5.1 Node.js com `jsonwebtoken`

```js
const jwt = require('jsonwebtoken');
const secret = process.env.JWT_SECRET;

// Gerar token
function generateToken(payload) {
  return jwt.sign(payload, secret, { algorithm: 'HS256', expiresIn: '1h' });
}

// Verificar token
function verifyToken(token) {
  try {
    return jwt.verify(token, secret);
  } catch (err) {
    throw new Error('Token inválido');
  }
}
```

### 5.2 Python com `PyJWT`

```py
import jwt
from datetime import datetime, timedelta

SECRET = 'seusegredo'

def create_token(user_id):
    now = datetime.utcnow()
    payload = {
        'sub': user_id,
        'iat': now,
        'exp': now + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET, algorithm='HS256')


def decode_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise Exception('Token expirado')
```

### 5.3 C# (.NET) com `System.IdentityModel.Tokens.Jwt`

```csharp
var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secret));
var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

var tokenDescriptor = new SecurityTokenDescriptor
{
    Subject = new ClaimsIdentity(new[] {
        new Claim(JwtRegisteredClaimNames.Sub, userId),
        new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
    }),
    Expires = DateTime.UtcNow.AddHours(1),
    SigningCredentials = credentials
};

var tokenHandler = new JwtSecurityTokenHandler();
var token = tokenHandler.CreateToken(tokenDescriptor);
var tokenString = tokenHandler.WriteToken(token);
```

---

## 6. Práticas de Segurança

1. **Use HTTPS** para evitar interceptação de tokens.
2. **Expire tokens rapidamente** (curta duração) e use refresh tokens.
3. **Proteja secret keys** em variáveis de ambiente ou vaults.
4. **Valide** todos os claims relevantes: `exp`, `nbf`, `iss`, `aud`.
5. **Não armazene informações sensíveis** (senhas, PII) no payload.
6. **Proteja contra XSS/CSRF** dependendo do método de armazenamento.
7. **Rotacione** e revogue keys/refresh tokens se necessário (lista negra).

---

## 7. Considerações Avançadas

### 7.1 JWE: Tokens Criptografados

* JSON Web Encryption (JWE) permite criptografar o conteúdo do JWT, garantindo confidencialidade.
* Formato: five partes: `header.encryptedKey.iv.ciphertext.tag`.

### 7.2 JWK: JSON Web Key

* Padrão para representar chaves públicas/privadas em JSON.
* Permite distribuição de chaves públicas via endpoint `/.well-known/jwks.json`.

### 7.3 Manipulação de Claims Dinâmicas

* **Roles/Permissions**: incluir arrays de permissões e checar no middleware.
* **Multitenancy**: claim `tenant_id` e scopo de acesso.

### 7.4 Algoritmos de Assinatura `none`

* **Nunca** use `alg: none`. Incluir validação estrita de algoritmo.

---

### Conclusão

JWT é uma ferramenta poderosa para autenticação e autorização sem estado. Compreender sua estrutura, mecanismos de assinatura e práticas de segurança é essencial para implementações seguras e escaláveis.
