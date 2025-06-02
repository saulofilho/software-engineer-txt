# Arquiteturas de Software

---

### **1. Monolítica**

- Toda a aplicação é um único bloco (código, lógica de negócios, banco, interface juntos).
- Ex: aplicações legadas ou simples.

---

### **2. Arquitetura em Camadas (Layered Architecture)**

- Divide o sistema em camadas (ex: apresentação, lógica, persistência).
- Muito usada em sistemas corporativos.

---

### **3. Arquitetura Orientada a Serviços (SOA - Service-Oriented Architecture)**

- Organiza o software como um conjunto de serviços reutilizáveis.
- Comunicação via mensagens padronizadas (SOAP, XML, etc.).

---

### **4. Microservices**

- Divide a aplicação em serviços pequenos, independentes, que se comunicam via APIs.
- Escalável, modular e ideal para DevOps e CI/CD.

---

### **5. Event-Driven (Baseada em Eventos)**

- Componentes reagem a eventos (mensagens, alterações, etc.).
- Muito usada em sistemas distribuídos e reativos.

---

### **6. Arquitetura em Barramento (ESB - Enterprise Service Bus)**

- Usa um barramento de comunicação central para interligar sistemas.
- Comum em grandes empresas com múltiplos sistemas legados.

---

### **7. Serverless**

- Código executado em funções independentes (FaaS).
- Escalável e com baixo custo operacional (ex: AWS Lambda, Azure Functions).

---

### **8. Arquitetura Orientada a Componentes**

- O sistema é composto por componentes reutilizáveis.
- Cada componente tem uma interface bem definida.

---

### **9. Arquitetura em Malha (Mesh Architecture)**

- Foco em comunicação entre serviços, com controle de tráfego, segurança e observabilidade (ex: Service Mesh com Istio).

---

### **10. Arquitetura Hexagonal (Ports and Adapters)**

- Núcleo da aplicação isolado da interface e infraestrutura.
- Facilita testes e substituição de tecnologias.

---

### **11. Arquitetura Limpa (Clean Architecture)**

- Separação rigorosa de responsabilidades com foco em independência de frameworks e UI.
- Inspirada por Uncle Bob (Robert C. Martin).

---

### **12. Arquitetura de Microsserviços Baseada em Domínio (DDD + Microservices)**

- Divide os microsserviços com base nos **Bounded Contexts** do DDD (Domain-Driven Design).

---

### **Tabela de Arquiteturas de Software**

| Arquitetura | Descrição | Vantagens | Desvantagens | Casos de uso comuns |
| --- | --- | --- | --- | --- |
| **Monolítica** | Toda a aplicação está num único bloco de código. | Simples de desenvolver e implantar. | Difícil de escalar e manter à medida que cresce. | Apps pequenos ou MVPs. |
| **Camadas (Layered)** | Divisão em camadas como UI, lógica, dados. | Separação de responsabilidades, organização. | Acoplamento entre camadas pode crescer. | Sistemas corporativos clássicos. |
| **SOA (Service-Oriented)** | Conjunto de serviços reutilizáveis que se comunicam via mensagens. | Reutilização e integração com legados. | Complexidade de orquestração, overhead de comunicação. | Grandes empresas com sistemas legados. |
| **Microservices** | App dividida em serviços pequenos e independentes. | Alta escalabilidade, deploys independentes. | Complexidade de gerenciamento, latência entre serviços. | Sistemas escaláveis como Netflix, Uber. |
| **Event-Driven** | Componentes reagem a eventos (pub/sub ou stream). | Alto desacoplamento, reativo, assíncrono. | Debug e rastreamento de eventos são mais difíceis. | E-commerces, IoT, sistemas reativos. |
| **ESB (Barramento de Serviços)** | Comunicação via barramento central entre sistemas. | Integração robusta entre sistemas heterogêneos. | Pode virar um "single point of failure" e gargalo. | Corporações com muitos sistemas internos. |
| **Serverless (FaaS)** | Funções executadas sob demanda na nuvem. | Escala automática, sem gerenciar servidores. | Cold start, dependência do provedor, difícil teste local. | APIs simples, automações, backends leves. |
| **Componentes (Component-Based)** | Aplicação montada a partir de componentes independentes. | Reutilização, manutenção facilitada. | Definir interfaces bem claras pode ser complexo. | Softwares modulares, UIs reutilizáveis. |
| **Service Mesh** | Camada de infraestrutura para comunicação entre microsserviços. | Segurança, observabilidade, controle de tráfego embutidos. | Curva de aprendizado alta, complexidade de configuração. | Kubernetes com muitos microsserviços. |
| **Hexagonal (Ports & Adapters)** | Núcleo de domínio isolado de infraestrutura. | Fácil de testar e manter, desacoplamento forte. | Mais trabalho inicial para estruturar corretamente. | Apps com necessidade de testes e manutenção longa. |
| **Clean Architecture** | Separação por regras de negócio, independente de UI, DB e frameworks. | Altamente testável, flexível a mudanças de tecnologia. | Mais complexa de implementar no início. | Aplicações críticas e com longa vida útil. |
| **DDD + Microservices** | Microsserviços modelados com base nos Bounded Contexts do DDD. | Alinhamento direto com o negócio, alta coesão. | Exige profundo conhecimento do domínio e boas práticas de DDD. | Sistemas corporativos complexos (bancos, ERPs). |

