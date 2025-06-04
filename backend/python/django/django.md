# Guia Completo de Django

Este guia apresenta, de forma detalhada e avançada, o **Django**, um framework web de alto nível em Python que incentiva o desenvolvimento rápido e o design limpo e pragmático. Cobre desde conceitos iniciais até tópicos avançados como autenticação, ORM, templates, middleware, testes e deploy.

---

## 1. O que é Django?

Django é um framework web open source escrito em Python, criado para simplificar o desenvolvimento de aplicações web complexas. Baseado no padrão **MTV** (Model–Template–View), o Django oferece:

* **Admin auto-gerado**: interface administrativa pronta para uso.
* **ORM poderoso**: abstração de banco de dados que permite escrever consultas em Python.
* **Sistema de URLs**: roteamento flexível via expressões regulares ou path converters.
* **Templates**: mecanismo de templates seguro e eficiente.
* **Formulários**: geração de formulários HTML, validação, limpeza e exibição de erros.
* **Autenticação embutida**: sistema de usuários, permissões e sessões.
* **Boas práticas**: convenção sobre configuração, DRY e reuso de componentes.

Versão mínima recomendada: Python 3.8+ e Django 3.x ou 4.x.

---

## 2. Instalação e Configuração Inicial

### 2.1 Criando e Ativando Ambiente Virtual

```bash
python3 -m venv venv
env/bin/activate      # Linux/macOS
venv\\Scripts\\activate  # Windows
```

### 2.2 Instalação do Django

```bash
pip install django
```

### 2.3 Criando Projeto Django

```bash
django-admin startproject myproject
cd myproject
python manage.py runserver
```

* Acesse `http://127.0.0.1:8000/` para ver página de boas-vindas.
* Estrutura inicial:

  ```
  myproject/
  │  manage.py       # comando para interagir com o projeto
  └── myproject/    # configurações do projeto
      │  __init__.py
      │  settings.py  # configurações centrais
      │  urls.py      # roteamento de URL global
      │  wsgi.py      # interface WSGI para deploy
      │  asgi.py      # interface ASGI para deploy async
  ```

---

## 3. Aplicativos Django (Apps)

### 3.1 Conceito de App

* Um projeto Django pode conter múltiplos **apps** independentes e reutilizáveis.
* Cada app possui models, views, urls, templates e arquivos estáticos próprios.

### 3.2 Criando um App

```bash
python manage.py startapp blog
```

* Estrutura do app `blog`:

  ```
  blog/
  │  __init__.py
  │  admin.py      # registro de models na admin
  │  apps.py       # configurações do app
  │  models.py     # definição de modelos (ORM)
  │  views.py      # funções/ classes de view
  │  tests.py      # testes do app
  │  urls.py       # roteamento específico do app (criar manualmente)
  │  migrations/   # arquivos de migração de banco
  │  templates/    # templates HTML (opcional)
  │  static/       # arquivos estáticos (JS/CSS/ imagens)
  ```

### 3.3 Registrando o App no Projeto

No `settings.py`:

```python
INSTALLED_APPS = [
    # apps nativos
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    # app customizado
    'blog.apps.BlogConfig',
]
```

---

## 4. Configurações Principais (settings.py)

### 4.1 Configurações de Banco de Dados

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

* PostgreSQL é recomendado em produção; SQLite padrão para dev.

### 4.2 Templates

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # diretório global de templates
        'APP_DIRS': True,  # busca em <app>/templates/
        'OPTIONS': { 'context_processors': [...] },
    },
]
```

### 4.3 Arquivos Estáticos e Mídia

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # diretório global de estáticos

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # arquivos enviados pelos usuários
```

### 4.4 Configurações de Segurança

```python
SECRET_KEY = 'gerar-chave-segura-aqui'
DEBUG = False  # sempre False em produção
ALLOWED_HOSTS = ['example.com', 'www.example.com']
```

* `DEBUG` habilita página de erro; nunca use em produção.
* `ALLOWED_HOSTS` define domínios válidos.

---

## 5. ORM (Object-Relational Mapping)

### 5.1 Definindo Modelos

```python
# blog/models.py
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
```

### 5.2 Migrações de Banco

```bash
python manage.py makemigrations blog
python manage.py migrate
```

* Cria tabelas correspondentes aos modelos.

### 5.3 Operações CRUD com ORM

```python
# Criar registros
author = Author.objects.create(name='Alice', email='alice@example.com')
post = Post(title='Olá Mundo', slug='ola-mundo', content='Conteúdo aqui', author=author)
post.save()

# Consultas
posts = Post.objects.filter(published=True)
post = Post.objects.get(slug='ola-mundo')
authors = Author.objects.all()

# Atualizar
post.title = 'Título Atualizado'
post.save()

# Excluir
post.delete()
```

### 5.4 Consultas Avançadas

```python
# Filtros complexos
from django.db.models import Q, Count

# Posts publicados no último mês
recent_posts = Post.objects.filter(
    published=True,
    created_at__gte=timezone.now() - timedelta(days=30)
)

# Autores com mais de 5 posts
authors = Author.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=5)

# Buscas com OR
results = Post.objects.filter(Q(title__icontains='Django') | Q(content__icontains='Python'))
```

---

## 6. Admin Django

### 6.1 Registrando Models

```python
# blog/admin.py
from django.contrib import admin
from .models import Author, Post

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'created_at')
    list_filter = ('published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
```

### 6.2 Criando Superusuário

```bash
python manage.py createsuperuser
```

* Acesse `http://127.0.0.1:8000/admin/` para gerenciar conteúdo via interface.

---

## 7. Views e URLs

### 7.1 Views Baseadas em Funções (FBV)

```python
# blog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.filter(published=True)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    return render(request, 'blog/post_detail.html', {'post': post})
```

### 7.2 Views Baseadas em Classes (CBV)

```python
# blog/views.py
from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(published=True)
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    queryset = Post.objects.filter(published=True)
```

### 7.3 URLs do App

```python
# blog/urls.py
from django.urls import path
from .views import post_list, post_detail, PostListView, PostDetailView

urlpatterns = [
    path('', post_list, name='post_list'),         # FBV
    path('<slug:slug>/', post_detail, name='post_detail'),  # FBV
    # ou CBV:
    # path('', PostListView.as_view(), name='post_list'),
    # path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
```

### 7.4 URLs do Projeto

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```

---

## 8. Templates e Contexto

### 8.1 Estrutura de Diretórios

```
myproject/
└── blog/
    └── templates/
        └── blog/
            ├── post_list.html
            └── post_detail.html
```

### 8.2 Exemplo de Template Base

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}Meu Blog{% endblock %}</title>
  <link rel="stylesheet" href="{% static 'css/styles.css' %}">
</head>
<body>
  <header>
    <h1><a href="{% url 'post_list' %}">Meu Blog</a></h1>
  </header>
  <main>
    {% block content %}{% endblock %}
  </main>
  <footer>
    <p>&copy; 2025 Meu Blog</p>
  </footer>
</body>
</html>
```

### 8.3 Exemplo de Template de Lista de Posts

```html
<!-- templates/blog/post_list.html -->
{% extends 'base.html' %}

{% block title %}Lista de Posts{% endblock %}

{% block content %}
  {% for post in posts %}
    <article>
      <h2><a href="{% url 'post_detail' slug=post.slug %}">{{ post.title }}</a></h2>
      <p>por {{ post.author.name }} em {{ post.created_at|date:'d/m/Y' }}</p>
      <p>{{ post.content|truncatewords:30 }}</p>
    </article>
  {% empty %}
    <p>Nenhum post disponível.</p>
  {% endfor %}
  {% if is_paginated %}
    <nav>
      {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">Anterior</a>
      {% endif %}
      <span>Página {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</span>
      {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">Próxima</a>
      {% endif %}
    </nav>
  {% endif %}
{% endblock %}
```

---

## 9. Formulários e Validação

### 9.1 Formulários com Django Forms

```python
# blog/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'author', 'published']

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Post.objects.filter(slug=slug).exists():
            raise forms.ValidationError("Slug já existe.")
        return slug
```

### 9.2 Usando o Formulário na View

```python
# blog/views.py
from django.shortcuts import redirect
from .forms import PostForm

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})
```

### 9.3 Template de Formulário

```html
<!-- templates/blog/post_form.html -->
{% extends 'base.html' %}

{% block title %}Criar Post{% endblock %}

{% block content %}
  <h2>Criar Post</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Salvar</button>
  </form>
{% endblock %}
```

---

## 10. Middleware e Context Processors

### 10.1 Creando Middleware Personalizado

```python
# myproject/middleware.py

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Antes da view
        print(f"Request path: {request.path}")
        response = self.get_response(request)
        # Após a view
        response['X-Hello'] = 'World'
        return response
```

No `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    ...
    'myproject.middleware.SimpleMiddleware',
]
```

### 10.2 Context Processors

```python
# myproject/context_processors.py

def site_info(request):
    return {'site_name': 'Meu Blog'}

# settings.py
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                ...
                'myproject.context_processors.site_info',
            ],
        },
    },
]
```

* Permite usar `{{ site_name }}` em qualquer template.

---

## 11. Autenticação e Autorização

### 11.1 Sistema de Usuários Padrão

* Django inclui modelo `User` em `django.contrib.auth.models` com campos `username`, `email`, `password`, `is_staff`, `is_superuser`.
* Crie superusuário:

  ```bash
  python manage.py createsuperuser
  ```

### 11.2 Protected Views com Decorators

```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
```

### 11.3 Permissões e Grupos

```python
from django.contrib.auth.models import Group, Permission

# Criar grupo e atribuir permissões
editors = Group.objects.create(name='Editors')
perm = Permission.objects.get(codename='change_post')
editors.permissions.add(perm)

# Atribuir usuário ao grupo
user.groups.add(editors)
```

### 11.4 Autenticação via Views

```python
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('post_list')
```

---

## 12. Testes Automatizados

### 12.1 Configurando pytest-django

```bash
pip install pytest pytest-django factory-boy
```

Crie `pytest.ini`:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = myproject.settings
python_files = tests.py test_*.py *_tests.py
```

### 12.2 Exemplo de Teste de Model e View

```python
# blog/tests/test_models.py
import pytest
from blog.models import Author

@pytest.mark.django_db
def test_author_str():
    author = Author.objects.create(name='Alice', email='alice@example.com')
    assert str(author) == 'Alice'

# blog/tests/test_views.py
from django.urls import reverse
from rest_framework.test import APIClient  # se usar DRF

@pytest.mark.django_db
def test_post_list_view(client):
    response = client.get(reverse('post_list'))
    assert response.status_code == 200
    assert b'Nenhum post' in response.content
```

* `@pytest.mark.django_db` permite acesso ao banco.
* `client` fixture faz requisições simuladas.

---

## 13. Deploy em Produção

### 13.1 Servidor WSGI com Gunicorn

```bash
pip install gunicorn
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 13.2 Configurando Nginx como Proxy Reverso

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /path/to/myproject;  # contém /static/
    }
    location /media/ {
        root /path/to/myproject;  # contém /media/
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 13.3 Configurações de Segurança em settings.py

```python
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
```

### 13.4 Variáveis de Ambiente e Configuração

* Use `django-environ` ou `python-decouple` para gerenciar segredos e configurações fora do código.

```python
# settings.py
import environ
env = environ.Env(DEBUG=(bool, False))

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')
DATABASES = { 'default': env.db() }
```

---

## 14. Boas Práticas e Considerações

1. **Mantenha `DEBUG=False`** em produção para não expor informações sensíveis.
2. **Use variáveis de ambiente** para configurações sensíveis (SECRET\_KEY, DB credentials).
3. **Divida configurações** em múltiplos arquivos (`settings/base.py`, `settings/prod.py`, `settings/dev.py`).
4. **Configure permissão de arquivo e diretórios** corretamente, especialmente para mídia e estáticos.
5. **Aplique limpezas periódicas**: verifique logs, migrations pendentes, arquivos antigos no media.
6. **Use WhiteNoise ou CDN** para servir arquivos estáticos em produção.
7. **Implemente caching** (Redis, Memcached) para otimizar desempenho.
8. **Proteja endpoints** com CSRF tokens e permissões adequadas.
9. **Documente a API** utilizando DRF e Swagger (drf-yasg) se estiver usando Django REST Framework.
10. **Teste e monitore**: configure Sentry, New Relic ou outras ferramentas para acompanhar erros e desempenho.

---

## 15. Conclusão

Django é um framework robusto e maduro, adequado para aplicações web de pequeno ao grande porte. Com recursos nativos para administração, ORM, roteamento, autenticação e segurança, permite entregar aplicações com rapidez e seguir boas práticas de desenvolvimento. Este guia cobertura desde conceitos básicos até tópicos avançados, fornecendo base sólida para criar e manter aplicações em Django.
