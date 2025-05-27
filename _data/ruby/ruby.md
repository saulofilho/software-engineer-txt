---

### **1. Fundamentos Avançados do Ruby**

- Estruturas de Dados (Arrays, Hashes, Sets, Structs)
- Controle de Fluxo (loops, iterators, blocks, procs, lambdas)
- Métodos e escopo (private, protected, public)
- Métodos Singleton e Metaprogramação
- Mixins e Módulos (include, extend, prepend)
- Manipulação de Strings e Expressões Regulares
- Symbols vs Strings
- Gestão de Exceções e Resiliência (rescue, retry, ensure)
- Duck Typing e Polimorfismo

### **2. Orientação a Objetos e Design Patterns**

- Princípios SOLID aplicados ao Ruby
- Design Patterns (Factory, Singleton, Observer, Decorator, Strategy)
- Active Record Pattern e Data Mapper Pattern
- Composição vs Herança no Ruby
- Service Objects e Query Objects

### **3. Performance e Otimização**

- Profiling de Código (Benchmark, `stackprof`, `ruby-prof`)
- Garbage Collection (GC tuning, generational GC)
- Otimização de Queries com ActiveRecord
- Técnicas de caching (memcached, redis)

### **4. Metaprogramação e Reflexão**

- `define_method`, `method_missing` e `respond_to?`
- `send` e `public_send`
- `class_eval` e `instance_eval`
- `method_added`, `included`, `extended` hooks
- DSLs internas e macros

### **5. Concorrência e Paralelismo**

- Threads (`Thread.new`, Mutex, ConditionVariable)
- Fibers e Enumerators
- Processos (`fork`, `Process.spawn`)
- Parallelism (`concurrent-ruby`, Celluloid, Sidekiq)

### **6. Testes e Qualidade de Código**

- RSpec, MiniTest, Capybara
- TDD/BDD
- Mocking e Stubbing (`double`, `allow`, `expect`)
- Cobertura de código com SimpleCov
- Linters e ferramentas de qualidade (RuboCop, Reek, Flay, Brakeman)

### **7. Gems e Ecossistema**

- Criar e publicar gems (`gemspec`, `bundler`, `rake release`)
- Gems essenciais: Pry, Sidekiq, Faraday, Dry-rb, Sorbet, FactoryBot, Devise
- Gerenciamento de Dependências (Bundler, Gemfile.lock)

### **8. Ferramentas e Boas Práticas**

- Code Style Guide do Ruby e Rails
- Estruturas de Logs (`Logger`, `Lograge`, `Structured Logging`)
- Monitoramento e debugging (`byebug`, `pry`, `rack-mini-profiler`)
- Ruby Versions e Gerenciadores (`rbenv`, `rvm`)

---

1.

### **📌 Estruturas de Dados no Ruby**

### **Arrays**

- Criando Arrays:
    
    ```ruby
    ruby
    CopiarEditar
    arr = [1, 2, 3]
    arr = Array.new(3, "ruby") # ["ruby", "ruby", "ruby"]
    
    ```
    
- Métodos úteis:
    
    ```ruby
    ruby
    CopiarEditar
    arr << 4  # Adiciona um elemento ao final
    arr.push(5) # Adiciona ao final
    arr.unshift(0) # Adiciona ao início
    arr.pop  # Remove o último elemento
    arr.shift # Remove o primeiro elemento
    arr.sample # Retorna um elemento aleatório
    arr.map { |n| n * 2 } # Retorna um novo array com os valores multiplicados
    arr.select(&:even?) # Filtra elementos pares
    
    ```
    
- Diferença entre `map` e `each`:
    
    ```ruby
    ruby
    CopiarEditar
    arr.each { |n| n * 2 } # Não altera o array original
    arr.map { |n| n * 2 } # Retorna um novo array com os valores alterados
    
    ```
    

### **Hashes**

- Criando Hashes:
    
    ```ruby
    ruby
    CopiarEditar
    h = { nome: "Alice", idade: 25 }
    h = Hash.new(0) # Valor padrão
    
    ```
    
- Métodos úteis:
    
    ```ruby
    ruby
    CopiarEditar
    h[:cidade] = "São Paulo" # Adiciona chave/valor
    h.delete(:idade) # Remove uma chave
    h.keys # Retorna todas as chaves
    h.values # Retorna todos os valores
    h.each { |chave, valor| puts "#{chave}: #{valor}" } # Iteração
    h.transform_keys(&:to_s) # Transforma todas as chaves em strings
    
    ```
    

### **Sets**

- Útil para armazenar valores únicos (mais eficiente que Arrays para essa finalidade).
    
    ```ruby
    ruby
    CopiarEditar
    require 'set'
    s = Set.new([1, 2, 3, 3])
    s.add(4)
    s.include?(2) # true
    s.delete(3)
    
    ```
    

### **Structs**

- Criar objetos simples sem precisar definir classes.
    
    ```ruby
    ruby
    CopiarEditar
    Pessoa = Struct.new(:nome, :idade)
    p = Pessoa.new("João", 30)
    puts p.nome # João
    
    ```
    

---

### **📌 Controle de Fluxo Avançado**

### **Loops e Iterators**

- `loop do`: Loop infinito
    
    ```ruby
    ruby
    CopiarEditar
    loop do
      puts "Executando..."
      break if rand(10) > 8
    end
    
    ```
    
- `while` e `until`:
    
    ```ruby
    ruby
    CopiarEditar
    i = 0
    while i < 5
      puts i
      i += 1
    end
    
    i = 10
    until i < 5
      puts i
      i -= 1
    end
    
    ```
    
- `for` vs `each`:
    
    ```ruby
    ruby
    CopiarEditar
    for i in 1..5
      puts i
    end
    
    (1..5).each { |i| puts i }
    
    ```
    
- `times`, `upto`, `downto`:
    
    ```ruby
    ruby
    CopiarEditar
    3.times { puts "Olá" }
    1.upto(5) { |n| puts n }
    5.downto(1) { |n| puts n }
    
    ```
    

---

### **📌 Blocks, Procs e Lambdas**

### **Blocks**

- Código passado como argumento de um método:
    
    ```ruby
    ruby
    CopiarEditar
    def executar
      yield if block_given?
    end
    
    executar { puts "Executando um bloco!" }
    
    ```
    
- Passando blocos explícitos (`&block`):
    
    ```ruby
    ruby
    CopiarEditar
    def executar(&bloco)
      bloco.call
    end
    
    executar { puts "Chamando um bloco explicitamente!" }
    
    ```
    

### **Procs**

- São objetos e podem ser armazenados em variáveis:
    
    ```ruby
    ruby
    CopiarEditar
    meu_proc = Proc.new { puts "Sou um Proc!" }
    meu_proc.call
    
    ```
    

### **Lambdas**

- Funcionam como Procs, mas verificam número correto de argumentos:
    
    ```ruby
    ruby
    CopiarEditar
    meu_lambda = ->(nome) { puts "Olá, #{nome}" }
    meu_lambda.call("Alice")
    
    ```
    

---

### **📌 Métodos e Escopo**

### **Escopo de Variáveis**

- `local`: Dentro de métodos e blocos (`nome`)
- `instance`: Usada dentro de objetos (`@nome`)
- `class`: Compartilhada entre instâncias (`@@contagem`)
- `global`: Acessível de qualquer lugar (`$nome` - ⚠️ Evitar uso!)

### **Métodos Private, Protected e Public**

- `public`: Padrão, acessível de qualquer lugar
- `private`: Só pode ser chamado dentro da classe
- `protected`: Pode ser chamado dentro da classe e subclasses

