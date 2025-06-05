# Guia Completo de Redmine

Este guia apresenta, de forma detalhada e avançada, o **Redmine**: instalação, configuração, funcionalidades principais, personalização, administração, integração e boas práticas. O Redmine é uma aplicação web de gerenciamento de projetos e rastreamento de problemas (issue tracking) escrita em Ruby on Rails.

---

## 1. O que é Redmine?

O **Redmine** é um sistema open source de gerenciamento de projetos desenvolvido em Ruby on Rails. Suas principais características incluem:

* **Gerenciamento de Múltiplos Projetos e Subprojetos**
* **Rastreamento de Problemas (Issues/Tasks)**
* **Controle de Versão Integrado**: suporte a SVN, Git, Mercurial, CVS, Bazaar.
* **Wiki e Fórum por Projeto**
* **Controle de Tempo** com registro de horas trabalhadas
* **Gantt Chart e Calendário** para visualização de cronogramas
* **Controle de Acesso Baseado em Funções (Role-Based Access Control)**
* **Temas e Localização** para múltiplos idiomas
* **Plugin Architecture**: extensibilidade para recursos adicionais

Em produção, normalmente é implantado em servidores Linux/Unix com bancos PostgreSQL ou MySQL.

---

## 2. Requisitos de Sistema

Para instalar o Redmine, os requisitos mínimos recomendados são:

* **Sistema Operacional**: Linux (Debian/Ubuntu, CentOS), macOS ou Windows (não recomendado em produção).
* **Ruby**: versão 2.7.x ou 3.x (ver site oficial para compatibilidade com versão Redmine).
* **Ruby on Rails**: versão compatível (ex: Rails 6.x para Redmine 4.x).
* **Banco de Dados**: PostgreSQL (recomendado) ou MySQL/MariaDB.
* **Servidor Web**: Passenger (Phusion Passenger) ou Puma + Nginx/Apache.
* **Gems** adicionais: bundler, imagemagick para miniaturas de anexos.

---

## 3. Instalação Passo a Passo

### 3.1 Preparando o Ambiente Ruby

1. **Instalar RVM ou rbenv** para gerenciar versões Ruby:

   ```bash
   # Exemplo com RVM
   ```

