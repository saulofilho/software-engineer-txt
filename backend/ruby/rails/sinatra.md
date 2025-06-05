# Guia Completo de Sinatra

Este guia apresenta de forma detalhada o **Sinatra**, um microframework web em Ruby leve e flexível, cobrindo desde conceitos básicos até tópicos avançados como modularização, templates, middleware, testes e deploy.

---

## 1. O que é Sinatra?

O **Sinatra** é um microframework minimalista para aplicações web em Ruby, criado por Blake Mizerany em 2007. Ao contrário de frameworks full-stack como Ruby on Rails, o Sinatra foca em simplicidade e flexibilidade:

* **Código mínimo**: define rotas e lógica diretamente sobre objetos HTTP.
* **Sem convenções rígidas**: sem estrutura de diretório obrigatória ou camadas pré-definidas.
* **Extensível**: integra-se facilmente a bibliotecas de terceiros.
* **Rápido para prototipação**: ideal para APIs, serviços web pequenos ou protótipos.

Sinatra inclui apenas o necessário para mapear URLs a blocos de código Ruby, deixando o desenvolvedor livre para escolher outras bibliotecas para ORM, templates, autenticação etc.

---

## 2. Instalando e Configurando o Ambiente

### 2.1 Requisitos Básicos

* **Ruby**: versão 2.5 ou superior recomendada.
* **Bundler**: para gerenciamento de dependências.
* **RVM** ou **rbenv**: para gerenciar versões Ruby (opcional, mas recomendado).

### 2.2 Instalação do Sinatra

1. Crie um diretório para o projeto:

   ```bash
   mkdir my_sinatra_app
   cd my_sinatra_app
   ```
2. Crie um `Gemfile` com:

   ```ruby
   source 'https://rubygems.org'

   gem 'sinatra', require: 'sinatra/base'
   gem 'thin'           # servidor HTTP leve
   gem 'puma'           # alternativa a Thin
   gem 'rack'           # interface de middleware
   gem 'shotgun', group: :development # recarregamento automático

   # Gems comuns complementares:
   gem 'activerecord', '~> 6.0'       # ORM
   gem 'sinatra-activerecord'         # integração AR
   gem 'sqlite3'                      # BD de desenvolvimento
   gem 'rake'                         # tarefas Rake para migrations
   gem 'erubis'                       # templates ERB otimizados
   gem 'tilt'                         # abstração de templates
   gem 'rack-flash3'                  # mensagens Flash
   gem 'rack-protection'              # proteção contra CSRF e XSS
   gem 'sinatra-contrib'              # extensões (JSON, cookies, etc.)
   ```
3. Instale as gems:

   ```bash
   bundle install
   ```

---

## 3. Estrutura de Projeto Recomendada

Embora Sinatra não imponha estrutura, recomenda-se organizar como:

```
my_sinatra_app/
├── config.ru           # ponto de entrada Rack
├── Gemfile
├── Rakefile            # tarefas (migrations, testes)
├── app/
│   ├── main.rb         # aplicativo principal (clássico ou modular)
│   ├── controllers/    # controllers organizados (opcional)
│   ├── models/         # classes de modelo (ActiveRecord)
│   ├── views/          # templates ERB/ERubis/Haml
│   ├── public/         # arquivos estáticos (CSS, JS, imagens)
│   └── helpers/        # módulos auxiliares
├── db/
│   ├── migrate/        # arquivos de migração ActiveRecord
│   └── schema.rb       # esquema do banco
├── config/
│   └── database.yml    # configurações de banco para ActiveRecord
└── spec/ (ou test/)
    └── ...             # testes RSpec ou Minitest
```

### 3.1 `config.ru`

```ruby
require './app/main'
run MyApp
```

* Pontos para Rack levantarem a aplicação.
* `MyApp` é a classe do Sinatra (estilo modular) a ser executada.

### 3.2 `Rakefile`

```ruby
require 'sinatra/activerecord/rake'
require './app/main'

namespace :db do
  task :load_config do
    require './config/database'
  end
end
```

* Inclui tarefas ActiveRecord (`db:migrate`, `db:setup`, `db:rollback`).

---

## 4. Aplicativo Básico (Estilo Clássico)

Em `app/main.rb`:

