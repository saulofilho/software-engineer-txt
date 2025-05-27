# Guia Completo de Filas e Mensageria: Kafka, RabbitMQ e Sidekiq

Este guia aborda arquiteturas de filas e mensageria, detalhando conceitos, funcionamento e exemplos práticos de três tecnologias populares: Apache Kafka, RabbitMQ e Sidekiq.

---

## 1. Introdução a Filas e Mensageria

Filas e sistemas de mensageria permitem desacoplar produtores de mensagens de consumidores, suportando processamento assíncrono, balanceamento de carga e alta disponibilidade.

* **Filas (Queues)**: armazenam mensagens em ordem FIFO (first-in, first-out).
* **Tópicos / Streams**: múltiplos consumidores podem ler a mesma mensagem.
* **Broker**: componente central que gerencia troca de mensagens.

**Vantagens**:

* Escalabilidade horizontal.
* Resiliência a falhas (retries, dead-letter queues).
* Controle de fluxo (backpressure).

---

## 2. Padrões de Mensageria

1. **Point-to-Point (fila única)**: cada mensagem é consumida por apenas um consumidor.
2. **Publish/Subscribe**: produtor publica em um tópico/exchange; múltiplos assinantes recebem cópias.
3. **Competing Consumers**: várias instâncias competem por mensagens na mesma fila para carga balanceada.
4. **Dead Letter Queue (DLQ)**: mensagens com falha são roteadas para filas de erro.

---

## 3. Apache Kafka

### 3.1 Arquitetura

* **Cluster**: múltiplos brokers.
* **Topic**: categoria de mensagens, particionada para paralelismo.
* **Partition**: sub-fila; mantém ordem dentro da partição.
* **Producer/Consumer**: enviam e recebem mensagens.

### 3.2 Garantias de Entrega

* **At most once**: possivelmente perde mensagens.
* **At least once**: pode duplicar; o consumidor deve ser idempotente.
* **Exactly once** (com Kafka Streams ou idempotência do producer).

### 3.3 Exemplo Java (Producer/Consumer)

```java
// Producer
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("enable.idempotence", "true");
Producer<String, String> producer = new KafkaProducer<>(props);
producer.send(new ProducerRecord<>("meu-topico", "chave", "mensagem"));
producer.close();

// Consumer
Properties cprops = new Properties();
cprops.put("bootstrap.servers", "localhost:9092");
cprops.put("group.id", "grupo1");
cprops.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
cprops.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
KafkaConsumer<String, String> consumer = new KafkaConsumer<>(cprops);
consumer.subscribe(List.of("meu-topico"));
while (true) {
  ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
  for (ConsumerRecord<String, String> record : records) {
    System.out.printf("offset=%d, key=%s, value=%s%n",
      record.offset(), record.key(), record.value());
  }
}
```

### 3.4 Configurações Importantes

* `replication.factor`: replicação para tolerância a falhas.
* `acks`: controle de confirmação.
* `retention.ms`: tempo de retenção de mensagens.

---

## 4. RabbitMQ

### 4.1 Arquitetura

* **Broker**: servidor RabbitMQ.
* **Exchange**: recebe mensagens de produtores e as roteia para filas.
* **Queue**: armazena mensagens.
* **Binding**: ligação Exchange→Queue com routing keys.

### 4.2 Tipos de Exchange

* **Direct**: roteia por chave exata.
* **Fanout**: broadcast a todas as filas ligadas.
* **Topic**: roteia por padrões (`*`, `#`).
* **Headers**: roteia por cabeçalhos em vez de routing key.

### 4.3 Exemplo Python (pika)

```python
import pika

# Producer
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')
channel.basic_publish(exchange='logs', routing_key='', body='Olá Mundo!')
connection.close()

# Consumer
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='logs', queue=queue_name)

def callback(ch, method, properties, body):
    print(f"Recebido {body}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print('Aguardando mensagens...')
channel.start_consuming()
```

### 4.4 Recursos Avançados

* **Dead-Letter Exchanges**: reentrega em filas de erro.
* **TTL**: expiração de mensagens e filas.
* **Confirmações de Publisher** e **Confirms**: garante persistência.

---

## 5. Sidekiq

Sidekiq é um framework Ruby para processamento de jobs em background, usando Redis como broker.

### 5.1 Conceitos

* **Worker**: classe Ruby que define o job.
* **Queue**: nome dado ao conjunto de jobs.
* **Client**: enfileira jobs.
* **Processo Sidekiq**: consome e executa jobs.

### 5.2 Exemplo Ruby

```ruby
# Gemfile
gem 'sidekiq'

# worker.rb
class EmailWorker
  include Sidekiq::Worker
  sidekiq_options queue: 'emails', retry: 5

  def perform(user_id, subject)
    user = User.find(user_id)
    UserMailer.with(user: user, subject: subject).welcome_email.deliver_now
  end
end

# Enfileirar job
EmailWorker.perform_async(42, 'Bem-vindo!')
```

### 5.3 Configuração Básica

```yaml
# config/sidekiq.yml
:queues:
  - [emails, 3]
  - [default, 1]

# Procfile (Heroku)
worker: bundle exec sidekiq -C config/sidekiq.yml
```

### 5.4 Monitoramento e UI

* **Web UI**: fornecido por `sidekiq/web`.
* **Retries**: estratégia exponencial, restrições de falha.

---

## 6. Comparação e Cenários de Uso

| Característica      | Kafka                        | RabbitMQ                     | Sidekiq                     |
| ------------------- | ---------------------------- | ---------------------------- | --------------------------- |
| Modelo              | Log distribuído (Streams)    | Broker clássico (Exchange)   | Job queue em Redis          |
| Persistência        | Disco                        | Disco / memória configurável | Redis                       |
| Performance         | Altíssima taxa de throughput | Baixa latência, menor escala | Dimensionado pela instância |
| Garantia de Entrega | At least once / Exactly once | At most once / At least once | At least once               |
| Caso de Uso Típico  | Logs, telemetria, eventos    | Filas de tarefas, RPC        | Processamento de background |

---

## 7. Considerações Avançadas

* **Idempotência**: fundamental para consumidores `at-least-once`.
* **Backpressure**: controle de fluxo em picos de carga.
* **Segurança**: TLS, autenticação (SASL para Kafka, TLS para RabbitMQ, Redis AUTH).
* **Monitoramento**: Prometheus + Grafana, métricas próprias.

---

## 8. Boas Práticas

1. **Isolar tópicos/filas por domínio de negócio**.
2. **Definir DLQs** para mensagens com falha.
3. **Implementar retries exponenciais**.
4. **Monitorar lag (Kafka)** e filas compridas.
5. **Dimensionar consumers/workers** conforme demanda.

---

## 9. Conclusão

Filas e sistemas de mensageria são cruciais para arquiteturas escaláveis e resilientes. Escolha a tecnologia adequada ao seu cenário: Kafka para alto throughput e retenção longa, RabbitMQ para flexibilidade de roteamento e Sidekiq para jobs em background em aplicações Ruby.
