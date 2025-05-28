# 🌐 DNS (Domain Name System)

O **DNS (Domain Name System)** é o sistema responsável por traduzir nomes de domínios legíveis por humanos (como `exemplo.com`) em endereços IP compreensíveis por máquinas (como `192.0.2.1`).

---

## 🔁 Como Funciona o DNS

1. **Usuário digita um domínio** no navegador (ex: `www.exemplo.com`).
2. **Consulta ao DNS** é feita para descobrir o IP correspondente.
3. **Servidores DNS** resolvem a consulta:
   - **DNS Recursivo**: Recebe a solicitação e procura a resposta.
   - **DNS Root**: Informa qual servidor autoritativo deve ser consultado.
   - **Servidor TLD**: Indica o servidor autoritativo do domínio de topo (como `.com`).
   - **Servidor Autoritativo**: Retorna o IP final.
4. **IP é retornado** ao navegador, que conecta ao servidor do site.

---

## 📦 Tipos de Registros DNS

| Tipo   | Descrição                                  | Exemplo                          |
|--------|--------------------------------------------|----------------------------------|
| `A`    | Aponta um domínio para um IP (IPv4)        | `exemplo.com → 192.0.2.1`        |
| `AAAA` | Aponta para um IP IPv6                     | `exemplo.com → 2001:db8::1`      |
| `CNAME`| Aponta um domínio para outro domínio       | `www.exemplo.com → exemplo.com`  |
| `MX`   | Define servidores de e-mail do domínio      | `mail.exemplo.com`               |
| `TXT`  | Texto livre (SPF, verificação de domínio)  | `v=spf1 include:_spf.google.com` |
| `NS`   | Indica quais servidores respondem pelo DNS | `ns1.exemplo.com`                |
| `SRV`  | Usado para serviços específicos (VoIP, etc) |                                  |
| `PTR`  | Usado para DNS reverso (IP → domínio)      |                                  |

---

## ⏱️ Tempo de Vida (TTL)

Cada registro DNS tem um **TTL (Time To Live)** que determina por quanto tempo ele pode ser armazenado em cache. Valores comuns: 300 segundos (5 minutos), 3600 segundos (1 hora).

---

## 🧠 Tipos de Servidores DNS

- **Recursivo**: Resolve a consulta completa para o cliente.
- **Autoritativo**: Contém os registros finais e responde pelas zonas do domínio.
- **Root**: Primeira etapa de uma resolução DNS, aponta para TLDs.

---

## 🧰 Ferramentas e Comandos DNS

- `dig exemplo.com` – Consulta DNS detalhada.
- `nslookup exemplo.com` – Consulta simples.
- `host exemplo.com` – Retorna registros DNS.
- Ferramentas online: DNS Checker, Google Dig Tool.

---

## ☁️ Provedores de DNS Populares

- **Públicos**:
  - Google DNS: `8.8.8.8`, `8.8.4.4`
  - Cloudflare: `1.1.1.1`
  - OpenDNS: `208.67.222.222`

- **Gerenciadores de zona DNS**:
  - AWS Route 53
  - Cloudflare DNS
  - GoDaddy, Namecheap
  - DigitalOcean DNS

---

> O DNS é essencial para o funcionamento da internet moderna. Sem ele, você teria que memorizar endereços IP para acessar sites!
