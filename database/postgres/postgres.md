# **PostgreSQL - Banco de Dados Relacional Avançado** 🛠️

O **PostgreSQL** é um dos bancos de dados relacionais mais poderosos e amplamente usados, especialmente em ambientes Ruby on Rails. Ele oferece **alta performance**, **robustez** e uma série de funcionalidades que o tornam muito atraente para aplicações complexas.

### **✅ O que você precisa saber sobre PostgreSQL:**

---

## **1️⃣ Fundamentos do PostgreSQL**

### **✅ Tipos de Dados:**

O PostgreSQL suporta uma vasta gama de tipos de dados nativos, o que o torna muito flexível.

### **Tipos de Dados Comuns:**

- **Inteiros e Flutuantes:**
    - `INTEGER`, `BIGINT`, `SMALLINT`, `DECIMAL`, `NUMERIC`, `FLOAT`, `REAL`
- **Strings:**
    - `TEXT`, `VARCHAR(n)`, `CHAR(n)`
- **Data e Hora:**
    - `DATE`, `TIME`, `TIMESTAMP`, `TIMESTAMPTZ` (timestamp com timezone), `INTERVAL`
- **Booleanos:**
    - `BOOLEAN` (com valores `TRUE` ou `FALSE`)
- **Outros Tipos Avançados:**
    - **JSON/JSONB**: Armazenamento de dados em formato JSON.
    - **HSTORE**: Armazenamento de pares chave-valor.
    - **ARRAY**: Arrays de qualquer tipo (ex: `INTEGER[]`, `TEXT[]`).
    - **UUID**: Identificadores únicos universais (muito útil para sistemas distribuídos).

### **✅ Constraints e Integridade de Dados:**

O PostgreSQL oferece uma variedade de **constraints** para garantir a integridade dos dados:

- **NOT NULL**: Garantir que uma coluna não aceite valores nulos.
- **UNIQUE**: Garantir que os valores em uma coluna sejam únicos.
- **CHECK**: Validar se os dados atendem a uma condição especificada.
- **FOREIGN KEY**: Estabelece relações entre tabelas.
- **PRIMARY KEY**: Combinação de **NOT NULL** e **UNIQUE**, usado para identificar registros de forma única.

---

## **2️⃣ Relacionamentos e Normalização**

### **✅ Tipos de Relacionamento:**

- **Um-para-um (1:1)**: Um registro em uma tabela está associado a exatamente um registro em outra tabela. Usualmente implementado com **FOREIGN KEY**.
- **Um-para-muitos (1:N)**: Um registro em uma tabela pode estar associado a vários registros em outra tabela. Comumente implementado através de uma chave estrangeira na tabela "muitos".
- **Muitos-para-muitos (N:M)**: Implementado por meio de uma tabela intermediária (tabela de associação) que tem **chaves estrangeiras** de ambas as tabelas.

### **✅ Normalização e Desnormalização:**

- **1NF (Primeira Forma Normal)**: Cada campo contém um único valor, sem grupos repetitivos.
- **2NF (Segunda Forma Normal)**: Elimina dependências parciais, ou seja, todos os atributos não-chave dependem da chave primária.
- **3NF (Terceira Forma Normal)**: Elimina dependências transitivas, ou seja, atributos não-chave devem depender apenas da chave primária.

Em PostgreSQL, você pode usar as constraints e tipos de dados para garantir que sua base de dados siga as melhores práticas de normalização.

---

## **3️⃣ Consultas Avançadas**

### **✅ SELECT e Joins:**

Os **Joins** em PostgreSQL são fundamentais para combinar dados de várias tabelas.

- **INNER JOIN**: Retorna registros que possuem correspondência em ambas as tabelas.

```sql
SELECT *
FROM produtos
INNER JOIN categorias ON produtos.categoria_id = categorias.id;
```

- **LEFT JOIN**: Retorna todos os registros da tabela à esquerda e os correspondentes da tabela à direita (se existirem).

```sql
SELECT *
FROM produtos
LEFT JOIN categorias ON produtos.categoria_id = categorias.id;
```

- **RIGHT JOIN**, **FULL OUTER JOIN**: Menos usados, mas podem ser úteis dependendo do cenário.

### **✅ Subqueries:**

Subconsultas podem ser úteis para executar consultas dentro de outras consultas.

```sql
SELECT nome, salario
FROM empregados
WHERE salario > (SELECT AVG(salario) FROM empregados);
```

### **✅ Agrupamento e Funções Agregadas:**

- **GROUP BY**: Agrupa dados com base em uma coluna específica.

```sql
SELECT categoria_id, COUNT(*)
FROM produtos
GROUP BY categoria_id;
```

- **Funções Agregadas**: `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`.

