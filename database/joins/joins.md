---

No **PostgreSQL** (e em bancos relacionais em geral), os diferentes tipos de **JOINs** determinam como as tabelas são combinadas e quais registros são retornados. Aqui estão todas as diferenças:

### 🔹 **INNER JOIN**

- Retorna apenas os registros que possuem correspondência em **ambas as tabelas**.
- Se não houver correspondência, a linha é descartada.

📌 **Exemplo:**

```sql
SELECT users.id, users.name, orders.id AS order_id
FROM users
INNER JOIN orders ON users.id = orders.user_id;

```

✅ **Somente usuários que têm pedidos aparecem no resultado.**

---

### 🔹 **LEFT JOIN (LEFT OUTER JOIN)**

- Retorna **todos os registros da tabela à esquerda** e apenas os correspondentes da tabela à direita.
- Se não houver correspondência, a parte da tabela da direita retorna **NULL**.

📌 **Exemplo:**

```sql
SELECT users.id, users.name, orders.id AS order_id
FROM users
LEFT JOIN orders ON users.id = orders.user_id;

```

✅ **Todos os usuários aparecem, mesmo os que não têm pedidos (com `order_id` como NULL).**

---

### 🔹 **RIGHT JOIN (RIGHT OUTER JOIN)**

- Retorna **todos os registros da tabela à direita** e apenas os correspondentes da tabela à esquerda.
- Se não houver correspondência, a parte da tabela da esquerda retorna **NULL**.

📌 **Exemplo:**

```sql
SELECT users.id, users.name, orders.id AS order_id
FROM users
RIGHT JOIN orders ON users.id = orders.user_id;

```

✅ **Todos os pedidos aparecem, mesmo os que não têm um usuário correspondente (com `users.id` como NULL).**

---

### 🔹 **FULL JOIN (FULL OUTER JOIN)**

- Retorna **todos os registros de ambas as tabelas**, preenchendo com **NULL** onde não houver correspondência.

📌 **Exemplo:**

```sql
SELECT users.id, users.name, orders.id AS order_id
FROM users
FULL JOIN orders ON users.id = orders.user_id;

```

✅ **Retorna todos os usuários e pedidos, mesmo os que não têm correspondência.**

---

### 🔹 **CROSS JOIN**

- Faz um **produto cartesiano** das tabelas, combinando **todas as linhas de uma com todas da outra**.
- Não precisa de condição `ON`.

📌 **Exemplo:**

```sql
SELECT users.name, orders.id AS order_id
FROM users
CROSS JOIN orders;

```

✅ **Se há 5 usuários e 3 pedidos, o resultado tem 15 linhas.**

---

### 🔹 **SELF JOIN**

- Junta uma tabela com ela mesma.
- Usado para comparar registros dentro da mesma tabela.

📌 **Exemplo:**

```sql
SELECT e1.name AS employee, e2.name AS manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.id;

```

✅ **Lista funcionários junto com seus gerentes.**

---

### **Resumo Rápido:**

| JOIN | Retorna |
| --- | --- |
| `INNER JOIN` | Somente correspondências |
| `LEFT JOIN` | Tudo da esquerda + correspondências |
| `RIGHT JOIN` | Tudo da direita + correspondências |
| `FULL JOIN` | Tudo de ambos os lados |
| `CROSS JOIN` | Produto cartesiano |
| `SELF JOIN` | Tabela unida a si mesma |

Quer exemplos no contexto de um **Rails App** usando ActiveRecord? 😊

4o

### Você disse:

sim

### O ChatGPT disse:

No **Ruby on Rails** com **ActiveRecord**, os joins podem ser feitos de maneira elegante e idiomática. Aqui estão os principais tipos de **JOINs** e como usá-los.

---

## **1️⃣ INNER JOIN (default em joins)**

No ActiveRecord, `joins` faz um **INNER JOIN**, ou seja, só traz registros que têm correspondência.

### **Exemplo**:

Listar **usuários que têm pedidos** (`User` com `Order`).

```ruby
ruby
CopiarEditar
User.joins(:orders)

```

🔹 Equivalente a:

```sql
SELECT users.* FROM users INNER JOIN orders ON users.id = orders.user_id;

```

✅ **Retorna apenas usuários que têm pedidos.**

---

## **2️⃣ LEFT JOIN (LEFT OUTER JOIN)**

Para incluir **todos os usuários**, mesmo os que não têm pedidos, usamos `left_outer_joins`.

### **Exemplo**:

```ruby
ruby
CopiarEditar
User.left_outer_joins(:orders)

```

🔹 Equivalente a:

```sql
SELECT users.* FROM users LEFT OUTER JOIN orders ON users.id = orders.user_id;

```

✅ **Retorna todos os usuários, preenchendo `NULL` para quem não tem pedidos.**

---

## **3️⃣ RIGHT JOIN (não tem no ActiveRecord)**

- O Rails **não suporta `RIGHT JOIN` nativamente**.
- Se precisar, use **SQL puro** com `from` e `joins`.

### **Exemplo**:

```ruby
ruby
CopiarEditar
User.from("users RIGHT JOIN orders ON users.id = orders.user_id")

```

✅ **Retorna todos os pedidos, mesmo sem usuário correspondente.**

---

## **4️⃣ FULL JOIN (FULL OUTER JOIN)**

- Também **não tem suporte nativo** no Rails.
- Mas podemos usar SQL puro.

### **Exemplo**:

```ruby
ruby
CopiarEditar
User.find_by_sql(<<-SQL)
  SELECT * FROM users
  FULL OUTER JOIN orders ON users.id = orders.user_id
SQL

```

✅ **Retorna tudo de ambos os lados, preenchendo `NULL` onde não há correspondência.**

---

## **5️⃣ CROSS JOIN (Produto cartesiano)**

- No Rails, usamos **Arel**.

### **Exemplo**:

```ruby
ruby
CopiarEditar
User.joins("CROSS JOIN orders")

```

🔹 Equivalente a:

```sql
SELECT users.*, orders.* FROM users CROSS JOIN orders;

```

✅ **Cada usuário é combinado com todos os pedidos (perigoso em tabelas grandes!).**

---

## **6️⃣ SELF JOIN (Relacionamento com a própria tabela)**

- Exemplo clássico: **Usuário e Gerente** (estrutura hierárquica).

### **Model**:

```ruby
ruby
CopiarEditar
class Employee < ApplicationRecord
  has_many :subordinates, class_name: "Employee", foreign_key: "manager_id"
  belongs_to :manager, class_name: "Employee", optional: true
end

```

### **Query**:

```ruby
ruby
CopiarEditar
Employee.joins(:manager).select("employees.*, managers.name AS manager_name")

```

✅ **Lista funcionários junto com o nome do gerente.**

---

## **Resumindo:**

| Tipo de JOIN | ActiveRecord | Alternativa |
| --- | --- | --- |
| INNER JOIN | `joins(:orders)` | - |
| LEFT JOIN | `left_outer_joins(:orders)` | - |
| RIGHT JOIN | ❌ | `from("users RIGHT JOIN orders ...")` |
| FULL JOIN | ❌ | `find_by_sql(...)` |
| CROSS JOIN | `joins("CROSS JOIN orders")` | - |
| SELF JOIN | `joins(:manager)` | - |