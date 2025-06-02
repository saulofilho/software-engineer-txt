# Guia Completo do Redis

Este guia apresenta, de forma detalhada e avançada, o Redis: conceitos, arquitetura, instalação, comandos essenciais e avançados, persistência, replicação, clustering, desempenho, casos de uso e boas práticas.

---

## 1. O que é o Redis?

Redis (Remote Dictionary Server) é um **armazenamento de estrutura de dados em memória** de código aberto, usado como banco de dados, cache e broker de mensagens. Desenvolvido por Salvatore Sanfilippo em 2009, o Redis suporta estruturas como strings, listas, conjuntos, hashes, sorted sets, bitmaps e streams, com operações atômicas de alto desempenho.

**Características principais**:

* **Armazenamento em memória** (in-memory) com opção de persistência em disco.
* **Baixa latência** (≤ millisegundos).
* **Suporte a múltiplos tipos de dados** avançados.
* **Persistência** via snapshots (RDB) e log de comandos (AOF).
* **Replicação e Cluster** para alta disponibilidade e escalabilidade.
* **Pub/Sub** e **Streams** para mensageria e processamento de eventos.

---

## 2. Arquitetura Redis

### 2.1 Processo Único e Event Loop

* Redis é **single-threaded** para a maioria das operações, usando um loop de evento (event loop) para I/O.
* A simplicidade do modelo evita concorrência de threads, garantindo latências consistentes.
* Operações atômicas em estruturas de dados significam que não há necessidade de locks internos.

### 2.2 Armazenamento em Memória e Persistência

* **Armazenamento em RAM**: todas as estruturas ficam na memória para acesso rápido.
* **Persistência Opcional**:

  * **RDB (Redis Database File)**: snapshots periódicos do dataset em arquivo binário.
  * **AOF (Append Only File)**: log de todas as operações de escrita, permitindo reconstruir dataset a partir do log.
  * É possível usar apenas RDB, apenas AOF, ou ambos (AOF para durabilidade e RDB para recuperações rápidas).

### 2.3 Replicação Mestre–Escravo

* Redis suporta **replicação assíncrona**:

  1. Um nó **escravo** conecta a um nó **mestre** e sincroniza o dataset via RDB ou AOF.
  2. Após sincronização inicial, o escritor continua recebendo comandos no mestre e reencaminhando para escravos.
* **Failover** manual ou via Sentinel.
* Escravos podem servir leituras, distribuindo carga.

### 2.4 Sentinel e Alta Disponibilidade

* **Redis Sentinel** monitora instâncias mestre e escravo.
* Funciona como orquestrador de failover automático: detecta falhas de mestre, promove um escravo a mestre e reconfigura outros escravos.
* Fornece serviço de descoberta de mestre para clientes.

### 2.5 Cluster Redis

* Redis Cluster é a solução nativa para **escala horizontal** com **sharding de dados** e **failover automático**.
* Divide *keyspace* em **16.384 slots**. Cada chave é mapeada a um slot via hash CRC16.
* Cada nó do cluster é responsável por um subconjunto de slots.
* **Replicação**: cada slot tem nó mestre e réplicas.
* **Failover**: se um mestre ficar indisponível, um escravo assume.

---

## 3. Instalação e Configuração

### 3.1 Requisitos

* Sistema Linux, macOS, Windows (via WSL ou Docker).
* GCC ou compilador compatível para compilar de código-fonte, opcionalmente pacote binário.

### 3.2 Compilação a partir do Código Fonte

```bash
# Clonar repositório Redis
git clone https://github.com/redis/redis.git
cd redis
# Compilar (produz serve e redis-cli em src/)
make
# Testar compilação
make test
# Instalar em /usr/local/bin (opcional)
sudo make install
```

### 3.3 Instalação via Pacotes

* **Debian/Ubuntu**:

  ```bash
  sudo apt update
  sudo apt install redis-server
  ```
* **CentOS/RHEL**:

  ```bash
  sudo yum install epel-release
  sudo yum install redis
  ```