```ruby
require 'sinatra'
require 'sinatra/json'
require 'sinatra/reloader' if development?
require 'rack-flash'

configure do
  enable :sessions
  set :session_secret, 'super_secret_key'
  use Rack::Flash
end

# Rota raiz
get '/' do
  erb :index
end

# Rota com parâmetro
get '/hello/:name' do
  @name = params[:name]
  erb :hello
end

# Exemplo de JSON
get '/api/status' do
  content_type :json
  json status: 'OK', time: Time.now
end

# Post form data
post '/login' do
  username = params[:username]
  password = params[:password]
  if username == 'admin' && password == 'senha'
    flash[:success] = 'Login bem-sucedido'
    redirect '/'
  else
    flash[:error] = 'Credenciais inválidas'
    redirect '/login'
  end
end

# Exemplo de rota protegida
get '/dashboard' do
  halt 401, 'Não autorizado' unless session[:user]
  erb :dashboard
end
```

* **Sinatra clássico**: define rotas diretamente em contexto global do arquivo.
* **Helpers**: `sinatra/json` para métodos `json`, `sinatra/reloader` recarrega em dev.
* **Sessões e Flash**: `enable :sessions`, `use Rack::Flash` para mensagens temporárias.
* **Proteção**: `halt 401` interrompe fluxo caso não autenticado.

---

## 5. Aplicativo Modular (Recomendado para Projetos Maiores)

Em `app/main.rb`:

```ruby
require 'sinatra/base'
require 'sinatra/activerecord'
require 'sinatra/json'
require 'sinatra/flash'
require './config/database'

class MyApp < Sinatra::Base
  register Sinatra::ActiveRecordExtension
  register Sinatra::Flash

  configure do
    enable :sessions
    set :session_secret, 'super_secret_key'
    set :public_folder, File.dirname(__FILE__) + '/public'
    set :views, File.dirname(__FILE__) + '/views'
  end

  # Helpers customizados
  helpers do
    def current_user
      @current_user ||= User.find(session[:user_id]) if session[:user_id]
    end

    def authenticate!
      redirect '/login' unless current_user
    end
  end

  # Rotas
  get '/' do
    erb :index
  end

  get '/login' do
    erb :login
  end

  post '/login' do
    user = User.find_by(username: params[:username])
    if user && user.authenticate(params[:password])
      session[:user_id] = user.id
      flash[:success] = 'Entrou com sucesso'
      redirect '/dashboard'
    else
      flash[:error] = 'Credenciais inválidas'
      redirect '/login'
    end
  end

  get '/dashboard' do
    authenticate!
    erb :dashboard
  end

  # API JSON
  get '/api/posts' do
    content_type :json
    posts = Post.all
    json posts: posts.map { |p| { id: p.id, title: p.title, body: p.body } }
  end

  # Exemplo de rota com ActiveRecord
  get '/posts/:id' do
    @post = Post.find(params[:id])
    erb :post
  end

  # Iniciar servidor se executado diretamente
  run! if app_file == $0
end
```

* **`register Sinatra::ActiveRecordExtension`** habilita tarefas DB e configurações.
* **Helpers**: métodos auxiliares para autenticação e usuário atual.
* **Configurações customizadas** para pasta de views e public.

---

## 6. Modelos com ActiveRecord

### 6.1 Configuração do Banco (`config/database.yml`)

```yaml
development:
  adapter: sqlite3
  database: db/development.sqlite3
  pool: 5
  timeout: 5000

test:
  adapter: sqlite3
  database: db/test.sqlite3
  pool: 5
  timeout: 5000

production:
  adapter: postgresql
  encoding: unicode
  database: myapp_production
  pool: 5
  username: myuser
  password: <%= ENV['MYAPP_DATABASE_PASSWORD'] %>
```

### 6.2 Definindo Modelos

#### 6.2.1 Modelo User

Em `app/models/user.rb`:

```ruby
require 'bcrypt'

class User < ActiveRecord::Base
  include BCrypt

  validates :username, presence: true, uniqueness: true
  validates :password_hash, presence: true

  def password
    @password ||= Password.new(password_hash)
  end

  def password=(new_password)
    @password = Password.create(new_password)
    self.password_hash = @password
  end

  def authenticate(test_password)
    password == test_password
  end
end
```

* **`bcrypt`** para criptografia de senhas.
* Armazena hash em coluna `password_hash`.
* Métodos `password` e `password=` para acesso seguro.

#### 6.2.2 Modelo Post

Em `app/models/post.rb`:

```ruby
class Post < ActiveRecord::Base
  belongs_to :user

  validates :title, presence: true
  validates :body, presence: true
end
```

### 6.3 Migrações

#### 6.3.1 Criar Migração de Usuários

```bash
bundle exec rake db:create_migration NAME=create_users
```

Em `db/migrate/TIMESTAMP_create_users.rb`:

