# Guia Completo de Padrão Pub/Sub (Publish–Subscribe)

Este guia explica o padrão de mensageria **Publish–Subscribe (Pub/Sub)**, cobrindo conceitos, arquiteturas, mecanismos de entrega, modelos de uso, exemplos práticos e considerações para escalabilidade e performance.

---

## 1. O que é Pub/Sub?

**Publish–Subscribe** é um padrão de comunicação assíncrona onde produtores (publishers) enviam mensagens a um canal sem conhecimento direto dos consumidores (subscribers). Consumidores se inscrevem em tópicos ou canais de interesse e recebem mensagens publicadas.

**Características principais**:

* **Desacoplamento**: Publishers não conhecem subscribers e vice-versa.
* **Escalabilidade**: múltiplos publishers e subscribers podem operar independentemente.
* **Entrega baseada em tópicos**: mensagens rotuladas por tópicos ou canais.

---

## 2. Componentes Fundamentais

1. **Publisher** (Produtor): publica mensagens em um tópico específico.
2. **Broker** (Servidor de Mensageria): recebe mensagens de publishers e as roteia para subscribers registrados.
3. **Subscriber** (Consumidor): cria assinaturas para tópicos e processa mensagens.
4. **Tópico/Canal**: identificador lógico para categorizar mensagens.
5. **Mensagem**: estrutura de dados enviada (pode conter cabeçalho, payload e metadados).

---

## 3. Modelos de Entrega

### 3.1 Push vs Pull

* **Push-based**: Broker envia (push) mensagens ativamente aos subscribers assim que chegam.
* **Pull-based**: Subscriber solicita (pull) mensagens do Broker em intervalos regulares ou quando pronto.

**Vantagens Push**:

* Latência baixa (entrega imediata).
* Simplicidade para o subscriber.

**Vantagens Pull**:

* Controle de ritmo (backpressure) para evitar sobrecarga.
* Recuperação mais flexível de mensagens (ex.: processamento em lote).

### 3.2 QoS e Garantias de Entrega

| QoS               | Descrição                                                                       |
| ----------------- | ------------------------------------------------------------------------------- |
| **At Most Once**  | Mensagem pode ser perdida; nunca duplicada.                                     |
| **At Least Once** | Mensagem pode ser entregue múltiplas vezes; garante entrega pelo menos uma vez. |
| **Exactly Once**  | Mensagem entregue exatamente uma vez; maior complexidade.                       |

Implementar Exactly Once requer mecanismos de idempotência no subscriber ou transações.

---

## 4. Padrões de Roteamento e Filtragem

### 4.1 Filtragem por Tópicos

* Mensagens publicadas incluem chave de tópico.
* Subscribers registram interesse em tópicos específicos ou padrões (wildcards).

### 4.2 Filtragem por Conteúdo

* Broker analisa conteúdo da mensagem e aplica regras de roteamento (ex.: CEP no Apache Pulsar).
* Útil para cenários dinâmicos onde tópicos fixos não são suficientes.

### 4.3 Fanout / Broadcast

* Publisher envia mensagem a um tópico único.
* Broker entrega cópias a todos os subscribers inscritos (fanout).

### 4.4 Partitionamento de Tópicos

* Tópicos particionados em múltiplas sub-áreas para paralelismo.
* Cada partição pode ter um líder e replique para alta disponibilidade.

---

## 5. Arquiteturas Comuns e Ferramentas Populares

| Ferramenta           | Modelo     | Linguagem/Plataforma | QoS Suportado                                           |
| -------------------- | ---------- | -------------------- | ------------------------------------------------------- |
| **Apache Kafka**     | Pull-based | JVM                  | At Least Once (idempotência opcional para Exactly Once) |
| **RabbitMQ**         | Push/Pull  | Erlang               | At Most Once, At Least Once (confirms)                  |
| **Redis Pub/Sub**    | Push-based | C                    | Best Effort (sem persistência)                          |
| **Google Pub/Sub**   | Hybrid     | Google Cloud         | At Least Once, Exactly Once (opcional)                  |
| **Amazon SNS/SQS**   | Push/Pull  | AWS                  | At Least Once                                           |
| **NATS**             | Push/Pull  | Go                   | At Most Once, At Least Once                             |
| **Apache Pulsar**    | Hybrid     | JVM                  | At Least Once, Exactly Once                             |
| **MQTT (Mosquitto)** | Push-based | C                    | QoS 0/1/2                                               |

---

## 6. Exemplo Prático com Apache Kafka

