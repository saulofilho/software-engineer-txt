# Guia Completo do Apache Kafka

Este guia apresenta de forma detalhada o Apache Kafka: arquitetura, componentes, conceitos-chave, casos de uso, exemplos práticos e boas práticas para implantação e operação.

---

## 1. O que é Apache Kafka?

Apache Kafka é uma plataforma de streaming distribuído e de alta taxa de transferência, projetada para publicar, assinar, armazenar e processar fluxos de registros em tempo real. Originalmente desenvolvido na LinkedIn e posteriormente doado à Apache Software Foundation, Kafka tornou-se amplamente adotado para casos de uso como coleta de logs, pipelines de dados, processamento de eventos e microserviços.

**Principais características**:

* **Alta taxa de transferência** (throughput): suporta milhões de eventos por segundo.
* **Baixa latência**: entrega mensagens em milissegundos.
* **Escalabilidade horizontal**: particiona dados entre múltiplos brokers.
* **Persistência**: mensagens são armazenadas em disco de forma sequencial (append-only).
* **Replicação**: alta disponibilidade e tolerância a falhas com réplicas de partições.
* **Modelo de publicação/assinatura** (Pub/Sub) com tópicos particionados.
* **Consumo desacoplado**: múltiplos grupos de consumidores podem ler independentemente.

---

## 2. Componentes da Arquitetura Kafka

### 2.1 Broker (Servidor)

* Um cluster Kafka é composto por múltiplos brokers que armazenam e replicam dados.
* Cada broker é identificado por um ID único.
* Brokers coordenam partições e gerenciam replicação.

### 2.2 Tópicos e Partições

* **Tópico**: categoria ou nome lógico para os fluxos de registros.
* **Partição**: cada tópico é dividido em várias partições; cada partição é uma sequência ordenada e imutável de registros, continuamente anexada.
* **Ordem Garantida**: dentro de uma partição, a ordem das mensagens é preservada.
* **Escalabilidade**: ao aumentar partições, é possível aumentar paralelismo e throughput.

![Diagrama de tópico particionado com três partições distribuídas em dois brokers](diagram_topic_partitions.png)

### 2.3 Replicação e Controle de Líderes

* **Replicação**: cada partição possui múltiplas réplicas, distribuídas em brokers diferentes para tolerância a falhas.
* **Líder de Partição**: apenas o líder de cada partição recebe e responde a operações de leitura/escrita para aquela partição.
* **Réplicas Follower**: seguem (replicam) o líder; se o líder falhar, um follower é promovido.
* **Configuração**: fator de replicação (replication.factor) e ISR (in-sync replicas).

### 2.4 Zookeeper (ou KRaft)

* Históricamente, Kafka usava Apache ZooKeeper para coordenar o cluster: manter metadados, líder de partições, configurações de tópicos.
* A partir do Kafka 2.8 (modo preview) e 3.x, está disponível o modo **KRaft** (Kafka Raft Metadata Mode), que elimina dependência de ZooKeeper, usando um Raft internal para metadados.

### 2.5 Producer (Produtor)

* Componente responsável por enviar (produzir) registros para tópicos Kafka.
* Define chaves, valores e particionamento (por chave ou round-robin).
* Possui configuração de **acks** para definir latência x durabilidade (0, 1, all).

### 2.6 Consumer (Consumidor)

* Lê (consome) registros de tópicos Kafka.
* Associado a **grupos de consumidores** (consumer groups).

  * Cada partição é consumida por apenas um membro do grupo para garantir paralelismo e ordem por partição.
* **Offset**: posição de leitura dentro de cada partição; gerenciado por Kafka (offset commits automáticos ou manuais).

### 2.7 Connectors e Ecosistema Kafka

* **Kafka Connect**: framework para integração com sistemas externos (bases de dados, sistemas de arquivos, sistemas de mensagens).
* **Kafka Streams**: biblioteca para processamento de stream embutido em aplicações Java/Scala, com abstrações de transformações, janelas e joins.
* **ksqlDB**: SQL on streams para consultas contínuas em tópicos Kafka.

---

## 3. Fundamentos de Funcionamento

### 3.1 Escrita Sequencial em Disco

* Partições são armazenadas como arquivos segmentados, com escrita **append-only**.
* Escrita sequencial reduz busca de disco (seeks) e melhora throughput.
* Dados são primeiramente gravados em **logs**:

  1. O produtor envia registro ao broker líder.
  2. Broker grava no log (arquivo segmentado) e retorna confirmação conforme configuração de **acks**.
  3. Followers replicam esses segmentos.

