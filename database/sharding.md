# Sharding em Banco de Dados

## 🧩 O que é Sharding?

**Sharding** é uma técnica de **particionamento horizontal** usada para distribuir os dados de um banco de dados em múltiplos servidores ou instâncias. Cada fragmento dos dados é chamado de **shard**, e contém uma parte dos registros da tabela original.

### Exemplo:

Uma tabela de usuários com 100 milhões de registros pode ser dividida em shards:

- **Shard 1**: usuários com IDs de 1 a 25 milhões  
- **Shard 2**: usuários com IDs de 25 a 50 milhões  
- **Shard 3**: usuários com IDs de 50 a 75 milhões  
- **Shard 4**: usuários com IDs de 75 a 100 milhões  

---

## 🛠 Tipos de Sharding

### 1. Sharding por Range (Intervalo)
Divide os dados com base em faixas de valores.

- Exemplo: ID de 1 a 1000 vai para o Shard A, 1001 a 2000 para o Shard B.

📌 **Prós:** fácil de entender.  
⚠️ **Contras:** pode causar desequilíbrio de carga.

---

### 2. Sharding por Hash
Utiliza uma função hash para distribuir os dados uniformemente.

- Exemplo: `hash(user_id) % número_de_shards`

📌 **Prós:** boa distribuição dos dados.  
⚠️ **Contras:** dificulta buscas por intervalo.

---

### 3. Sharding Geográfico
Baseia-se na localização dos dados.

- Exemplo: usuários da Europa em um shard, da América em outro.

📌 **Prós:** útil para sistemas globais.  
⚠️ **Contras:** mais complexo para usuários que mudam de localização.

---

## ✅ Vantagens do Sharding

- **Escalabilidade horizontal:** fácil de escalar adicionando novos servidores.
- **Melhoria de performance:** menos dados por shard = consultas mais rápidas.
- **Alta disponibilidade:** falha em um shard não afeta os demais diretamente.

---

## ❌ Desvantagens do Sharding

- **Complexidade de implementação**
- **Transações entre shards são difíceis**
- **Reparticionamento de dados é custoso**

---

## 🔧 Ferramentas e Bancos com Suporte a Sharding

- **MongoDB**: possui suporte nativo a sharding.
- **Apache Cassandra**: sharding faz parte da arquitetura base.
- **MySQL**: pode ser usado com middleware como ProxySQL ou Vitess.
- **PostgreSQL**: suporta sharding com Citus ou implementações manuais.

---

## 📌 Conclusão

Sharding é uma técnica poderosa para escalar bancos de dados de forma horizontal, mas deve ser usada com cuidado devido à sua complexidade e desafios associados à manutenção e consistência dos dados.
