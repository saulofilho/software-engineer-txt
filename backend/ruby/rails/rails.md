# Guia Completo de Ruby on Rails

Este guia aborda, de forma avançada, o **Ruby on Rails** (Rails), um framework web de código aberto que segue o padrão MVC, enfatizando convenção sobre configuração e permitindo desenvolvimento rápido de aplicações robustas.

---

## 1. O que é Ruby on Rails?

* **Rails** é um framework web escrito em Ruby, criado por David Heinemeier Hansson em 2004. Ele fornece uma estrutura completa para construir aplicações web seguindo o padrão **MVC** (Model–View–Controller) e o princípio **DRY** (Don't Repeat Yourself).
* **Principais filosofias**:

  * **Convention over Configuration (CoC)**: convenções predefinidas reduzem necessidade de arquivos de configuração.
  * **Don't Repeat Yourself (DRY)**: evitar duplicação de código por meio de abstrações.
* **Componentes principais**:

  * **ActiveRecord**: ORM para interagir com bancos de dados relacionais.
  * **ActionController**: gerencia requisições HTTP e lógica de controle.
  * **ActionView**: renderiza templates (ERB, Haml, Slim).
  * **Routing**: mapeia URLs para controllers/actions.
  * **ActiveSupport**: extensão da linguagem Ruby com utilitários.
  * **ActionMailer**: envio de emails.
  * **ActiveJob**: abstração para jobs em background.
  * **Asset Pipeline**: gerenciamento de CSS, JavaScript e imagens.

---

## 2. Instalação e Configuração Inicial

### 2.1 Requisitos

* **Ruby**: versão 2.7.x ou 3.x.
* **Rails**: versão 6.x ou 7.x.
* **Bundler**: gerenciador de gems.
* **Banco de Dados**: PostgreSQL (recomendado), MySQL, SQLite (para desenvolvimento).

### 2.2 Instalando Ruby (rbenv/RVM)

```bash
# Exemplo com rbenv

# Instalar dependências (Ubuntu)
sudo apt update && sudo apt install -y git curl libssl-dev libreadline-dev zlib1g-dev

# Clonar rbenv e ruby-build
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build

# Alterar configurações de shell
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
source ~/.bashrc

# Instalar Ruby
eval "$(rbenv init -)"
rbenv install 3.1.2
rbenv global 3.1.2
ruby -v  # verificar versão

# Instalar Bundler
gem install bundler
```

### 2.3 Instalando Rails

```bash
gem install rails -v 7.0.4  # exemplo de versão
rails -v  # verificar versão instalada
```

### 2.4 Criando Novo Projeto Rails

```bash
rails new myapp -d postgresql --css=bootstrap
cd myapp
```

* `-d postgresql`: define PostgreSQL como banco de dados padrão.
* `--css=bootstrap`: adiciona suporte ao Bootstrap via importmap ou webpacker.

### 2.5 Configuração do Banco de Dados (database.yml)

```yaml
# config/database.yml

development:
  adapter: postgresql
  encoding: unicode
  database: myapp_development
  pool: 5
  username: myuser
  password: <%= ENV['MYAPP_DATABASE_PASSWORD'] %>
  host: localhost

# test e production seguem padrões semelhantes
```

Após configurar variáveis de ambiente:

```bash
rails db:create
rails db:migrate
```

---

## 3. Estrutura de Diretórios

```
myapp/
├── app/
│   ├── assets/         # CSS, JavaScript, imagens via Asset Pipeline
│   ├── controllers/    # controllers MVC
│   ├── helpers/        # modules de ajuda para views
│   ├── jobs/           # ActiveJob para background jobs
│   ├── mailers/        # ActionMailer
│   ├── models/         # classes ActiveRecord
│   ├── views/          # templates ERB
│   └── channels/       # ActionCable WebSockets
├── bin/                # executáveis (rails, rake)
├── config/             # rotas, ambiente, inicializadores
│   ├── environments/   # configurações específicas (development, production, test)
│   ├── initializers/   # arquivos Ruby carregados em inicialização
│   ├── locales/        # arquivos de tradução (I18n)
│   └── routes.rb       # definição de rotas
├── db/                 # migrations, seeds, schema
├── lib/                # bibliotecas personalizadas
│   └── tasks/          # rake tasks personalizadas
├── log/                # logs de aplicação
├── public/             # ativos públicos (favicon, robots.txt)
├── storage/            # ActiveStorage para blobs e arquivos
├── test/ ou spec/      # testes (Minitest ou RSpec)
├── tmp/                # arquivos temporários (cache, pids)
├── vendor/             # gems vendorizadas (opcional)
├── Gemfile             # especifica dependências da aplicação
└── config.ru           # Rack configuration
```

---

## 4. MVC: Models, Views e Controllers

### 4.1 Models (ActiveRecord)

* **Gerar Model**:

  ```bash
  rails generate model Article title:string body:text published:boolean
  ```

  * Gera arquivo de migration em `db/migrate/` e classe `app/models/article.rb`.

* **Migration Exemplo**:

  ```ruby
  class CreateArticles < ActiveRecord::Migration[6.1]
    def change
      create_table :articles do |t|
        t.string :title, null: false
        t.text :body
        t.boolean :published, default: false

        t.timestamps
      end
    end
  end
  ```

* **Migrations**:

  ```bash
  rails db:migrate
  rails db:rollback  # reverter última migration
  rails db:schema:load  # recriar schema a partir de schema.rb
  ```

* **Definindo Associações e Validações**:

  ```ruby
  class Article < ApplicationRecord
    belongs_to :user
    has_many :comments, dependent: :destroy

    validates :title, presence: true, length: { minimum: 5 }
    validates :body, presence: true
  end
  ```

* **Consultas Avançadas** (ActiveRecord Query Interface):

  ```ruby
  # Where, Order, Limit, Offset
  Article.where(published: true).order(created_at: :desc).limit(10)

  # Joins e Includes para eager loading
  Article.joins(:user).where(users: { active: true })
  Article.includes(:comments).where(id: 1)

  # Scopes
  class Article < ApplicationRecord
    scope :published, -> { where(published: true) }
    scope :recent, -> { order(created_at: :desc).limit(5) }
  end
  ```

### 4.2 Controllers (ActionController)

* **Gerar Controller**:

  ```bash
  rails generate controller Articles index show new edit
  ```

  * Gera `app/controllers/articles_controller.rb`, views correspondentes e rota básica.

* **Exemplo de Controller**:

  ```ruby
  class ArticlesController < ApplicationController
    before_action :set_article, only: %i[show edit update destroy]
    before_action :authenticate_user!, except: %i[index show]

    def index
      @articles = Article.published.recent
    end

    def show
    end

    def new
      @article = current_user.articles.build
    end

    def create
      @article = current_user.articles.build(article_params)
      if @article.save
        redirect_to @article, notice: 'Artigo criado com sucesso.'
      else
        render :new, status: :unprocessable_entity
      end
    end

    def edit
      authorize! :edit, @article  # usando CanCanCan para autorização
    end

    def update
      if @article.update(article_params)
        redirect_to @article, notice: 'Artigo atualizado.'
      else
        render :edit, status: :unprocessable_entity
      end
    end

    def destroy
      @article.destroy
      redirect_to articles_url, notice: 'Artigo excluído.'
    end

    private

    def set_article
      @article = Article.find(params[:id])
    end

    def article_params
      params.require(:article).permit(:title, :body, :published)
    end
  end
  ```

* **Filtros** (`before_action`, `after_action`, `around_action`) gerenciam callbacks comuns.

* **Strong Parameters** via `permit` e `require` previnem atribuição massiva insegura.

### 4.3 Views (ActionView)

* **Templates ERB** em `app/views/articles/`:

  * `index.html.erb`, `show.html.erb`, `new.html.erb`, `edit.html.erb`.
  * Sintaxe ERB: `<%= @article.title %>` para interpolar Ruby.

* **Layouts** em `app/views/layouts/application.html.erb`:

  ```erb
  <!DOCTYPE html>
  <html>
  <head>
    <title>MyApp</title>
    <%= csrf_meta_tags %>
    <%= csp_meta_tag %>
    <%= stylesheet_link_tag 'application', media: 'all', 'data-turbo-track': 'reload' %>
    <%= javascript_include_tag 'application', 'data-turbo-track': 'reload', defer: true %>
  </head>

  <body>
    <%= render 'shared/navbar' %>
    <div class="container">
      <% flash.each do |key, msg| %>
        <div class="alert alert-<%= key %>"><%= msg %></div>
      <% end %>
      <%= yield %>
    </div>
  </body>
  </html>
  ```

* **Partials** (arquivos iniciados com `_`, ex: `_form.html.erb`) para código de view reutilizável:

  ```erb
  <!-- app/views/articles/_form.html.erb -->
  <%= form_with(model: @article, local: true) do |form| %>
    <% if @article.errors.any? %>
      <div class="error_messages">
        <h2><%= pluralize(@article.errors.count, "erro") %> impediram o salvamento:</h2>
        <ul>
          <% @article.errors.full_messages.each do |msg| %>
            <li><%= msg %></li>
          <% end %>
        </ul>
      </div>
    <% end %>

    <div class="field">
      <%= form.label :title %>
      <%= form.text_field :title %>
    </div>
    <div class="field">
      <%= form.label :body %>
      <%= form.text_area :body %>
    </div>
    <div class="actions">
      <%= form.submit %>
    </div>
  <% end %>
  ```

* **Helpers** em `app/helpers/application_helper.rb` e helpers específicos de controller:

  ```ruby
  module ApplicationHelper
    def format_date(date)
      date.strftime('%d/%m/%Y') if date
    end
  end
  ```

---

## 5. Rotas (Routing)

* **Definição** em `config/routes.rb`:

  ```ruby
  Rails.application.routes.draw do
    root 'articles#index'
    resources :articles do
      resources :comments, only: %i[create destroy]
    end
    devise_for :users
  end
  ```

* **Recursos RESTful** (`resources :articles`) gera rotas para ações padrão (index, show, new, edit, create, update, destroy).

* **Rotas Aninhadas**: `resources :articles do resources :comments end` gera `/articles/:article_id/comments`.

* **Rotas Personalizadas**:

  ```ruby
  get '/about', to: 'pages#about'
  patch '/articles/:id/publish', to: 'articles#publish', as: :publish_article
  ```

* **Rotas de API** usando `namespace`:

  ```ruby
  namespace :api do
    namespace :v1 do
      resources :articles, defaults: { format: :json }
    end
  end
  ```

* **Visualizar Todas as Rotas**:

  ```bash
  rails routes
  ```

---

## 6. ActiveRecord: Migrations, Associações e Validações

### 6.1 Migrations Avançadas

* **Criar Migration**:

  ```bash
  rails generate migration AddPublishedAtToArticles published_at:datetime
  ```

* **Migrações Customizadas**:

  ```ruby
  class AddIndexToArticlesTitle < ActiveRecord::Migration[6.1]
    def change
      add_index :articles, :title, unique: true
    end
  end
  ```

* **Diretrizes**:

  * Prefira métodos idempotentes (`add_column`, `add_index`) sem SQL cru.
  * Para alteração de coluna complexa, use `change_column_null` e `update_all`.
  * Use `reversible do |dir| ... end` para migrações que não suportam `change` reversa automática.

### 6.2 Associações

* **Tipos de Associação**:

  * `belongs_to` (muitos para um).
  * `has_many` (um para muitos).
  * `has_one` (um para um).
  * `has_many :through` (associação via tabela intermediária).
  * `has_and_belongs_to_many` (join table sem modelo).

* **Exemplos**:

  ```ruby
  class User < ApplicationRecord
    has_many :articles, dependent: :nullify
    has_many :comments, through: :articles
  end

  class Article < ApplicationRecord
    belongs_to :user
    has_many :comments, dependent: :destroy
    has_many :tags, through: :taggings
  end

  class Comment < ApplicationRecord
    belongs_to :article
    belongs_to :user, optional: true
  end
  ```

* **Opções Importantes**:

  * `dependent: :destroy` para remoção em cascata.
  * `optional: true` em `belongs_to` para permitir nulos.
  * `inverse_of` para otimização de carregamento.
  * `counter_cache` para contador de associações.

### 6.3 Validações e Callbacks

* **Validações Comuns**:

  ```ruby
  class User < ApplicationRecord
    validates :email, presence: true, uniqueness: true, format: { with: URI::MailTo::EMAIL_REGEXP }
    validates :username, presence: true, length: { minimum: 3, maximum: 32 }
  end
  ```

* **Callbacks** (`before_save`, `after_create`, `around_update` etc.):

  ```ruby
  class Article < ApplicationRecord
    before_save :set_published_at

    private

    def set_published_at
      self.published_at ||= Time.current if published_changed? && published
    end
  end
  ```

* **Transações**:

  ```ruby
  ActiveRecord::Base.transaction do
    user.save!
    profile.save!
  end
  rescue ActiveRecord::RecordInvalid => e
    # tratar erro e rollback automático
  ```

---

## 7. Funcionalidades Persistentes

### 7.1 ActiveStorage

* **Instalação**:

  ```bash
  rails active_storage:install
  rails db:migrate
  ```

* **Configuração** em `config/storage.yml`:

  ```yaml
  local:
    service: Disk
    root: <%= Rails.root.join("storage") %>

  amazon:
    service: S3
    access_key_id: <%= ENV['AWS_ACCESS_KEY_ID'] %>
    secret_access_key: <%= ENV['AWS_SECRET_ACCESS_KEY'] %>
    region: <%= ENV['AWS_REGION'] %>
    bucket: <%= ENV['AWS_BUCKET'] %>
  ```

* **Uso em Models**:

  ```ruby
  class Article < ApplicationRecord
    has_one_attached :cover_image
    has_many_attached :documents
  end
  ```

* **Exibição em Views**:

  ```erb
  <!-- Mostrar imagem redimensionada -->
  <%= image_tag article.cover_image.variant(resize_to_limit: [300, 300]) if article.cover_image.attached? %>
  ```

* **Envio via Formulário**:

  ```erb
  <%= form_with(model: @article, local: true) do |f| %>
    <%= f.file_field :cover_image %>
    <%= f.file_field :documents, multiple: true %>
    <!-- demais campos -->
  <% end %>
  ```

### 7.2 Action Cable (WebSockets)

* **Configuração**:

  * Em `config/cable.yml` defina adapter (Redis recomendado).
  * No `routes.rb`: `mount ActionCable.server => "/cable"`

* **Gerar Channel**:

  ````bash
  rails generate channel Chat\ n```
  - Gera `app/channels/chat_channel.rb` e `app/javascript/channels/chat_channel.js`.

  ````

* **Exemplo de Channel**:

  ```ruby
  # app/channels/chat_channel.rb
  class ChatChannel < ApplicationCable::Channel
    def subscribed
      stream_from "chat_#{params[:room]}"
    end

    def receive(data)
      ActionCable.server.broadcast("chat_#{params[:room]}", data)
    end
  end
  ```

* **Exemplo de JS (frontend)**:

  ```js
  // app/javascript/channels/chat_channel.js
  import consumer from "./consumer"

  consumer.subscriptions.create({ channel: "ChatChannel", room: "general" }, {
    received(data) {
      const messages = document.getElementById('messages')
      messages.insertAdjacentHTML('beforeend', `<p>${data.user}: ${data.message}</p>`)
    },
    sendMessage(user, message) {
      this.perform('receive', { user: user, message: message })
    }
  })
  ```

* **Uso em Views**:

  ```erb
  <!-- app/views/chats/show.html.erb -->
  <div id="messages"></div>
  <%= form_with url: '#', id: 'message_form', local: true do |f| %>
    <%= f.text_field :message, id: 'message_input' %>
    <%= f.submit 'Enviar' %>
  <% end %>

  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const chatChannel = consumer.subscriptions.subscriptions[0]
      document.getElementById('message_form').addEventListener('submit', (e) => {
        e.preventDefault()
        const message = document.getElementById('message_input').value
        chatChannel.sendMessage('<%= current_user.username %>', message)
        document.getElementById('message_input').value = ''
      })
    })
  </script>
  ```

---

## 8. Segurança e Gerenciamento de Acesso

### 8.1 Autenticação (Devise)

* **Instalação**:

  ```bash
  # Adicionar ao Gemfile
  ```

gem 'devise'
bundle install
rails generate devise\:install

````
- **Configuração Inicial**:
```bash
rails generate devise User
rails db:migrate
````