* **Homebrew (macOS)**:

  ```bash
  brew install redis
  ```

### 3.4 Configuração Básica (`redis.conf`)

* Localização típica: `/etc/redis/redis.conf` ou `~/redis/redis.conf`.
* **Port** (padrão 6379): porta TCP para conexões.
* **Bind**: IPs em que o servidor escuta (padrão `127.0.0.1`).
* **Protected Mode**: impede conexões externas quando `bind` não está configurado.
* **requirepass**: define senha para clientes.
* **maxmemory** e **maxmemory-policy**: define limite de uso de memória e política de expulsão (eviction).
* **appendonly**: habilita AOF e define `appendfsync` (sempre, a cada segundo, nunca).
* **save**: define intervalos para snapshots RDB (por ex.: `save 900 1` — salve se ao menos 1 alteração em 900s).

---

## 4. Tipos de Dados e Comandos Essenciais

### 4.1 Strings

* **Uso**: valores binários ou de texto (limite 512 MB).
* **Comandos**:

  * `SET key value [EX seconds] [PX milliseconds] [NX|XX]`: armazena valor com opções de expiração e condição.
  * `GET key`: obtém valor.
  * `INCR key`, `DECR key`: incrementa/decrementa numericamente.

### 4.2 Hashes

* **Uso**: mapeia campos para valores, ideal para representar objetos.
* **Comandos**:

  * `HSET key field value`: define campo.
  * `HGET key field`: obtém valor de campo.
  * `HGETALL key`: obtém todos campos/valores.
  * `HINCRBY key field increment`: incrementa campo numericamente.

### 4.3 Lists (Listas)

* **Uso**: coleções ordenadas duplicáveis, implementadas como listas ligadas.
* **Comandos**:

  * `LPUSH key value [value ...]`, `RPUSH key value [value ...]`: insere à esquerda ou direita.
  * `LPOP key`, `RPOP key`: remove e retorna elemento da esquerda ou direita.
  * `LRANGE key start stop`: obtém sublista por índices.
  * `BRPOP key [timeout]`: bloqueia até valor disponível.

### 4.4 Sets (Conjuntos)

* **Uso**: coleções não ordenadas de elementos únicos.
* **Comandos**:

  * `SADD key member [member ...]`: adiciona membros.
  * `SMEMBERS key`: obtém todos membros.
  * `SISMEMBER key member`: verifica existência.
  * `SINTER key1 key2 ...`: intersecção de conjuntos.
  * `SRANDMEMBER key [count]`: retorna membro aleatório.

### 4.5 Sorted Sets (ZSets)

* **Uso**: sets ordenados por pontuação (`score`), adequado para ranking e leaderboard.
* **Comandos**:

  * `ZADD key [NX|XX] [CH] [INCR] score member [score member ...]`: adiciona membros com pontuação.
  * `ZRANGE key start stop [WITHSCORES]`: obtém intervalo classificado por rank.
  * `ZREM key member [member ...]`: remove membros.
  * `ZINCRBY key increment member`: incrementa pontuação.
  * `ZRANGEBYSCORE key min max [WITHSCORES]`: obtém intervalo por pontuação.

### 4.6 Bitmaps e Bitfields

* **Uso**: manipulação de bits em strings, para tracking de presença ou estatísticas.
* **Comandos**:

  * `SETBIT key offset value`: define bit no offset (0 ou 1).
  * `GETBIT key offset`: obtém bit.
  * `BITCOUNT key [start end]`: conta bits com valor 1.
  * `BITFIELD key ...`: operações atômicas em múltiplos bits.

### 4.7 HyperLogLog

* **Uso**: estimativa de cardinalidade (contagem de valores distintos) com erro \~0,81%.
* **Comandos**:

  * `PFADD key element [element ...]`: adiciona elementos para estimativa.
  * `PFCOUNT key [key ...]`: obtém estimativa de cardinalidade.
  * `PFMERGE destkey sourcekey [sourcekey ...]`: mescla estruturas.

