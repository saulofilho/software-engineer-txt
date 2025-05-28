# Guia Completo de NoSQL

Este guia apresenta uma visão avançada de bancos de dados NoSQL, incluindo tipos, casos de uso, modelagem, exemplos de consultas e considerações de performance e escalabilidade.

---

## 1. Introdução a NoSQL

* **NoSQL**: termo genérico para sistemas de banco de dados não relacionais, projetados para escalabilidade horizontal e flexibilidade de esquema.
* Surgiu para atender demandas de Big Data, alta disponibilidade e agilidade de desenvolvimento.
* **Características comuns**:

  * Sem esquema fixo (schema-less).
  * Escalabilidade horizontal (sharding / particionamento automático).
  * Modelo de consistência eventual em vez de ACID completo.

---

## 2. Principais Categorias de NoSQL

| Tipo            | Descrição                                        | Exemplos              |
| --------------- | ------------------------------------------------ | --------------------- |
| **Key-Value**   | Armazena pares chave-valor simples               | Redis, DynamoDB       |
| **Document**    | Armazena documentos JSON/BSON flexíveis          | MongoDB, Couchbase    |
| **Wide-Column** | Armazena tabelas com colunas dinâmicas por linha | Cassandra, HBase      |
| **Graph**       | Representa dados como nós e arestas              | Neo4j, JanusGraph     |
| **Time-Series** | Otimizado para dados temporais com alta ingestão | InfluxDB, TimescaleDB |

---

## 3. Modelagem de Dados

### 3.1 Key-Value

* **Chave** única mapeada para um valor arbitrário.
* **Uso**: caches, sessões, configurações.

```bash
# Redis
SET session:123 "user_data"
GET session:123
```

### 3.2 Document

* **Documento**: JSON, BSON ou YAML.
* **Coleções**: agrupam documentos.
* Suporta índices em campos aninhados.

```js
// MongoDB
db.users.insertOne({
  _id: 1,
  name: "Alice",
  address: { city: "SP", zip: "01000-000" },
  tags: ["admin","user"]
});

// Consulta
db.users.find({"address.city": "SP"});
```

### 3.3 Wide-Column

* **Linhas** identificadas por chave de partição.
* **Colunas** agrupadas em famílias e dinâmicas.

```cql
// Cassandra
CREATE TABLE users (
  user_id uuid PRIMARY KEY,
  name text,
  email text
) WITH comment='User data';

SELECT * FROM users WHERE user_id = 1234;
```

### 3.4 Graph

* **Nós** representam entidades, **arestas** representam relações.
* Suporta consultas de grafos (traversals).

```cypher
// Neo4j
CREATE (a:Person {name:'Bob'}), (b:Person {name:'Carol'}), (a)-[:FRIEND]->(b);
MATCH (p:Person)-[:FRIEND]->(friend) WHERE p.name='Bob' RETURN friend.name;
```

### 3.5 Time-Series

* Índices otimizados por timestamp.
* Operações de agregação por intervalo de tempo.

```sql
-- InfluxQL
SELECT mean("value") FROM "cpu_usage" WHERE time > now() - 1h GROUP BY time(1m);
```

---

## 4. Consistência e Disponibilidade

* **Modelo CAP**: Coerência, Disponibilidade, Tolerância a Partições (escolher dois).
* **Consistência Eventual**: diferentes réplicas convergem ao mesmo estado com o tempo.
* **Consistência Forte** (em alguns NoSQL): MongoDB replica primária-leitura primária; Cassandra suporta QUORUM.

---

## 5. Escalabilidade e Sharding

* **Sharding** automático (MongoDB, Cassandra): distribui dados entre nós.
* **Chave de partição**: escolhida para balancear carga e evitar hotspots.

```js
// MongoDB Shard Key
sh.shardCollection("db.collection", { user_id: "hashed" });
```

---

## 6. Indexação e Performance

* **Índices Simples e Compostos**: suportados por maioria (MongoDB, Cassandra secundários, Redis Sorted Sets).
* **TTL Indexes**: expiração automática de documentos (Redis expira chaves, MongoDB TTL Index).
* **In-Memory vs On-Disk**: Redis mantém tudo em RAM; outros usam cache LRU.

---

## 7. Transações e Multidocumento

* **Atomicidade de documento único**: garantida na maioria.
* **Transações ACID multi-documento**: suportadas em MongoDB 4.x, Cassandra 4.x (lightweight transactions) com limitações de performance.

```js
// MongoDB transação
const session = client.startSession();
session.startTransaction();
try {
  db.collection1.insertOne(doc1, { session });
  db.collection2.insertOne(doc2, { session });
  session.commitTransaction();
} catch (e) {
  session.abortTransaction();
}
session.endSession();
```

---

## 8. Casos de Uso e Trade-offs

| Tipo        | Uso Ideal                                        | Trade-offs                             |
| ----------- | ------------------------------------------------ | -------------------------------------- |
| Key-Value   | Cache, session, configuração                     | Sem consulta complexa                  |
| Document    | APIs RESTful, CMS, e-commerce                    | Operações de escrita maiores           |
| Wide-Column | Telemetria, IoT, logs                            | Modelagem de consultas antes do design |
| Graph       | Redes sociais, recomendações, detecção de fraude | Custo de armazenamento (meta dados)    |
| Time-Series | Monitoramento, métricas, IoT                     | Retenção e downsampling                |

---

## 9. Ferramentas Populares

* **Key-Value**: Redis, DynamoDB, Riak KV.
* **Document**: MongoDB, CouchDB, Couchbase.
* **Wide-Column**: Cassandra, HBase, ScyllaDB.
* **Graph**: Neo4j, JanusGraph, Amazon Neptune.
* **Time-Series**: InfluxDB, TimescaleDB, Prometheus.

---

## 10. Boas Práticas

1. **Escolher o tipo certo** de NoSQL conforme requisitos de consulta e consistência.
2. **Modelar dados pensando na consulta**: duplication aceitável para performance.
3. **Planejar shard key** para balanceamento de carga.
4. **Monitorar métricas de latência e uso** (-built-in dashboards, Prometheus).
5. **Gerenciar TTL e arquivamento** para retenção de dados.

---

## 11. Conclusão

Bancos de dados NoSQL oferecem flexibilidade, performance e escalabilidade para cenários de Big Data e microserviços. Compreender os tipos, trade-offs e práticas de modelagem é essencial para arquitetar sistemas robustos e eficientes.