### 3.2 Lê Leitura via Page Cache

* Consumidores leem de logs sequenciais; Kafka confia no **page cache** do sistema operacional.
* Consumidor busca (fetch) lote de registros de uma partição a partir de um offset específico.

### 3.3 Partitioners e Distribuição de Chaves

* **Particionador por Chave**: padrão, hash da chave determina partição, garantindo que todos registros com mesma chave vão para mesma partição.
* **Particionador Round-Robin**: sem chave, para balancear uniformemente.
* Aplicação deve escolher estratégia correta para requisitos de ordenação e distribuição de carga.

### 3.4 Gerenciamento de Offsets

* Kafka mantém offsets por par (grupo de consumidor, partição).
* **Commit Automático**: consumer auto.commit.interval.ms define frequência de commits.
* **Commit Manual**: fábrica consumo síncrono, uso de commitSync() ou commitAsync() para maior controle.

---

## 4. Configurações Importantes

| Configuração                            | Descrição                                                         | Valor Típico / Observação                                                     |
| --------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `bootstrap.servers`                     | Lista de brokers para conectar (host\:port).                      | `"kafka1:9092,kafka2:9092"`                                                   |
| `acks`                                  | Nível de confirmação (0, 1, all).                                 | `all` para maior durabilidade; `0` para latência mínima.                      |
| `key.serializer`/`value.serializer`     | Serializadores de chaves/valores no produtor.                     | `StringSerializer`, `AvroSerializer`, `ByteArraySerializer`                   |
| `key.deserializer`/`value.deserializer` | Desserializadores no consumidor.                                  | `StringDeserializer`, `AvroDeserializer`                                      |
| `group.id`                              | ID do grupo de consumidores.                                      | Qualquer string; todos consumers com mesmo `group.id` formam grupo.           |
| `enable.auto.commit`                    | Se o consumidor deve auto-commitar offsets.                       | `false` para controle manual.                                                 |
| `auto.offset.reset`                     | Quando não há offset inicial: `earliest` ou `latest`.             | `earliest` para ler desde início; `latest` para apenas novos dados.           |
| `num.partitions`                        | Número de partições por tópico (definido ao criar tópico).        | Dépendendo do throughput esperado.                                            |
| `replication.factor`                    | Número de réplicas por partição.                                  | Pelo menos 2 para tolerância a falhas.                                        |
| `retention.ms`                          | Tempo de retenção de logs em milissegundos.                       | `604800000` (7 dias).                                                         |
| `segment.ms` / `segment.bytes`          | Tamanho de segmentos de log (time/bytes).                         | Ajuste com base em volume de dados e I/O.                                     |
| `min.insync.replicas`                   | Número mínimo de réplicas em sincronia para `acks=all` funcionar. | 2 em clusters de 3 réplicas (garante pelo menos 1 falha tolerável sem perda). |

---

## 5. Instalação Básica

### 5.1 Requisitos

* Java 8 ou superior.
* Sistema operacional Linux, macOS ou Windows.
* Memória suficiente (min 2 GB para ambiente de dev).

### 5.2 Baixar e Descompactar

```bash
wget https://downloads.apache.org/kafka/3.4.0/kafka_2.13-3.4.0.tgz
tar -xzf kafka_2.13-3.4.0.tgz
cd kafka_2.13-3.4.0
```

### 5.3 Iniciar ZooKeeper (modo legado) ou KRaft

* **Modo Legado (com ZooKeeper)**:

  ```bash
  bin/zookeeper-server-start.sh config/zookeeper.properties
  ```
* **Modo KRaft (Kafka Raft Metadata Mode, versão 2.8.0+ em prévia)**:

  1. Iniciar broker em modo CTA (controller):

     ```bash
     KAFKA_KRAFT_BROKER_ID=1 bin/kafka-storage.sh format -t <UUID> -c config/kraft/server.properties
     bin/kafka-server-start.sh config/kraft/server.properties
     ```
  2. (Opcional) Adicionar brokers adicionais.

### 5.4 Iniciar Kafka Broker

* **Modo Legado**:

  ```bash
  bin/kafka-server-start.sh config/server.properties
  ```
* **Modo KRaft**:

  ```bash
  bin/kafka-server-start.sh config/kraft/server.properties
  ```

---

## 6. Operações Básicas via CLI

### 6.1 Criar Tópico

```bash
bin/kafka-topics.sh --create \
  --topic meu-topico \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 2
```

### 6.2 Listar Tópicos