### 6.1 Setup Básico

```properties
# servidor Kafka
bootstrap.servers=localhost:9092
```

### 6.2 Producer em Java

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
KafkaProducer<String, String> producer = new KafkaProducer<>(props);
for (int i = 0; i < 10; i++) {
  ProducerRecord<String, String> record = new ProducerRecord<>("meu-topico", Integer.toString(i), "mensagem " + i);
  producer.send(record);
}
producer.close();
```

### 6.3 Consumer em Java

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "grupo1");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Collections.singletonList("meu-topico"));
while (true) {
  ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
  for (ConsumerRecord<String, String> record : records) {
    System.out.printf("offset=%d, key=%s, value=%s%n", record.offset(), record.key(), record.value());
  }
}
```

---

## 7. Exemplo com Redis Pub/Sub (Node.js)

### 7.1 Publisher

```js
const redis = require('redis');
const publisher = redis.createClient();
publisher.publish('canal1', 'Olá subscribers!');
```

### 7.2 Subscriber

```js
const redis = require('redis');
const subscriber = redis.createClient();
subscriber.subscribe('canal1');
subscriber.on('message', (channel, message) => {
  console.log(`Recebido no ${channel}: ${message}`);
});
```

**Observação**: Redis Pub/Sub não armazena mensagens; se subscriber estiver offline, mensagem é perdida.

---

## 8. Casos de Uso Típicos

* **Notificações em Tempo Real**: chat, alertas, dashboards.
* **Streaming de Dados**: logs, métricas, telemetria.
* **Atualizações de Cache**: invalidar múltiplos nós após escrita.
* **Integração de Microserviços**: desacoplamento via eventos.
* **IoT**: sensores publicam dados e múltiplos sistemas processam.

---

## 9. Padronização em Nuvem

### 9.1 Google Cloud Pub/Sub

* **Push/Pull**: subscribers podem escolher.
* Entrega “at-least-once” por padrão; deduplicação pode ser aplicada.
* **Dead-letter Topics**: mensagens não processadas podem ser redirecionadas.

### 9.2 AWS SNS/SQS

* **SNS** (Simple Notification Service): Pub/Sub puro, push para endpoints HTTP, SQS, emails.
* **SQS** (Simple Queue Service): filas pull-based.
* Podem ser combinados para criar modelo Pub/Sub com durabilidade.

---

## 10. Consistência, Retenção e Ordenação

* **Ordenação**: alguns sistemas (Kafka) garantem ordenação dentro de partições; outros não.
* **Retenção**: duração que mensagens permanecem no broker (Kafka, Pulsar).
* **Persistência**: filas duráveis versus memória volátil.

---

## 11. Escalabilidade e Alta Disponibilidade

* **Clustering**: múltiplos brokers que replicam partições/tópicos.
* **Partições**: permitem paralelismo; cada partição servida por múltiplos consumers em um grupo.
* **Replicação**: número de réplicas configura redundância e tolerância a falhas.
* **Rebalanceamento**: ao adicionar ou remover consumidores, cargas de partição são redistribuídas.

---

## 12. Monitoramento e Observabilidade

* **Métricas**: latência de entrega, taxa de produção/consumo, tamanho de filas, lag de consumidor.
* **Ferramentas**: Prometheus + Grafana (Kafka Exporter), RabbitMQ Management, Cloud Provider dashboards.
* **Logging**: rastreamento de IDs de correlação para eventos.

---

## 13. Considerações de Segurança

* **Autenticação**: TLS + certificados (Kafka SASL\_SSL, RabbitMQ TLS).
* **Autorização**: controle de acesso por tópico (ACLs).
* **Criptografia em repouso**: criptografar discos dos brokers.
* **Isolamento de Rede**: VPC, sub-redes privadas.

---

## 14. Boas Práticas

1. **Escolha QoS Adequado**: use at least once ou exactly once conforme necessidade de dados críticos.
2. **Defina Retenção Adequada**: balanceie entre consumo tardio e uso de disco.
3. **Projetar para Idempotência**: subscribers devem tratar duplicações.
4. **Monitorar Lag de Consumidor**: detectar atrasos de processamento.
5. **Dimensionar Partições**: equilibre paralelismo e overhead de gerenciamento.

---

## 15. Conclusão

O padrão Pub/Sub é essencial para arquiteturas baseadas em eventos e sistemas escaláveis. Compreender modelos de entrega, QoS, arquiteturas de broker e práticas de segurança e monitoramento garante implementações robustas e eficientes.
