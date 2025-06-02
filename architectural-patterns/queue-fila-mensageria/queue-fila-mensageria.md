# Guia Completo de Sistemas de Mensageria

Este guia aborda de forma abrangente os conceitos, padrões, ferramentas e práticas para implementar sistemas de mensageria em arquiteturas distribuídas.

---

## 1. Introdução à Mensageria

**Mensageria** refere-se ao uso de componentes intermediários (*message brokers*) para troca assíncrona de mensagens entre sistemas ou componentes, oferecendo desacoplamento, resiliência e escalabilidade.

**Vantagens**:

1. **Desacoplamento**: produtores e consumidores não precisam estar ativos simultaneamente.
2. **Escalabilidade**: permite balanceamento de carga e paralelismo.
3. **Resiliência**: filas persistentes absorvem picos e toleram falhas temporárias.
4. **Flexibilidade**: múltiplos consumidores podem processar a mesma mensagem em padrões Pub/Sub.

**Padrões Comuns**:

* **Point-to-Point (Fila)**: cada mensagem consumida por apenas um consumidor.
* **Publish–Subscribe (Pub/Sub)**: mensagens entregues a todos assinantes de um tópico.
* **Streaming**: fluxo contínuo de eventos, com retenção e replay (Kafka, Pulsar).

---

## 2. Componentes Principais

| Componente       | Função                                                                                  |
| ---------------- | --------------------------------------------------------------------------------------- |
| **Producer**     | Publica mensagens em filas ou tópicos.                                                  |
| **Consumer**     | Recebe/processa mensagens de filas ou tópicos.                                          |
| **Broker**       | Gere filas/tópicos, roteia mensagens e garante entrega conforme configuração de QoS.    |
| **Exchange**     | (RabbitMQ) Recebe mensagens de produtor e roteia para filas via bindings e roteamento.  |
| **Queue**        | Armazena mensagens até que sejam consumidas.                                            |
| **Topic**        | Canal lógico categorizador de mensagens (Kafka, Pub/Sub).                               |
| **Subscription** | Registro de interesse em um tópico; conserva metadados de offset ou posição de consumo. |

---

## 3. Modelos de Entrega e Garantias de Qualidade de Serviço (QoS)

### 3.1 Modelos de Entrega

* **Point-to-Point (Fila)**:

  * Producer envia mensagem para uma fila.
  * Apenas um Consumer retira cada mensagem.
* **Publish–Subscribe (Tópico)**:

  * Producer publica em um tópico/exchange.
  * Mensagem entregue a todos Consumers inscritos nesse tópico.
* **Stream**:

  * Dados gravados em log contínuo (particionado).
  * Consumers leem a partir de offsets, podendo reprocessar (replay).

### 3.2 Garantias de Entrega (QoS)

| Nível             | Descrição                                                                                        |
| ----------------- | ------------------------------------------------------------------------------------------------ |
| **At Most Once**  | Mensagem pode ser perdida; não é duplicada.                                                      |
| **At Least Once** | Garante entrega ao menos uma vez; pode haver duplicação.                                         |
| **Exactly Once**  | Mensagem entregue exatamente uma vez, sem duplicação ou perda; requer idempotência e transações. |

**Considerações**: Implementar Exactly Once é mais caro; muitas vezes usa-se At Least Once com lógica idempotente no Consumer.

---

## 4. Padrões de Roteamento e Filtragem

### 4.1 Filtragem por Tópicos

* Baseia-se em chaves de tópicos ou padrões (wildcards).
* Ferramentas: Kafka Topics (partições), RabbitMQ Topic Exchange.

### 4.2 Filtragem por Conteúdo

* Broker examina conteúdo (ex.: campos JSON) e direciona mensagens conforme regras (Content-based Routing).
* Útil quando não há tópicos fixos ou para cenários dinâmicos.

### 4.3 Roteamento Direto e Fanout

* **Direct Exchange (RabbitMQ)**: roteia com base em routing key exata.
* **Fanout Exchange (RabbitMQ)**: replica mensagem para todas filas ligadas sem considerar chave.
* **Cloud Pub/Sub**: tópicos implícitos; todos subscribers recebem mensagens.

---

## 5. Principais Ferramentas de Mensageria

| Ferramenta               | Modelo                    | Linguagem/Stack | QoS              | Use Case Típico                                 |
| ------------------------ | ------------------------- | --------------- | ---------------- | ----------------------------------------------- |
| **RabbitMQ**             | AMQP (Push/Pull)          | Erlang          | Ao menos uma vez | Filas tradicionais, RPC, Pub/Sub                |
| **Apache Kafka**         | Log Partitioned (Pull)    | Java/Scala      | At-Least/Exactly | Streaming, eventos, logs                        |
| **Redis Pub/Sub**        | In-Memory (Push)          | C               | Best Effort      | Notificações em tempo real (cache invalidation) |
| **AWS SQS/SNS**          | Fila + Tópico (Pull/Push) | AWS Cloud       | At-Least Once    | Microserviços, desacoplamento                   |
| **Google Cloud Pub/Sub** | Hybrid (Pull/Push)        | Google Cloud    | At-Least/Exactly | Streaming global, IoT                           |
| **Azure Service Bus**    | Fila/Topic (Pull)         | Azure Cloud     | Ao menos uma vez | Mensageria empresarial                          |
| **Apache Pulsar**        | Stream + Topic (Hybrid)   | Java            | At-Least/Exactly | Eventos, IoT, geo-distribuído                   |
| **NATS**                 | Pub/Sub (Push)            | Go              | At Most/At Least | Microserviços leves                             |
| **ActiveMQ**             | JMS (Pull)                | Java            | Ao menos uma vez | Integração corporativa (JMS)                    |

