# 🛡️ WAF (Web Application Firewall)

Um **WAF** protege aplicações web ao filtrar e monitorar o tráfego HTTP/HTTPS entre usuários e aplicações.

## 🔐 Protege Contra:
- Injeção SQL (SQL Injection)
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Inclusão de arquivos remotos (RFI)
- Exploração de falhas do protocolo HTTP
- Ataques de dia zero (em alguns casos)

## ⚙️ Como Funciona:
1. **Inspeção de Requisições**: Analisa cabeçalhos, corpo e parâmetros de cada requisição.
2. **Comparação com Regras**: Usa regras baseadas em assinaturas ou comportamentos.
3. **Ação**: Pode permitir, bloquear ou desafiar a requisição (ex: CAPTCHA).
4. **Registro e Alertas**: Gera logs e alertas para análise e resposta.

## 🧠 Tipos de WAF
- **Baseado em Rede**: Appliance físico, alta performance.
- **Baseado em Host**: Instalado no servidor da aplicação.
- **Baseado em Nuvem (SaaS)**: Fácil de escalar e gerenciado por terceiros.

## 🔄 Diferenças: WAF vs Firewall Tradicional

| Característica       | WAF                         | Firewall Tradicional        |
|----------------------|-----------------------------|------------------------------|
| Camada de atuação    | Aplicação (HTTP/HTTPS)      | Rede (IP/TCP/UDP)            |
| Entende HTTP/S?      | Sim                         | Não                          |
| Protege contra XSS/SQLi? | Sim                     | Não                          |

## 🧰 Soluções Populares
- **Cloud**:
  - Cloudflare WAF
  - AWS WAF
  - Azure Web Application Firewall
  - Imperva Cloud WAF

- **Self-hosted**:
  - ModSecurity (Apache, NGINX, IIS)
  - NAXSI (para NGINX)

---

> Um WAF é essencial para proteger APIs e aplicações web modernas contra ameaças comuns e vulnerabilidades conhecidas.