```ruby
class CreateUsers < ActiveRecord::Migration[6.0]
  def change
    create_table :users do |t|
      t.string :username, null: false
      t.string :password_hash, null: false
      t.timestamps
    end
    add_index :users, :username, unique: true
  end
end
```

#### 6.3.2 Criar Migração de Posts

```bash
bundle exec rake db:create_migration NAME=create_posts
```

Em `db/migrate/TIMESTAMP_create_posts.rb`:

```ruby
class CreatePosts < ActiveRecord::Migration[6.0]
  def change
    create_table :posts do |t|
      t.string :title, null: false
      t.text :body, null: false
      t.references :user, foreign_key: true
      t.timestamps
    end
  end
end
```

#### 6.3.3 Executar Migrações

```bash
bundle exec rake db:migrate
```

---

## 7. Templates e Views (ERB)

### 7.1 Configuração de Views

* Por padrão, Sinatra busca templates em `views/`.
* Use extensões como `tilt/erb` ou `erubis` para renderização.

### 7.2 Exemplo de View

Em `app/views/layout.erb`:

```erb
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title><%= yield(:title) || 'My Sinatra App' %></title>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <% if flash[:success] %>
    <p class="flash success"><%= flash[:success] %></p>
  <% end %>
  <% if flash[:error] %>
    <p class="flash error"><%= flash[:error] %></p>
  <% end %>

  <%= yield %>
</body>
</html>
```

Em `app/views/index.erb`:

```erb
<% content_for :title do %>Página Inicial<% end %>

<h1>Bem-vindo ao My Sinatra App</h1>
<% if current_user %>
  <p>Olá, <%= current_user.username %>! <a href="/logout">Sair</a></p>
<% else %>
  <p><a href="/login">Entrar</a> ou <a href="/signup">Registrar</a></p>
<% end %>

<ul>
  <% Post.all.each do |post| %>
    <li><a href="/posts/<%= post.id %>"><%= post.title %></a> por <%= post.user.username %></li>
  <% end %>
</ul>
```

---

## 8. Helpers e Middleware

### 8.1 Helpers

No aplicativo modular, defina em `app/helpers/authentication_helper.rb`:

```ruby
module AuthenticationHelper
  def current_user
    @current_user ||= User.find(session[:user_id]) if session[:user_id]
  end

  def logged_in?
    !!current_user
  end
end
```

E registre em `app/main.rb`:

```ruby
helpers AuthenticationHelper
```

### 8.2 Middleware

Sinatra roda sobre Rack. Adicione middlewares em `app/main.rb`:

```ruby
use Rack::Session::Cookie, key: 'rack.session',
                           path: '/',
                           secret: 'another_secret_key'
use Rack::Protection
```

* **Rack::Session::Cookie**: manipula sessões via cookies.
* **Rack::Protection**: protege contra ataques comuns (CSRF, XSS, clickjacking).

---

## 9. Rotas e Parâmetros

### 9.1 Definição de Rotas

* `get '/path' do ... end` para GET.
* `post '/path' do ... end` para POST.
* `put`, `patch`, `delete` para outras requisições HTTP.

### 9.2 Parâmetros de URL

```ruby
get '/users/:id' do
  @user = User.find(params[:id])
  erb :user
end

get '/search' do
  query = params[:q]
  @results = Post.where('title LIKE ?', "%#{query}%")
  erb :search_results
end
```

* `params[:id]` para segmentos na rota.
* Querystring em `params[:q]` para `/search?q=sinatra`.

### 9.3 Redirecionamentos e Status

```ruby
post '/signup' do
  user = User.new(username: params[:username], password: params[:password])
  if user.save
    redirect '/login'
  else
    erb :signup, locals: { errors: user.errors.full_messages }
  end
end

get '/secret' do
  redirect '/login', 401 unless logged_in?
  erb :secret
end
```

* `redirect` envia status 302 por padrão (ou 301 se especificado).
* Segundo parâmetro em `redirect` define código HTTP.

---

## 10. Autenticação e Sessões

### 10.1 Registro e Login

Em `app/main.rb`:

```ruby
get '/signup' do
  erb :signup
end

post '/signup' do
  user = User.new(username: params[:username], password: params[:password])
  if user.save
    flash[:success] = 'Conta criada. Faça login.'
    redirect '/login'
  else
    erb :signup, locals: { errors: user.errors.full_messages }
  end
end

get '/login' do
  erb :login
end

post '/login' do
  user = User.find_by(username: params[:username])
  if user && user.authenticate(params[:password])
    session[:user_id] = user.id
    flash[:success] = 'Entrou com sucesso'
    redirect '/dashboard'
  else
    flash[:error] = 'Credenciais inválidas'
    redirect '/login'
  end
end

get '/logout' do
  session.clear
  flash[:success] = 'Desconectado'
  redirect '/'
end
```