### 4.8 Streams

* **Uso**: estrutura de log de eventos persistente, similar a Kafka, ideal para processamento de eventos.
* **Comandos**:

  * `XADD key [MAXLEN approx] * field value [field value ...]`: adiciona evento com ID gerado.
  * `XRANGE key start end [COUNT count]`: lê intervalo em ordem cronológica.
  * `XREAD [BLOCK milliseconds] STREAMS key [key ...] ID [ID ...]`: lê eventos a partir de IDs, bloqueando opcionalmente.
  * `XGROUP CREATE key groupname id`: cria grupo de consumo.
  * `XREADGROUP GROUP group consumer STREAMS key [key ...] ID [ID ...]`: lê eventos em contexto de grupo.

### 4.9 Geospatial

* **Uso**: armazenar coordenadas e consultas espaciais.
* **Comandos**:

  * `GEOADD key longitude latitude member`: adiciona ponto geoespacial.
  * `GEORADIUS key longitude latitude radius m|km|ft|mi WITHDIST WITHCOORD`: consulta por proximidade.
  * `GEOHASH key member [member ...]`: obtém geohash.

### 4.10 HyperLogLog, Bitmaps e Probabilísticos

* Redis fornece estruturas probabilísticas para casos de uso de cardinalidade (HyperLogLog), top N (TopK via RedisBloom) e contagem aproximada.

---

## 5. Persistência: RDB e AOF

### 5.1 RDB (Redis Database File)

* **Snapshots** periódicos do dataset em formato compactado, determinado por diretrizes em `save <seconds> <changes>`.
* **Vantagens**: arquivos RDB são compactos, rápidos para reinício.
* **Desvantagens**: pode perder dados entre snapshots (não durabilidade em tempo real).

### 5.2 AOF (Append Only File)

* **Log de Comandos**: cada operação de escrita é adicionada a um arquivo AOF.
* **Sincronização**:

  * `appendfsync always`: segura, mas lenta.
  * `appendfsync everysec` (padrão): grava no segundo, bom trade-off.
  * `appendfsync no`: rápida, mas sem garantia.
* **Rewrite**: AOF pode ser reescrito periodicamente para remover comandos redundantes.

### 5.3 Configuração Recomendada

* Em produção, use **RDB + AOF** para combinar reinício rápido e durabilidade.
* Ajuste `appendfsync` e `auto-aof-rewrite-percentage` para balancear I/O.

---

## 6. Replicação e Alta Disponibilidade

### 6.1 Configuração de Réplica (Slave)

* Para configurar réplicas, no `redis.conf` do nó escravo:

  ```ini
  replicaof <master_ip> <master_port>
  ```
* O escravo faz aprendizado inicial (sync) e depois replica incrementos (comando PSYNC).
* Réplicas podem responder a leituras se `replica-read-only yes`.

### 6.2 Sentinel

* **Sentinel** monitora mestres e escravos, detecta falhas e promove automaticamente:

  1. **monitor** directives no `sentinel.conf`: lista de mestres a serem monitorados.
  2. **quorum**: número mínimo de sentinelas que devem concordar que um mestre está offline.
  3. **failover**: lógica de promoção de escravo a mestre e reconfiguração de outros.

**Exemplo de `sentinel.conf`**:

```ini
port 26379
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel auth-pass mymaster minha_senha
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 10000
```

### 6.3 Redis Cluster

* Redis Cluster utiliza sharding nativo e failover integrado com múltiplos nós.
* Requer ao menos **3 mestres** (para quórum) e idealmente **3 réplicas**.
* **Ferramenta de criação de cluster**: `redis-cli --cluster create <ip1:port1> <ip2:port2> ... --cluster-replicas 1`.
* **Slots**: mapeamento de chaves para slots (0–16383).
* **Rebalanceamento**: remapeamento de slots entre nós à medida que a topologia muda.

---

## 7. Segurança e Autenticação

### 7.1 Autenticação Simples

