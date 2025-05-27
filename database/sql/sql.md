# Guia Avançado de SQL

Abaixo está um guia de nível avançado sobre SQL, cobrindo desde modelagem até técnicas avançadas de consulta, otimização de desempenho, manipulação de dados semi-estruturados e programação no banco. Cada seção traz exemplos práticos em SQL.

---

## 1. Modelagem Relacional e Normalização

1. **Formas Normais**

   * **1FN**: todos os atributos atômicos.
   * **2FN**: sem dependência parcial (tabelas com chave composta).
   * **3FN**: sem dependência transitiva.
   * **BCNF**: toda dependência funcional é de uma chave candidata.

   ```sql
   -- Exemplo: decompondo para 3FN
   -- Tabela inicial: Orders(order_id, customer_name, customer_email, product_id, qty)
   -- Separar Customer:
   CREATE TABLE Customer (
     customer_id SERIAL PRIMARY KEY,
     name TEXT NOT NULL,
     email TEXT UNIQUE NOT NULL
   );
   CREATE TABLE Orders (
     order_id SERIAL PRIMARY KEY,
     customer_id INT REFERENCES Customer(customer_id),
     product_id INT,
     qty INT
   );
   ```

2. **Chaves Surrogates vs. Naturais**

   * **Surrogate**: SERIAL/UUID; isolada de mudanças de negócio.
   * **Natural**: dados reais (ex: CPF); cuidado com mutabilidade.

---

## 2. Técnicas Avançadas de Consulta

### 2.1 Common Table Expressions (CTEs)

* **Não recursivas** para organizar consultas complexas:

  ```sql
  WITH TopSales AS (
    SELECT
      seller_id,
      SUM(amount) AS total_sales
    FROM sales
    GROUP BY seller_id
    HAVING SUM(amount) > 100000
  )
  SELECT c.name, t.total_sales
  FROM TopSales t
  JOIN sellers c ON c.id = t.seller_id;
  ```

* **Recursivas** para hierarquias:

  ```sql
  WITH RECURSIVE subordinates AS (
    SELECT id, manager_id, name
    FROM employees
    WHERE id = 1  -- CEO
    UNION ALL
    SELECT e.id, e.manager_id, e.name
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.id
  )
  SELECT * FROM subordinates;
  ```

### 2.2 Window Functions

* **Agregações “deslizantes”** sem agrupar linhas:

  ```sql
  SELECT
    order_id,
    order_date,
    amount,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date
                      ROWS BETWEEN 4 PRECEDING AND CURRENT ROW)
      AS rolling_5_orders
  FROM orders;
  ```

* **Ranking**:

  ```sql
  SELECT
    employee_id,
    department_id,
    salary,
    RANK()    OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_rank,
    DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dense_rank
  FROM employees;
  ```

### 2.3 LATERAL Joins

Para subconsultas dependentes de cada linha:

```sql
SELECT
  p.id,
  p.name,
  recent_orders.last_order_date
FROM products p
LEFT JOIN LATERAL (
  SELECT MAX(o.order_date) AS last_order_date
  FROM orders o
  WHERE o.product_id = p.id
) AS recent_orders ON TRUE;
```

---

## 3. Otimização e Desempenho

### 3.1 Índices

* **B-tree** (padrão): ordens, buscas de igualdade e intervalo.
* **Hash**: apenas igualdade (PostgreSQL).
* **GiST / SP-GiST / GIN**: para dados geométricos, documentos JSONB, textos.

```sql
-- Índice parcial só em registros ativos
CREATE INDEX idx_active_users ON users(email)
WHERE active = TRUE;
```

* **Cobertura** (covering index):

```sql
CREATE INDEX idx_sales_covering ON sales(customer_id, sale_date, amount);
-- Consulta só lê do índice, sem tocar na tabela.
```