---

## 6. Exemplos Práticos

### 6.1 RabbitMQ – Fila Pontual (Point-to-Point)

#### Producer (Python com pika)

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

message = 'Hello World!'
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(delivery_mode=2) # torna a mensagem persistente
)
print(f"[x] Sent {message}")
connection.close()
```

#### Consumer (Python com pika)

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    print(f"[x] Received {body}")
    # simular trabalho
    time.sleep(body.count(b'.'))
    print("[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='task_queue', on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
```

**Observações**:

* `durable=True` e `delivery_mode=2` garantem persistência.
* `basic_qos(prefetch_count=1)` impede que RabbitMQ envie múltiplas mensagens não confirmadas ao mesmo Consumer.

---

### 6.2 Apache Kafka – Streaming Distribuído

#### Producer em Java

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("acks", "all");

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
for (int i = 0; i < 5; i++) {
    ProducerRecord<String, String> record = new ProducerRecord<>("meu-topico", Integer.toString(i), "mensagem " + i);
    producer.send(record, (metadata, exception) -> {
        if (exception == null) {
            System.out.printf("Sent to partition %d with offset %d%n", metadata.partition(), metadata.offset());
        } else {
            exception.printStackTrace();
        }
    });
}
producer.close();
```

#### Consumer em Java

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "grupo1");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("enable.auto.commit", "false");

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(List.of("meu-topico"));

try {
    while (true) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            System.out.printf("offset = %d, key = %s, value = %s%n", record.offset(), record.key(), record.value());
        }
        consumer.commitSync(); // commit manual após processar
    }
} finally {
    consumer.close();
}
```

**Observações**:

* `acks=all` assegura durabilidade de dados.
* `enable.auto.commit=false` e `commitSync()` ajustam QoS (At Least Once).

---

## 7. Boas Práticas

1. **Escolha Adequada de QoS**: use At Most Once se perda ocasional for aceitável; At Least Once para robustez; Exactly Once quando duplicação não for permitida.
2. **Idempotência no Consumer**: idempotent consumers lidam com duplicações sem efeitos colaterais.
3. **Configurar Tópicos/Filas Duráveis**: para persistência e recuperação de falhas.
4. **Partitionamento e Escalabilidade**: dimensione número de partições (Kafka) ou filas para paralelismo.
5. **Backpressure e Controle de Fluxo**: configure `prefetch_count` (RabbitMQ) ou ajuste consumidores (Kafka) para evitar sobrecarga.
6. **Monitoramento e Alertas**: monitore métricas como lag de consumidores, tamanho de filas, taxa de erros.
7. **Segurança**: implemente autenticação (SASL, TLS) e autorização (ACLs) para access control.
8. **Modelagem de Mensagens**: defina schema (Avro, Protobuf, JSON Schema) e versionamento para compatibilidade.

---

## 8. Considerações de Desempenho

* **Persistência vs In-Memory**: depende de durabilidade desejada (Redis é in-memory; Kafka e RabbitMQ têm opções persistentes).
* **Latency vs Throughput**: sistemas Pull (Kafka) podem ter maior latência que Push (RabbitMQ), mas maior throughput geral.
* **Batching**: agrupar mensagens para reduzir overhead de I/O (Producer/Consumer).
* **Compactação**: habilitar compressão de mensagens (Kafka: gzip, snappy) para reduzir banda.

---

## 9. Cenários de Uso

| Cenário                         | Ferramenta Indicada              | Padrão                  |
| ------------------------------- | -------------------------------- | ----------------------- |
| Fila de tarefas assíncronas     | RabbitMQ, SQS, Azure Service Bus | Point-to-Point          |
| Processamento de Logs e Eventos | Kafka, Pulsar                    | Stream                  |
| Notificações em tempo real      | Redis Pub/Sub, NATS              | Pub/Sub                 |
| Arquitetura Event-Driven        | Kafka, RabbitMQ, Pulsar          | Pub/Sub com Event Store |
| Comunicação IoT                 | MQTT (Mosquitto), Kafka          | Pub/Sub MQTT / Stream   |

---

## 10. Conclusão

Sistemas de mensageria são fundamentais para arquiteturas distribuídas modernas, habilitando comunicação assíncrona, escalabilidade e resiliência. A escolha da ferramenta adequada e a configuração correta de padrões de entrega e roteamento garantem sistemas robustos e eficientes.
