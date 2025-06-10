# Guia Completo de Cybersecurity

Este guia aborda, em nível avançado, o **cybersecurity** (segurança da informação e cibernética), cobrindo conceitos fundamentais, ameaças, frameworks, controles técnicos e administrativos, além de práticas recomendadas para proteger ativos digitais.

---

## 1. Introdução e Objetivos

* **Definição**: conjunto de práticas e tecnologias para proteger sistemas, redes e dados contra acessos não autorizados, ataques e vulnerabilidades.
* **Objetivos principais (CIA)**:

  * **Confidencialidade**: garantir que informação seja acessível apenas a quem autorizado.
  * **Integridade**: assegurar que dados não sejam alterados de forma não autorizada.
  * **Disponibilidade**: manter sistemas e dados acessíveis quando necessário.

---

## 2. Conceitos e Terminologia

| Termo               | Descrição                                                          |
| ------------------- | ------------------------------------------------------------------ |
| **Vetor de Ameaça** | Modo pelo qual um atacante explora vulnerabilidade.                |
| **Vulnerabilidade** | Fraqueza em sistema que pode ser explorada.                        |
| **Exploit**         | Código ou técnica que aproveita vulnerabilidade.                   |
| **Malware**         | Software malicioso (vírus, trojan, ransomware).                    |
| **APT**             | Ameaça Persistente Avançada: ataque prolongado e direcionado.      |
| **Phishing**        | Engenharia social via e-mail ou sites falsos.                      |
| **Zero Trust**      | Modelo de segurança que não confia em nada dentro ou fora da rede. |

---

## 3. Panorama de Ameaças

* **Malware**: vírus, worms, trojans, ransomware, spyware.
* **Ataques de rede**: DDoS, Man-in-the-Middle, ARP Poisoning.
* **Aplicações Web**: injeção SQL, XSS, CSRF, deserialização insegura.
* **Engenharia Social**: phishing, spear-phishing, BEC (Business Email Compromise).
* **Insider Threats**: colaboradores mal-intencionados ou descuidados.
* **Ameaças emergentes**: ataques a IoT, cadeia de suprimentos (supply chain), deepfakes.

---

## 4. Frameworks e Normas

* **ISO/IEC 27001**: sistema de gestão de segurança da informação (SGSI).
* **NIST Cybersecurity Framework (CSF)**: identificar, proteger, detectar, responder, recuperar.
* **CIS Controls**: 20 controles críticos para defesa cibernética.
* **PCI DSS**: segurança de dados de cartões de pagamento.
* **LGPD e GDPR**: proteção de dados pessoais e privacidade.

---

## 5. Gestão de Riscos

1. **Identificação**: mapear ativos, ameaças e vulnerabilidades.
2. **Avaliação**: análise qualitativa e quantitativa de risco (probabilidade × impacto).
3. **Tratamento**: mitigação (controles), transferência (seguros), aceitação, eliminação.
4. **Monitoramento**: revisar métricas e indicadores de risco (KRIs).

---

## 6. Arquitetura de Segurança

* **Defesa em Profundidade**: múltiplas camadas de controles (perímetro, rede, host, aplicação).
* **Zonificação**: segmentação de rede (VLANs, DMZs).
* **Zero Trust**: autenticar e autorizar sempre, princípio do menor privilégio.
* **Segurança em Camadas**: física, lógica, aplicações, dados.

---

## 7. Segurança de Redes

* **Firewalls** (stateful, WAF) para filtrar tráfego.
* **IDS/IPS**: detectar e prevenir intrusões.
* **VPN e TLS**: criptografia de trânsito.
* **Segmentação**: ACLs, microsegmentação (SDN).
* **Network Access Control (NAC)**: controlar dispositivos na rede.

---

## 8. Segurança de Aplicações

* **OWASP Top 10**: injeção, autenticação quebrada, XSS, exposição de dados sensíveis etc.
* **SAST/DAST**: análise estática e dinâmica de código.
* **DevSecOps**: integrar segurança no ciclo CI/CD.
* **Review de Código Seguro**: checklists e pair programming.

---

## 9. Criptografia

* **Simétrica** (AES, DES) e **Assimétrica** (RSA, ECC).
* **Hashing**: SHA-2/3, bcrypt, Argon2 para senhas.
* **PKI**: certificados x.509, autoridade certificadora (CA).
* **TLS/HTTPS**: proteger comunicação web.
* **Encriptação de Dados em Repouso**: EFS, BitLocker, criptografia de disco.

---

## 10. Gestão de Identidade e Acesso (IAM)

* **Autenticação Multifator (MFA)**: TOTP, U2F.
* **Single Sign-On (SSO)**: SAML, OAuth2/OIDC.
* **RBAC/ABAC**: controle de acesso baseado em papéis ou atributos.
* **Privileged Access Management (PAM)**: cofre de credenciais sensíveis.

---

## 11. Segurança em Cloud

* **Shared Responsibility Model**: divisão de responsabilidades CSP vs cliente.
* **CSPM**: Cloud Security Posture Management para detectar configurações inseguras.
* **CASB**: Cloud Access Security Broker para controlar uso de SaaS.
* **Segurança de Containers**: image scanning, runtime protection, Kubernetes RBAC.

---

## 12. Monitoramento e Detecção

* **SIEM**: agregação de logs, correlação de eventos (Splunk, ELK, QRadar).
* **SOAR**: orquestração e automação de resposta a incidentes.
* **Threat Intelligence**: feeds de IOC (Indicators of Compromise).
* **CTI**: análise proativa de ameaças.

---

## 13. Resposta a Incidentes e Forense

1. **Plano de Resposta**: playbooks e times (CSIRT/CERT).
2. **Detecção e Contenção**: isolar sistemas, recolher evidências.
3. **Erradicação e Recuperação**: eliminar malware, restaurar backups.
4. **Análise Forense**: coleta de artefatos, timeline, relatório.

---

## 14. Conformidade e Auditoria

* **Auditorias Internas/Externas**: pentests, fuzzing, compliance reviews.
* **Certificações**: ISO 27001, SOC 2, PCI DSS.
* **Governança**: políticas, procedimentos, treinamento.

---

## 15. Boas Práticas e Recomendações

1. **Atualizações e Patch Management**: processos automatizados.
2. **Backup e Disaster Recovery**: testes regulares de restauração.
3. **Treinamento e Conscientização**: phishing simulado, CTFs internos.
4. **Red Team/Blue Team**: exercícios de adversarial e defesa.
5. **Segurança por Design (PbD)**: incorporar requisitos de segurança desde o início.

---

## 16. Conclusão

A segurança cibernética é uma disciplina multidisciplinar que exige abordagem integrada de pessoas, processos e tecnologia. Implementar controles robustos, manter vigilância contínua e evoluir com as ameaças é fundamental para proteger ativos e minimizar riscos.