```ruby
class Pessoa
  def initialize(nome)
    @nome = nome
  end

  def falar
    dizer_algo # Método privado chamado internamente
  end

  private

  def dizer_algo
    puts "Olá, meu nome é #{@nome}"
  end
end

p = Pessoa.new("Carlos")
p.falar # OK
p.dizer_algo # ERRO: método privado
```

---

### **📌 Métodos Singleton e Metaprogramação**

- Criando métodos de instância dinamicamente:
    
    ```ruby
    obj = Object.new
    def obj.meu_metodo
      "Método Singleton"
    end
    puts obj.meu_metodo # OK
    ```
    
- `method_missing`: Interceptando chamadas de métodos inexistentes
    
    ```ruby
    class Dynamic
      def method_missing(nome, *args)
        puts "Você chamou #{nome} com #{args}"
      end
    end
    
    d = Dynamic.new
    d.algum_metodo("teste") # "Você chamou algum_metodo com ["teste"]"
    ```
    

---

### **📌 Manipulação de Strings e Expressões Regulares**

- Interpolação e manipulação
    
    ```ruby
    ruby
    CopiarEditar
    nome = "Ruby"
    puts "Olá, #{nome}" # Interpolação
    puts nome.upcase # "RUBY"
    puts nome.downcase # "ruby"
    puts nome.gsub("u", "o") # "Roby"
    
    ```
    
- Expressões Regulares
    
    ```ruby
    ruby
    CopiarEditar
    texto = "O email é contato@email.com"
    regex = /[\w.]+@[\w.]+/
    puts texto.match(regex) # "contato@email.com"
    
    ```
    

---

### **📌 Gestão de Exceções e Resiliência**

- `begin-rescue`
    
    ```ruby
    ruby
    CopiarEditar
    begin
      1 / 0
    rescue ZeroDivisionError => e
      puts "Erro: #{e.message}"
    ensure
      puts "Sempre executa!"
    end
    
    ```
    
- `retry` e `raise`
    
    ```ruby
    ruby
    CopiarEditar
    tentativa = 0
    begin
      tentativa += 1
      raise "Erro!" if tentativa < 3
      puts "Sucesso na tentativa #{tentativa}"
    rescue
      retry if tentativa < 3
    end
    
    ```
    

---

---

## **📌 Duck Typing no Ruby** 🦆

O conceito de **Duck Typing** vem da frase:

*"Se anda como um pato e faz 'quack' como um pato, então deve ser um pato."*

Ou seja, no Ruby, o tipo de um objeto **não importa tanto quanto seu comportamento**. Em vez de verificar explicitamente o tipo de um objeto, verificamos se ele responde aos métodos esperados.

### **Exemplo Clássico: Sem Duck Typing (Ruim)**

```ruby
ruby
CopiarEditar
def fazer_quack(pato)
  if pato.is_a?(Pato)
    pato.quack
  else
    raise "Isso não é um pato!"
  end
end

```

Acima, estamos amarrando nosso código a uma classe específica (`Pato`), o que reduz flexibilidade.

### **Com Duck Typing (Melhor)**

```ruby
ruby
CopiarEditar
def fazer_quack(animal)
  animal.quack
end

class Pato
  def quack
    puts "Quack! 🦆"
  end
end

class Pessoa
  def quack
    puts "Estou imitando um pato! 🗣️"
  end
end

pato = Pato.new
humano = Pessoa.new

fazer_quack(pato)  # Quack! 🦆
fazer_quack(humano) # Estou imitando um pato! 🗣️

```

✅ **Vantagem**: O método `fazer_quack` funciona com qualquer objeto que tenha o método `quack`, sem se preocupar com o tipo.

### **Verificando se um objeto responde a um método**

Se quisermos ser mais seguros, podemos usar `respond_to?`:

```ruby
ruby
CopiarEditar
def fazer_quack(animal)
  if animal.respond_to?(:quack)
    animal.quack
  else
    puts "Isso não sabe fazer quack!"
  end
end

```

Agora, só chamamos `quack` se o objeto realmente tiver esse método.

---

## **📌 Polimorfismo no Ruby** 🏛️

**Polimorfismo** significa "muitas formas" e permite que diferentes classes compartilhem **a mesma interface** (ou conjunto de métodos) sem necessidade de herança.

### **1️⃣ Polimorfismo via Herança**

Aqui, classes diferentes herdam de uma classe base e sobrescrevem métodos.

```ruby
ruby
CopiarEditar
class Animal
  def falar
    "Som genérico"
  end
end

class Cachorro < Animal
  def falar
    "Au au! 🐶"
  end
end

class Gato < Animal
  def falar
    "Miau! 🐱"
  end
end

animais = [Cachorro.new, Gato.new]

animais.each { |animal| puts animal.falar }
# Saída:
# "Au au! 🐶"
# "Miau! 🐱"

```

✅ **Vantagem**: Podemos tratar `Cachorro` e `Gato` como `Animal` sem se preocupar com suas classes específicas.

---

### **2️⃣ Polimorfismo via Duck Typing (Sem Herança)**

O Ruby permite polimorfismo sem herança, apenas exigindo que os objetos implementem um mesmo método.

```ruby
ruby
CopiarEditar
class Email
  def enviar
    puts "Enviando email... 📧"
  end
end

class SMS
  def enviar
    puts "Enviando SMS... 📲"
  end
end

class NotificacaoPush
  def enviar
    puts "Enviando Push Notification... 🔔"
  end
end

# Método genérico que aceita qualquer objeto que tenha 'enviar'
def notificar(metodo)
  metodo.enviar
end

notificar(Email.new)  # Enviando email...
notificar(SMS.new)    # Enviando SMS...
notificar(NotificacaoPush.new) # Enviando Push Notification...

```

✅ **Vantagem**: Qualquer classe que tenha `enviar` pode ser usada sem precisar de uma hierarquia de herança.

---

### **Conclusão**

1. **Duck Typing** permite criar código mais flexível ao focar no comportamento dos objetos, não em sua classe.
2. **Polimorfismo** ajuda a criar código reutilizável e extensível, seja via herança ou via Duck Typing.

---

# **📌 2. Orientação a Objetos e Design Patterns**

## **1️⃣ Princípios SOLID no Ruby**

Os princípios SOLID ajudam a escrever código limpo, modular e extensível.

### **✅ S — Single Responsibility Principle (SRP)**

*"Uma classe deve ter apenas uma única razão para mudar."*

**❌ Exemplo ruim (múltiplas responsabilidades):**

```ruby
ruby
CopiarEditar
class Relatorio
  def gerar
    puts "Gerando relatório..."
  end

  def salvar_no_banco
    puts "Salvando no banco de dados..."
  end
end

```

Essa classe faz **duas coisas**: gera e salva um relatório.

**✅ Exemplo bom (separando responsabilidades):**

```ruby
ruby
CopiarEditar
class GeradorDeRelatorio
  def gerar
    puts "Gerando relatório..."
  end
end

class SalvarRelatorio
  def salvar
    puts "Salvando no banco de dados..."
  end
end

```

Agora cada classe tem **apenas uma responsabilidade**.

---

### **✅ O — Open/Closed Principle (OCP)**

*"Uma classe deve estar aberta para extensão, mas fechada para modificação."*

**❌ Exemplo ruim (modificando a classe sempre que um novo tipo de relatório aparece):**

```ruby
ruby
CopiarEditar
class Relatorio
  def gerar(tipo)
    if tipo == :pdf
      puts "Gerando PDF..."
    elsif tipo == :csv
      puts "Gerando CSV..."
    end
  end
end

```

A cada novo formato, precisamos modificar a classe.

**✅ Exemplo bom (uso de herança para extensão):**