### 3.2 EXPLAIN / EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE
SELECT * FROM orders WHERE order_date > '2025-01-01';
```

* Analise **Seq Scan** vs. **Index Scan**
* Verifique **cost**, **rows**, **actual time**, **loops**.

### 3.3 Particionamento

Dividir tabelas grandes em partições (por data, por faixa de valores):

```sql
CREATE TABLE sales (
  sale_id SERIAL,
  sale_date DATE NOT NULL,
  amount NUMERIC
) PARTITION BY RANGE (sale_date);

CREATE TABLE sales_2024 PARTITION OF sales
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE sales_2025 PARTITION OF sales
  FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

---

## 4. Transações e Concorrência

### 4.1 Níveis de Isolamento (ANSI SQL)

* **READ UNCOMMITTED**
* **READ COMMITTED** (padrão PostgreSQL)
* **REPEATABLE READ**
* **SERIALIZABLE**

```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- operações...
COMMIT;
```

### 4.2 Locks e Deadlocks

* Use `SELECT FOR UPDATE` para bloquear linhas:

  ```sql
  BEGIN;
  SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  COMMIT;
  ```

* Monitore deadlocks via logs do SGBD.

---

## 5. Programação no Banco

### 5.1 Stored Procedures e Functions

* **Função** retorna valor:

  ```sql
  CREATE FUNCTION calc_discount(total NUMERIC) RETURNS NUMERIC AS $$
  BEGIN
    IF total > 1000 THEN
      RETURN total * 0.1;
    ELSE
      RETURN 0;
    END IF;
  END; $$ LANGUAGE plpgsql;
  ```

* **Procedure** (não retorna):

  ```sql
  CREATE PROCEDURE archive_old_orders(cutoff DATE) LANGUAGE plpgsql AS $$
  BEGIN
    INSERT INTO orders_archive SELECT * FROM orders WHERE order_date < cutoff;
    DELETE FROM orders WHERE order_date < cutoff;
  END; $$;
  ```

### 5.2 Triggers

Automatizar auditoria, validações complexas:

```sql
CREATE TABLE audit_log (
  id SERIAL PRIMARY KEY,
  table_name TEXT,
  operation TEXT,
  changed_at TIMESTAMP DEFAULT NOW()
);

CREATE FUNCTION log_changes() RETURNS trigger AS $$
BEGIN
  INSERT INTO audit_log(table_name, operation)
    VALUES (TG_TABLE_NAME, TG_OP);
  RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_audit
  AFTER INSERT OR UPDATE OR DELETE ON orders
  FOR EACH ROW EXECUTE FUNCTION log_changes();
```

---

## 6. Dados Semi-Estruturados e Full-Text

### 6.1 JSON/JSONB

* **Indexar** campos:

  ```sql
  CREATE INDEX idx_orders_details ON orders USING GIN (details jsonb_path_ops);
  ```

* **Consultas**:

  ```sql
  SELECT * FROM orders
  WHERE details->>'status' = 'shipped';
  ```

### 6.2 Busca Full-Text (PostgreSQL)

```sql
ALTER TABLE articles
  ADD COLUMN tsv tsvector GENERATED ALWAYS AS (
    to_tsvector('portuguese', coalesce(title, '') || ' ' || coalesce(body, ''))
  ) STORED;

CREATE INDEX idx_articles_tsv ON articles USING GIN(tsv);

-- Pesquisa:
SELECT * FROM articles
WHERE tsv @@ plainto_tsquery('portuguese', 'evolução do SQL');
```

---

## 7. Escalabilidade e Alta Disponibilidade

* **Replicações** síncronas/assíncronas.
* **Sharding** em múltiplos nós (ex: Citus, Vitess).
* **Connection Pooling** (PgBouncer).
* **Backups** incrementais e PITR.

---

### Conclusão

Este panorama aborda desde a modelagem até tópicos de alto desempenho e programação interna do banco. Recomenda-se aprofundar em cada recurso no manual do seu SGBD (PostgreSQL, SQL Server, Oracle etc.) para detalhes de sintaxe e limitações específicas.