* Defina `requirepass minha_senha` no `redis.conf` do servidor.
* Clientes devem usar `AUTH minha_senha` antes de comandos.

### 7.2 TLS/SSL

* Para criptografar tráfego e autenticar:

  1. Gere certificados (CA, servidor, cliente).
  2. Configure `tls-port`, `tls-cert-file`, `tls-key-file`, `tls-ca-cert-file` em `redis.conf`.
  3. Habilite `protected-mode no` quando usar TLS remota.

### 7.3 ACL (Redis 6+)

* Redis 6 introduziu **Access Control Lists** (ACL) para múltiplos usuários com permissões específicas:

  * Defina usuários em `users.acl` ou via `ACL SETUSER`.
  * Exemplos:

    ```bash
    ACL SETUSER alice on >senha ~* +@all
    ACL SETUSER bob on >senha ~cache:* +get +set
    ```
  * Permite restringir comandos e chaves a cada usuário.

---

## 8. Desempenho e Tuning

### 8.1 Políticas de Expulsão (Eviction)

Defina `maxmemory-policy` quando `maxmemory` for atingido:

* `noeviction`: retorna erro em comandos de escrita.
* `volatile-lru`: remove chave menos usada entre chaves com `EXPIRE`.
* `allkeys-lru`: remove menos usada entre todas as chaves.
* `volatile-random`: remove aleatoriamente chaves expiráveis.
* `allkeys-random`: remove aleatoriamente entre todas chaves.
* `volatile-ttl`: remove chave com menor tempo de vida entre expiráveis.

### 8.2 Gerenciamento de Memória

* Ajuste `maxmemory` para evitar trocas de swap.
* Monitore uso de memória via `INFO memory` ou `redis-cli memory stats`.
* **Lazy freeing**: operações como `DEL` podem liberar memória assincronamente (`lazyfree-lazy-eviction`, `lazyfree-lazy-expire`).

### 8.3 Persistência e I/O

* Ajuste `io-threads`: Redis 6+ permite threads de I/O para operações de rede.
* O AOF pode causar I/O intenso; use `appendfsync everysec` e `auto-aof-rewrite-percentage` para balancear.
* Ajuste `hz` (frequência de ticks internos) para tarefas de manutenção (expiração, RDB, atualização de estatísticas).

### 8.4 Pipeline e Multithreading no Cliente

* Use **pipelines** (`MULTI`/`EXEC` no redis-cli ou pipeline em bibliotecas) para agrupar múltiplos comandos e reduzir latência de rede.
* Clientes modernos suportam **multiplexação** para enviar múltiplas requisições simultâneas.

---

## 9. Módulos Redis

Redis suporta módulos extensíveis em C, Rust ou outras línguas:

* **RediSearch**: motor de busca full-text para Redis.
* **RedisJSON**: armazenamento nativo de documentos JSON com consultas.
* **RedisGraph**: extension de grafos via Cypher.
* **RedisBloom**: estruturas probabilísticas (Bloom Filter, Cuckoo Filter, Top-K).
* **RedisTimeSeries**: otimizado para dados temporais.

Use `MODULE LOAD <path>` para carregar dinamicamente.

---

## 10. Monitoramento e Observabilidade

### 10.1 Métricas Internas (INFO)

Comando `INFO [section]` expõe métricas:

* **Server**: versão, OS, uptime.
* **Clients**: conexões ativas.
* **Memory**: uso por dataset, peak, fragmentation.
* **Persistence**: status de RDB e AOF.
* **Stats**: comandos processados, hits/misses de cache.
* **Replication**: estado de mestre/escravo.
* **Cluster**: slots e estado do cluster.

### 10.2 Ferramentas e Integrações

* **Prometheus Exporter**: redis\_exporter para coletar métricas e expô-las para Prometheus.
* **Grafana**: dashboards prontos para Redis.
* **ELK Stack**: logs de performance e slow-queries.
* **RedisInsight**: GUI oficial para monitorar instâncias e acessar dados.