```sql
SELECT AVG(salario)
FROM empregados;
```

---

## **4️⃣ Índices e Performance**

### **✅ Índices:**

Os **índices** são cruciais para melhorar a performance de consultas, principalmente em bancos de dados grandes.

- **Índices Simples**:

```sql
CREATE INDEX idx_nome ON empregados(nome);
```

- **Índices Compostos**: Para consultas que filtram por mais de uma coluna.

```sql
CREATE INDEX idx_nome_salario ON empregados(nome, salario);
```

- **Índices com UNIQUE**: Impedem a duplicação de valores na coluna indexada.

```sql
CREATE UNIQUE INDEX idx_email_unique ON empregados(email);
```

- **Índices Parciais**: Índices que são aplicados a apenas um subconjunto de dados.

```sql
CREATE INDEX idx_ativos ON empregados(salario) WHERE status = 'ativo';
```

### **✅ Analisando e Otimizando Consultas com EXPLAIN:**

O PostgreSQL oferece a palavra-chave **EXPLAIN** para mostrar o plano de execução de uma consulta.

```sql
EXPLAIN ANALYZE
SELECT * FROM produtos WHERE categoria_id = 1;
```

Isso ajudará a identificar gargalos de performance, como falta de índices.

---

## **5️⃣ Transações e Controle de Concurrency**

### **✅ Transações:**

O PostgreSQL permite que você execute várias operações de forma **atômica** usando transações.

- **Iniciar e Confirmar uma Transação:**

```sql
BEGIN;
UPDATE produtos SET preco = 100 WHERE id = 1;
COMMIT;
```

- **Rollback**: Caso algo dê errado, você pode reverter as alterações.

```sql
BEGIN;
UPDATE produtos SET preco = 100 WHERE id = 1;
ROLLBACK;
```

### **✅ Isolamento de Transações:**

- **READ UNCOMMITTED**: Transações podem ler dados não confirmados.
- **READ COMMITTED**: Transações leem apenas dados confirmados.
- **REPEATABLE READ**: As leituras são consistentes dentro de uma transação.
- **SERIALIZABLE**: O nível mais alto de isolamento, garantindo que nenhuma outra transação possa interferir.

---

## **6️⃣ Funcionalidades Avançadas do PostgreSQL**

### **✅ Funções e Procedimentos Armazenados:**

PostgreSQL permite escrever **funções** e **procedimentos armazenados** para encapsular a lógica do lado do banco de dados.

```sql
CREATE FUNCTION soma_valores(a INT, b INT) RETURNS INT AS $$
BEGIN
  RETURN a + b;
END;
$$ LANGUAGE plpgsql;
```

### **✅ Views:**

Views são consultas armazenadas no banco de dados que podem ser tratadas como tabelas.

```sql
CREATE VIEW produtos_ativos AS
SELECT nome, preco FROM produtos WHERE ativo = TRUE;
```

### **✅ Triggers:**

Triggers são procedimentos que são automaticamente executados em resposta a eventos (INSERT, UPDATE, DELETE) em uma tabela.

```sql
CREATE TRIGGER atualiza_timestamp
AFTER UPDATE ON produtos
FOR EACH ROW
EXECUTE FUNCTION atualiza_data_modificacao();
```

---

## **7️⃣ PostgreSQL com Rails**

### **✅ Configuração de PostgreSQL no Rails:**

- **Gemfile**:

```ruby
ruby
CopiarEditar
gem 'pg', '~> 1.1'
```

- **Database Configuration** (em `config/database.yml`):

```yaml
yaml
CopiarEditar
development:
  adapter: postgresql
  database: minha_app_development
  username: postgres
  password: password
  host: localhost
```

### **✅ Migrations**:

Rails gera **migrations** para interagir com o banco de dados. Quando você define um modelo com `rails generate model`, ele cria automaticamente as migrations.

Exemplo de criação de tabela:

```ruby
ruby
CopiarEditar
create_table :produtos do |t|
  t.string :nome
  t.decimal :preco, precision: 10, scale: 2
  t.timestamps
end

```

---

# **📌 Conclusão**

1. **Tipos de Dados**: PostgreSQL é muito flexível, oferecendo uma ampla gama de tipos de dados nativos.
2. **Consultas Avançadas**: Inclui **joins**, **subqueries**, **funções agregadas**, e muito mais.
3. **Índices e Performance**: Use **índices** e a palavra-chave **EXPLAIN** para otimizar consultas.
4. **Transações e Concorrência**: Assegure que seu banco de dados siga as melhores práticas de isolamento de transações.
5. **Funções Avançadas**: Aproveite **funções armazenadas**, **triggers** e **views** para maior eficiência.