* **Rotas Geradas**: `/users/sign_in`, `/users/sign_up`, `/users/edit`, etc.
* **Autenticar Controllers**:

  ```ruby
  class ArticlesController < ApplicationController
    before_action :authenticate_user!, except: %i[index show]
    # ...
  end
  ```

### 8.2 Autorização (Pundit ou CanCanCan)

#### 8.2.1 Pundit

* **Instalação**:

  ```bash
  gem 'pundit'
  bundle install
  rails generate pundit:install
  ```

* **Definir Policies**:

  ```ruby
  # app/policies/article_policy.rb
  class ArticlePolicy < ApplicationPolicy
    def update?
      user.admin? || record.user == user
    end

    def destroy?
      user.admin?
    end
  end
  ```

* **Usar nas Controllers**:

  ```ruby
  class ArticlesController < ApplicationController
    before_action :authenticate_user!
    after_action :verify_authorized, except: %i[index show]

    def edit
      @article = Article.find(params[:id])
      authorize @article
    end

    def update
      @article = Article.find(params[:id])
      authorize @article
      if @article.update(article_params)
        redirect_to @article
      else
        render :edit
      end
    end
  end
  ```

#### 8.2.2 CanCanCan

* **Instalação**:

  ```bash
  gem 'cancancan'
  bundle install
  rails generate cancan:ability
  ```