---

### **1. Mobile Apps**

| Arquiteturas indicadas | Por quê? |
| --- | --- |
| **Camadas (Layered)** | Organiza bem código entre UI, lógica e dados. Ideal para apps nativos (MVC, MVVM, MVP). |
| **Hexagonal / Clean Architecture** | Boa separação entre regras de negócio e interface, facilita testes e manutenção. |
| **Componentes** | Permite reaproveitamento de UI (Flutter, React Native). |
| **Event-Driven (local)** | Útil para apps com notificações, sensores ou interações assíncronas. |

---

### **2. IoT (Internet das Coisas)**

| Arquiteturas indicadas | Por quê? |
| --- | --- |
| **Event-Driven** | Ideal para dispositivos que reagem a sensores e eventos em tempo real. |
| **Microservices** | Backend escalável para lidar com muitos dispositivos simultâneos. |
| **Serverless** | Reduz custo e escala automaticamente para ingestão de dados de sensores. |
| **Service Mesh** | Em soluções maiores com microsserviços IoT, ajuda na comunicação entre serviços. |

---

### **3. Fintech / Bancos**

| Arquiteturas indicadas | Por quê? |
| --- | --- |
| **Clean Architecture** | Facilita testes, segurança e escalabilidade — essencial para sistemas bancários. |
| **DDD + Microservices** | Permite dividir por domínios de negócio (conta, cartão, crédito, etc.) com regras isoladas. |
| **Event-Driven** | Ótimo para notificações de transações, conciliação, auditoria em tempo real. |
| **SOA / ESB** | Ainda muito usada em bancos tradicionais para integração com sistemas legados. |

---

### **4. E-commerce**

| Arquiteturas indicadas | Por quê? |
| --- | --- |
| **Microservices** | Catálogo, carrinho, pagamento, etc. como serviços separados — escalabilidade e modularidade. |
| **Event-Driven** | Promoções, alterações de estoque, notificações, tudo via eventos. |
| **Serverless** | Ideal para promoções/eventos de pico (ex: Black Friday), escala e cobra só pelo uso. |
| **Hexagonal** | Facilita testes em lógica de carrinho, pedidos, descontos, etc. |

---

### **5. SaaS / Web Apps**

| Arquiteturas indicadas | Por quê? |
| --- | --- |
| **Camadas** | Clássico para sistemas com frontend, backend e banco bem definidos. |
| **Microservices** | Escalabilidade e deploys independentes por módulos (ex: billing, auth, dashboard). |
| **Clean Architecture** | Evita dependência de tecnologias específicas, facilita manutenção e expansão. |
| **Componentes** | UIs reutilizáveis e dinâmicas (ex: dashboards modulares). |

---

### **6. Startups / MVPs**

| Arquiteturas indicadas | Por quê? |
| --- | --- |
| **Monolítica** | Rápido de desenvolver e colocar no ar; ideal para validar ideias. |
| **Camadas** | Organização mínima já com alguma separação útil para escalar depois. |
| **Serverless** | Barato e rápido para subir MVPs com poucos endpoints. |

---

Se quiser, posso gerar um **PDF visual** com essas tabelas, ou adaptar ainda mais para um cenário específico que você esteja desenvolvendo (tipo: "quero lançar um app fintech com backend escalável"). Quer que eu monte o PDF ou adaptar pra algum projeto teu?