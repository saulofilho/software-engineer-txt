### **Princípios de Engenharia de Software**

- SOLID: Princípios para um código bem estruturado e fácil de manter.
  - Single Responsibility Principle (SRP): Cada classe deve ter uma única responsabilidade.
  - Open/Closed Principle (OCP): Classes devem estar abertas para extensão, mas fechadas para modificação.
  - Liskov Substitution Principle (LSP): Objetos de uma classe derivada devem poder substituir objetos da classe base.
  - Interface Segregation Principle (ISP): Interfaces específicas em vez de interfaces genéricas.
  - Dependency Inversion Principle (DIP): Dependa de abstrações, não de implementações concretas.
- DRY (Don't Repeat Yourself):
  - Evita duplicação de código, tornando-o reutilizável e fácil de manter.
- KISS (Keep It Simple, Stupid):
  - Código deve ser simples e direto, evitando complexidade desnecessária.
- YAGNI (You Ain’t Gonna Need It):
  - Não implemente funcionalidades antes de realmente precisar delas.

---

### **Concorrência, Paralelismo e Threading no Ruby**

- Ruby usa **GIL (Global Interpreter Lock)**, o que limita a execução real de threads em paralelo.
- Para tarefas CPU-bound, **processos** são mais eficientes que threads.
- Para tarefas I/O-bound, **threads** podem melhorar desempenho.
- Gems úteis para concorrência em Ruby:
    - **Sidekiq**: Para jobs em segundo plano usando Redis.
    - **Concurrent-ruby**: Oferece estruturas para concorrência como `ThreadPoolExecutor`.
    - **Celluloid**: Programação concorrente orientada a atores.

---

### **Filas e Processamento em Segundo Plano**

- **Sidekiq** (usa Redis) → Melhor opção para jobs assíncronos no Rails.
- **Resque** (usa Redis) → Similar ao Sidekiq, mas usa processos em vez de threads.
- **DelayedJob** (usa banco de dados) → Boa opção se não quiser usar Redis.
    - Exemplo de um job em **Sidekiq**:
    
    ```ruby
    class HardWorker
      include Sidekiq::Worker
    
      def perform(name, count)
        puts "Trabalhando #{count} vezes para #{name}"
      end
    end
    ```
    
    Para enfileirar o job:
    
    ```ruby
    HardWorker.perform_async("João", 5)
    ```
    

---

### **Estruturas de Dados e Algoritmos**

- **Busca Binária**: Divide um array ordenado ao meio para encontrar um elemento.
    
    ```ruby
    def busca_binaria(arr, alvo)
      esquerda, direita = 0, arr.length - 1
      while esquerda <= direita
        meio = (esquerda + direita) / 2
        return meio if arr[meio] == alvo
        arr[meio] < alvo ? esquerda = meio + 1 : direita = meio - 1
      end
      nil
    end
    ```
    
- **Árvore Binária**: Estrutura onde cada nó tem no máximo dois filhos.
    
    ```ruby
    class Node
      attr_accessor :valor, :esquerda, :direita
    
      def initialize(valor)
        @valor = valor
        @esquerda = nil
        @direita = nil
      end
    end
    ```
    
- **Loops e Estruturas de Controle**
    
    ```ruby
    (1..5).each { |i| puts i }  # Loop de 1 a 5
    while condition do
      # Código
    end
    ```
    

---

### **Ruby Avançado e Rails**

- **Metaprogramação**: Criar métodos dinamicamente usando `define_method` ou `method_missing`.
    - **Mixin e Módulos**:
        - Reutilização de código sem herança.
    - **ActiveRecord e ORM**:
        - Query otimizada e indexação de banco de dados.
    - **Cache (Memcached, Redis)**:
        - Melhorar performance.

---

## **1. Estruturas de Dados**

### **1.1 Arrays (Listas)**

- Estrutura **dinâmica** e indexada.
- Tempo de acesso a um elemento: **O(1)** (acesso direto).
- Inserção/remoção no final: **O(1)**.
- Inserção/remoção no meio/início: **O(n)** (reorganiza elementos).

Exemplo:

```ruby
arr = [1, 2, 3, 4, 5]
arr << 6           # Adiciona ao final
arr.unshift(0)     # Adiciona ao início
arr.delete_at(2)   # Remove elemento no índice 2
p arr  # [0, 1, 3, 4, 5, 6]
```

---

### **1.2 Hash (Dicionário)**

- Estrutura de **chave-valor**.
- Acesso a um elemento: **O(1)** (mapeamento hash).
- Inserção/remoção: **O(1)** na média, mas pode ser **O(n)** no pior caso (colisão).

Exemplo:

```ruby
hash = { "nome" => "João", "idade" => 30 }
hash["cidade"] = "São Paulo"
hash.delete("idade")
p hash  # {"nome"=>"João", "cidade"=>"São Paulo"}
```

---

### **1.3 Pilha (Stack)**

- **LIFO (Last In, First Out)** → O último elemento a entrar é o primeiro a sair.
- Uso comum: histórico de navegação, chamadas recursivas.

Exemplo:

```ruby
class Stack
  def initialize
    @stack = []
  end

  def push(element)
    @stack << element
  end

  def pop
    @stack.pop
  end

  def peek
    @stack.last
  end
end

stack = Stack.new
stack.push(1)
stack.push(2)
p stack.pop  # 2
```

---

### **1.4 Fila (Queue)**

- **FIFO (First In, First Out)** → O primeiro elemento a entrar é o primeiro a sair.
- Uso comum: filas de processos, jobs em background.

Exemplo usando `Array`:

```ruby
class Queue
  def initialize
    @queue = []
  end

  def enqueue(element)
    @queue << element
  end

  def dequeue
    @queue.shift
  end
end

queue = Queue.new
queue.enqueue(1)
queue.enqueue(2)
p queue.dequeue  # 1
```

Para melhor performance, use **`Queue` da stdlib** (evita deslocamento de elementos):

```ruby
require 'thread'
queue = Queue.new
queue.push(1)
queue.push(2)
p queue.pop  # 1
```

---

### **1.5 Deque (Double-ended Queue)**

- Permite inserção e remoção em **ambas as extremidades** (**O(1)**).
- Útil para **algoritmos de busca** e **sistemas de cache**.

```ruby
require 'deque'
deque = Deque.new
deque.push_front(1)
deque.push_back(2)
p deque.pop_front  # 1
```

---

### **1.6 Conjuntos (Set)**

- Estrutura sem **valores duplicados**.
- Inserção, remoção e busca em **O(1)** (mapeamento hash).

```ruby
require 'set'
set = Set.new
set.add(1)
set.add(2)
set.add(1)  # Ignorado
p set.to_a  # [1, 2]
```

---

### **1.7 Árvores**

- Estrutura hierárquica com nós conectados.
- **Árvore Binária**: Cada nó tem no máximo dois filhos.
- **Árvore Balanceada (AVL, Red-Black Tree)**: Mantém eficiência em buscas.
- **Árvore de Busca Binária (BST)**: Para buscas rápidas **O(log n)**.

Exemplo:

```ruby
class Node
  attr_accessor :value, :left, :right

  def initialize(value)
    @value = value
    @left = nil
    @right = nil
  end
end

class BinaryTree
  def initialize
    @root = nil
  end

  def insert(value)
    @root = insert_rec(@root, value)
  end

  def insert_rec(node, value)
    return Node.new(value) if node.nil?
    if value < node.value
      node.left = insert_rec(node.left, value)
    else
      node.right = insert_rec(node.right, value)
    end
    node
  end
end

tree = BinaryTree.new
tree.insert(10)
tree.insert(5)
tree.insert(15)
```

---

## **2. Algoritmos Importantes**

### **2.1 Busca Linear**

A **busca linear** (ou **linear search**) é um algoritmo simples que percorre um array elemento por elemento até encontrar o valor desejado ou atingir o final da lista.

---

### **📌 Exemplo de busca linear em Ruby**

```ruby
ruby
CopiarEditar
def busca_linear(array, alvo)
  array.each_with_index do |elemento, indice|
    return indice if elemento == alvo
  end
  nil # Retorna nil se não encontrar o elemento
end

numeros = [10, 25, 30, 45, 50]
puts busca_linear(numeros, 30) # Saída: 2
puts busca_linear(numeros, 100) # Saída: nil

```

🔹 O método percorre o array e retorna o **índice** do elemento encontrado. Se o valor não estiver presente, retorna `nil`.

---

### **2.1 Busca Binária (O(log n))**

- Requer **array ordenado**.
- Divide pela metade até encontrar o elemento.

```ruby

def busca_binaria(arr, alvo)
  esquerda, direita = 0, arr.length - 1
  while esquerda <= direita
    meio = (esquerda + direita) / 2
    return meio if arr[meio] == alvo
    arr[meio] < alvo ? esquerda = meio + 1 : direita = meio - 1
  end
  nil
end

arr = [1, 3, 5, 7, 9]
p busca_binaria(arr, 5)  # 2
```

---

### **2.2 Ordenação**

- **Bubble Sort (O(n²))**: Simples, mas ineficiente.
- **QuickSort (O(n log n) no caso médio)**: Divide e conquista.
- **MergeSort (O(n log n))**: Divide o array, ordena e mescla.

### **QuickSort**

```ruby
def quicksort(arr)
  return arr if arr.length <= 1
  pivo = arr.delete_at(arr.length / 2)
  menores, maiores = arr.partition { |x| x < pivo }
  quicksort(menores) + [pivo] + quicksort(maiores)
end

p quicksort([3, 1, 4, 1, 5, 9, 2, 6])
```

---

### **2.3 Recursão**

- Uma função chama a si mesma até atingir um caso base.
- **Fatorial**:

```ruby
def fatorial(n)
  return 1 if n == 0
  n * fatorial(n - 1)
end

p fatorial(5)  # 120
```

- **Fibonacci**:

```ruby
def fibonacci(n)
  return n if n <= 1
  fibonacci(n - 1) + fibonacci(n - 2)
end

p fibonacci(6)  # 8
```

> Dica: Recursão pode ser otimizada com memoization.
> 

**Memoization** é uma técnica de otimização usada para armazenar os resultados de funções já calculadas, evitando chamadas repetitivas e melhorando a performance do código. Em Ruby, isso é feito geralmente com variáveis de instância ou hashes.

### 📌 **Exemplo básico de memoization em Ruby**

```ruby
def fibonacci(n, memo = {})
  return n if n <= 1
  memo[n] ||= fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
end

puts fibonacci(10) # => 55
```

🔹 Aqui, `memo[n] ||= ...` armazena o resultado de `fibonacci(n)` para evitar cálculos repetidos.

---

## **3. Complexidade de Tempo**

| Algoritmo | Melhor Caso | Médio Caso | Pior Caso |
| --- | --- | --- | --- |
| Busca Linear | O(1) | O(n) | O(n) |
| Busca Binária | O(1) | O(log n) | O(log n) |
| Bubble Sort | O(n) | O(n²) | O(n²) |
| QuickSort | O(n log n) | O(n log n) | O(n²) |
| MergeSort | O(n log n) | O(n log n) | O(n log n) |

---

### **1. SOLID**

### **S - Single Responsibility Principle (SRP)**

Cada classe deve ter uma única responsabilidade.

Exemplo:

```ruby
# Antes de aplicar SRP
class Order
  def initialize
    @items = []
  end

  def add_item(item)
    @items << item
  end

  def total
    @items.sum(&:price)
  end

  def save
    # Lógica para salvar no banco de dados
  end
end

# Depois de aplicar SRP
class Order
  def initialize
    @items = []
  end

  def add_item(item)
    @items << item
  end

  def total
    @items.sum(&:price)
  end
end

class OrderRepository
  def save(order)
    # Lógica para salvar no banco de dados
  end
end
```

*Explicação*: A classe `Order` agora tem apenas a responsabilidade de gerenciar os itens da ordem, e `OrderRepository` cuida do salvamento no banco de dados.

---

### **O - Open/Closed Principle (OCP)**

As classes devem estar abertas para extensão, mas fechadas para modificação.

Exemplo:

```ruby
ruby
CopiarEditar
# Antes de aplicar OCP
class AreaCalculator
  def calculate(shape)
    if shape.is_a?(Circle)
      return Math::PI * shape.radius**2
    elsif shape.is_a?(Rectangle)
      return shape.width * shape.height
    end
  end
end

# Depois de aplicar OCP
class AreaCalculator
  def calculate(shape)
    shape.area
  end
end

class Circle
  attr_reader :radius

  def initialize(radius)
    @radius = radius
  end

  def area
    Math::PI * radius**2
  end
end

class Rectangle
  attr_reader :width, :height

  def initialize(width, height)
    @width = width
    @height = height
  end

  def area
    width * height
  end
end

```

*Explicação*: Em vez de modificar a classe `AreaCalculator` toda vez que uma nova forma for adicionada, agora você pode adicionar novas formas sem alterar o código existente, apenas criando novas classes que implementem `area`.

---

### **L - Liskov Substitution Principle (LSP)**

Subclasses devem ser substituíveis por suas superclasses sem afetar o comportamento esperado.

Exemplo:

```ruby
ruby
CopiarEditar
# Antes de aplicar LSP
class Bird
  def fly
    puts "Flying!"
  end
end

class Penguin < Bird
  def fly
    raise "Penguins can't fly!"
  end
end

# Depois de aplicar LSP
class Bird
  def move
    puts "Moving!"
  end
end

class Sparrow < Bird
  def move
    puts "Flying!"
  end
end

class Penguin < Bird
  def move
    puts "Waddling!"
  end
end

```

*Explicação*: A classe `Penguin` agora segue o contrato da classe `Bird` sem quebrar a expectativa de que todos os pássaros podem "mover-se".

---

### **I - Interface Segregation Principle (ISP)**

É melhor ter várias interfaces específicas do que uma única interface genérica.

Exemplo:

```ruby
ruby
CopiarEditar
# Antes de aplicar ISP
class Animal
  def swim
    # Implementação de natação
  end

  def fly
    # Implementação de voo
  end
end

class Fish < Animal
  # Não pode voar, então deixa o método vazio
end

# Depois de aplicar ISP
class Swimmable
  def swim; end
end

class Flyable
  def fly; end
end

class Fish
  include Swimmable
end

class Bird
  include Flyable
  include Swimmable
end

```

*Explicação*: Agora, as funcionalidades de natação e voo são separadas em interfaces distintas, evitando métodos desnecessários em classes que não implementam essas funcionalidades.

---

### **D - Dependency Inversion Principle (DIP)**

As classes de alto nível não devem depender de classes de baixo nível. Ambas devem depender de abstrações.

Exemplo:

```ruby
ruby
CopiarEditar
# Antes de aplicar DIP
class LightBulb
  def turn_on
    puts "Bulb is on"
  end

  def turn_off
    puts "Bulb is off"
  end
end

class Switch
  def initialize(bulb)
    @bulb = bulb
  end

  def operate
    @bulb.turn_on
  end
end

# Depois de aplicar DIP
class Switchable
  def turn_on; end
  def turn_off; end
end

class LightBulb < Switchable
  def turn_on
    puts "Bulb is on"
  end

  def turn_off
    puts "Bulb is off"
  end
end

class Switch
  def initialize(device)
    @device = device
  end

  def operate
    @device.turn_on
  end
end

```

*Explicação*: Agora, a classe `Switch` depende de uma abstração (`Switchable`) em vez de uma implementação concreta (`LightBulb`).

---

### **2. DRY (Don't Repeat Yourself)**

Evitar duplicação de código. Use métodos reutilizáveis e abstrações.

Exemplo:

```ruby
ruby
CopiarEditar
# Antes de aplicar DRY
class Order
  def total
    sum = 0
    @items.each do |item|
      sum += item.price
    end
    sum
  end

  def discount
    sum = 0
    @items.each do |item|
      sum += item.discount
    end
    sum
  end
end

# Depois de aplicar DRY
class Order
  def sum_items(attribute)
    @items.sum { |item| item.send(attribute) }
  end

  def total
    sum_items(:price)
  end

  def discount
    sum_items(:discount)
  end
end

```

*Explicação*: O método `sum_items` evita a duplicação de código ao calcular a soma de diferentes atributos dos itens.

---

### **3. KISS (Keep It Simple, Stupid)**

Mantenha o código simples e direto. Evite complexidade desnecessária.

Exemplo:

```ruby
ruby
CopiarEditar
# Antes de aplicar KISS
class User
  def initialize(age)
    if age < 0
      raise "Idade não pode ser negativa"
    end

    @age = age
  end
end

# Depois de aplicar KISS
class User
  def initialize(age)
    @age = age
  end

  def age_valid?
    @age >= 0
  end
end

```

*Explicação*: O código foi simplificado e a lógica de validação foi extraída para um método `age_valid?`, mantendo a responsabilidade da classe mais clara.

---

### **4. YAGNI (You Ain't Gonna Need It)**

Não adicione funcionalidades ou complexidade até que seja necessário.

Exemplo:

```ruby
ruby
CopiarEditar
# Antes de aplicar YAGNI
class Car
  def start_engine
    # Inicia o motor
  end

  def stop_engine
    # Para o motor
  end

  def check_warnings
    # Verifica alertas
  end

  def display_dashboard
    # Mostra o painel
  end
end

# Depois de aplicar YAGNI
class Car
  def start_engine
    # Inicia o motor
  end

  def stop_engine
    # Para o motor
  end
end

```

*Explicação*: A classe `Car` foi simplificada, removendo funcionalidades que não são essenciais neste momento. A complexidade não foi introduzida antes da necessidade real.

---

### Test-Driven Development (TDD) e Domain-Driven Design (DDD) em Ruby

TDD e DDD são duas abordagens diferentes, mas que podem ser usadas em conjunto para escrever código mais confiável, sustentável e alinhado ao domínio do negócio.

---

## **TDD (Test-Driven Development)**

TDD (Desenvolvimento Guiado por Testes) é uma metodologia de desenvolvimento de software onde os testes são escritos antes do código. O ciclo de TDD segue três etapas principais:

1. **Red**: Escreva um teste que falha porque a funcionalidade ainda não foi implementada.
2. **Green**: Implemente o código mínimo necessário para fazer o teste passar.
3. **Refactor**: Refatore o código garantindo que os testes ainda passem.

Essa abordagem garante que o código seja bem testado desde o início e evita a introdução de bugs.

### **Exemplo de TDD em Ruby**

Vamos criar uma classe `Calculadora` usando TDD com **RSpec**:

1. **Escrevemos o teste primeiro (`spec/calculadora_spec.rb`):**

```ruby
ruby
CopiarEditar
require 'rspec'
require_relative '../calculadora'

RSpec.describe Calculadora do
  it 'soma dois números' do
    calculadora = Calculadora.new
    expect(calculadora.soma(2, 3)).to eq(5)
  end
end

```

1. **Criamos a implementação mínima (`calculadora.rb`):**

```ruby
ruby
CopiarEditar
class Calculadora
  def soma(a, b)
    a + b
  end
end

```

1. **Executamos os testes:**

```
sh
CopiarEditar
rspec spec/calculadora_spec.rb

```

Se o teste passar, seguimos para refatoração, garantindo que o código fique limpo e eficiente.

---

## **DDD (Domain-Driven Design)**

DDD (Design Guiado pelo Domínio) é um modelo de desenvolvimento de software focado na complexidade do negócio. Ele enfatiza a criação de um modelo de domínio bem definido e a comunicação com especialistas da área para desenvolver software que reflita melhor as regras e entidades do negócio.

### **Principais Conceitos do DDD**

1. **Entidades** – Objetos com identidade única e ciclo de vida.
2. **Value Objects** – Objetos sem identidade, apenas com valores imutáveis.
3. **Aggregates** – Conjunto de objetos que são manipulados como uma única unidade.
4. **Repositories** – Classes que abstraem a persistência e recuperação de entidades.
5. **Services de Domínio** – Contêm lógica de negócio que não pertence a uma única entidade.

### **Exemplo de DDD em Ruby**

Vamos modelar um domínio de pedidos de um e-commerce.

### **1. Criando uma entidade (`models/pedido.rb`)**

```ruby
ruby
CopiarEditar
class Pedido
  attr_reader :id, :itens, :total

  def initialize(id)
    @id = id
    @itens = []
    @total = 0
  end

  def adicionar_item(produto, quantidade)
    item = ItemPedido.new(produto, quantidade)
    @itens << item
    calcular_total
  end

  private

  def calcular_total
    @total = @itens.sum(&:preco_total)
  end
end

```

### **2. Criando um Value Object (`models/item_pedido.rb`)**

```ruby
ruby
CopiarEditar
class ItemPedido
  attr_reader :produto, :quantidade, :preco_total

  def initialize(produto, quantidade)
    @produto = produto
    @quantidade = quantidade
    @preco_total = produto.preco * quantidade
  end
end

```

### **3. Criando um Repository (`repositories/pedido_repository.rb`)**

```ruby
ruby
CopiarEditar
class PedidoRepository
  def initialize
    @pedidos = []
  end

  def salvar(pedido)
    @pedidos << pedido
  end

  def buscar_por_id(id)
    @pedidos.find { |p| p.id == id }
  end
end

```

---

## **Juntando TDD e DDD**

Podemos aplicar TDD para garantir que nosso modelo de domínio (DDD) funcione corretamente.

### **Testando a entidade Pedido (`spec/pedido_spec.rb`)**

```ruby
ruby
CopiarEditar
require 'rspec'
require_relative '../models/pedido'
require_relative '../models/item_pedido'

RSpec.describe Pedido do
  it 'adiciona um item ao pedido e calcula o total' do
    produto = double('Produto', preco: 10.0)
    pedido = Pedido.new(1)
    pedido.adicionar_item(produto, 2)

    expect(pedido.itens.count).to eq(1)
    expect(pedido.total).to eq(20.0)
  end
end

```

---

## **Conclusão**

- **TDD** garante que o código seja testável e confiável desde o início.
- **DDD** foca na modelagem do domínio para que o código represente melhor a lógica do negócio.
- Em **Ruby**, frameworks como **RSpec** ajudam a estruturar testes, enquanto o design orientado a objetos facilita a implementação de conceitos do DDD.

---

### Load Balancer

- Sim, quase sempre tem. Pode ser um ELB (AWS), NGINX, HAProxy ou outro.
- Ele é quem faz o roteamento das requisições externas para os serviços internos.
- Normalmente usado junto de um proxy reverso para balancear e proteger APIs.

---

### ✅ Proxy Reverso

- Pode ser o próprio Load Balancer ou um componente à parte (NGINX, Traefik, Envoy).
- Faz terminação de SSL, autenticação de requests, controle de rate limit, e roteamento inteligente.
- Em Kubernetes é comum usar um **Ingress Controller** (que é basicamente um proxy reverso gerenciado).

---

### ✅ Redundância de Banco de Dados

- Sempre recomendado, principalmente com clusters (Postgres com Patroni, MySQL com Group Replication, MongoDB ReplicaSet, etc.).
- Replicação síncrona ou assíncrona, dependendo do caso.
- Alta disponibilidade via failover automático ou manual.

---

### ✅ Auto-scaling

- Kubernetes faz auto-scaling de pods automaticamente (HPA - Horizontal Pod Autoscaler).
- Infraestrutura (máquinas virtuais ou nodes) geralmente escalada com Terraform + auto-scaling groups (AWS, GCP).
- Pode ser baseado em CPU, memória, filas, ou métricas customizadas (como latência ou throughput).

---

### ✅ Kubernetes + Skaffold + Terraform

- **Terraform** provisiona a infra (rede, VPC, clusters, bancos, balancers).
- **Kubernetes** orquestra os containers e mantém os serviços funcionando.
- **Skaffold** facilita o ciclo de desenvolvimento (build, deploy e teste local e em clusters).

---

### ✅ Comunicação entre as peças

Pode ter uma combinação de:

1. **HTTP/REST** - Clássico, simples, direto.
2. **gRPC** - Se precisar de performance e comunicação binária.
3. **Mensageria** - Se for desacoplado ou assíncrono:
    - **Kafka** para *event streaming*.
    - **RabbitMQ** para filas tradicionais.
    - **SNS/SQS** (AWS) para pub/sub e filas simples.
4. **Service Mesh** - (opcional) Istio ou Linkerd para gerenciar comunicações internas, segurança e observabilidade.

---

Uma **classe standalone** (ou independente) é uma classe que pode funcionar sozinha, sem depender diretamente de outras classes ou frameworks externos.

### No contexto do Ruby on Rails:

Em Ruby, uma **classe standalone** é uma classe que não herda diretamente de `ActiveRecord::Base` (ou outra classe do Rails) e pode ser usada sem um ambiente Rails completo.

### Exemplo de Classe Standalone em Ruby:

```ruby
ruby
CopiarEditar
class Calculadora
  def soma(a, b)
    a + b
  end
end

calc = Calculadora.new
puts calc.soma(2, 3) # Saída: 5

```

Essa classe **não depende do Rails**, do ActiveRecord ou de outra estrutura externa. Ela pode ser usada em qualquer projeto Ruby.

### Exemplo de Classe Standalone no Rails:

Se você quiser uma classe standalone dentro de um projeto Rails, mas sem herdar de `ApplicationRecord`, pode fazer algo assim:

```ruby
ruby
CopiarEditar
class ConversorTemperatura
  def self.celsius_para_fahrenheit(celsius)
    (celsius * 9.0 / 5) + 32
  end
end

puts ConversorTemperatura.celsius_para_fahrenheit(30) # Saída: 86.0

```

Essa classe pode ser colocada dentro do diretório `app/lib/` no Rails e usada sem precisar de um banco de dados.

---

No Rails, **concern** é uma forma de organizar e reutilizar código em **models** e **controllers**. Ele é um módulo que permite agrupar lógica comum para evitar duplicação, facilitando a manutenção e organização do código.

### Uso principal do **concern**:

1. **Reutilização de código**: Compartilhar lógica entre múltiplos models ou controllers.
2. **Organização**: Separar responsabilidades e manter os arquivos mais limpos.
3. **Facilidade de manutenção**: Evita código duplicado e melhora a modularização.

---

### Como usar concern em models

Os **concerns** de models ficam no diretório `app/models/concerns/` e são incluídos nos models usando `include`.

### Exemplo:

Criando um concern para timestamps personalizados:

```ruby
ruby
CopiarEditar
# app/models/concerns/timestampable.rb
module Timestampable
  extend ActiveSupport::Concern

  included do
    before_create :set_created_at
  end

  def set_created_at
    self.created_at = Time.current
  end
end

```

Agora podemos incluir esse concern em qualquer model:

```ruby
ruby
CopiarEditar
# app/models/user.rb
class User < ApplicationRecord
  include Timestampable
end

```

---

### Como usar concern em controllers

Os **concerns** de controllers ficam no diretório `app/controllers/concerns/` e funcionam de forma similar aos de models.

### Exemplo:

Criando um concern para autenticação:

```ruby
ruby
CopiarEditar
# app/controllers/concerns/authenticatable.rb
module Authenticatable
  extend ActiveSupport::Concern

  included do
    before_action :authenticate_user!
  end

  private

  def authenticate_user!
    redirect_to login_path unless current_user
  end
end

```

Agora podemos incluir esse concern em qualquer controller:

```ruby
ruby
CopiarEditar
# app/controllers/dashboard_controller.rb
class DashboardController < ApplicationController
  include Authenticatable
end

```

---

### Resumo

- **Concerns** ajudam a manter o código DRY (Don't Repeat Yourself).
- Permitem organizar funcionalidades compartilhadas de forma modular.
- Podem ser usados tanto em models quanto em controllers.