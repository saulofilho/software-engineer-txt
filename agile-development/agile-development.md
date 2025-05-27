# Guia Completo de Metodologias Ágeis

Este guia aborda de forma aprofundada os princípios, frameworks e práticas de metodologias ágeis, oferecendo exemplos, dicas de adoção e métricas para equipes de software.

---

## 1. Introdução e Contexto Histórico

* **Década de 1990**: insatisfação com processos pesados (CMMI, RUP, Waterfall).
* **2001**: 17 praticantes assinam o Manifesto Ágil em Snowbird, Utah.

**Manifesto Ágil (2001)**:

> *"Estamos descobrindo melhores formas de desenvolver software fazendo-o e ajudando outros a fazê-lo..."*

4 valores fundamentais:

1. **Indivíduos e interações** mais que processos e ferramentas.
2. **Software funcionando** mais que documentação abrangente.
3. **Colaboração com o cliente** mais que negociação de contratos.
4. **Responder a mudanças** mais que seguir um plano.

12 princípios norteadores:

* Entrega de software funcional continuamente, ciclos curtos.
* Mudanças de requisitos bem-vindas, mesmo tardiamente.
* Stakeholders e desenvolvedores trabalhando juntos.
* Projetos construídos em torno de pessoas motivadas.
* Comunicação face a face como mais eficaz.
* Software funcionando é a medida primária de progresso.
* Sustentabilidade de ritmo de trabalho constante.
* Atenção contínua à excelência técnica.
* Simplicidade é essencial.
* Equipes auto-organizadas.
* Inspeção e adaptação regulares.

---

## 2. Frameworks Ágeis Principais

### 2.1 Scrum

* **Papéis**:

  * **Product Owner**: define e prioriza o backlog.
  * **Scrum Master**: facilita o processo, remove impedimentos.
  * **Time de Desenvolvimento**: cross-functional, auto-organizado.

* **Eventos (Cerimônias)**:

  1. **Sprint Planning** (planejamento do Sprint).
  2. **Daily Scrum** (reunião diária de 15 min).
  3. **Sprint Review** (apresentação do increment).
  4. **Sprint Retrospective** (o que funcionou / melhorar).

* **Artefatos**:

  * **Product Backlog**: lista priorizada de itens (User Stories).
  * **Sprint Backlog**: itens selecionados para Sprint + plano de entrega.
  * **Increment**: soma de todos os itens "Done" no Sprint.

```markdown
# Exemplo de User Story
**Título**: Como usuário, quero resetar minha senha para recuperar acesso.
**Critérios de Aceitação**:
- Enviar e-mail de reset.
- Link válido por 24h.
```

### 2.2 Kanban

* **Princípios**: visualizar fluxo, limitar WIP (Work In Progress), gerenciar fluxo, políticas explícitas, implementar feedback, melhorar colaborativamente.
* **Quadro Kanban**: colunas típicas Backlog › To Do › Doing › Review › Done.
* **Métricas**:

  * **Lead Time**: tempo desde pedido até entrega.
  * **Cycle Time**: tempo desde início da execução até conclusão.
  * **Throughput**: quantidade de itens concluídos por unidade de tempo.

### 2.3 Extreme Programming (XP)

* **Práticas principais**:

  * Pair Programming.
  * Test-Driven Development (TDD).
  * Integração Contínua.
  * Refatoração constante.
  * Cliente no local.

### 2.4 Lean Software Development

* Derivado do Sistema Toyota de Produção.
* **Princípios**: eliminar desperdícios, amplificar aprendizado, decidir o mais tarde possível, entregar o mais rápido possível, empoderar equipe, construir qualidade, ver o todo.

### 2.5 Scrumban

* Híbrido Scrum + Kanban.
* Mantém Sprints e eventos Scrum, mas com fluxo contínuo do Kanban.

---

## 3. Escalando Metodologias Ágeis

### 3.1 SAFe (Scaled Agile Framework)

* Níveis: **Team**, **Program**, **Large Solution**, **Portfolio**.
* Ágil em escala com ARTs (Agile Release Trains).

### 3.2 LeSS (Large-Scale Scrum)

* Expande Scrum para múltiplas equipes num mesmo Product Backlog.
* 1 Product Owner, eventos compartilhados.

### 3.3 Nexus

* Escala Scrum para 3–9 equipes.
* Nexus Integration Team gerencia integrações.

### 3.4 DAD (Disciplined Agile Delivery)

* Combina Scrum, Kanban, XP, Agile Modeling em um ciclo de vida flexível.

---

## 4. Cerimônias e Eventos Detalhados

| Cerimônia            | Objetivo                                 | Duração típica             |
| -------------------- | ---------------------------------------- | -------------------------- |
| Sprint Planning      | Planejar o trabalho do Sprint            | 2–4 horas (Para 2 semanas) |
| Daily Scrum          | Sincronizar equipe, remover impedimentos | 15 minutos                 |
| Sprint Review        | Demonstrar increment para stakeholders   | 1–2 horas                  |
| Sprint Retrospective | Inspeção e adaptação do processo         | 1–2 horas                  |

---

## 5. Artefatos e Ferramentas de Gerenciamento

* **Backlog**: Jira, Azure DevOps, Trello.
* **Quadro Kanban**: Kanbanize, LeanKit.
* **CI/CD**: Jenkins, GitHub Actions, GitLab CI.
* **Comunicação**: Slack, Microsoft Teams.

---

## 6. Métricas Ágeis e KPIs

* **Velocity**: média de pontos entregues por Sprint (Scrum).
* **Burn-down / Burn-up Charts**: progresso do Sprint ou Release.
* **Lead Time / Cycle Time** (Kanban).
* **Cumulative Flow Diagram**: visualiza fluxo e gargalos.

---

## 7. Boas Práticas de Adoção

1. **Treinamento e Coaching**: capacitar times e liderança.
2. **Pilotos**: começar em um time antes de escalar.
3. **Cultura de Feedback**: reuniões de Retrospective efetivas.
4. **Políticas Explícitas**: definições claras de pronto (DoD) e pronto para desenvolvimento (DoR).
5. **Melhoria Contínua**: Kaizen e inspeções regulares.

---

## 8. Desafios Comuns e Como Superar

| Desafio                      | Solução                                 |
| ---------------------------- | --------------------------------------- |
| Resistência à mudança        | Workshops, comunicação transparente     |
| Falta de comprometimento     | Empowerment, metas claras               |
| Backlog mal refinado         | Refinement regular, Definition of Ready |
| Alta variabilidade de escopo | Timeboxing, revisão de prioridades      |
| Dependências entre equipes   | Planejamento conjunto, X-Teams          |

---

## 9. Ferramentas Populares

* **Jira**: robustez, customização.
* **Azure DevOps**: integração Microsoft.
* **Trello**: simplicidade, Kanban.
* **ClickUp**, **Asana**, **Monday.com**.

---

## Conclusão

A adoção de metodologias ágeis requer mais do que processos, mas uma mudança cultural focada em entrega de valor, colaboração e adaptação contínua. Escolha o framework que melhor se encaixe no contexto da equipe e espaço para evoluir conforme a maturidade aumenta.