```bash
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

### 6.3 Publicar Mensagens (Console Producer)

```bash
bin/kafka-console-producer.sh \
  --topic meu-topico \
  --bootstrap-server localhost:9092
> Hello Kafka
> Teste streaming
```

### 6.4 Consumir Mensagens (Console Consumer)

```bash
bin/kafka-console-consumer.sh \
  --topic meu-topico \
  --bootstrap-server localhost:9092 \
  --from-beginning
```

### 6.5 Descrever Tópico

```bash
bin/kafka-topics.sh --describe \
  --topic meu-topico \
  --bootstrap-server localhost:9092
```

---

## 7. API de Producer em Java (Exemplo)

```java
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import java.util.Properties;

public class SimpleProducer {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.ACKS_CONFIG, "all");

        KafkaProducer<String, String> producer = new KafkaProducer<>(props);
        try {
            for (int i = 0; i < 10; i++) {
                String key = "key-" + i;
                String value = "mensagem " + i;
                ProducerRecord<String, String> record = new ProducerRecord<>("meu-topico", key, value);
                producer.send(record, (metadata, exception) -> {
                    if (exception == null) {
                        System.out.printf("Enviado para partição %d com offset %d%n", metadata.partition(), metadata.offset());
                    } else {
                        exception.printStackTrace();
                    }
                });
            }
        } finally {
            producer.close();
        }
    }
}
```

---

## 8. API de Consumer em Java (Exemplo)

```java
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.serialization.StringDeserializer;
import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class SimpleConsumer {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "grupo-exemplo");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Collections.singletonList("meu-topico"));

        try {
            while (true) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                for (ConsumerRecord<String, String> record : records) {
                    System.out.printf("Recebido: partição=%d, offset=%d, key=%s, value=%s%n",
                            record.partition(), record.offset(), record.key(), record.value());
                }
                consumer.commitSync();
            }
        } finally {
            consumer.close();
        }
    }
}
```

---

## 9. Casos de Uso Comuns

1. **Coleta de Logs e Métricas**: ingestão de grandes volumes de dados de logs, métricas e eventos.
2. **Pipelines de Dados**: transferência de dados entre sistemas de armazenamento e processamento (ETL em tempo real).
3. **Processamento de Streaming**: aplicações de tempo real com **Kafka Streams** ou **ksqlDB**.
4. **Microserviços**: troca de eventos entre microserviços desacoplados.
5. **Replicação de Banco de Dados**: usar Kafka Connect para CDC (Change Data Capture).

---

## 10. Monitoramento e Observabilidade

* **Métricas Internas**: JMX expos Kafka metrics (Bytes in/out, Request rate, ISR status, Consumer lag).
* **Ferramentas**:

  * **Prometheus + Grafana**: usar `kafka_exporter` para coletar métricas e criar dashboards.
  * **Confluent Control Center**: versão comercial para monitorar clusters.
  * **Burrow**: monitor de lag de consumidores.
* **Logs**: broker, producer e consumer logs configuráveis em `log4j.properties`.
* **Alertas**: definir alertas para eventos como: ISR abaixo do fator de replicação, aumento de latência, falhas de broker.

---

## 11. Alta Disponibilidade e Tolerância a Falhas

1. **Replicação de Partições**: defina `replication.factor ≥ 2` e `min.insync.replicas` para manter durabilidade em face de falhas de broker.
2. **Controle de Líder**: use `unclean.leader.election.enable=false` para evitar perda de dados ao eleger líderes não sincronizados.
3. **Balanceamento de Partições**: use `kafka-reassign-partitions.sh` ou o recurso de auto-reambiente para redistribuir partições em novos brokers.
4. **Backup de Logs**: armazene logs em discos redundantes, use snapshots de volumes ou backup de S3 para retenção de longo prazo.
5. **Multi-Data Center**: configure replicação entre clusters (MirrorMaker 2) para disaster recovery.

---

## 12. Segurança

1. **Autenticação**:

   * **SASL\_SSL** (Kerberos / SCRAM / PLAIN): autenticação mútua entre clientes e brokers.
   * **SSL/TLS**: criptografa tráfego entre clientes e brokers.
2. **Autorização (ACLs)**:

   * Defina ACLs para permitir ou negar operações de leitura/escrita em tópicos, grupos de consumidores e clusters.
   * `kafka-acls.sh --add --allow-principal User:app1 --operation Read --topic meu-topico`
3. **Criptografia de Logs**:

   * Uso de LUKS, dm-crypt ou EBS com criptografia para armazenar logs em disco.
4. **Network Security**:

   * Isolar brokers em VPC privada, usar regras de firewall para restringir portas (9092, 9093).
   * Habilitar autenticação mútua SSL para prevenção de tráfego malicioso.

---

## 13. Otimizações de Performance

1. **Batching de Mensagens**:

   * Ajuste `linger.ms` e `batch.size` no producer para agrupar mais mensagens por requisição.
2. **Compressão**:

   * Use `compression.type` (gzip, snappy, lz4, zstd) para reduzir uso de rede e armazenamento.
3. **Tuning de Segmentos de Log**:

   * Ajuste `segment.bytes` e `segment.ms` para controlar tamanho e tempo de rotação de segmentos.
4. **Ajuste de `replica.fetch.max.bytes` e `fetch.max.bytes`**:

   * Ajuste para melhorar throughput de replicação e consumo.
5. **Desfragmentação de Arquivos**:

   * Use `log.retention.check.interval.ms` para remover automaticamente segmentos antigos, evitando sobrecarga de disco.

---

## 14. Versionamento de Schemas (Avro/Schema Registry)

* **Problema**: Consumidores e produtores podem usar diferentes versões de esquema JSON.
* **Solução**: Use **Avro** com **Confluent Schema Registry** para gerenciar versões de esquema.

  1. Produtor registra esquema no Schema Registry.
  2. Mensagens são serializadas em Avro (key + payload).
  3. Consumidor busca esquema compatível para desserializar.
* **Compatibilidade**:

  * **BACKWARD**: novas versões podem ler dados antigos.
  * **FORWARD**: dados novos podem ser lidos por consumidores antigos.
  * **FULL**: combina ambas.

---

## 15. Padrões de Uso Avançados

### 15.1 Streams Windows e Joins

* Use Kafka Streams ou ksqlDB para janelas de tempo:

  ```java
  KStream<String, Long> clicks = builder.stream("click-events");
  TimeWindows windows = TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5));
  KTable<Windowed<String>, Long> aggregated = clicks
      .groupByKey()
      .windowedBy(windows)
      .count(Materialized.as("click-counts"));
  ```

### 15.2 Chang Data Capture (CDC) com Kafka Connect

* Use **Debezium** para extrair alterações de bancos (MySQL, PostgreSQL) e publicar em tópicos Kafka.
* Consumidores downstream podem aplicar mudanças em data warehouses ou caches.

### 15.3 Kafka Streams Topologias Multi-Stage

* Você pode criar pipelines complexos dividindo lógica em múltiplos tópicos intermediários:

  1. Tópico de ingestão bruta.
  2. Tópico de eventos filtrados/categorizados.
  3. Tópico de agregações em janelas.

### 15.4 MirrorMaker e Replicação Global

* **MirrorMaker 2** para replicar tópicos entre clusters em diferentes regiões (multi-datacenter).
* Útil para geodistribuição e recuperação de desastres.

---

## 16. Troubleshooting Comum

1. **Consumer Lag Alto**:

   * Verifique uso de CPU/memória nos consumers, ajuste tamanho de partições, verifique throughput do broker.
2. **Under-Replicated Partitions**:

   * Cheque ISR, identifique brokers lentos ou offline.
3. **Garbage Collection (GC) Alta Latência**:

   * Ajuste heap size de Java, use G1GC ou ZGC para menor pausa.
4. **Conflito de Configurações de ACL**:

   * Revise ACLs com `kafka-acls.sh --list`.
5. **Problemas de Network / DNS**:

   * Brokers devem estar acessíveis por nome ou IP configurado em `advertised.listeners`.
6. **Erros de Serialização**:

   * Confira compatibilidade de schemata e checagem de Avro deserializador.

---

## 17. Boas Práticas Gerais

1. **Monitorar**: implemente coleta de métricas, crie dashboards e alertas para lag, uso de disco, throughput.
2. **Planejar capacidade**: dimensionar número de brokers, partições e replicação conforme crescimento projetado.
3. **Testar falhas**: simule falhas de brokers (testes de caos) para validar tolerância.
4. **Manter Upgrade Regular**: siga versões LTS, teste upgrades em ambiente de staging.
5. **Documentar**: arquitetura de tópicos, retenção, políticas de replicação, processos de failover.

---

## 18. Conclusão

Apache Kafka é a espinha dorsal de muitos sistemas de dados modernos, fornecendo pipelines de eventos em tempo real, alta escalabilidade e resiliência. Compreender sua arquitetura, configurações críticas e práticas avançadas é essencial para construir aplicações distribuídas de alto desempenho e confiáveis.