```ruby
ruby
CopiarEditar
class Relatorio
  def gerar
    raise "Deve ser implementado pela subclasse"
  end
end

class RelatorioPDF < Relatorio
  def gerar
    puts "Gerando PDF..."
  end
end

class RelatorioCSV < Relatorio
  def gerar
    puts "Gerando CSV..."
  end
end

```

Agora podemos adicionar novos tipos de relatórios **sem modificar** a classe original.

---

### **✅ L — Liskov Substitution Principle (LSP)**

*"Se uma classe filha substitui a classe pai, ela deve manter o comportamento esperado."*

**❌ Exemplo ruim (classe filha alterando o comportamento da classe pai):**

```ruby
ruby
CopiarEditar
class Ave
  def voar
    puts "Voando..."
  end
end

class Pinguim < Ave
end

pinguim = Pinguim.new
pinguim.voar  # ❌ ERRO! Pinguins não voam

```

A classe `Pinguim` **não deveria herdar** de `Ave` se não consegue voar.

**✅ Exemplo bom (corrigindo com composição):**

```ruby
ruby
CopiarEditar
class Ave
end

class Voador
  def voar
    puts "Voando..."
  end
end

class Pinguim < Ave
end

class Andorinha < Ave
  include Voador
end

Andorinha.new.voar # "Voando..."

```

Agora, só **aves que voam** têm o comportamento de voo.

---

### **✅ I — Interface Segregation Principle (ISP)**

*"Uma classe não deve ser forçada a implementar métodos que não usa."*

**❌ Exemplo ruim (classe forçada a implementar métodos irrelevantes):**

```ruby
ruby
CopiarEditar
class Trabalhador
  def programar
    raise "Deve ser implementado"
  end

  def atender_clientes
    raise "Deve ser implementado"
  end
end

class Desenvolvedor < Trabalhador
  def programar
    puts "Codando..."
  end

  def atender_clientes
    puts "Fazendo atendimento técnico..." # 😬 Ruim!
  end
end

```

A classe `Desenvolvedor` **não deveria ter que implementar** `atender_clientes`.

**✅ Exemplo bom (criando interfaces separadas):**

```ruby
ruby
CopiarEditar
module Programador
  def programar
    puts "Codando..."
  end
end

module Atendimento
  def atender_clientes
    puts "Falando com clientes..."
  end
end

class Desenvolvedor
  include Programador
end

class Suporte
  include Atendimento
end

```

Agora cada classe implementa **apenas o que precisa**.

---

### **✅ D — Dependency Inversion Principle (DIP)**

*"Módulos de alto nível não devem depender de módulos de baixo nível diretamente."*

**❌ Exemplo ruim (dependência direta em uma classe específica):**

```ruby
ruby
CopiarEditar
class MySQLDatabase
  def salvar
    puts "Salvando no MySQL..."
  end
end

class Servico
  def initialize
    @banco = MySQLDatabase.new
  end

  def salvar_dados
    @banco.salvar
  end
end

```

O `Servico` depende diretamente do `MySQLDatabase`, dificultando a troca para outro banco.

**✅ Exemplo bom (uso de abstração para independência):**

```ruby
ruby
CopiarEditar
class Database
  def salvar
    raise "Deve ser implementado"
  end
end

class MySQLDatabase < Database
  def salvar
    puts "Salvando no MySQL..."
  end
end

class Servico
  def initialize(banco)
    @banco = banco
  end

  def salvar_dados
    @banco.salvar
  end
end

banco = MySQLDatabase.new
Servico.new(banco).salvar_dados # "Salvando no MySQL..."

```

Agora podemos trocar `MySQLDatabase` por qualquer outro banco **sem modificar o código da `Servico`**.

---

## **2️⃣ Design Patterns no Ruby**

### **✅ Factory Pattern**

Facilita a criação de objetos sem expor a lógica de instância.

```ruby
ruby
CopiarEditar
class Animal
  def falar
    raise "Deve ser implementado"
  end
end

class Cachorro < Animal
  def falar
    "Au au!"
  end
end

class Gato < Animal
  def falar
    "Miau!"
  end
end

class AnimalFactory
  def self.criar(tipo)
    case tipo
    when :cachorro then Cachorro.new
    when :gato then Gato.new
    else raise "Tipo desconhecido"
    end
  end
end

animal = AnimalFactory.criar(:cachorro)
puts animal.falar # "Au au!"

```

---

### **✅ Singleton Pattern**

Garante que apenas **uma instância** da classe seja criada.

```ruby
ruby
CopiarEditar
require 'singleton'

class Configuracao
  include Singleton

  attr_accessor :tema

  def initialize
    @tema = "Escuro"
  end
end

config1 = Configuracao.instance
config2 = Configuracao.instance

puts config1.object_id == config2.object_id # true (mesmo objeto)

```

---

### **✅ Observer Pattern**

Permite que múltiplos objetos sejam notificados quando algo acontece.

```ruby
ruby
CopiarEditar
class Publicador
  attr_reader :observadores

  def initialize
    @observadores = []
  end

  def adicionar_observador(observador)
    @observadores << observador
  end

  def notificar
    @observadores.each(&:atualizar)
  end
end

class Assinante
  def atualizar
    puts "Recebi uma atualização!"
  end
end

noticia = Publicador.new
joao = Assinante.new

noticia.adicionar_observador(joao)
noticia.notificar # "Recebi uma atualização!"

```

---

# **📌 3. Performance e Otimização** 🚀

A otimização de performance no Ruby envolve **profiling de código, garbage collection tuning, otimização de queries e técnicas de caching**. Vamos explorar cada um desses tópicos em detalhes.

---

## **1️⃣ Profiling de Código (Benchmark, stackprof, ruby-prof)**

O primeiro passo para otimizar o código é **descobrir onde estão os gargalos**. Para isso, usamos ferramentas de **profiling** que analisam tempo de execução e consumo de CPU/memória.

### **✅ Benchmark (Medição Simples de Tempo)**

O módulo `Benchmark` é útil para medir o tempo de execução de um bloco de código.

```ruby
ruby
CopiarEditar
require 'benchmark'

tempo = Benchmark.measure do
  100_000.times { "Ruby".reverse }
end

puts tempo.real  # Tempo total em segundos

```

✅ **Quando usar?**

- Comparar métodos diferentes e escolher o mais rápido.
- Medir tempo total de execução de partes específicas do código.

---

### **✅ stackprof (Profiling de CPU e Memória)**

O **stackprof** é útil para detectar onde o código está gastando mais tempo.

**Instalação:**

```
gem install stackprof

```

**Uso:**

```ruby
ruby
CopiarEditar
require 'stackprof'

StackProf.run(mode: :cpu, out: 'stackprof.dump') do
  1_000_000.times { "Ruby".reverse }
end

```

Depois, analisamos o relatório gerado:

```
stackprof stackprof.dump --text

```

✅ **Quando usar?**

- Identificar quais métodos estão consumindo mais CPU.
- Encontrar gargalos específicos dentro do código.

---

### **✅ ruby-prof (Profiling Detalhado)**

O `ruby-prof` fornece um relatório detalhado de tempo de CPU, chamadas de método e uso de memória.

**Instalação:**

```
gem install ruby-prof

```

**Uso:**

```ruby
ruby
CopiarEditar
require 'ruby-prof'

RubyProf.start
100_000.times { "Ruby".reverse }
result = RubyProf.stop

# Exibir o relatório no terminal
RubyProf::FlatPrinter.new(result).print(STDOUT)

```

✅ **Quando usar?**

- Precisa de um perfil detalhado de execução.
- Descobrir quais métodos estão gastando mais tempo.

---

## **2️⃣ Garbage Collection (GC tuning, generational GC)**

O **Garbage Collector (GC)** do Ruby remove objetos não utilizados para liberar memória. Porém, rodá-lo muitas vezes pode prejudicar a performance.