gpg --keyserver hkp\://pool.sks-keyservers.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
\curl -sSL [https://get.rvm.io](https://get.rvm.io) | bash -s stable --ruby
source \~/.rvm/scripts/rvm
rvm install 2.7.6
rvm use 2.7.6 --default

````

2. **Instalar Bundler**:
```bash
gem install bundler
````

### 3.2 Clonar Repositório do Redmine

```bash
# Versão estável 4.2.x (exemplo)
cd /opt
sudo git clone -b 4.2-stable https://github.com/redmine/redmine.git
sudo chown -R deploy:deploy redmine
cd redmine
```

### 3.3 Configuração do Banco de Dados

1. **Instalar cliente e servidor** (PostgreSQL como exemplo):

   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib libpq-dev
   ```

2. **Criar usuário e banco**:

   ```bash
   sudo -i -u postgres
   createuser --pwprompt redmine_user
   createdb -O redmine_user redmine_db
   exit
   ```

3. **Configurar `config/database.yml`**:

   ```yaml
   production:
     adapter: postgresql
     database: redmine_db
     host: localhost
     username: redmine_user
     password: sua_senha_aqui
     encoding: utf8
   ```

### 3.4 Instalar Dependências e Gems

```bash
cd /opt/redmine
gem install bundler
bundle install --without development test
```

* `--without development test` exclui gems de desenvolvimento/teste em produção.

### 3.5 Gerar Secret Token e Inicializar Banco

```bash
bundle exec rake generate_secret_token
RAILS_ENV=production bundle exec rake db:migrate
RAILS_ENV=production bundle exec rake redmine:load_default_data
```

* **Importante**: no carregamento de dados padrão, selecione idioma e configurações básicas.

### 3.6 Configurar Servidor Web (Nginx + Passenger)

1. **Instalar Passenger + Nginx** (Ubuntu/Debian):

   ```bash
   # Instalar dependências
   ```

gem install passenger
apt install libnginx-mod-http-passenger nginx

# Habilitar Passenger no Nginx

sudo vi /etc/nginx/nginx.conf

# Verificar se a diretiva passenger\_root está presente

````

2. **Configurar Virtual Host** em `/etc/nginx/sites-available/redmine`:
```nginx
upstream redmine {
    server unix:/opt/redmine/tmp/sockets/passenger_redmine.sock;
}

server {
    listen 80;
    server_name redmine.example.com;
    passenger_enabled on;
    passenger_app_env production;
    root /opt/redmine/public;

    access_log /var/log/nginx/redmine.access.log;
    error_log /var/log/nginx/redmine.error.log;

    location ~ ^/(\.svn|\.git) {
        deny all;
    }
}
````

3. **Habilitar e reiniciar Nginx**:

   ```bash
   sudo ln -s /etc/nginx/sites-available/redmine /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

### 3.7 Configurar Permissões

```bash
cd /opt/redmine
sudo chown -R deploy:www-data files log tmp public/plugin_assets
sudo chmod -R 755 files log tmp public/plugin_assets
```

* **Deploy**: grupo do sistema web (`www-data`) para permitir uploads e geração de assets.

---

## 4. Configurações Básicas (config/configuration.yml)

O arquivo `configuration.yml` contém ajuste de funções principais:

```yaml
production:
  email_delivery:
    delivery_method: :smtp
    smtp_settings:
      address: "smtp.example.com"
      port: 587
      domain: 'example.com'
      authentication: :login
      user_name: 'user@example.com'
      password: 'sua_senha'
      enable_starttls_auto: true

  rmagick_magick_path: /usr/bin/convert # para geração de miniaturas
  attachments_storage_path: /opt/redmine/files
```

* **email\_delivery** configura notificações por e-mail.
* **rmagick\_magick\_path** aponta para o executável do ImageMagick ou GraphicsMagick.
* **attachments\_storage\_path** define onde arquivos anexados serão armazenados (padrão `files/`).

---

## 5. Funcionalidades Principais

### 5.1 Projetos e Subprojetos

* **Projetos**: unidades de trabalho com nome, identificador, descrição, status (ativo/arquivado).
* **Subprojetos**: herdam configurações (membros, versões, etc.) de projetos pai.
* **Configuração**: gestor de projeto atribui módulos habilitados (Issues, Wiki, Repositório, Fórum).

### 5.2 Rastreamento de Problemas (Issues)

* **Campos**: ID, assunto, descrição, prioridade, status, categoria, versão designada, data de início etc.
* **Custom Fields**: campos personalizados por projeto ou global.
* **Workflows Personalizados**: definir transições de status por função.
* **Sub-tarefas** e **tarefas relacionadas**: permitir hierarquia de issues.
* **Registro de Tempo**: cada issue pode ter horas registradas, vinculadas a atividades e data.
* **Assignee/Watcher**: atribuir responsáveis e quem acompanha (notificações).

### 5.3 Controle de Versão Integrado

* **Repositórios**: Git, SVN, Mercurial, CVS etc. configurados em `Settings → Repositories`.
* **Exibição de Código**: cliques em arquivos permitem visualizar conteúdo e histórico.
* **Diff e Blame** para alterações.
* **Repositório Externo**: pode apontar para repositório remoto (Git via SSH).

### 5.4 Wiki e Documentação

* **Wiki por Projeto**: páginas wiki que podem ser hierarquizadas.
* **Markup**: utiliza Markdown, Textile, BBCode, reStructuredText, entre outros.
* **Histórico de Versão e Diferenças** de cada página.
* **Proteção de Páginas**: restringir edição por função de usuário.

### 5.5 Fórum e Debate

* **Fórum por Projeto**: categorias de discussão e tópicos para comunicação de equipe.
* **Permissões**: definir quem pode criar, responder e encerrar tópicos.

### 5.6 Gantt Chart e Calendário

* **Gantt Chart**: gera visualização de cronograma com datas de início/prazo de milestones e issues.
* **Calendário**: exibe issues e versões de acordo com datas de início e prazo.

### 5.7 Registro de Tempo (Time Tracking)

* **Entradas de Tempo**: usuários registram horas gastas em issues, vinculadas a atividades (desenvolvimento, teste).
* **Relatórios de Tempo**: gerar relatórios customizados por projeto, issue, usuário e intervalo de datas.

### 5.8 Controle de Membros e Permissões

* **Membros**: associar usuários a projetos, definindo funções (role) com permissões específicas (visualizar issues, editar Wiki, gerenciar membros).
* **Funções Padrão**: Manager, Developer, Reporter, Guest.
* **Permissões Granulares**: delegar acesso a módulos individuais (Issues, Wiki, Repositório).

### 5.9 Notificações por Email

* **Configuração SMTP** em `configuration.yml`.
* **Emails Automatizados**: criação/atualização de issue, mudanças de status, novos comentários.
* **Opções de Subscrição**: usuários podem escolher receber notificações por projeto, issue ou alterações específicas.

---

## 6. Administração e Personalização

### 6.1 Admin Web Interface

Acesso como administrador para:

* Gerenciar usuários e permissões globais.
* Criar e editar projetos.
* Definir trackers, status, prioridades, atividades e tipos de documentos globais.
* Configurar idiomas, fuso horário e tema.

### 6.2 Temas e Layout

* **Temas Padrão**: Redmine inclui temas claros e escuros.
* **Criação de Temas Customizados**: criar diretório `public/themes/<nome_tema>` com arquivos CSS, imagens e templates parciais (layouts).
* **Seleção de Tema**: em `Administration → Settings → Display → Theme` ou permissão por usuário.

### 6.3 Campos Personalizados (Custom Fields)

* **Tipos Suportados**: texto, lista suspensa, inteiro, data, booleano, múltiplo (associações).
* **Aplicação**: issues, projetos, usuários, tempo, documentos, entradas de tempo.
* **Visibilidade Condicional**: definir para quais funções ou projetos o campo deve aparecer.

### 6.4 Localização e Idiomas

* **Idiomas Suportados**: múltiplos fornecidos pela comunidade (PT-BR, EN, ES etc.).
* **Configuração Global**: em `Administration → Languages`.
* **Escolha de Idioma por Usuário**: cada usuário pode selecionar o idioma preferido do perfil.

### 6.5 Plugins e Extensões

1. **Instalar Plugin**:

   ```bash
   cd /opt/redmine/plugins
   git clone <repo-do-plugin> plugin_name
   cd /opt/redmine
   ```

gem install bundler
bundle install
RAILS\_ENV=production bundle exec rake redmine\:plugins\:migrate

````
2. **Plugins Populares**:
   - **Redmine Agile**: visão de quadro Kanban/Scrum.  
   - **Redmine Checklists**: permite adicionar checklists em issues.  
   - **Redmine LDAP Auth**: autenticação via LDAP/AD.  
   - **Redmine CRM**: funcionalidades de CRM (contatos, empresas).  
3. **Remover Plugin**: remover pasta do plugin, depois:
   ```bash
   RAILS_ENV=production bundle exec rake redmine:plugins:migrate NAME=plugin_name VERSION=0
````

4. **Atualizar Plugins**: executar `bundle install` e `rake redmine:plugins:migrate` após atualizar código.

---

## 7. Backup e Restauração

### 7.1 Backup de Banco de Dados

* **PostgreSQL**:

  ```bash
  pg_dump -U redmine_user redmine_db > redmine_db_backup.sql
  ```
* **MySQL/MariaDB**:

  ```bash
  mysqldump -u redmine_user -p redmine_db > redmine_db_backup.sql
  ```

### 7.2 Backup de Arquivos

* **Diretório `files/`**: contém todos os arquivos anexados (imagens, documentos).
* **Diretório `plugins/`**: código de plugins instalados (versões customizadas).
* **Diretório `themes/`**: temas customizados.

```bash
cd /opt/redmine
tar czvf redmine_files_backup.tar.gz files/ plugins/ public/themes/
```

### 7.3 Restauração

1. **Banco de Dados**:

   ```bash
   psql -U redmine_user redmine_db < redmine_db_backup.sql  # PostgreSQL
   mysql -u redmine_user -p redmine_db < redmine_db_backup.sql  # MySQL
   ```
2. **Arquivos**: descompactar em `/opt/redmine`:

   ```bash
   ```

tar xzvf redmine\_files\_backup.tar.gz -C /opt/redmine

````
3. **Permissões**: ajustar proprietário e permissões conforme seção de instalação.

---

## 8. Integrações e API REST

### 8.1 REST API Embutida

Redmine oferece uma API RESTful para interagir programaticamente com recursos:
- **Autenticação**: via **API key** (token) do usuário ou basic auth (usuário/senha).  
- **Formato de Resposta**: JSON ou XML configurável por extensão de URL (`.json` ou `.xml`).

#### 8.1.1 Exemplos de Endpoints

| Recurso          | Método HTTP | Exemplo de URL                                      | Descrição                          |
| ---------------- | ----------- | --------------------------------------------------- | ---------------------------------- |
| Listar Projects  | GET         | `/projects.json?key=API_TOKEN`                      | Retorna lista de projetos          |
| Criar Issue      | POST        | `/issues.json?key=API_TOKEN`                        | Cria nova issue (payload JSON)     |
| Atualizar Issue  | PUT         | `/issues/123.json?key=API_TOKEN`                    | Atualiza issue com ID 123          |
| Obter Usuário    | GET         | `/users/5.json?key=API_TOKEN`                       | Retorna dados do usuário 5         |

#### 8.1.2 Exemplo de Requisição com cURL

```bash
# Obter lista de projetos
curl -H "Content-Type: application/json" \
  -u username:password \
  https://redmine.example.com/projects.json
# Criar issue
echo '{"issue": {"project_id": 1, "subject": "Bug encontrado", "description": "Descrição detalhada"}}' \
| curl -H "Content-Type: application/json" \
     -H "X-Redmine-API-Key: API_TOKEN" \
     -d @- \
     -X POST https://redmine.example.com/issues.json
````

### 8.2 Integração com GIT/Webhook de SCM

* **Configurar Repositório no Redmine**: em `Settings → Repository`, escolha `Git` e forneça URL ou caminho local.
* **Hooks de Commit**: para registrar mensagens de commit como comentários de issue, inclua palavras-chave como `refs #123` no commit.
* **Automatic Revision Linking**: habilitar em `Administration → Settings → Repository` (`Display revision author and date` e `Display commit messages`).

---

## 9. Tarefas Agendadas e Cron

* **Agendamento de Tarefas**: o Redmine utiliza tarefas Rake para operações como limpeza de sessões e envio de emails pendentes.

```bash
# Enviar notificações pendentes
cd /opt/redmine
RAILS_ENV=production bundle exec rake redmine:email:send_them_pending

# Limpar sessões expiradas
env RAILS_ENV=production bundle exec rake db:session:trim
```

* **Configurar Cron** (exemplo `/etc/cron.d/redmine`):

  ```cron
  # Envia emails pendentes a cada 5 minutos
  */5 * * * * deploy /usr/local/rbenv/shims/bundle exec rake -f /opt/redmine/Rakefile redmine:email:send_them_pending RAILS_ENV=production
  # Limpa sessões todo dia à meia-noite
  0 0 * * * deploy /usr/local/rbenv/shims/bundle exec rake -f /opt/redmine/Rakefile db:session:trim RAILS_ENV=production
  ```

---

## 10. Monitoramento e Performance

### 10.1 Logs e Nível de Log

* Logs do Redmine ficam em `log/production.log`. Defina o nível em `config/environments/production.rb`:

  ```ruby
  config.log_level = :info # ou :warn, :error, :debug
  ```
* Rotacione logs periodicamente via `logrotate` ou ferramentas similares.

### 10.2 Métricas Básicas

* **Visitas a Páginas**: medir através de ferramentas externas (Google Analytics) ou plugins Redmine.
* **Atividade de Issues**: uso de *queries* e relatórios para identificar gargalos.
* **Uso de Memória e CPU**: monitorar processos Ruby (Unicorn/Puma) com ferramentas como New Relic ou Munin.

### 10.3 Cache e Otimização

* **Cache de Página**: habilitar cache fragmentado em `config/environments/production.rb`:

  ```ruby
  config.action_controller.perform_caching = true
  config.cache_store = :memory_store, { size: 64.megabytes }
  ```
* **Cache de View Fragment**: usar helper `cache` em templates (ERB):

  ```erb
  <% cache do %>
    <%= render 'issues_list', issues: @issues %>
  <% end %>
  ```
* **Otimização de Banco de Dados**: adicionar índices em colunas frequentemente filtradas (e.g., `status_id`, `assigned_to_id`).
* **Desativar Módulos Não Usados**: em `Administration → Settings → Modules`, para reduzir overhead.

---

## 11. Backup, Upgrade e Manutenção

### 11.1 Backup Completo

* **Banco de Dados**: siga instruções da seção 7.
* **Arquivos de Anexos e Tema**: faça tar.gz de `files/`, `public/themes/` e `plugins/`.
* **Configurações**: backup de `config/database.yml`, `configuration.yml`, `settings.yml`, `repositories/`.

### 11.2 Atualização de Versão

1. **Parar Servidor**:

   ```bash
   sudo systemctl stop nginx
   sudo systemctl stop redmine  # se estiver usando serviço systemd
   ```
2. **Backup Completo** (conforme acima).
3. **Obter Nova Versão**:

   ```bash
   cd /opt/redmine
   git fetch
   git checkout 4.2-stable  # ou versão desejada
   git submodule update --init --recursive
   ```
4. **Atualizar Gems**:

   ```bash
   bundle install --without development test
   ```
5. **Executar Migrações**:

   ```bash
   RAILS_ENV=production bundle exec rake db:migrate
   ```
6. **Instalar e Migrar Plugins**:

   ```bash
   RAILS_ENV=production bundle exec rake redmine:plugins:migrate
   ```
7. **Limpar Cache**:

   ```bash
   RAILS_ENV=production bundle exec rake tmp:cache:clear
   ```
8. **Reiniciar Serviços**:

   ```bash
   sudo systemctl start redmine
   sudo systemctl start nginx
   ```

### 11.3 Tarefas de Manutenção

* **Limpeza de Sessões**: `rake db:session:trim`.
* **Limpeza de Logs Antigos**: usar `logrotate`.
* **Reindexar Textos** (se usar plugins de busca full-text).
* **Verificar Plugins Obsoletos**: remover ou atualizar.

---

## 12. Segurança e Controle de Acesso

### 12.1 Configurações de Segurança

* **Chave Secreta (secret\_token)**: gerada automaticamente em `config/initializers/secret_token.rb`. Manter fora do versionamento se personalizada.
* **HTTPS**: obrigar cabeçalhos HSTS em Nginx e configuração `config.force_ssl = true` em `production.rb`.
* **Content Security Policy (CSP)**: configurar via gems como `secure_headers`.

### 12.2 Autenticação Externa

* **LDAP/Active Directory**: usar plugin `ldap_authentication` ou `redmine_ldap_sync`.
* **Single Sign-On (SSO)**: integrar com CAS, OAuth2, OpenID via plugins:

  * `redmine_omniauth_google`: autenticação Google OAuth2.
  * `redmine_omniauth_cas`: CAS.

### 12.3 Controle de Acesso e Permissões

* **Funções Globais**: Administradores com acesso irrestrito.
* **Funções de Projeto**: configurar permissão por módulo (Ver Issues, Editar Wiki, Gerenciar Tempo etc.).
* **Membros**: vincular usuários a projetos específicos.
* **Restrição de Ações**: controle de quem pode criar, editar, excluir issues e atualizações de status.

---

## 13. Integrações e Recursos Avançados

### 13.1 Webhooks e API Extensions

* **Webhooks Padrão**: Redmine Core não inclui webhooks, mas plugins como `redmine_webhooks` permitem acionar requisições HTTP em eventos de issue, documentos, etc.
* **Exemplo de Configuração de Webhook**:

  1. Instalar plugin: `cd plugins && git clone https://github.com/jgraichen/redmine_webhooks.git`
  2. Migrar: `RAILS_ENV=production bundle exec rake redmine:plugins:migrate`
  3. Em `Settings → Webhooks`, adicionar URL e eventos (issue creation, update etc.).

### 13.2 Integração com Sistemas de Chat/Notificações

* **Slack**: plugin `redmine_slack` ou `redmine_chat_telegram` para Telegram.
* **HipChat/Matrix**: via plugins específicos para receber notificações de novos issues.

### 13.3 Relatórios Personalizados (Custom Reports)

* **Custom Queries**: criar consultas salvas de issues via filtros avançados e exportar como CSV ou PDF.
* **Gantt e Roadmap**: uso avançado de versões (Milestones) para planejamento.
* **Gráficos**: plugin `redmine_xlsx_exporter` ou usar plugins que geram gráficos de burndown e dashboards.

---

## 14. Troubleshooting e FAQs

### 14.1 Problemas Comuns

| Sintoma                                 | Possíveis Causas                                  | Solução                                                   |
| --------------------------------------- | ------------------------------------------------- | --------------------------------------------------------- |
| Erro 500 ao acessar Redmine             | Permissões incorretas em `files/`, `log/`, `tmp/` | Ajustar `chown` e `chmod` conforme seção de instalação    |
| Imagens/Anexos não carregam             | Dependência ImageMagick não instalada             | Instalar `imagemagick` e configurar `rmagick_magick_path` |
| Migração de banco falha                 | Versão Ruby/Rails incompatível                    | Verificar compatibilidade de versão Redmine/Rails/Ruby    |
| Notificações de e-mail não enviam       | Configuração SMTP incorreta                       | Rever `configuration.yml` e testar via `rails console`    |
| Plugins não aparecem ou travam Redmine  | Versão do plugin incompatível                     | Atualizar plugin ou Redmine para versões compatíveis      |
| Acesso lento a grandes repositórios Git | Exibição de repositório sem cache habilitado      | Habilitar `repository_cache` em configurações             |

### 14.2 Comandos Úteis

```bash
# Verificar versão Redmine
cd /opt/redmine
bundle exec rails runner "puts Redmine::VERSION.to_s"

# Acessar console Rails em produção
RAILS_ENV=production bundle exec rails console

# Limpar cache de ativos
RAILS_ENV=production bundle exec rake tmp:cache:clear
```

---

## 15. Boas Práticas

1. **Manter Redmine Atualizado**: aplique atualizações de segurança e correções de bugs regularmente.
2. **Fazer Backups Automáticos**: configure scripts diários/semanais para backup de BD e arquivos de anexos.
3. **Limitar Plugins a Necessários**: muitos plugins podem degradar performance; avalie impacto antes da instalação.
4. **Monitorar Performance**: acompanhe uso de CPU, memória, I/O e tempos de resposta no servidor web e banco.
5. **Segurança em Primeiro Lugar**: habilite HTTPS, use senhas fortes, controle acesso de administradores.
6. **Documentar Fluxos de Trabalho**: defina padrões de criação, atualização e fechamento de issues para equipe.
7. **Revisar Permissões Periodicamente**: garantir que somente usuários apropriados tenham acesso a projetos confidenciais.
8. **Usar Versionamento de Base de Dados**: mantenha um processo claro de migrações e rollbacks.
9. **Manter Logs Organizados**: configure rotação de logs e monitore alertas de erros críticos.
10. **Planejar Escalabilidade**: em casos de crescimento, considere separar banco e servidores web, usar memcached, otimizar índices.

---

## 16. Conclusão

O Redmine é uma poderosa ferramenta de gerenciamento de projetos e rastreamento de problemas, adequada para equipes que precisam de controle colaborativo e extensibilidade via plugins. Dominando configuração, personalização e operações, é possível criar um ambiente robusto e seguro, alinhado às necessidades do time de desenvolvimento e gerenciamento.