* **`session[:user_id]`** armazena ID do usuário no cookie de sessão.
* **`session.clear`** remove todos valores de sessão.

### 10.2 Protegendo Rotas

```ruby
get '/dashboard' do
  redirect '/login' unless logged_in?
  erb :dashboard
end
```

* Utilize helper `logged_in?` para verificar autenticação.

---

## 11. Conexão a Banco e ActiveRecord Avançado

### 11.1 Configurando ActiveRecord

Em `config/database.rb`:

```ruby
require 'active_record'
env = ENV['RACK_ENV'] || 'development'
config = YAML.load_file('config/database.yml')[env]
ActiveRecord::Base.establish_connection(config)
```

* Carrega configuração do YAML e conecta ao DB.
* Chame este arquivo em `app/main.rb` antes de definir rotas.

### 11.2 Escopos e Callbacks

Em `app/models/post.rb`:

```ruby
class Post < ActiveRecord::Base
  belongs_to :user
  scope :recent, -> { order(created_at: :desc) }
  before_save :generate_slug

  private

  def generate_slug
    self.slug = title.parameterize if slug.blank?
  end
end
```

* **`scope :recent`** para referência `Post.recent`.
* **`before_save`** para gerar `slug` automaticamente.

### 11.3 Transações

```ruby
post '/transfer' do
  ActiveRecord::Base.transaction do
    sender = User.find(params[:from])
    receiver = User.find(params[:to])
    amount = params[:amount].to_i

    sender.balance -= amount
    receiver.balance += amount

    sender.save!
    receiver.save!
  end
  'Transferência concluída'
rescue ActiveRecord::RecordInvalid
  'Erro na transferência'
end
```

* **`transaction`** garante rollback em caso de exceção.

---

## 12. Middleware Rack e Extensões

### 12.1 Uso de Middleware

Em `app/main.rb`, antes das rotas:

```ruby
use Rack::Deflater           # comprime respostas HTTP
use Rack::Session::Cookie, key: 'rack.session', secret: 'secret'
use Rack::Protection         # proteção contra CSRF, XSS
```

* **`use`** insere middleware Rack na pilha de execução.
* **`Rack::Deflater`** comprime saída para melhorar performance.

### 12.2 Extensões Sinatra

* **Sinatra-Contrib**: pacote de extensões oficiais (JSON, Cookies, Namespace, MultiRoute).
* **Sinatra-Flash**: mensagens flash entre requisições.
* **Sinatra-Param**: validação de parâmetros simples.

Algo como:

```ruby
require 'sinatra/namespace'
require 'sinatra/param'

register Sinatra::Namespace

namespace '/api' do
  before do
    content_type :json
  end

  get '/status' do
    json status: 'OK'
  end
end
```

* **`Sinatra::Namespace`** permite agrupar rotas sob um prefixo.
* **`Sinatra::Param`** valida parâmetros com expressões regulares, tipos:

  ```ruby
  get '/search' do
    param :q, String, required: true, min_length: 3
    param :page, Integer, default: 1
    # lógica de busca...
  end
  ```

---

## 13. Testes Automatizados

### 13.1 Minitest (Padrão)

#### 13.1.1 Configuração

No `Gemfile`, inclua:

```ruby
group :test do
  gem 'minitest'
  gem 'rack-test'
end
```

No `Rakefile`, adicione tarefa:

```ruby
require 'rake/testtask'

Rake::TestTask.new do |t|
  t.pattern = 'spec/**/*_test.rb'
  t.libs << 'test'
end

task default: :test
```

#### 13.1.2 Exemplo de Teste de Rota

Em `spec/app_test.rb`:

```ruby
require 'minitest/autorun'
require 'rack/test'
require_relative '../app/main'

env = 'test'
Rack::Test::Methods

def app
  MyApp.new
end

class MainAppTest < Minitest::Test
  def test_index_returns_200
    get '/'
    assert last_response.ok?
    assert_includes last_response.body, 'Bem-vindo'
  end

  def test_login_failure
    post '/login', username: 'invalido', password: 'senha'
    assert last_response.redirect?
    follow_redirect!
    assert_includes last_response.body, 'Credenciais inválidas'
  end
end
```

* **`Rack::Test::Methods`** fornece métodos `get`, `post`, `last_response`.
* Testes validam respostas HTTP e conteúdo de páginas.