* **Definir Regras**:

  ```ruby
  # app/models/ability.rb
  class Ability
    include CanCan::Ability

    def initialize(user)
      user ||= User.new # guest
      if user.admin?
        can :manage, :all
      else
        can :read, Article
        can [:update, :destroy], Article, user_id: user.id
      end
    end
  end
  ```

* **Usar nas Controllers**:

  ```ruby
  class ArticlesController < ApplicationController
    load_and_authorize_resource

    def destroy
      # @article carregado e autorizado
      @article.destroy
      redirect_to articles_path, notice: 'Artigo excluído.'
    end
  end
  ```

---

## 9. APIs JSON: Rails como API-only

### 9.1 Criando Aplicação API-only

```bash
rails new myapi --api -d postgresql
cd myapi
```

* Remove middleware de views, visando performance.
* Configurações em `config/application.rb`: `config.api_only = true`.

### 9.2 Serialização de Models (ActiveModel Serializers ou Fast JSON API)

#### 9.2.1 ActiveModel Serializers

* **Instalação**:

  ```bash
  gem 'active_model_serializers'
  bundle install
  rails generate serializer article
  ```

* **Exemplo de Serializer**:

  ```ruby
  # app/serializers/article_serializer.rb
  class ArticleSerializer < ActiveModel::Serializer
    attributes :id, :title, :body, :published, :created_at
    belongs_to :user
    has_many :comments
  end
  ```