### **✅ Como funciona o GC no Ruby?**

- Ruby usa um **GC generacional**:
    - **Objetos jovens** são coletados rapidamente.
    - **Objetos antigos** são verificados com menos frequência.
- O GC roda automaticamente, mas pode ser ajustado.

### **✅ Otimizando o GC**

Podemos ajustar as variáveis de ambiente para melhorar a performance.

```
export RUBY_GC_HEAP_OLDOBJECT_LIMIT_FACTOR=2

```

Isso faz com que o GC colete objetos antigos **com menos frequência**, reduzindo pausas na execução.

Também podemos **forçar a execução do GC manualmente** (com cuidado!):

```ruby
ruby
CopiarEditar
GC.start

```

✅ **Quando otimizar o GC?**

- Aplicações com **muita alocação e liberação de objetos**.
- Reduzir pausas do GC em **aplicações de tempo real**.

---

## **3️⃣ Otimização de Queries com ActiveRecord**

O ActiveRecord do Rails pode gerar queries ineficientes se não for bem utilizado.

### **✅ Evitar N+1 Queries**

**Problema:**

```ruby
ruby
CopiarEditar
Post.all.each do |post|
  puts post.comments.count
end

```

Isso gera **uma query para buscar os posts + uma query para cada post** (N+1 queries).

**Solução:**

```ruby
ruby
CopiarEditar
Post.includes(:comments).each do |post|
  puts post.comments.count
end

```

Agora, o ActiveRecord faz **apenas duas queries**:

- Uma para buscar os posts.
- Outra para buscar os comentários de todos os posts.

---

### **✅ Usar `select` para evitar carga excessiva**

Se não precisarmos de todos os campos de uma tabela, podemos otimizar a query:

```ruby
ruby
CopiarEditar
User.select(:id, :name).where(active: true)

```

Isso evita carregar colunas desnecessárias.

---

### **✅ Índices no Banco de Dados**

Adicionar índices melhora a performance das buscas.

```ruby
ruby
CopiarEditar
class AddIndexToUsers < ActiveRecord::Migration[6.0]
  def change
    add_index :users, :email, unique: true
  end
end

```

✅ **Quando otimizar queries?**

- Se notar **queries lentas no banco**.
- Se o **N+1 Query Problem** estiver impactando a aplicação.
- Se tabelas grandes estiverem **sem índices**.

---

## **4️⃣ Técnicas de Caching (memcached, redis)**

Caching reduz o tempo de resposta armazenando dados frequentemente acessados.

### **✅ Fragment Caching (Rails)**

Podemos armazenar partes de views no cache para melhorar performance.

```
erb
CopiarEditar
<% cache @article do %>
  <h1><%= @article.title %></h1>
  <p><%= @article.body %></p>
<% end %>

```

Isso evita processar a mesma view toda vez.

---

### **✅ Memcached**

**Instalação:**

```
brew install memcached
gem install dalli

```

**Configuração no Rails (`config/environments/production.rb`)**:

```ruby
ruby
CopiarEditar
config.cache_store = :mem_cache_store, "localhost"

```

**Uso no código:**

```ruby
ruby
CopiarEditar
Rails.cache.write("chave", "valor", expires_in: 5.minutes)
Rails.cache.read("chave")

```

✅ **Quando usar?**

- Melhorar tempo de resposta de aplicações Rails.
- Evitar processamento repetitivo de dados frequentemente usados.

---

### **✅ Redis (Caching e Background Jobs)**

**Instalação:**

```
brew install redis
gem install redis

```

**Configuração no Rails (`config/environments/production.rb`)**:

```ruby
ruby
CopiarEditar
config.cache_store = :redis_cache_store, { url: "redis://localhost:6379/0" }

```

**Uso no código:**

```ruby
ruby
CopiarEditar
Rails.cache.write("user_1", { nome: "João" }, expires_in: 10.minutes)
Rails.cache.read("user_1")

```

✅ **Quando usar?**

- Cache de alta performance para dados dinâmicos.
- Background jobs no Sidekiq (que usa Redis).

---

## **📌 Conclusão**

1. **Profiling de Código**
    - `Benchmark` para medições simples.
    - `stackprof` para profiling de CPU/memória.
    - `ruby-prof` para análise detalhada de performance.
2. **Garbage Collection (GC tuning)**
    - Ruby usa GC generacional.
    - Ajustes no GC podem reduzir pausas e melhorar performance.
3. **Otimização de Queries no ActiveRecord**
    - **Evitar N+1 queries** com `includes`.
    - **Usar `select`** para carregar menos dados.
    - **Criar índices no banco** para buscas rápidas.
4. **Caching (memcached, Redis)**
    - **Fragment Caching** no Rails.
    - **Memcached** para armazenar dados frequentemente acessados.
    - **Redis** para cache rápido e background jobs.

---

# **📌 4. Metaprogramação e Reflexão** 🚀

Metaprogramação no Ruby permite **modificar classes e métodos em tempo de execução**, criar **DSLs (Domain-Specific Languages)** e até definir código dinamicamente.

---

## **1️⃣ `define_method`, `method_missing` e `respond_to?`**

### **✅ `define_method` (Criando Métodos Dinamicamente)**

Usamos `define_method` para **criar métodos em tempo de execução** dentro de uma classe.

```ruby
ruby
CopiarEditar
class Pessoa
  [:nome, :idade, :cidade].each do |atributo|
    define_method(atributo) do
      instance_variable_get("@#{atributo}")
    end

    define_method("#{atributo}=") do |valor|
      instance_variable_set("@#{atributo}", valor)
    end
  end
end

p = Pessoa.new
p.nome = "João"
p.idade = 30

puts p.nome  # "João"
puts p.idade # 30

```

✅ **Quando usar?**

- Criar métodos dinamicamente para reduzir repetição.
- Implementar **APIs dinâmicas**.

---

### **✅ `method_missing` (Interceptando Chamadas de Método Inexistentes)**

Chamado quando um método **não existe**.

```ruby
ruby
CopiarEditar
class Config
  def method_missing(nome, *args)
    if nome.to_s.start_with?("get_")
      chave = nome.to_s.split("_", 2).last
      puts "Buscando configuração: #{chave}"
    else
      super
    end
  end
end

config = Config.new
config.get_database # "Buscando configuração: database"
config.get_api_key  # "Buscando configuração: api_key"

```

**⚠️ Cuidado!**

- Pode dificultar debugging.
- Sempre chame `super` para métodos que não deseja interceptar.

---

### **✅ `respond_to?` (Verificando Se um Método Existe)**

Usado para evitar erros ao chamar métodos desconhecidos.

```ruby
ruby
CopiarEditar
class Exemplo
  def teste
    "ok"
  end
end

e = Exemplo.new
puts e.respond_to?(:teste)        # true
puts e.respond_to?(:nao_existe)   # false

```

✅ **Quando usar?**

- Evitar chamadas a `method_missing` em métodos inválidos.
- Melhor compatibilidade com bibliotecas externas.

---

## **2️⃣ `send` e `public_send`**

### **✅ `send` (Chamando Métodos de Forma Dinâmica)**

Podemos chamar métodos mesmo sem conhecê-los antecipadamente.

```ruby
ruby
CopiarEditar
class Pessoa
  def saudacao
    "Olá!"
  end
end

pessoa = Pessoa.new
puts pessoa.send(:saudacao) # "Olá!"

```

**⚠️ `send` ignora visibilidade!**

```ruby
ruby
CopiarEditar
class Exemplo
  private
  def segredo
    "Não deveria ser acessível!"
  end
end

e = Exemplo.new
puts e.send(:segredo) # "Não deveria ser acessível!"

```

### **✅ `public_send` (Respeita a Visibilidade do Método)**

Para **evitar chamar métodos privados**, use `public_send`.

```ruby
ruby
CopiarEditar
puts e.public_send(:segredo) # Erro: método privado

```

✅ **Quando usar?**

- `send`: Quando precisa acessar métodos privados (com cautela).
- `public_send`: Quando só precisa de métodos públicos.

---

## **3️⃣ `class_eval` e `instance_eval`**

### **✅ `class_eval` (Modificando Classes em Tempo de Execução)**

Permite adicionar métodos ou modificar classes **de fora dela**.

```ruby
ruby
CopiarEditar
class Pessoa; end

Pessoa.class_eval do
  def falar
    "Oi!"
  end
end

puts Pessoa.new.falar # "Oi!"

```

✅ **Quando usar?**

- Adicionar métodos a uma classe dinamicamente.

---

### **✅ `instance_eval` (Modificando Apenas uma Instância)**

Altera **apenas um objeto específico**.

```ruby
ruby
CopiarEditar
p = Pessoa.new

p.instance_eval do
  def segredo
    "Segredo só para esta instância!"
  end
end

puts p.segredo # "Segredo só para esta instância!"

```

✅ **Quando usar?**

- Modificar **apenas uma instância**, sem impactar toda a classe.

---

## **4️⃣ `method_added`, `included`, `extended` Hooks**

### **✅ `method_added` (Intercepta a Definição de Métodos)**

Executa código sempre que um novo método for definido.

```ruby
ruby
CopiarEditar
class Teste
  def self.method_added(nome)
    puts "Método #{nome} foi adicionado!"
  end

  def ola
    puts "Oi!"
  end
end

# "Método ola foi adicionado!"

```

✅ **Quando usar?**

- Logar criação de métodos.
- Aplicar restrições em tempo de execução.

---

### **✅ `included` e `extended` (Executando Código ao Incluir um Módulo)**

**`included`** → Chamado quando um módulo é **incluído** em uma classe.

**`extended`** → Chamado quando um módulo é **extendido** por uma classe.

```ruby
ruby
CopiarEditar
module MeuModulo
  def self.included(base)
    puts "#{base} incluiu #{self}"
  end

  def self.extended(base)
    puts "#{base} estendeu #{self}"
  end
end

class MinhaClasse
  include MeuModulo
end
# "MinhaClasse incluiu MeuModulo"

obj = Object.new
obj.extend(MeuModulo)
# "#<Object:0x00007ff> estendeu MeuModulo"

```

✅ **Quando usar?**

- **Executar lógica** quando um módulo for incluído/extendido.
- Criar **DSLs que configuram classes dinamicamente**.

---

## **5️⃣ DSLs Internas e Macros**

DSLs (Domain-Specific Languages) permitem criar APIs elegantes no Ruby.

### **✅ Exemplo de DSL (Simulação de Configuração)**

```ruby
ruby
CopiarEditar
class Config
  def self.definir(nome, valor)
    define_method(nome) { valor }
  end
end

class AppConfig < Config
  definir :app_name, "MeuApp"
  definir :versao, "1.0.0"
end

config = AppConfig.new
puts config.app_name # "MeuApp"
puts config.versao   # "1.0.0"

```

✅ **Quando usar?**

- Criar APIs elegantes, como o `ActiveRecord`.

---

### **✅ Macros (Definição de Métodos de Forma Elegante)**

```ruby
ruby
CopiarEditar
class MeuModelo
  def self.campo(nome)
    define_method(nome) do
      instance_variable_get("@#{nome}")
    end

    define_method("#{nome}=") do |valor|
      instance_variable_set("@#{nome}", valor)
    end
  end
end

class Usuario < MeuModelo
  campo :nome
  campo :email
end

u = Usuario.new
u.nome = "João"
puts u.nome # "João"

```

✅ **Quando usar?**

- Criar DSLs elegantes no estilo Rails.

---

# **📌 Conclusão**

1. **Métodos Dinâmicos**
    - `define_method`: Cria métodos dinamicamente.
    - `method_missing`: Intercepta chamadas de métodos inexistentes.
    - `respond_to?`: Verifica se um método existe.
2. **Execução Dinâmica**
    - `send`: Chama métodos dinamicamente (inclui privados).
    - `public_send`: Chama métodos públicos dinamicamente.
3. **Avaliação de Código**
    - `class_eval`: Modifica classes.
    - `instance_eval`: Modifica uma única instância.
4. **Hooks e Callbacks**
    - `method_added`: Executa código ao definir um método.
    - `included` e `extended`: Executam código ao incluir módulos.
5. **DSLs e Macros**
    - Criam APIs elegantes e flexíveis.

---

# **📌 5. Concorrência e Paralelismo** 🚀

Concorrência permite que múltiplas tarefas rodem simultaneamente, enquanto paralelismo permite que rodem **ao mesmo tempo em múltiplos núcleos de CPU**.

---

## **1️⃣ Threads (`Thread.new`, `Mutex`, `ConditionVariable`)**

Threads permitem **executar tarefas concorrentes** dentro do mesmo processo.

### **✅ Criando Threads Simples (`Thread.new`)**

```ruby
ruby
CopiarEditar
threads = []

5.times do |i|
  threads << Thread.new do
    sleep(rand(1..3))
    puts "Thread #{i} terminou!"
  end
end

threads.each(&:join)

```

**⚠️ Problema:** Sem controle, múltiplas threads podem acessar os mesmos dados ao mesmo tempo, causando **race conditions**.

---

### **✅ `Mutex` (Evitando Condições de Corrida)**

O **Mutex (Mutual Exclusion)** impede que múltiplas threads acessem um recurso simultaneamente.

```ruby
ruby
CopiarEditar
mutex = Mutex.new
saldo = 100

threads = 5.times.map do
  Thread.new do
    mutex.synchronize do
      temp = saldo
      sleep(0.1)  # Simulando um atraso
      saldo = temp - 10
    end
  end
end

threads.each(&:join)
puts "Saldo final: #{saldo}"  # Saldo correto!

```

✅ **Quando usar?**

- Proteger **recursos compartilhados** contra condições de corrida.

---

### **✅ `ConditionVariable` (Controle de Sincronização entre Threads)**

Usamos `ConditionVariable` para **permitir que uma thread espere um evento** antes de continuar.

```ruby
ruby
CopiarEditar
mutex = Mutex.new
cond_var = ConditionVariable.new
pronto = false

produtor = Thread.new do
  mutex.synchronize do
    sleep 2
    pronto = true
    cond_var.signal
  end
end

consumidor = Thread.new do
  mutex.synchronize do
    cond_var.wait(mutex) until pronto
    puts "Consumidor recebeu o sinal!"
  end
end

[produtor, consumidor].each(&:join)

```

✅ **Quando usar?**

- Quando uma **thread depende de outra para continuar**.

---

## **2️⃣ Fibers e Enumerators**

**Fibers** são **corrotinas leves** que oferecem mais controle que threads, permitindo **pausar e retomar manualmente a execução**.

### **✅ Criando um Fiber**

```ruby
ruby
CopiarEditar
fiber = Fiber.new do
  puts "Iniciando Fiber"
  Fiber.yield
  puts "Continuando Fiber"
end

fiber.resume  # "Iniciando Fiber"
fiber.resume  # "Continuando Fiber"

```

**⚠️ Limitação:** Diferente de threads, Fibers **não são concorrentes**, mas sim **cooperativos** (executam quando chamados).

---

### **✅ Enumerators como Geradores (Lazy Evaluation)**

Podemos usar `Enumerator` para **processar grandes volumes de dados** sem carregar tudo na memória.

