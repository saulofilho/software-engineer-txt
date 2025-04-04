# Linguagens

### **1. Ruby**

- **Paradigma**: Orientado a objetos puro.
- **Sintaxe**: Muito legível e expressiva (quase como pseudocódigo).
- **Uso comum**: Desenvolvimento web com Ruby on Rails.
- **Performance**: Mais lenta comparada a Go e .NET.
- **Ecossistema**: Forte em web, mas perdeu popularidade para outras stacks.
- **Ideal para**: Startups, MVPs rápidos, apps web com foco em produtividade.

---

### **2. Python**

- **Paradigma**: Multi-paradigma (OO, funcional, imperativo).
- **Sintaxe**: Simples e legível.
- **Uso comum**: Ciência de dados, automação, web (Django, Flask), IA.
- **Performance**: Interpretação lenta, mas existem otimizações (Cython, PyPy).
- **Ecossistema**: Muito vasto, com bibliotecas para quase tudo.
- **Ideal para**: Scripts, data science, prototipagem, ensino, IA/ML.

---

### **3. .NET (C#)**

- **Paradigma**: Orientado a objetos, com suporte a funcional.
- **Sintaxe**: Inspirada em C, semelhante ao Java.
- **Uso comum**: Sistemas corporativos, APIs, desktop, jogos (Unity).
- **Performance**: Muito boa com o .NET Core (agora .NET 5/6/7).
- **Ecossistema**: Robusto para apps corporativos e integração com Windows.
- **Ideal para**: Empresas, sistemas grandes, apps Windows, jogos com Unity.

---

### **4. Go (Golang)**

- **Paradigma**: Procedural, com concorrência como destaque.
- **Sintaxe**: Simples e enxuta, com tipagem estática.
- **Uso comum**: Backend, APIs, sistemas distribuídos, infra (ex: Docker, Kubernetes).
- **Performance**: Quase no nível de C — muito rápida.
- **Ecossistema**: Crescendo bastante, foco em performance e simplicidade.
- **Ideal para**: Sistemas de alta performance, microserviços, DevOps.

---

### **Resumo rápido por critérios:**

| Critério | Ruby | Python | .NET (C#) | Go |
| --- | --- | --- | --- | --- |
| Facilidade | Alta | Alta | Média | Alta |
| Velocidade | Baixa | Baixa | Alta | Muito Alta |
| Concorrência | Fraca | Média | Boa | Excelente |
| Popularidade | Média | Muito alta | Alta | Alta |
| Web Dev | Excelente | Boa | Boa | Boa |
| Backend API | Boa | Boa | Excelente | Excelente |
| Data Science | Fraca | Excelente | Média | Fraca |
| Sistemas grandes | Fraca | Média | Excelente | Boa |

---

# API Development

### **1. Go (Golang)**

- **Melhor escolha se performance é crítica**.
- Ideal para **alta concorrência**, microserviços, cloud-native.
- APIs muito rápidas e leves.
- Mais "baixo nível" que Python ou Ruby, então exige um pouco mais de código.
- Muito usado por empresas como Google, Uber, Twitch, etc.

**Prós:** Velocidade, concorrência, binários standalone.

**Contras:** Sintaxe mais rígida, menos "ergonômico" que Python/Ruby.

---

### **2. .NET (C#)**

- Excelente para APIs corporativas e sistemas complexos.
- Ótima performance com ASP.NET Core.
- Muito bom suporte a REST, GraphQL, autenticação, etc.
- Melhor escolha se o time já trabalha com C# ou precisa de integração com produtos Microsoft.

**Prós:** Performance, robustez, ferramentas empresariais.

**Contras:** Pode ser mais verboso, depende do .NET SDK.

---

### **3. Python (Flask / FastAPI / Django)**

- Melhor escolha para prototipagem rápida e quando já se usa Python (ex: IA, scripts).
- **FastAPI** é moderno, rápido, com suporte a OpenAPI, async, etc.
- Muito produtivo para APIs de pequena/média escala.

**Prós:** Rápido de desenvolver, muita documentação, grande comunidade.

**Contras:** Menor desempenho em produção (comparado a Go/.NET), pode precisar de tunagem com gunicorn/uvicorn.

---

### **4. Ruby (Ruby on Rails / Sinatra)**

- Ainda bom para APIs pequenas a médias.
- Desenvolvimento muito produtivo com Rails API mode.
- Mas está menos em alta hoje para APIs novas, exceto se já há base em Ruby.

**Prós:** Alta produtividade.

**Contras:** Performance e escalabilidade abaixo das outras opções.

---

### **Resumo prático para API**: