# Guia Completo do FastAPI

Este guia apresenta de forma detalhada o **FastAPI**, um framework moderno e de alta performance para construir APIs em Python, cobrindo desde conceitos básicos até tópicos avançados como segurança, dependências, testes e deploy.

---

## 1. O que é FastAPI?

O **FastAPI** é um framework assíncrono para criar APIs RESTful e GraphQL em Python, lançado em 2018 por Sebastián Ramírez. Baseado em **Starlette** para a parte de networking e **Pydantic** para validação de dados, o FastAPI possui as seguintes características:

* **Alto desempenho**: comparável a frameworks em Go e Node.js utilizando Uvicorn/Hypercorn.
* **Validação automática**: utiliza Pydantic para validação de dados de entrada e saída.
* **Documentação interativa**: gera documentação automática Swagger/OpenAPI disponível em `/docs` e Redoc em `/redoc`.
* **Tipagem estática**: usa anotações de tipo Python para gerar validações e documentação.
* **Suporte a async/await**: permite handlers assíncronos sem esforço extra.
* **Facilidade de uso**: minimalista, com poucos arquivos de configuração.

---

## 2. Instalação e Configuração Inicial

### 2.1 Requisitos

* Python 3.7 ou superior.
* idealmente um ambiente virtual (venv ou Conda).

### 2.2 Instalação

```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar FastAPI e Uvicorn para servidor ASGI
pip install fastapi uvicorn
```

### 2.3 Estrutura de Projeto Básica

```
project/
├── app/
│   ├── main.py        # ponto de entrada da aplicação
│   ├── routers/       # módulos de rota
│   │   └── items.py   # exemplo de rota
│   ├── models/        # modelos Pydantic e ORM
│   └── dependencies/  # dependências (DB, autenticação)
├── tests/             # testes unitários e integração
│   └── test_main.py
├── requirements.txt   # dependências do projeto
└── README.md
```

---

## 3. Criando a Primeira API

### 3.1 Aplicação Mínima

```python
# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

Rode a aplicação:

```bash
uvicorn app.main:app --reload
```

* O servidor estará disponível em `http://127.0.0.1:8000/`.
* A documentação Swagger estará em `http://127.0.0.1:8000/docs`.
* A documentação Redoc estará em `http://127.0.0.1:8000/redoc`.

### 3.2 Path Operations (Rotas) e Métodos HTTP

```python
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: dict):
    return {"item": item}
```

* Path parameter `item_id` é convertido para `int`.
* Query parameter `q` é opcional.
* No POST, o corpo JSON é recebido como `dict` por padrão (ver Pydantic abaixo).

---

## 4. Validação e Modelos com Pydantic

### 4.1 Modelos Pydantic

```python
# app/models/item.py
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
```

### 4.2 Uso de Modelos em Path Operations

```python
# app/main.py (continuação)
from fastapi import FastAPI
from app.models.item import Item

app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        total = item.price + item.tax
        item_dict.update({"total": total})
    return item_dict
```

* FastAPI converte automaticamente o JSON recebido para instância de `Item`.
* Se faltar algum campo obrigatório, retorna status 422 com detalhes da validação.

### 4.3 Resposta com Modelos Pydantic

```python
from fastapi import FastAPI
from app.models.item import Item

app = FastAPI()

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    return Item(name="Foo", price=10.5, tax=1.5)
```

* `response_model=Item` garante que apenas campos definidos em `Item` sejam retornados, filtrando dados sensíveis.

---

## 5. Dependências e Injeção de Dependência

### 5.1 Funções de Dependência Básicas

```python
from fastapi import Depends, HTTPException, status
from typing import Optional

fake_users_db = {"alice": {"username": "alice", "disabled": False}}

async def get_current_user(token: str):
    user = fake_users_db.get(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user

@app.get("/users/me")
def read_users_me(current_user = Depends(get_current_user)):
    return current_user
```

* `Depends()` indica que FastAPI deve chamar a função `get_current_user` e passar seu resultado como parâmetro.

### 5.2 Dependências com Cabeçalhos e Cookies

```python
from fastapi import Header, Cookie

async def get_token_header(x_token: str = Header(...)):
    if x_token != "mysecrettoken":
        raise HTTPException(status_code=400, detail="X-Token inválido")

@app.get("/protected", dependencies=[Depends(get_token_header)])
def protected_route():
    return {"message": "Acesso permitido"}
```

* `Header(...)` extrai valor de cabeçalho; `Cookie(...)` funciona similarmente.
* Ao usar `dependencies=[...]`, a dependência é avaliada antes do endpoint, e seu retorno não é passado.

### 5.3 Dependências com Classe

```python
from fastapi import Depends
from typing import Generator

class Database:
    def __init__(self):
        self.connection = "connection"
    def close(self):
        pass

async def get_db() -> Generator:
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
def read_items(db: Database = Depends(get_db)):
    return {"db": db.connection}
```

* Usando geradores, permitimos lógica de cleanup no bloco `finally`.

---

## 6. Autenticação e Segurança

### 6.1 Autenticação com OAuth2 e JWT

```python
# app/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "secretkey"
ALGORITHM = "HS256"

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.post("/token")
def login():
    # Implementar lógica de autenticação, retornar JWT
    return {"access_token": "tokenvalue", "token_type": "bearer"}

@app.get("/users/me")
def read_users_me(username: str = Depends(verify_token)):
    return {"user": username}
```

* `OAuth2PasswordBearer` extrai token do cabeçalho `Authorization: Bearer <token>`.
* `jose` faz codificação e decodificação JWT.

### 6.2 CORS e Middleware de Segurança

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

* Middleware deve ser adicionado antes de rotas para configurar CORS.

---

## 7. Middleware e Eventos do Ciclo de Vida

### 7.1 Middleware Customizado

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
n    response.headers["X-Process-Time"] = str(process_time)
    return response
```

* Middleware registra tempo de processamento e adiciona cabeçalho personalizado.

### 7.2 Eventos de Inicialização e Finalização

```python
@app.on_event("startup")
async def on_startup():
    # conectar a DB, inicializar conexões
    pass

@app.on_event("shutdown")
async def on_shutdown():
    # fechar conexões, limpar recursos
    pass
```

* Eventos são úteis para preparar recursos antes de servir requisições.

---

## 8. Background Tasks

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def write_log(message: str):
    with open("log.txt", mode="a") as f:
        f.write(message)

@app.post("/send-notification/{email}")
def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notificação enviada para {email}\n")
    return {"message": "Notificação agendada"}
```

* `BackgroundTasks` permite executar funções após retornar resposta.

---

## 9. Testes com pytest e TestClient

### 9.1 Instalando Dependências de Teste

```bash
pip install pytest pytest-asyncio httpx
```

### 9.2 Exemplo de Teste

```python
# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}

@pytest.mark.asyncio
async def test_create_item():
    data = {"name": "Item1", "price": 10.5}
    response = client.post("/items/", json=data)
    assert response.status_code == 200
    assert response.json()["name"] == "Item1"
```

* `TestClient` usa **starlette.testclient** para fazer requisições sem precisar de servidor externo.

---

## 10. Documentação Automática e Customização OpenAPI

### 10.1 Anotações de Metadados

```python
@app.get(
    "/items/{item_id}",
    summary="Obter item",
    description="Retorna um item pelo seu ID",
    response_description="Detalhes do item"
)
def read_item(item_id: int):
    return {"item_id": item_id}
```

* Parâmetros `summary`, `description` e `response_description` aparecem em `/docs`.

### 10.2 Tags de Roteamento

```python
@app.get("/users/{user_id}", tags=["users"])
def read_user(user_id: int):
    return {"user_id": user_id}
```

* Rotas agrupadas por `tags` na documentação.

### 10.3 Customizando OpenAPI Schema

```python
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API Exemplo",
        version="1.0.0",
        description="Descrição da API Exemplo",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

* Permite ajustar título, versão e descrição do schema.

---

## 11. Deploy em Produção

### 11.1 Servidores ASGI com Uvicorn e Gunicorn

```bash
# Com Uvicorn puro
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Com Gunicorn e Uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

* Geralmente, usa-se **Gunicorn** para gerenciar múltiplos processos e **Uvicorn** como worker ASGI.

### 11.2 Dockerização

```dockerfile
# Dockerfile\ nFROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]
```

```bash
# Build e run
docker build -t fastapi-app .
docker run -d -p 80:80 fastapi-app
```

### 11.3 Deploy em Nuvem

* **AWS**: Elastic Beanstalk, ECS, Fargate, Lambda (via API Gateway).
* **Azure**: App Service, Azure Functions.
* **Google Cloud**: Cloud Run, App Engine.

---

## 12. Integrações Comuns

* **Banco de Dados Relacional**: SQLAlchemy, Tortoise ORM, Databases (async).
* **Banco de Dados NoSQL**: MongoDB (Motor, Beanie), Redis (aioredis).
* **Filas/ Mensageria**: Celery (RabbitMQ/Redis), Kafka-python.
* **Autenticação/OAuth2**: OAuth2PasswordBearer, JWT, Auth0.
* **ORMs Async**: SQLModel (criado pelo autor do FastAPI), GINO, Tortoise.

---

## 13. Boas Práticas e Dicas

1. **Use Pydantic para Validação**: aproveite anotações de tipo para evitar validações manuais.
2. **Separe Rotas em Módulos**: organize endpoints em arquivos dentro de `routers/`.
3. **Utilize Dependências**: para conexão ao DB, autenticação e configurações.
4. **Evite Bloquear o Event Loop**: use bibliotecas compatíveis com async (por ex., `httpx` invés de `requests`).
5. **Configuração via Variáveis de Ambiente**: não deixe segredos no código.
6. **Documente com Anotações**: enriqueça a documentação Swagger com `summary`, `description`, `tags`.
7. **Teste Endpoints**: use `TestClient` e `pytest` para automação de testes.
8. **Monitore em Produção**: exponha métricas via Prometheus (Starlette Prometheus).
9. **Versão da API**: utilize prefixos de rota (`/v1`, `/v2`) para gerenciamento de versões.
10. **Atualize Dependências**: FastAPI se integra a Starlette e Pydantic; mantenha atualizados para aproveitar melhorias.

---

## 14. Conclusão

O FastAPI é um framework poderoso para construir APIs rápidas, seguras e bem documentadas em Python. Aproveitando Python moderno, tipagem estática e as bibliotecas Starlette e Pydantic, o FastAPI agiliza desenvolvimento, garante alta performance e documentação automática. Este guia cobriu desde o básico até tópicos avançados para ajudá-lo a criar aplicações de produção robustas.