```ruby
ruby
CopiarEditar
enumerator = Enumerator.new do |yielder|
  10.times do |i|
    sleep(1)
    yielder << i
  end
end

puts enumerator.next  # 0
puts enumerator.next  # 1

```

✅ **Quando usar?**

- Para processar **streams de dados grandes sem ocupar muita memória**.

---

## **3️⃣ Processos (`fork`, `Process.spawn`)**

Diferente das threads, que compartilham memória, **processos são independentes**, cada um com seu próprio espaço de memória.

### **✅ `fork` (Criando um Novo Processo)**

```ruby
ruby
CopiarEditar
pid = fork do
  puts "Processo filho rodando (PID: #{Process.pid})"
  sleep 2
end

puts "Processo pai esperando filho (PID: #{pid})"
Process.wait(pid)  # Aguarda o processo filho terminar

```

✅ **Quando usar?**

- Para **executar tarefas em paralelo sem problemas de compartilhamento de memória**.

---

### **✅ `Process.spawn` (Executar Comandos Externos sem Bloquear)**

Diferente de `fork`, `Process.spawn` **não bloqueia a execução do programa principal**.

```ruby
ruby
CopiarEditar
pid = Process.spawn("sleep 5")
puts "Processo #{pid} iniciado"
Process.wait(pid)
puts "Processo #{pid} terminou"

```

✅ **Quando usar?**

- Para rodar **processos externos** sem bloquear o código Ruby.

---

## **4️⃣ Paralelismo (Concurrent-ruby, Celluloid, Sidekiq)**

Como Ruby tem **GIL**, precisamos de **gems externas** para rodar código realmente em paralelo.

---

### **✅ `concurrent-ruby` (Thread Pool)**

`concurrent-ruby` permite **executar tarefas em paralelo usando um pool de threads**.

**Instalação:**

```
gem install concurrent-ruby

```

**Uso:**

```ruby
ruby
CopiarEditar
require 'concurrent'

pool = Concurrent::FixedThreadPool.new(5)

10.times do |i|
  pool.post { puts "Tarefa #{i} executada na thread #{Thread.current}" }
end

pool.shutdown
pool.wait_for_termination

```

✅ **Quando usar?**

- Para **executar muitas tarefas simultaneamente sem criar milhares de threads**.

---

### **✅ Sidekiq (Processamento de Background com Redis)**

Sidekiq usa **processos separados** para rodar jobs de background paralelamente.

**Instalação:**

```
gem install sidekiq

```

**Definição de um job:**

```ruby
ruby
CopiarEditar
class MeuJob
  include Sidekiq::Worker

  def perform(nome)
    puts "Processando #{nome}"
  end
end

```

**Execução do job:**

```ruby
ruby
CopiarEditar
MeuJob.perform_async("Tarefa 1")

```

✅ **Quando usar?**

- Para **tarefas assíncronas** como envio de e-mails, processamento de imagens, etc.

---

# **📌 Conclusão**

1. **Threads (Concorrência no Mesmo Processo)**
    - `Thread.new`: Cria threads concorrentes.
    - `Mutex`: Evita race conditions.
    - `ConditionVariable`: Coordena a execução entre threads.
2. **Fibers (Corrotinas Leves)**
    - Permitem **pausar e retomar** código manualmente.
    - Úteis para **processamento assíncrono de dados**.
3. **Processos (Paralelismo Real)**
    - `fork`: Cria um processo filho.
    - `Process.spawn`: Executa comandos externos.
4. **Bibliotecas de Paralelismo**
    - `concurrent-ruby`: Pool de threads eficiente.
    - `Sidekiq`: Jobs de background com Redis.

---

# **📌 6. Testes e Qualidade de Código** 🚀

Ruby tem um **ecossistema forte de testes**, e escrever **código testável** é essencial para garantir manutenibilidade e evitar bugs.

---

## **1️⃣ RSpec, MiniTest, Capybara**

### **✅ RSpec (Framework de Testes Mais Usado)**

RSpec é **descritivo e expressivo**, ideal para TDD e BDD.

📌 **Instalação:**

```
gem install rspec
rspec --init

```

📌 **Testando uma Classe com RSpec:**

```ruby
ruby
CopiarEditar
# lib/calculadora.rb
class Calculadora
  def soma(a, b)
    a + b
  end
end

```

```ruby
ruby
CopiarEditar
# spec/calculadora_spec.rb
require_relative '../lib/calculadora'

RSpec.describe Calculadora do
  it "soma dois números corretamente" do
    calc = Calculadora.new
    expect(calc.soma(2, 3)).to eq(5)
  end
end

```

📌 **Rodando os testes:**

```
rspec

```

✅ **Por que usar?**

- DSL legível.
- Fácil integração com Mocking e Stubbing.

---

### **✅ MiniTest (Incluso no Ruby, Alternativa ao RSpec)**

```ruby
ruby
CopiarEditar
require 'minitest/autorun'

class TestCalculadora < Minitest::Test
  def test_soma
    assert_equal 5, Calculadora.new.soma(2, 3)
  end
end

```

✅ **Quando usar?**

- Quando quer **tests minimalistas e rápidos** sem dependências extras.

---

### **✅ Capybara (Testes de Integração e E2E)**

Capybara é usado para **testes de interface simulando um usuário real**.

📌 **Instalação:**

```
gem install capybara

```

📌 **Exemplo de Teste de UI:**

```ruby
ruby
CopiarEditar
require 'capybara/rspec'

Capybara.app = MeuApp

describe "Página Inicial", type: :feature do
  it "exibe o título corretamente" do
    visit '/'
    expect(page).to have_content("Bem-vindo")
  end
end

```

✅ **Quando usar?**

- Testar **fluxos de usuário** no navegador.

---

## **2️⃣ TDD e BDD (Test-Driven Development e Behavior-Driven Development)**

### **✅ TDD (Test-Driven Development)**

Fluxo de TDD:

1. **Escreva um teste que falha**.
2. **Implemente a funcionalidade mínima para passar no teste**.
3. **Refatore o código sem quebrar os testes**.

📌 **Exemplo de TDD em Ação:**

```ruby
ruby
CopiarEditar
# Escrevemos o teste primeiro
it "retorna verdadeiro se o número é par" do
  expect(Numero.par?(4)).to be true
end

```

```ruby
ruby
CopiarEditar
# Implementamos o código depois
class Numero
  def self.par?(num)
    num.even?
  end
end

```

### **✅ BDD (Behavior-Driven Development)**

BDD se foca no **comportamento do sistema**.

```ruby
ruby
CopiarEditar
describe "Login de Usuário" do
  it "permite um usuário válido fazer login" do
    usuario = Usuario.new("email@example.com", "senha123")
    expect(usuario.login).to eq("Bem-vindo!")
  end
end

```

✅ **Quando usar?**

- **TDD** para código bem estruturado e fácil de testar.
- **BDD** para descrever comportamento esperado de forma clara.

---

## **3️⃣ Mocking e Stubbing (`double`, `allow`, `expect`)**

Mocking e Stubbing são usados para **simular comportamentos de objetos sem precisar de implementações reais**.

### **✅ Criando um Mock (`double`)**

```ruby
ruby
CopiarEditar
usuario = double("Usuario", nome: "João")
puts usuario.nome  # "João"

```

### **✅ Stubbing (`allow`)**

```ruby
ruby
CopiarEditar
allow(usuario).to receive(:idade).and_return(30)
puts usuario.idade  # 30

```

### **✅ Expectativas (`expect`)**

```ruby
ruby
CopiarEditar
expect(usuario).to receive(:salvar)
usuario.salvar

```

✅ **Quando usar?**

- Quando **não queremos chamar dependências reais** (ex: API externa, banco de dados).

---

## **4️⃣ Cobertura de Código com SimpleCov**

SimpleCov **mede o quanto do código está coberto por testes**.

📌 **Instalação:**

```
gem install simplecov

```

📌 **Configuração no `spec_helper.rb`:**

```ruby
ruby
CopiarEditar
require 'simplecov'
SimpleCov.start

```

📌 **Rodando os testes e gerando o relatório:**

```
rspec
open coverage/index.html

```

✅ **Quando usar?**

- Para garantir que **testamos todas as partes críticas do código**.

---

## **5️⃣ Linters e Ferramentas de Qualidade**

### **✅ RuboCop (Padrão de Código e Best Practices)**

📌 **Instalação:**

```
gem install rubocop

```

📌 **Rodando:**

```
rubocop

```

📌 **Corrigindo automaticamente:**

```
rubocop -A

```

✅ **Quando usar?**

- Para **manter o código limpo e idiomático**.

---

### **✅ Reek (Detecta "Code Smells")**

📌 **Instalação:**

```
gem install reek

```

📌 **Rodando:**

```
reek

```

✅ **Quando usar?**

- Identificar **código complexo e difícil de manter**.

---

### **✅ Flay (Detecta Código Duplicado)**

📌 **Instalação:**

```
gem install flay

```

📌 **Rodando:**

```
flay lib/

```

✅ **Quando usar?**

- Para **reduzir código repetitivo e melhorar manutenibilidade**.

---

### **✅ Brakeman (Verificação de Segurança para Rails)**

📌 **Instalação:**

```
gem install brakeman

```

📌 **Rodando:**

```
brakeman

```

✅ **Quando usar?**

- Para **identificar vulnerabilidades de segurança no Rails**.

---

# **📌 Conclusão**

1. **Testes Automatizados**
    - `RSpec`: Testes unitários e BDD.
    - `MiniTest`: Alternativa minimalista.
    - `Capybara`: Testes de interface.
2. **TDD e BDD**
    - TDD → **Escreve testes antes do código**.
    - BDD → **Foca no comportamento esperado**.
3. **Mocking e Stubbing**
    - `double`: Criar mocks.
    - `allow`: Definir comportamento falso.
    - `expect`: Verificar chamadas esperadas.
4. **Cobertura de Código**
    - SimpleCov mede a **cobertura dos testes**.
5. **Ferramentas de Qualidade**
    - **RuboCop**: Corrige código ruim.
    - **Reek**: Encontra código com "cheiro ruim".
    - **Flay**: Detecta código duplicado.
    - **Brakeman**: Segurança em Rails.

---

# **📌 7. Gems e Ecossistema** 🚀

O ecossistema Ruby é fortemente impulsionado por **gems** – bibliotecas reutilizáveis que adicionam funcionalidades ao código.

---

## **1️⃣ Criando e Publicando Gems**