* **Usar no Controller**:

  ```ruby
  class Api::V1::ArticlesController < ApplicationController
    def index
      articles = Article.published
      render json: articles, each_serializer: ArticleSerializer
    end

    def show
      article = Article.find(params[:id])
      render json: article
    end
  end
  ```

#### 9.2.2 Fast JSON API (jsonapi-serializer)

* **Instalação**:

  ```bash
  gem 'jsonapi-serializer'
  bundle install
  ```

* **Definir Serializer**:

  ```ruby
  # app/serializers/article_serializer.rb
  class ArticleSerializer
    include JSONAPI::Serializer
    attributes :title, :body, :published, :created_at
    belongs_to :user
    has_many :comments
  end
  ```

* **Usar no Controller**:

  ```ruby
  class Api::V1::ArticlesController < ApplicationController
    def index
      articles = Article.published
      render json: ArticleSerializer.new(articles).serializable_hash
    end

    def show
      article = Article.find(params[:id])
      render json: ArticleSerializer.new(article).serializable_hash
    end
  end
  ```

### 9.3 Versionamento de API e Namespace

* **Configurar Rotas**:

  ```ruby
  namespace :api do
    namespace :v1 do
      resources :articles
    end
  end
  ```
* **Serialização e Conformidade JSON\:API**:

  * Adote padrões de nomenclatura (underscored, plural).
  * Fornecer metadados e links nos responses.

---

## 10. Testes Automatizados