### 13.2 RSpec (Opcional)

No `Gemfile`:

```ruby
group :test do
  gem 'rspec'
  gem 'rack-test'
  gem 'factory_bot'
end
```

Execute:

```bash
bundle exec rspec --init
```

Exemplo `spec/app_spec.rb`:

```ruby
require 'spec_helper'
require 'rack/test'
require_relative '../app/main'

RSpec.describe MyApp do
  include Rack::Test::Methods

  def app
    MyApp.new
  end

  it 'exibe a página inicial' do
    get '/'
    expect(last_response).to be_ok
    expect(last_response.body).to include('Bem-vindo')
  end

  it 'falha ao fazer login com credenciais inválidas' do
    post '/login', username: 'abc', password: '123'
    follow_redirect!
    expect(last_response.body).to include('Credenciais inválidas')
  end
end
```

---

## 14. Deploy em Produção

### 14.1 Servidor Rack (Puma)

No `Gemfile`:

```ruby
gem 'puma'
```

Crie arquivo `config/puma.rb`:

```ruby
workers Integer(ENV['WEB_CONCURRENCY'] || 2)
threads_count = Integer(ENV['MAX_THREADS'] || 5)
threads threads_count, threads_count
preload_app!
rackup DefaultRackup
port ENV['PORT'] || 3000
environment ENV['RACK_ENV'] || 'production'

on_worker_boot do
  require './config/database'
end
```

Para iniciar:

```bash
bundle exec puma -C config/puma.rb
```

### 14.2 Nginx como Proxy Reverso

```nginx
upstream sinatra_app {
    server unix:/path/to/myapp/tmp/sockets/puma.sock;
}

server {
    listen 80;
    server_name example.com;
    root /path/to/myapp/public;

    location / {
        proxy_pass http://sinatra_app;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /assets {
        expires max;
        add_header Cache-Control public;
    }

    error_page 500 502 503 504 /500.html;
}
```

* **`proxy_pass`** aponta para socket unix gerado pelo Puma.
* **Arquivos estáticos** servidos diretamente do diretório `public/`.

### 14.3 Containers Docker

Crie `Dockerfile`:

```dockerfile
FROM ruby:3.0
WORKDIR /app
COPY Gemfile* ./
RUN bundle install
COPY . .
CMD ["bundle", "exec", "puma", "-C", "config/puma.rb"]
```

Crie `docker-compose.yml`:

```yaml
version: '3'
services:
  web:
    build: .
    command: bundle exec puma -C config/puma.rb
    volumes:
      - .:/app
    ports:
      - "3000:3000"
    environment:
      - RACK_ENV=production
      - DATABASE_URL=postgres://user:pass@db:5432/myapp_production
    depends_on:
      - db
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp_production
    volumes:
      - db_data:/var/lib/postgresql/data
volumes:
  db_data:
```

---

## 15. Boas Práticas e Considerações

1. **Separar Lógica de Negócio**: evite colocar muito código nas rotas; extraia para classes de serviço ou modelos.
2. **Manter Rotas Simples**: cada rota deve ter responsabilidade única; use métodos ou classes auxiliares para lógica complexa.
3. **Validação de Parâmetros**: utilize `Sinatra::Param` ou validações manuais para proteger a aplicação contra parâmetros maliciosos.
4. **Proteger Contra Vulnerabilidades**: habilite `Rack::Protection` e sanitize entradas em views para prevenção de XSS/CSRF.
5. **Banco de Dados Eager Loading**: use `includes` ao recuperar associações para evitar N+1 queries.
6. **Versionamento de Banco**: use tarefas Rake e ActiveRecord migrations para manter histórico de esquema.
7. **Cache**: utilize `Rack::Cache` ou Redis para cache de respostas ou fragmentos.
8. **Logs e Monitoramento**: configure logger adequado, acrescente identificação de request ID em logs para rastreamento.
9. **Ambientes Separados**: configure separadamente `development`, `test` e `production` via `environment.rb` ou variáveis de ambiente.
10. **Testes Abrangentes**: priorize testes de rota, lógica de modelo e integração com banco usando Minitest ou RSpec.

---

## 16. Conclusão

Sinatra é ideal para aplicações web enxutas, APIs e serviços que demandam leveza e rapidez de desenvolvimento. Com uma comunidade madura e ecossistema de extensões, permite criar desde protótipos até sistemas em produção. Este guia cobriu desde a configuração inicial até práticas avançadas, oferecendo uma base completa para desenvolver aplicações robustas usando Sinatra.