Ruby permite criar suas próprias gems e publicá-las no [RubyGems.org](https://rubygems.org/).

### **✅ Criando uma Gem do Zero**

📌 **Gerando o esqueleto do projeto com `bundle gem`**

```
bundle gem minha_gem

```

📌 **Isso cria a estrutura:**

```
b
minha_gem/
│── lib/                 # Código principal
│   └── minha_gem.rb
│── minha_gem.gemspec    # Especificações da gem
│── Rakefile             # Tarefas automáticas
│── README.md            # Documentação
│── Gemfile              # Dependências

```

---

### **✅ Configurando o `.gemspec`**

O arquivo `.gemspec` define as configurações da gem.

```ruby
ruby
CopiarEditar
Gem::Specification.new do |spec|
  spec.name          = "minha_gem"
  spec.version       = "0.1.0"
  spec.authors       = ["Seu Nome"]
  spec.summary       = "Uma gem incrível!"
  spec.files         = Dir["lib/**/*.rb"]
  spec.required_ruby_version = ">= 2.7"
  spec.add_dependency "faraday", "~> 2.0"
end

```

---

### **✅ Construindo e Instalando a Gem Localmente**

```
gem build minha_gem.gemspec
gem install minha_gem-0.1.0.gem

```

---

### **✅ Publicando no RubyGems**

📌 **Crie uma conta no [RubyGems](https://rubygems.org/)** e rode:

```
gem push minha_gem-0.1.0.gem

```

🚀 Agora sua gem está publicada!

---

## **2️⃣ Gems Essenciais para um Desenvolvedor Ruby**

Aqui estão **gems essenciais** que um **senior Ruby developer** deve conhecer:

### **🔹 Pry (Debugging no Console Interativo)**

📌 **Instalação:**

```
gem install pry

```

📌 **Uso:**

```ruby
ruby
CopiarEditar
require 'pry'
binding.pry  # Pausa a execução e abre um console interativo

```

✅ **Quando usar?**

- Para **depuração interativa** em código Ruby.

---

### **🔹 Sidekiq (Processamento Assíncrono com Redis)**

📌 **Instalação:**

```
gem install sidekiq

```

📌 **Exemplo de Job:**

```ruby
ruby
CopiarEditar
class MeuJob
  include Sidekiq::Worker

  def perform(nome)
    puts "Processando #{nome}"
  end
end

```

📌 **Execução do Job:**

```ruby
ruby
CopiarEditar
MeuJob.perform_async("Tarefa 1")

```

✅ **Quando usar?**

- Para **tarefas em background**, como envio de e-mails e processamento de imagens.

---

### **🔹 Faraday (HTTP Requests Simples e Flexíveis)**

📌 **Instalação:**

```
gem install faraday

```

📌 **Exemplo de Uso:**

```ruby
ruby
CopiarEditar
require 'faraday'

response = Faraday.get('https://jsonplaceholder.typicode.com/todos/1')
puts response.body

```

✅ **Quando usar?**

- Para fazer **requisições HTTP de forma flexível**.

---

### **🔹 Dry-rb (Codebase Mais Modular e Funcional)**

O **Dry-rb** é um conjunto de gems que ajuda a melhorar o design de código Ruby.

📌 **Instalação:**

```
gem install dry-struct

```

📌 **Exemplo de Uso (`dry-struct`)**

```ruby
ruby
CopiarEditar
require 'dry-struct'

class Usuario < Dry::Struct
  attribute :nome, Types::String
  attribute :idade, Types::Integer
end

u = Usuario.new(nome: "João", idade: 30)
puts u.nome  # João

```

✅ **Quando usar?**

- Quando deseja um **código mais estruturado e seguro**.

---

### **🔹 Sorbet (Tipagem Estática no Ruby)**

📌 **Instalação:**

```
gem install sorbet

```

📌 **Uso:**

```ruby
ruby
CopiarEditar
require 'sorbet-runtime'

class Calculadora
  extend T::Sig

  sig { params(a: Integer, b: Integer).returns(Integer) }
  def soma(a, b)
    a + b
  end
end

```

✅ **Quando usar?**

- Para **tipagem estática** e mais segurança no código.

---

### **🔹 FactoryBot (Factories para Testes)**

📌 **Instalação:**

```
gem install factory_bot

```

📌 **Exemplo de Factory:**

```ruby
ruby
CopiarEditar
FactoryBot.define do
  factory :usuario do
    nome { "João" }
    email { "joao@example.com" }
  end
end

```

✅ **Quando usar?**

- Para criar **dados de teste rapidamente** em specs.

---

### **🔹 Devise (Autenticação Rápida no Rails)**

📌 **Instalação:**

```
gem install devise

```

📌 **Gerando a configuração:**

```
rails generate devise:install

```

✅ **Quando usar?**

- Para **autenticação de usuários** em aplicações Rails.

---

## **3️⃣ Gerenciamento de Dependências (Bundler, Gemfile.lock)**

O **Bundler** gerencia gems e suas versões em projetos Ruby.

---

### **✅ Instalando o Bundler**

```
gem install bundler

```

📌 **Exemplo de `Gemfile`:**

```ruby
ruby
CopiarEditar
source "https://rubygems.org"

gem "rails", "~> 7.0"
gem "sidekiq"
gem "pry"

```

📌 **Instalando as dependências:**

```
bundle install

```

📌 **Atualizando gems:**

```
bundle update

```

📌 **Gerando um `Gemfile.lock`:**

```
bundle lock

```

✅ **Quando usar?**

- Sempre que precisar gerenciar **dependências em projetos Ruby**.

---

# **📌 Conclusão**

1. **Criando e Publicando Gems**
    - `bundle gem` → Gera estrutura básica.
    - `gem build` → Compila a gem.
    - `gem push` → Publica no RubyGems.
2. **Gems Essenciais**
    - **Depuração:** `pry`
    - **Background Jobs:** `sidekiq`
    - **HTTP Requests:** `faraday`
    - **Tipagem Estática:** `sorbet`
    - **Factories:** `factory_bot`
    - **Autenticação:** `devise`
3. **Gerenciamento de Dependências**
    - `Bundler` → Instala e gerencia gems.
    - `Gemfile.lock` → Garante que versões sejam fixas.

---

# **📌 8. Ferramentas e Boas Práticas** 🚀

Manter **código limpo, organizado e eficiente** é essencial para um **Senior Ruby Developer**.

---

## **1️⃣ Code Style Guide do Ruby e Rails**

### **✅ Estilo de Código Ruby**

O **Ruby Style Guide** (https://rubystyle.guide/) define as boas práticas do código Ruby.

📌 **Principais Regras:**

✅ Use **2 espaços** para identação, nunca tab.

✅ Use `snake_case` para nomes de métodos e variáveis.

✅ Use `CamelCase` para classes e módulos.

✅ Evite `if` inline para código complexo.

```ruby
ruby
CopiarEditar
# Certo ✅
class Usuario
  def initialize(nome)
    @nome = nome
  end
end

# Errado ❌
class usuario
  def Initialize(Nome)
    @Nome = Nome
  end
end

```

---

### **✅ Estilo de Código Rails**

📌 **O Rails tem seu próprio guia**:

https://rails.rubystyle.guide/

✅ **Principais práticas:**

- **Evite callbacks complexos (`before_save`, `after_create`)**.
- **Prefira scopes sobre métodos de classe**.
- **Use `find_each` para grandes quantidades de registros**.

```ruby
ruby
CopiarEditar
# Certo ✅
class Usuario < ApplicationRecord
  scope :ativos, -> { where(ativo: true) }
end

# Errado ❌
class Usuario < ApplicationRecord
  def self.ativos
    where(ativo: true)
  end
end

```

---

## **2️⃣ Estruturas de Logs (Logger, Lograge, Structured Logging)**

### **✅ Logger (Padrão do Ruby)**

O `Logger` já vem embutido no Ruby e Rails.

📌 **Uso Básico:**

```ruby
ruby
CopiarEditar
require 'logger'

logger = Logger.new(STDOUT)
logger.info("Isso é uma informação")
logger.warn("Isso é um aviso")
logger.error("Isso é um erro!")

```

📌 **Log no Rails (`config/application.rb`)**

```ruby
ruby
CopiarEditar
config.logger = Logger.new(STDOUT)
config.log_level = :info  # :debug, :warn, :error, :fatal

```

✅ **Boa prática:**

- Use `Logger` para rastrear erros sem expor informações sensíveis.

---

### **✅ Lograge (Logs Estruturados no Rails)**

Por padrão, os logs do Rails são verbosos. **Lograge** os torna mais legíveis.

📌 **Instalação:**

```
gem install lograge

```

📌 **Configuração no `config/environments/production.rb`:**

```ruby
ruby
CopiarEditar
config.lograge.enabled = true
config.lograge.formatter = ->(data) { data.to_json }

```

✅ **Quando usar?**

- Para **formatar logs de forma estruturada** e melhorar a observabilidade.

---

### **✅ Structured Logging (Logs em JSON para Monitoramento)**

📌 **Exemplo com `lograge` e `ActiveSupport::Logger`**

```ruby
ruby
CopiarEditar
logger = ActiveSupport::Logger.new(STDOUT)
logger.formatter = ->(severity, time, progname, msg) { { level: severity, time: time, message: msg }.to_json }

```

✅ **Quando usar?**

- Quando precisa de logs **estruturados para monitoramento** em ferramentas como **ELK, Datadog, Splunk**.

---

## **3️⃣ Monitoramento e Debugging (byebug, pry, rack-mini-profiler)**

### **✅ Byebug (Debugging Interativo para Ruby)**

📌 **Instalação:**

```
gem install byebug

```

📌 **Uso:**

```ruby
ruby
CopiarEditar
require 'byebug'

def soma(a, b)
  byebug  # Pausa a execução aqui
  a + b
end

soma(2, 3)

```

✅ **Quando usar?**

- Para **pausar a execução** e inspecionar variáveis no terminal.

---

### **✅ Pry (Console Interativo Mais Poderoso que IRB)**

📌 **Instalação:**

```
gem install pry

```

📌 **Substituir o IRB por Pry:**

```
pry

```

📌 **Adicionar um `binding.pry` no código:**

```ruby
ruby
CopiarEditar
require 'pry'

def saudacao(nome)
  binding.pry  # Pausa aqui e entra no console interativo
  "Olá, #{nome}!"
end

saudacao("João")

```

✅ **Quando usar?**

- Para **depurar e explorar objetos dinamicamente**.

---

### **✅ rack-mini-profiler (Monitoramento de Performance no Rails)**

📌 **Instalação:**

```
gem install rack-mini-profiler

```

📌 **Configuração no `config/application.rb`:**

```ruby
ruby
CopiarEditar
Rack::MiniProfiler.config.auto_inject = true

```

🚀 **Agora você vê um painel de performance no topo do app Rails!**

✅ **Quando usar?**

- Para **monitorar consultas SQL lentas, tempo de resposta e gargalos**.

---

## **4️⃣ Ruby Versions e Gerenciadores (rbenv, rvm)**

### **✅ rbenv (Gerenciador de Versão Ruby mais Leve e Rápido)**

📌 **Instalação no Linux/macOS:**

```
brew install rbenv
rbenv install 3.2.2
rbenv global 3.2.2

```

📌 **Verificando a versão:**

```
ruby -v

```

✅ **Quando usar?**

- Quando quer um gerenciador **leve e sem modificar shell scripts**.

---

### **✅ RVM (Gerenciador de Ruby Completo)**

📌 **Instalação:**

```
\curl -sSL https://get.rvm.io | bash -s stable

```

📌 **Instalando Ruby com RVM:**

```
rvm install 3.2.2
rvm use 3.2.2 --default

```

✅ **Quando usar?**

- Quando precisa gerenciar **múltiplas versões e configurações do Ruby**.

---

# **📌 Conclusão**

1. **Code Style Guide**
    - Use **2 espaços** para identação.
    - Prefira `snake_case` para métodos e `CamelCase` para classes.
    - Rails: **evite callbacks complexos** e prefira **scopes**.
2. **Logging**
    - **Logger** para logs básicos.
    - **Lograge** para logs mais limpos no Rails.
    - **Structured Logging** para logs em JSON.
3. **Debugging e Monitoramento**
    - **Byebug** para pausas interativas.
    - **Pry** para exploração dinâmica.
    - **rack-mini-profiler** para monitoramento de performance.
4. **Gerenciadores de Ruby**
    - **rbenv** (mais leve, recomendado).
    - **RVM** (mais completo, útil para múltiplas versões).

---