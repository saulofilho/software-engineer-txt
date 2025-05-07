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

---

## **1. Arquitetura MVC (Model-View-Controller)**

Rails já implementa MVC por padrão. Aqui está um exemplo simples:

### **Model (`app/models/user.rb`)**

```ruby
class User < ApplicationRecord
  validates :name, presence: true
end

```

### **Controller (`app/controllers/users_controller.rb`)**

```ruby
class UsersController < ApplicationController
  def index
    @users = User.all
  end
end

```

### **View (`app/views/users/index.html.erb`)**

```
erb
CopiarEditar
<% @users.each do |user| %>
  <p><%= user.name %></p>
<% end %>

```

---

## **2. Arquitetura Hexagonal (Ports and Adapters)**

Aqui separamos a lógica de negócios dos detalhes de infraestrutura.

### **Porta (Interface) (`app/ports/user_repository.rb`)**

```ruby
class UserRepository
  def find_all
    raise NotImplementedError
  end
end

```

### **Adaptador (`app/adapters/user_active_record_repository.rb`)**

```ruby
class UserActiveRecordRepository < UserRepository
  def find_all
    User.all
  end
end

```

### **Uso no Controller (`app/controllers/users_controller.rb`)**

```ruby
class UsersController < ApplicationController
  def index
    repository = UserActiveRecordRepository.new
    @users = repository.find_all
  end
end

```

---

## **3. DDD (Domain-Driven Design)**

Aqui dividimos o código em camadas: **Domain**, **Application**, **Infrastructure**, **UI**.

### **Entidade (`app/domain/user.rb`)**

```ruby
class User
  attr_reader :name

  def initialize(name)
    @name = name
  end
end

```

### **Repositório (`app/infrastructure/repositories/user_repository.rb`)**

```ruby
class UserRepository
  def find_all
    User.all.map { |user| User.new(user.name) }
  end
end

```

### **Caso de Uso (`app/application/use_cases/list_users.rb`)**

```ruby
class ListUsers
  def initialize(user_repository)
    @user_repository = user_repository
  end

  def call
    @user_repository.find_all
  end
end

```

### **Controller (`app/controllers/users_controller.rb`)**

```ruby
class UsersController < ApplicationController
  def index
    use_case = ListUsers.new(UserRepository.new)
    @users = use_case.call
  end
end

```

---

## **4. TDD (Test-Driven Development)**

TDD é uma abordagem, então aqui está um exemplo de teste antes da implementação:

### **Teste (`spec/models/user_spec.rb`)**

```ruby
require 'rails_helper'

RSpec.describe User, type: :model do
  it "é inválido sem um nome" do
    user = User.new(name: nil)
    expect(user).not_to be_valid
  end
end

```

Depois, escrevemos o modelo para passar no teste:

### **Model (`app/models/user.rb`)**

```ruby
class User < ApplicationRecord
  validates :name, presence: true
end

```

---

## **5. Clean Architecture**

Aqui seguimos o padrão de camadas.

### **Entidade (`app/domain/user.rb`)**

```ruby
class User
  attr_accessor :name

  def initialize(name)
    @name = name
  end
end

```

### **Caso de Uso (`app/application/user_service.rb`)**

```ruby
class UserService
  def initialize(user_repository)
    @user_repository = user_repository
  end

  def list_users
    @user_repository.all
  end
end

```

### **Repositório (`app/infrastructure/repositories/user_repository.rb`)**

```ruby
class UserRepository
  def all
    User.all.map { |u| User.new(u.name) }
  end
end

```

### **Controller (`app/controllers/users_controller.rb`)**

```ruby
class UsersController < ApplicationController
  def index
    service = UserService.new(UserRepository.new)
    @users = service.list_users
  end
end

```

---

## **6. Service Objects**

Criamos um **service object** para encapsular a lógica.

### **Service (`app/services/user_creator.rb`)**

```ruby
class UserCreator
  def initialize(name)
    @name = name
  end

  def call
    User.create!(name: @name)
  end
end

```

### **Uso no Controller**

```ruby
class UsersController < ApplicationController
  def create
    UserCreator.new(params[:name]).call
    redirect_to users_path
  end
end

```

---

## **7. Interactor Pattern**

Parecido com Service Objects, mas segue o padrão **Interactors**.

### **Interactor (`app/interactors/create_user.rb`)**

```ruby
class CreateUser
  def initialize(name)
    @name = name
  end

  def call
    User.create!(name: @name)
  end
end

```

### **Uso no Controller**

```ruby
class UsersController < ApplicationController
  def create
    CreateUser.new(params[:name]).call
    redirect_to users_path
  end
end

```

---

## **8. CQRS (Command Query Responsibility Segregation)**

Separa comandos e consultas.

### **Query Object (`app/queries/list_users_query.rb`)**

```ruby
class ListUsersQuery
  def call
    User.all
  end
end

```

### **Command Object (`app/commands/create_user_command.rb`)**

```ruby
class CreateUserCommand
  def initialize(name)
    @name = name
  end

  def execute
    User.create!(name: @name)
  end
end

```

### **Uso no Controller**

```ruby
class UsersController < ApplicationController
  def index
    @users = ListUsersQuery.new.call
  end

  def create
    CreateUserCommand.new(params[:name]).execute
    redirect_to users_path
  end
end

```

---

## **9. Event-Driven Architecture (EDA)**

Eventos são emitidos para comunicação assíncrona.

### **Publicador (`app/events/user_created_event.rb`)**

```ruby
class UserCreatedEvent
  def self.call(user)
    ActiveSupport::Notifications.instrument("user.created", user: user)
  end
end

```

### **Listener (`config/initializers/event_listeners.rb`)**

```ruby
ActiveSupport::Notifications.subscribe("user.created") do |name, start, finish, id, payload|
  Rails.logger.info "Usuário criado: #{payload[:user].name}"
end

```

### **Uso no Controller**