---

## 11. Casos de Uso Típicos

1. **Cache de Alto Desempenho**:

   * Armazenar resultados de consultas a banco de dados ou conteúdo estático.
   * Exemplos: página web, sessão de usuário.
2. **Session Store**:

   * Armazenamento de sessões de usuário com TTL curto.
3. **Colas e Filas (Task Queues)**:

   * Uso de Lists (LPUSH/BRPOP) ou Streams para filas de trabalho.
   * Bibliotecas: RQ (Python), Bull (Node.js), Sidekiq (Ruby).
4. **Leaderboard e Contagem**:

   * Sorted Sets para rankings em jogos e sites sociais.
5. **Pub/Sub para Notificações**:

   * Broadcasting em tempo real (chat, alertas).
6. **Geospatial**:

   * Consultas de proximidade em mapas e serviços baseados em localização.
7. **Contagem Aproximada**:

   * HyperLogLog para estimativa de usuários únicos.
8. **Rate Limiting**:

   * Contadores e tokens bucket para controlar requisições.
9. **Streams para Processamento de Eventos**:

   * Processamento de logs e pipelines de eventos em tempo real.

---

## 12. Tópicos Avançados

### 12.1 Transações e Lua Scripting

* **MULTI/EXEC**: transações atômicas, mas sem rollback automático.
* **WATCH**: para transações baseadas em otimistic locking.
* **Lua Scripting**: scripts executados atomicamente no servidor. Ideal para lógicas complexas que requerem várias operações atômicas.

  ```lua
  -- exemplo de script Lua para decremento condicional
  local stock = tonumber(redis.call('GET', KEYS[1]))
  if stock <= 0 then
    return -1
  end
  redis.call('DECR', KEYS[1])
  return stock - 1
  ```

  ```bash
  redis-cli EVAL "...script..." 1 product_stock
  ```

### 12.2 Redis em Contêineres e Kubernetes

* **Docker**:

  ```bash
  docker run -d --name redis -p 6379:6379 redis:latest
  ```
* **Docker Compose**:

  ```yaml
  version: '3'
  services:
    redis:
      image: redis:6.2
      ports:
        - "6379:6379"
  ```
* **Helm Chart (Kubernetes)**:

  ```bash
  helm repo add bitnami https://charts.bitnami.com/bitnami
  helm install my-redis bitnami/redis --set cluster.enabled=true
  ```

### 12.3 Backup e Recuperação

* **Dump RDB**: arquivo `dump.rdb`, pode ser copiado para recuperação.
* **AOF**: arquivo `appendonly.aof`, rewrite automático filtra comandos redundantes.
* **Estratégia**: combine snapshots RDB periódicos e AOF para garantir durabilidade e rápida recuperação.

---

## 13. Boas Práticas e Considerações

1. **Dimensionar Memória**: planejar memória suficiente para dataset + overhead (cabeçalhos, fragmentação).
2. **Eviction Adequado**: configure política de expulsão conforme caso de uso (cache vs dados críticos).
3. **Persistência vs Performance**: escolha entre RDB, AOF ou ambos; AOF com `everysec` costuma ser padrão em produção.
4. **Monitorar Uso de Memória**: evite swap, que degrada performance dramaticamente.
5. **Replicação e Failover**: configure Sentinels ou use Cluster para alta disponibilidade.
6. **Segurança em Produção**: habilite autenticação, TLS e ACL.
7. **Teste de Carga**: use ferramentas como `redis-benchmark` e `memtier_benchmark` para avaliar performance.
8. **Atualizações Sem Downtime**: use réplicas para promoção canary antes de migrações de versão.

---

## 14. Conclusão

O Redis oferece uma plataforma poderosa e versátil para múltiplos cenários: cache, filas, mensageria, contagem, ranking, processamento de eventos e muito mais. Dominar sua arquitetura, tipos de dados, persistência, replicação e tuning é essencial para aproveitar ao máximo seu desempenho e escalabilidade.