### 10.1 Frameworks de Teste

* **Minitest** (embutido no Rails).
* **RSpec** (popular na comunidade).
* **FactoryBot** para factories de teste.
* **Faker** para dados falsos.

### 10.2 Configurando RSpec

* **Instalação**:

  ```bash
  # Adicionar ao Gemfile no grupo de desenvolvimento/test
  ```

group \:development, \:test do
gem 'rspec-rails', '\~> 5.0'
gem 'factory\_bot\_rails'
gem 'faker'
end

bundle install
rails generate rspec\:install

```

- **Estrutura de Diretórios**:
```

spec/
├── controllers/
├── models/
├── factories/
├── serializers/
├── requests/
└── rails\_helper.rb

````

### 10.3 Exemplo de Teste de Model (RSpec + FactoryBot)

```ruby
# spec/models/article_spec.rb
require 'rails_helper'

RSpec.describe Article, type: :model do
subject { build(:article) }

it { is_expected.to validate_presence_of(:title) }
it { is_expected.to validate_length_of(:title).is_at_least(5) }
it { is_expected.to belong_to(:user) }
it { is_expected.to have_many(:comments).dependent(:destroy) }
end
````

* **Configurar Factory**:

  ```ruby
  # spec/factories/articles.rb
  FactoryBot.define do
    factory :article do
      title { Faker::Lorem.sentence(word_count: 3) }
      body  { Faker::Lorem.paragraph(sentence_count: 2) }
      published { false }
      association :user
    end
  end
  ```

### 10.4 Teste de Controller / Request Specs

```ruby
# spec/requests/articles_spec.rb
require 'rails_helper'

