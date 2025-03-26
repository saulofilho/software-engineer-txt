No Ruby on Rails, a arquitetura tradicional segue o padrão **MVC (Model-View-Controller)**, mas existem diversas abordagens arquiteturais que podem ser aplicadas conforme a necessidade do projeto. Algumas das principais são:

### 1. **Arquitetura em Camadas Tradicional (MVC)**

- **Model**: Responsável pela lógica de negócios e comunicação com o banco de dados.
- **View**: Camada de apresentação, renderizando HTML, JSON, etc.
- **Controller**: Gerencia as requisições, chamando modelos e renderizando as views.

### 2. **Arquitetura Hexagonal (Ports and Adapters)**

- Separa a lógica de negócio da infraestrutura.
- Define **"ports"** (interfaces para comunicação) e **"adapters"** (implementações concretas).
- Facilita a troca de banco de dados, interfaces de API e outras dependências externas.

### 3. **DDD (Domain-Driven Design)**

- Organiza o código focando no domínio do negócio.
- Divide o sistema em **camadas**, como:
    - **Domain** (entidades, agregados, value objects)
    - **Application** (casos de uso)
    - **Infrastructure** (persistência, APIs externas)
    - **UI** (interface do usuário)

### 4. **TDD (Test-Driven Development)**

- Não é exatamente uma arquitetura, mas sim uma abordagem para desenvolvimento.
- Primeiro escreve os testes e depois o código, garantindo confiabilidade.

### 5. **Arquitetura Clean (Clean Architecture)**

- Similar ao DDD, mas foca em **separação de responsabilidades**.
- Divide o sistema em **regras de negócio puras** (núcleo da aplicação) e **infraestrutura** (banco de dados, APIs).
- Usa conceitos como **Use Cases**, **Repositories**, **Entities** e **Interfaces**.

### 6. **Service Objects**

- Separa responsabilidades específicas em classes de serviço.
- Evita lógica de negócios nos Models e Controllers.

### 7. **Interactor Pattern**

- Similar ao Service Object, mas organiza a lógica em classes chamadas **Interactors**.
- Cada interactor executa um único caso de uso.

### 8. **CQRS (Command Query Responsibility Segregation)**

- Separa comandos (ações que alteram o estado) de consultas (ações que apenas leem dados).
- Pode ser usado junto com **Event Sourcing** para rastrear mudanças no sistema.

### 9. **Event-Driven Architecture (EDA)**

- Baseia-se em eventos para comunicação assíncrona entre componentes.
- Usa **event buses** como Sidekiq, Kafka, ou ActiveSupport::Notifications.

### **Conclusão**

Cada arquitetura tem suas vantagens e desvantagens, e a escolha depende do contexto do projeto. Muitas vezes, um projeto Rails começa com MVC tradicional e evolui para padrões mais sofisticados como **Service Objects, DDD ou Clean Architecture** conforme cresce.