RSpec.describe 'Articles API', type: :request do
  let(:user) { create(:user) }
  let!(:articles) { create_list(:article, 5, user: user) }
  let(:article_id) { articles.first.id }

  describe 'GET /api/v1/articles' do
    before { get '/api/v1/articles' }

    it 'retorna todos artigos' do
      expect(json.size).to eq(5)
    end

    it 'retorna status code 200' do
      expect(response).to have_http_status(200)
    end
  end

  describe 'GET /api/v1/articles/:id' do
    before { get "/api/v1/articles/#{article_id}" }

    context 'quando o recurso existe' do
      it 'retorna o artigo' do
        expect(json['id']).to eq(article_id)
      end

      it 'retorna status code 200' do
        expect(response).to have_http_status(200)
      end
    end

    context 'quando o recurso não existe' do
      let(:article_id) { 0 }

      it 'retorna status code 404' do
        expect(response).to have_http_status(404)
      end

      it 'retorna mensagem de erro' do
        expect(response.body).to match(/Couldn't find Article/)
      end
    end
  end
end
```

* **Helpers para JSON** em `spec/support/request_spec_helper.rb`:

  ```ruby
  module RequestSpecHelper
    def json
      JSON.parse(response.body)
    end
  end
  ```
* **Incluir Helpers** em `rails_helper.rb`:

  ```ruby
  RSpec.configure do |config|
    config.include RequestSpecHelper, type: :request
    config.include FactoryBot::Syntax::Methods
  end
  ```

---

## 11. Test-Driven Development (TDD) e Desenvolvimento Guiado por Ciência de Testes

* **Ciclo Red-Green-Refactor**:

  1. **Red**: escreva um teste falho.
  2. **Green**: implemente código mínimo para passar no teste.
  3. **Refactor**: limpe e otimize o código mantendo testes verdes.

* **Benefícios**:

  * Software com menor número de bugs.
  * Design orientado a comportamento.
  * Documentação por testes.

* **Práticas**:

  * Cobertura de teste mínima de 80%.
  * Foco em testes de unidade e testes de integração/feature.
  * Uso de ferramentas de análise de cobertura como SimpleCov.

---

## 12. Deploy em Produção

### 12.1 Servidores de Aplicação

* **Puma**: servidor web/threaded padrão no Rails 5+.
* **Passenger**: integrado a Nginx/Apache via módulo.
* **Unicorn**: servidor baseado em processos forking (bom para CPU-bound).

### 12.2 Configuração Básica de Puma

```ruby
# config/puma.rb

environment ENV.fetch("RAILS_ENV") { "development" }
threads_count = ENV.fetch("RAILS_MAX_THREADS") { 5 }
threads threads_count, threads_count

port ENV.fetch("PORT") { 3000 }

# Workers para cluster mode
workers ENV.fetch("WEB_CONCURRENCY") { 2 }
preload_app!

# Checar master process antes de forkar
on_worker_boot do
  ActiveRecord::Base.establish_connection if defined?(ActiveRecord)
end
```

### 12.3 Configuração Nginx como Proxy Reverso

```nginx
upstream puma_server {
    server unix:///home/deploy/myapp/shared/tmp/sockets/puma.sock;
}

server {
    listen 80;
    server_name example.com;

    root /home/deploy/myapp/current/public;

    location ^~ /assets/ {
        gzip_static on;
        expires max;
        add_header Cache-Control public;
    }

    try_files $uri/index.html $uri @puma;

    location @puma {
        proxy_pass http://puma_server;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    error_page 500 502 503 504 /500.html;
    client_max_body_size 4G;
    keepalive_timeout 10;
}
```

### 12.4 Banco de Dados em Produção

* **Migrar**:

  ```bash
  RAILS_ENV=production rails db:migrate
  ```
* **Seeds** (dados iniciais):

  ```bash
  RAILS_ENV=production rails db:seed
  ```

### 12.5 Assets e Precompilação

* **Pré-compilar Assets**:

  ```bash
  RAILS_ENV=production rails assets:precompile
  ```
* **Cache**: usar configurador de CDN ou armazenamento S3 via gems como `asset_sync`.

### 12.6 Gerenciamento de Processo

* **Systemd** exemplar `/etc/systemd/system/myapp.service`:

  ```ini
  [Unit]
  Description=Puma HTTP Server for MyApp
  After=network.target

  [Service]
  Type=simple
  User=deploy
  WorkingDirectory=/home/deploy/myapp/current
  ExecStart=/home/deploy/.rbenv/shims/bundle exec puma -C /home/deploy/myapp/current/config/puma.rb
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```

* **Iniciar/Parar**:

  ```bash
  sudo systemctl enable myapp
  sudo systemctl start myapp
  sudo systemctl status myapp
  ```

---

## 13. Boas Práticas e Padrões de Projeto

1. **Seguir Padrões SOLID**: aplicar princípios de design orientados a objetos para controllers, models e serviços.
2. **Service Objects / Form Objects**: extrair lógica de negócio complexa para classes em `app/services`.

   ```ruby
   # Exemplo de Service Object
   class Articles::Publish
     def initialize(article)
       @article = article
     end

     def call
       ActiveRecord::Base.transaction do
         @article.update!(published: true, published_at: Time.current)
         NotificationMailer.with(article: @article).published_email.deliver_later
       end
     rescue ActiveRecord::RecordInvalid
       false
     end
   end
   ```
3. **Presenter/Decorator Patterns**: separar lógica de apresentação usando gems como Draper.
4. **Serializer Patterns para APIs**: usar serializers dedicados para manter controllers enxutos.
5. **Background Jobs**: extrair trabalhos demorados para ActiveJob (Sidekiq, Resque).
6. **Caching**: usar fragment caching, Russian Doll Caching e low-level caching com Redis.
7. **Internacionalização (I18n)**: organizar arquivos em `config/locales/*.yml` e usar `t('key')` em views.
8. **Proteção contra CSRF e XSS**: usar `csrf_meta_tags`, `sanitize`, UJS para links destructivos.
9. **Segurança de SQL**: evitar interpolação, usar query methods e prepared statements.
10. **Documentar API**: usar Swagger via gems como `rswag` para gerar documentação interativa.

---

## 14. Monitoramento, Logs e Performance

### 14.1 Logs

* Logs padrão em `log/production.log`. Configure nível em `config/environments/production.rb`:

  ```ruby
  config.log_level = :info
  ```
* **Tags de Logger**: adicionar informações como `request_id`:

  ```ruby
  # config/environments/production.rb
  config.log_tags = [:request_id, ->(req) { req.remote_ip }]
  ```

### 14.2 Ferramentas de Monitoramento

* **New Relic / Skylight / Scout**: performance e apm.
* **Rollbar / Sentry**: captura de exceções.
* **Bullet Gem**: para detectar N+1 queries em desenvolvimento.
* **Rack Mini Profiler**: perfil em tempo real no ambiente de desenvolvimento.

### 14.3 Otimizações de Banco de Dados

* **Indexação**: adicionar índices nas colunas utilizadas em `WHERE`, `ORDER BY`.
* **Query Caching**: habilitar `config.action_controller.perform_caching = true` e usar `cache` em views.
* **Eager Loading**: usar `includes` para evitar N+1 queries.

### 14.4 Caching

* **Fragment Caching**:

  ```erb
  <% cache article do %>
    <%= render partial: 'article', locals: { article: article } %>
  <% end %>
  ```
* **Russian Doll Caching**: aninhar caches fragmentados para invalidação eficiente.
* **Low-Level Caching**:

  ```ruby
  Rails.cache.fetch("article_#{article.id}", expires_in: 12.hours) do
    article.expensive_computation
  end
  ```
* **Cache Store**: configurar Redis em `config/environments/production.rb`:

  ```ruby
  config.cache_store = :redis_cache_store, { url: ENV['REDIS_URL'], namespace: 'cache' }
  ```

---

## 15. Internacionalização (I18n)

* **Configurações** em `config/application.rb`:

  ```ruby
  config.i18n.default_locale = :en
  config.i18n.available_locales = [:en, :'pt-BR']
  ```
* **Arquivos de Tradução** em `config/locales/*.{yml}`:

  ```yaml
  # config/locales/pt-BR.yml
  pt-BR:
    hello: "Olá"
    articles:
      title: "Título"
  ```
* **Uso em Views**: `<%= t('hello') %>`, `<%= t('articles.title') %>`.
* **Locale Based on User Preference**: definir em ApplicationController:

  ```ruby
  before_action :set_locale

  def set_locale
    I18n.locale = current_user&.locale || params[:locale] || I18n.default_locale
  end
  ```
* **Rotas com Locale**: opcionalmente prefixar rotas (`/pt-BR/articles`).

---

## 16. APIs Externas e Integrações

### 16.1 HTTP Clients

* **Faraday**: biblioteca flexível para requisições HTTP.

  ```ruby
  response = Faraday.get('https://api.example.com/data')
  data = JSON.parse(response.body)
  ```
* **HTTParty** ou **Net::HTTP** nativo.

### 16.2 OAuth e OpenID Connect

* **OmniAuth**: middleware de autenticação com prov\~e\~\~edur possíveis (Google, Facebook, GitHub).
* **Configuração**:

  ```ruby
  # Gemfile
  ```

gem 'omniauth'
gem 'omniauth-google-oauth2'

````
```ruby
# config/initializers/omniauth.rb
Rails.application.config.middleware.use OmniAuth::Builder do
  provider :google_oauth2, ENV['GOOGLE_CLIENT_ID'], ENV['GOOGLE_CLIENT_SECRET'], {
    scope: 'userinfo.email, userinfo.profile'
  }
end
````

### 16.3 Background Jobs (ActiveJob e Sidekiq)

* **ActiveJob** abstratifica diferentes backends:

  ```ruby
  # app/jobs/send_email_job.rb
  class SendEmailJob < ApplicationJob
    queue_as :default

    def perform(user_id)
      user = User.find(user_id)
      UserMailer.welcome_email(user).deliver_now
    end
  end
  ```

  * **Sidekiq** é backend popular: adicionar `gem 'sidekiq'` e configurar `config/application.rb`: `config.active_job.queue_adapter = :sidekiq`.
  * **Executar Sidekiq**:

    ```bash
    bundle exec sidekiq
    ```

### 16.4 Webhooks e Eventos

* **ActiveSupport::Notifications** para instrumentação personalizada.

  ```ruby
  ActiveSupport::Notifications.instrument('article.created', article_id: @article.id)
  ```

  * Inscrever listeners em `config/initializers/notifications.rb`.
* **Webhooks**: implementar controllers que recebam requests e processem payloads JSON.

---

## 17. Estrutura em Camadas e Padrões de Projeto

### 17.1 Service Objects

* **Motivação**: extrair lógica complexa ou transacional de controllers e models.
* **Exemplo**:

  ```ruby
  # app/services/articles/publish_service.rb
  class Articles::PublishService
    def initialize(article, user)
      @article = article
      @user = user
    end

    def call
      return false unless @user.admin? || @article.user == @user
      @article.transaction do
        @article.update!(published: true, published_at: Time.current)
        Articles::NotifySubscribersJob.perform_later(@article.id)
      end
      true
    rescue ActiveRecord::RecordInvalid
      false
    end
  end
  ```

### 17.2 Form Objects (Reform, ActiveModel::Model)

* **Uso**: agrupar validações e atributos de múltiplos modelos ou dados não persistentes.
* **Exemplo**:

  ```ruby
  # app/forms/article_form.rb
  class ArticleForm
    include ActiveModel::Model

    attr_accessor :title, :body, :user_id
    validates :title, presence: true, length: { minimum: 5 }

    def save
      return false unless valid?
      @article = Article.create(title: title, body: body, user_id: user_id)
    end
  end
  ```

### 17.3 Decorator/Presenter (Draper)

* **Instalação**: `gem 'draper'`, `bundle install`, `rails generate draper:install`.
* **Exemplo de Decorator**:

  ```ruby
  # app/decorators/article_decorator.rb
  class ArticleDecorator < Draper::Decorator
    delegate_all

    def formatted_published_at
      object.published_at.strftime('%d/%m/%Y') if object.published_at
    end

    def comments_count
      h.pluralize(object.comments.count, 'comentário')
    end
  end
  ```
* **Uso em Views**:

  ```erb
  <% decorate @article do |article| %>
    <p><%= article.formatted_published_at %></p>
    <p><%= article.comments_count %></p>
  <% end %>
  ```

### 17.4 Concerns

* **Uso**: extrair comportamento compartilhado entre múltiplos controllers ou models.

* **Exemplo**:

  ```ruby
  # app/models/concerns/slugifiable.rb
  module Slugifiable
    extend ActiveSupport::Concern

    included do
      before_validation :generate_slug, if: :title_changed?
      validates :slug, presence: true, uniqueness: true
    end

    def generate_slug
      self.slug = title.parameterize
    end
  end

  # Em Article model\ nclass Article < ApplicationRecord
    include Slugifiable
  end
  ```

---

## 18. Observabilidade e Logging

### 18.1 Logging Customizado

* **Usar Logger Rails**:

  ```ruby
  Rails.logger.info "Usuário #{current_user.id} criou um artigo"
  Rails.logger.error "Erro ao salvar artigo: #{@article.errors.full_messages.join(', ')}"
  ```
* **Tags de Log**:

  ```ruby
  # config/environments/production.rb
  config.log_tags = [ :request_id, ->(req) { req.remote_ip } ]
  ```
* **Formato JSON** (para ELK stack): usar gems como `lograge`.

### 18.2 Métricas e APM

* **New Relic / Datadog / Skylight**: instalar gem e configurar API key.
* **ActiveSupport::Notifications**: instrumentar eventos customizados.

  ```ruby
  ActiveSupport::Notifications.subscribe('render_template.action_view') do |name, start, finish, id, payload|
    duration = (finish - start) * 1000
    Rails.logger.info "Rendered #{payload[:identifier]} in #{duration.round(2)}ms"
  end
  ```

### 18.3 Ferramentas de Depuração em Desenvolvimento

* **Byebug / Pry**: pontas de interrupção no código para inspeção interativa.

  ```ruby
  # app/controllers/articles_controller.rb
  def show
    byebug
    @article = Article.find(params[:id])
  end
  ```
* **Bullet Gem**: detectar N+1 e otimizar queries.

  ```ruby
  # Gemfile (development)
  gem 'bullet'
  ```

  ```ruby
  # config/environments/development.rb
  config.after_initialize do
    Bullet.enable = true
    Bullet.alert = true
    Bullet.bullet_logger = true
    Bullet.console = true
  end
  ```

---

## 19. Internacionalização (I18n)

* **Configuração** em `config/application.rb`:

  ```ruby
  config.i18n.default_locale = :'pt-BR'
  config.i18n.available_locales = [:en, :'pt-BR', :es]
  ```
* **Arquivos de Tradução** (`config/locales/pt-BR.yml`):

  ```yaml
  pt-BR:
    hello: "Olá"
    articles:
      title: "Título"
      body: "Conteúdo"
    errors:
      messages:
        blank: "não pode ficar em branco"
  ```
* **Uso em Views e Models**: `<%= t('hello') %>`, `I18n.t('articles.title')`, `Model.human_attribute_name('title')`.
* **Locale Dinâmico por Usuário**:

  ```ruby
  class ApplicationController < ActionController::Base
    before_action :set_locale

    def set_locale
      I18n.locale = current_user&.locale || params[:locale] || I18n.default_locale
    end

    def default_url_options
      { locale: I18n.locale }
    end
  end
  ```

---

## 20. Versionamento de Código e CI/CD

### 20.1 Controle de Versão (Git)

* **Convenção de Commits**: use padrão Conventional Commits para gerar changelogs automáticos.
* **Branching Model**: GitFlow ou Trunk-Based Development.

### 20.2 Integração Contínua (CI)

* **GitHub Actions** exemplo `.github/workflows/ci.yml`:

  ```yaml
  name: CI
  on: [push, pull_request]

  jobs:
    build:
      runs-on: ubuntu-latest
      services:
        db:
          image: postgres:13
          env:
            POSTGRES_USER: postgres
            POSTGRES_PASSWORD: postgres
          ports:
            - 5432:5432
          options: >-
            --health-cmd="pg_isready -U postgres" \
            --health-interval=10s \
            --health-timeout=5s \
            --health-retries=5
      env:
        RAILS_ENV: test
        DATABASE_URL: postgres://postgres:postgres@localhost:5432/myapp_test
      steps:
        - uses: actions/checkout@v3
        - uses: ruby/setup-ruby@v1
          with:
            ruby-version: 3.1
        - name: Install dependencies
          run: |
            gem install bundler
            bundle install --jobs 4 --retry 3
        - name: Set up database
          run: |
            bundle exec rails db:create db:schema:load
        - name: Run tests
          run: |
            bundle exec rspec
  ```

### 20.3 Deploy Contínuo (CD)

* **Heroku**: `git push heroku main`, configurar buildpacks.
* **Capistrano** para deploy em servidores próprios:

  ```ruby
  # Capfile
  require 'capistrano/setup'
  require 'capistrano/deploy'
  require 'capistrano/rails'
  require 'capistrano/passenger'
  ```

  ```ruby
  # config/deploy.rb
  lock '3.17.0'
  set :application, 'myapp'
  set :repo_url, 'git@github.com:user/myapp.git'
  set :deploy_to, '/var/www/myapp'
  set :branch, 'main'
  set :linked_files, %w[config/master.key]
  set :linked_dirs, %w[log tmp/pids tmp/cache tmp/sockets public/system storage]

  namespace :deploy do
    after :finishing, 'deploy:cleanup'
  end
  ```

---

## 21. Boas Práticas

1. **Uso de Convenções**: siga padrões Rails para estrutura de diretórios e nomenclatura de classes.
2. **Extrair Lógica para Service Objects**: controllers devem ser finos, delegando complexidade a serviços.
3. **Manter Modelos Enxutos**: evite métodos longos; use concerns para comportamento compartilhado.
4. **Escrever Testes Automatizados**: cubra models, controllers, requests e features (Capybara).
5. **Usar Transactions e Tratamento de Erros**: garantir consistência de dados em operações críticas.
6. **Prevenir N+1 Queries**: utilize `includes` e bullet em desenvolvimento.
7. **Configurar Caching Apropriadamente**: acelerar views estáticas e consultas pesadas.
8. **Implementar Autorizações Granulares**: use Pundit ou CanCanCan para controle de acesso.
9. **Monitorar Performance e Logs**: adicionar gems de APM, configurar logs JSON.
10. **Gerenciar Dependências com Bundler**: fixe versões estáveis e atualize regularmente.

---

## 22. Conclusão

O Ruby on Rails é um framework maduro e poderoso, ideal para construir aplicações web de todos os tamanhos. Ao seguir convenções, aplicar boas práticas e utilizar o vasto ecossistema de gems, é possível desenvolver rapidamente soluções escaláveis e de manutenção simplificada.
