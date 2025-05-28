# AWS

---

Claro! Aqui vai uma visão abrangente e técnica sobre os principais tópicos da **AWS (Amazon Web Services)** que um **engenheiro de software sênior** precisa dominar, especialmente para arquitetura, desenvolvimento, escalabilidade e segurança em ambientes cloud:

---

### **1. Fundamentos da AWS**

- **Regiões e zonas de disponibilidade**: escolha de regiões para latência, conformidade e resiliência.
- **IAM (Identity and Access Management)**: políticas, roles, permissões, princípios de menor privilégio, IAM roles para serviços.
- **Billing e Pricing**: entender pricing models (On-demand, Reserved, Spot), AWS Cost Explorer, orçamento, alocação por tags.

---

### **2. Serviços de Computação**

- **EC2**: tipos de instância, Auto Scaling, AMIs, user-data scripts, EBS, placement groups.
- **ECS / Fargate / EKS**: orquestração de containers com Docker, task definitions, clusters, service discovery.
- **Lambda**: arquitetura serverless, cold start, limits (timeout, memória), concurrency, provisioned concurrency.
- **Elastic Beanstalk**: PaaS para deploy simplificado.

---

### **3. Armazenamento**

- **S3**: versionamento, políticas de bucket, replicação, classes de armazenamento (Standard, IA, Glacier), S3 events.
- **EBS**: tipos (gp2, gp3, io1), snapshots, performance tuning.
- **EFS**: NFS compartilhado, throughput e performance modes.
- **FSx**: para sistemas de arquivos como Windows FS ou Lustre.

---

### **4. Bancos de Dados**

- **RDS**: PostgreSQL, MySQL, Aurora; backup automático, Multi-AZ, read replicas, tuning de parâmetros.
- **DynamoDB**: NoSQL, throughput, partições, índices secundários, TTL, streams.
- **ElastiCache**: Redis e Memcached.
- **Athena**: consultas SQL em dados no S3 (serverless data lake).

---

### **5. Redes e Integrações**

- **VPC**: subnets públicas/privadas, route tables, NAT Gateway, security groups vs. NACLs.
- **Load Balancers**: ALB, NLB, target groups, health checks.
- **API Gateway**: REST ou HTTP APIs, throttling, authorization com IAM ou Cognito.
- **CloudFront**: CDN, cache policies, integração com S3 e Lambda@Edge.

---

### **6. DevOps e CI/CD**

- **CodePipeline, CodeBuild, CodeDeploy**: automação de deploys.
- **CloudFormation / CDK / Terraform**: infraestrutura como código (IaC).
- **CloudWatch**: logs, métricas customizadas, dashboards, alarms.
- **X-Ray**: tracing distribuído.
- **EventBridge / SNS / SQS**: arquitetura orientada a eventos.

---

### **7. Segurança e Compliance**

- **IAM policies e SCPs (Service Control Policies)**.
- **KMS**: criptografia de dados, chave gerenciada pelo cliente.
- **AWS WAF & Shield**: proteção contra ataques.
- **CloudTrail**: auditoria de chamadas de API.

---

### **8. Arquitetura e Melhores Práticas**

- **Well-Architected Framework**: pilares de segurança, confiabilidade, performance, eficiência operacional e custo.
- **Alta disponibilidade e tolerância a falhas**.
- **Escalabilidade horizontal vs. vertical**.
- **Design para falhas (Design for failure)**.

---

### **9. Observabilidade e Monitoramento**

- **Logs estruturados (JSON logs)** com CloudWatch.
- **Metrics e dashboards**.
- **Tracing distribuído com X-Ray ou OpenTelemetry**.

---

### **10. Casos de uso e arquiteturas serverless/event-driven**

- Microserviços com Lambda + API Gateway + DynamoDB.
- Processamento assíncrono com SQS + Lambda.
- Data Lake com S3 + Glue + Athena.

---

Se quiser, posso montar um **roadmap com links oficiais**, ou até mesmo simular **cenários práticos de arquitetura AWS** (ex: migrar um monolito para serverless). Quer que eu siga nessa linha?


Perfeito! Vamos então montar um **roadmap estruturado**, com foco em um **engenheiro de software sênior**, cobrindo teoria, prática e boas práticas em **arquitetura na AWS**. Dividido por **níveis de domínio** (do essencial ao avançado), com **links oficiais da AWS** para estudo prático e referência.

---

## **Roadmap AWS para Engenheiro de Software Sênior**

---

### **Fase 1 – Fundamentos (Essencial)**

### 1.1. Conceitos de Cloud e AWS

- [AWS Global Infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/)
- [Regiões vs Zonas de disponibilidade](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html)
- [Pricing e calculadora de custos](https://calculator.aws.amazon.com/)

### 1.2. IAM

- [IAM Concepts](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- IAM Policies, Roles, MFA, least privilege

### 1.3. VPC e Rede

- [Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- Subnets públicas/privadas, NAT Gateway, Route Tables, Security Groups

---

### **Fase 2 – Computação e Armazenamento**

### 2.1. EC2 e Auto Scaling

- [EC2 Overview](https://docs.aws.amazon.com/ec2/index.html)
- Auto Scaling Groups + Load Balancer

### 2.2. S3

- [Amazon S3](https://docs.aws.amazon.com/s3/index.html)
- Classes de armazenamento, policies de bucket, versionamento, eventos S3

### 2.3. Lambda e Serverless

- [AWS Lambda Docs](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- Concurrency, cold start, integração com SQS/SNS/API Gateway

---

### **Fase 3 – Banco de Dados**

### 3.1. RDS e Aurora

- [Amazon RDS](https://docs.aws.amazon.com/rds/index.html)
- Multi-AZ, backups, replicas, failover

### 3.2. DynamoDB

- [Amazon DynamoDB](https://docs.aws.amazon.com/dynamodb/index.html)
- Throughput, partições, índices secundários, padrões serverless

### 3.3. ElastiCache

- [ElastiCache Redis](https://docs.aws.amazon.com/elasticache/latest/red-ug/WhatIs.html)

---

### **Fase 4 – Arquitetura Serverless e Event-Driven**

### 4.1. API Gateway + Lambda + DynamoDB

- [API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
- [EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/what-is-amazon-eventbridge.html)

### 4.2. SQS + SNS

- [Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
- [SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)

### 4.3. Step Functions

- [Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- Orquestração de workflows serverless

---

### **Fase 5 – CI/CD e Infra como Código**

### 5.1. CodePipeline / CodeBuild / CodeDeploy

- [CI/CD com AWS](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html)

### 5.2. Infraestrutura como Código

- [AWS CloudFormation](https://docs.aws.amazon.com/cloudformation/index.html)
- [AWS CDK (TypeScript, Python, etc.)](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
- Alternativa: Terraform

---

### **Fase 6 – Observabilidade e Segurança**

### 6.1. Monitoramento

- [Amazon CloudWatch](https://docs.aws.amazon.com/cloudwatch/)
- Logs, alarms, dashboards, métricas customizadas

### 6.2. Tracing

- [AWS X-Ray](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html)

### 6.3. Segurança

- [AWS KMS (Key Management Service)](https://docs.aws.amazon.com/kms/)
- [AWS WAF](https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html)
- [CloudTrail](https://docs.aws.amazon.com/cloudtrail/)

---

### **Fase 7 – Padrões de Arquitetura e Boas Práticas**

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- Design para falha, escalabilidade horizontal, desacoplamento, eventual consistency
- Padrões: Saga, CQRS, Event Sourcing (com EventBridge e DynamoDB)

---

### **Exemplo de Arquitetura Serverless Moderna**

```
plaintext
CopiarEditar
Usuário -> API Gateway -> Lambda -> DynamoDB
                        |
                    -> EventBridge -> Lambda (background tasks)
                        |
                    -> S3 / SNS / SQS

```

---

Se quiser, posso desenhar essa arquitetura em diagrama ou montar uma simulação de projeto real com essa stack (infra como código + API + eventos + monitoramento). Quer seguir por esse caminho prático?

Show! Vamos então montar um **exemplo completo e prático de arquitetura serverless moderna na AWS**, com todos os componentes que um engenheiro sênior precisa saber aplicar.

---

## **Projeto Simulado: “Order Processing API” (API de pedidos)**

### **Cenário**

Você precisa criar um sistema para receber pedidos via API, salvar no banco, disparar eventos para processamento assíncrono (ex: envio de email, faturamento), e manter tudo monitorado, escalável e seguro.

---

## **Arquitetura**

### **Fluxo de dados:**

```
css
CopiarEditar
[Usuário]
   │
   ▼
[API Gateway] ──▶ [Lambda - OrderHandler] ──▶ [DynamoDB - Orders]
                                 │
                                 ├──▶ [EventBridge - OrderPlaced]
                                 │         ├──▶ Lambda - SendEmail
                                 │         └──▶ Lambda - GenerateInvoice
                                 │
                                 └──▶ [S3 - Logs / Backups]

```

---

## **Componentes com links e configs sugeridas:**

### 1. **API Gateway**

- Endpoint REST/HTTP com autenticação por API Key ou Cognito.
- [API Gateway Docs](https://docs.aws.amazon.com/apigateway/)

### 2. **Lambda (OrderHandler)**

- Linguagem: Node.js, Python ou Go.
- Função:
    - Valida o payload
    - Salva no DynamoDB
    - Dispara evento no EventBridge
- [Lambda Docs](https://docs.aws.amazon.com/lambda/)

### 3. **DynamoDB (Orders)**

- Tabela: `Orders`
    - PK: `orderId`
    - Attributes: `userId`, `items`, `status`, `createdAt`
- Throughput: on-demand ou provisionado com autoscaling.
- [DynamoDB Docs](https://docs.aws.amazon.com/dynamodb/)

### 4. **EventBridge**

- Cria um *bus customizado* chamado `OrderEventsBus`.
- Dispara eventos como:
    
    ```json
    json
    CopiarEditar
    {
      "source": "app.orders",
      "detail-type": "OrderPlaced",
      "detail": {
        "orderId": "123",
        "userId": "abc",
        "amount": 299
      }
    }
    
    ```
    
- [EventBridge Docs](https://docs.aws.amazon.com/eventbridge/)

### 5. **Lambdas (SendEmail, GenerateInvoice)**

- Triggadas por EventBridge.
- Executam tarefas assíncronas (mandar email, gerar fatura PDF).

### 6. **S3**

- Armazena logs, faturas geradas e arquivos auxiliares.
- Pode acionar eventos para processamento adicional (ex: OCR, backup).

### 7. **Observabilidade**

- **CloudWatch Logs** para todas as Lambdas.
- **Dashboards** com métricas de invocação, erro e latência.
- **X-Ray** habilitado para tracing completo.

### 8. **Infra como Código (CDK ou Terraform)**

- Provisiona todos os recursos com CI/CD.
- Exemplo com CDK (TypeScript ou Python):

```
ts
CopiarEditar
// CDK (TypeScript) - Simplificado
new lambda.Function(this, 'OrderHandler', {
  runtime: lambda.Runtime.NODEJS_20_X,
  code: lambda.Code.fromAsset('lambda/order'),
  handler: 'index.handler',
  environment: {
    TABLE_NAME: ordersTable.tableName,
    EVENT_BUS: eventBus.eventBusName,
  }
});

```

---

### **Bônus: Boas Práticas**

- **Retry + DLQ** configurado em todas as funções Lambda.
- **Segurança**:
    - IAM Roles mínimos.
    - KMS para criptografia de dados sensíveis.
    - Logging de eventos de API Gateway via CloudTrail.
- **Cost Optimization** com provisioned concurrency onde necessário.

---

### Quer ver isso em:

- Diagrama visual?
- Código (ex: CDK, Terraform ou YAML)?
- Simulação com chamadas de API (payloads)?

Me diz como prefere que eu continue e te mostro.

Imagem criada

[](https://sdmntpreastus2.oaiusercontent.com/files/00000000-2474-51f6-9fb8-2e5757dccbac/raw?se=2025-04-04T21%3A12%3A15Z&sp=r&sv=2024-08-04&sr=b&scid=41aec5f7-a9a8-50cf-93c3-469069aa1378&skoid=a47cd303-16a2-427e-8efb-2ce406116005&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-04-04T09%3A06%3A48Z&ske=2025-04-05T09%3A06%3A48Z&sks=b&skv=2024-08-04&sig=360hEGWx3Hucs4jISJk%2B0S9wkik/lma6%2BHBG4902L8c%3D)

[](https://sdmntpreastus2.oaiusercontent.com/files/00000000-2474-51f6-9fb8-2e5757dccbac/raw?se=2025-04-04T21%3A12%3A15Z&sp=r&sv=2024-08-04&sr=b&scid=41aec5f7-a9a8-50cf-93c3-469069aa1378&skoid=a47cd303-16a2-427e-8efb-2ce406116005&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-04-04T09%3A06%3A48Z&ske=2025-04-05T09%3A06%3A48Z&sks=b&skv=2024-08-04&sig=360hEGWx3Hucs4jISJk%2B0S9wkik/lma6%2BHBG4902L8c%3D)

[](https://sdmntpreastus2.oaiusercontent.com/files/00000000-2474-51f6-9fb8-2e5757dccbac/raw?se=2025-04-04T21%3A12%3A15Z&sp=r&sv=2024-08-04&sr=b&scid=41aec5f7-a9a8-50cf-93c3-469069aa1378&skoid=a47cd303-16a2-427e-8efb-2ce406116005&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-04-04T09%3A06%3A48Z&ske=2025-04-05T09%3A06%3A48Z&sks=b&skv=2024-08-04&sig=360hEGWx3Hucs4jISJk%2B0S9wkik/lma6%2BHBG4902L8c%3D)

Avalie esta imagem

Aqui está o diagrama da arquitetura.

Agora vamos para o código de infraestrutura (com AWS CDK) e simulação de payloads da API. Vou usar TypeScript como exemplo, mas posso adaptar para Python ou Terraform se quiser.

---

## **1. Código de Infraestrutura – AWS CDK (TypeScript)**

### **Estrutura do projeto**

```
pgsql
CopiarEditar
cdk-order-api/
├── bin/
│   └── cdk-order-api.ts
├── lib/
│   └── order-stack.ts
├── lambda/
│   ├── orderHandler.js
│   ├── sendEmail.js
│   └── generateInvoice.js
├── cdk.json
└── package.json

```

---

### **`order-stack.ts` (resumo do CDK Stack)**

```
ts
CopiarEditar
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as apigw from 'aws-cdk-lib/aws-apigateway';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class OrderStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB
    const ordersTable = new dynamodb.Table(this, 'OrdersTable', {
      partitionKey: { name: 'orderId', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    });

    // EventBridge
    const orderBus = new events.EventBus(this, 'OrderEventBus', {
      eventBusName: 'OrderEventsBus'
    });

    // S3
    const bucket = new s3.Bucket(this, 'OrderStorage');

    // Lambda - OrderHandler
    const orderHandler = new lambda.Function(this, 'OrderHandler', {
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: 'orderHandler.handler',
      code: lambda.Code.fromAsset('lambda'),
      environment: {
        TABLE_NAME: ordersTable.tableName,
        EVENT_BUS_NAME: orderBus.eventBusName
      }
    });

    ordersTable.grantReadWriteData(orderHandler);
    orderBus.grantPutEventsTo(orderHandler);

    // API Gateway
    const api = new apigw.RestApi(this, 'OrderApi');
    const orderResource = api.root.addResource('order');
    orderResource.addMethod('POST', new apigw.LambdaIntegration(orderHandler));

    // Lambdas para Email e Invoice
    const sendEmail = new lambda.Function(this, 'SendEmail', {
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: 'sendEmail.handler',
      code: lambda.Code.fromAsset('lambda'),
    });

    const generateInvoice = new lambda.Function(this, 'GenerateInvoice', {
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: 'generateInvoice.handler',
      code: lambda.Code.fromAsset('lambda'),
    });

    // EventBridge -> targets
    orderBus.addRule('OnOrderPlaced', {
      eventPattern: {
        source: ['app.orders'],
        detailType: ['OrderPlaced']
      },
      targets: [new targets.LambdaFunction(sendEmail), new targets.LambdaFunction(generateInvoice)]
    });
  }
}

```

---

### **2. Lambda de exemplo (`orderHandler.js`)**

```
js
CopiarEditar
const AWS = require('aws-sdk');
const dynamo = new AWS.DynamoDB.DocumentClient();
const eventbridge = new AWS.EventBridge();

exports.handler = async (event) => {
  const body = JSON.parse(event.body);
  const order = {
    orderId: Date.now().toString(),
    userId: body.userId,
    items: body.items,
    status: 'PENDING',
    createdAt: new Date().toISOString()
  };

  await dynamo.put({
    TableName: process.env.TABLE_NAME,
    Item: order
  }).promise();

  await eventbridge.putEvents({
    Entries: [{
      Source: 'app.orders',
      DetailType: 'OrderPlaced',
      EventBusName: process.env.EVENT_BUS_NAME,
      Detail: JSON.stringify(order)
    }]
  }).promise();

  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'Order placed', orderId: order.orderId })
  };
};

```

---

## **3. Simulação de chamada da API (payload)**

**Request:**

```
http
CopiarEditar
POST /order
Content-Type: application/json

{
  "userId": "user-123",
  "items": [
    { "sku": "prod-01", "qty": 2 },
    { "sku": "prod-99", "qty": 1 }
  ]
}

```

**Response:**

```json
json
CopiarEditar
{
  "message": "Order placed",
  "orderId": "1712165789012"
}

```

---

Se quiser, posso também gerar:

- Código completo do CDK num zip.
- Versão Terraform.
- Testes automatizados para Lambda/API.
Quer algum desses próximos?

Aqui está o **projeto completo em AWS CDK (TypeScript)** com Lambda, API Gateway, DynamoDB, EventBridge, e S3:

**Download cdk-order-api.zip**

---

Agora, vou gerar:

1. A versão em **Terraform** da mesma infra.
2. Um exemplo de **testes automatizados para a Lambda** (usando Jest).

Quer que eu siga com os dois agora ou tem preferência por um primeiro? 

Perfeito! Aqui estão os dois arquivos que você pediu:

1. **Infraestrutura com Terraform**:
    
    Download terraform-order-api.zip
    
2. **Testes automatizados com Jest para Lambda**:
    
    Download lambda-jest-tests.zip
    

---

Se quiser agora:

- Versão Python do CDK?
- Deploy guiado com comandos?
- Simular execução e logs?

É só me dizer! 

Maravilha! Vamos nessa com os **3**:

---

## **1. CDK em Python – Infraestrutura equivalente**

### Estrutura:

```
markdown
CopiarEditar
cdk_order_api_py/
├── app.py
├── cdk_order_api_py/
│   ├── __init__.py
│   └── order_stack.py
├── lambda/
│   ├── order_handler.py
│   ├── send_email.py
│   └── generate_invoice.py
├── requirements.txt

```

### **`app.py`**

```python
python
CopiarEditar
#!/usr/bin/env python3
import aws_cdk as cdk
from cdk_order_api_py.order_stack import OrderStack

app = cdk.App()
OrderStack(app, "OrderStack")
app.synth()

```

### **`order_stack.py` (resumido)**

```python
python
CopiarEditar
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as ddb,
    aws_events as events,
    aws_events_targets as targets,
    aws_s3 as s3
)
from constructs import Construct

class OrderStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        table = ddb.Table(self, "OrdersTable",
            partition_key={"name": "orderId", "type": ddb.AttributeType.STRING},
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST
        )

        event_bus = events.EventBus(self, "OrderBus", event_bus_name="OrderEventsBus")
        bucket = s3.Bucket(self, "OrderStorage")

        handler = _lambda.Function(self, "OrderHandler",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset("lambda"),
            handler="order_handler.handler",
            environment={
                "TABLE_NAME": table.table_name,
                "EVENT_BUS_NAME": event_bus.event_bus_name
            }
        )
        table.grant_read_write_data(handler)
        event_bus.grant_put_events_to(handler)

        api = apigw.RestApi(self, "OrderAPI")
        order = api.root.add_resource("order")
        order.add_method("POST", apigw.LambdaIntegration(handler))

        send_email = _lambda.Function(self, "SendEmail",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset("lambda"),
            handler="send_email.handler"
        )

        invoice = _lambda.Function(self, "GenerateInvoice",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset("lambda"),
            handler="generate_invoice.handler"
        )

        rule = events.Rule(self, "OnOrderPlaced",
            event_bus=event_bus,
            event_pattern={
                "source": ["app.orders"],
                "detail-type": ["OrderPlaced"]
            },
            targets=[targets.LambdaFunction(send_email), targets.LambdaFunction(invoice)]
        )

```

### **Lambda Exemplo (`order_handler.py`)**

```python
python
CopiarEditar
import os
import boto3
import json
from datetime import datetime

dynamo = boto3.client('dynamodb')
eventbridge = boto3.client('events')

def handler(event, context):
    data = json.loads(event['body'])
    order_id = str(int(datetime.now().timestamp() * 1000))

    dynamo.put_item(
        TableName=os.environ['TABLE_NAME'],
        Item={
            'orderId': {'S': order_id},
            'userId': {'S': data['userId']},
            'status': {'S': 'PENDING'},
            'createdAt': {'S': datetime.utcnow().isoformat()}
        }
    )

    eventbridge.put_events(
        Entries=[{
            'Source': 'app.orders',
            'DetailType': 'OrderPlaced',
            'EventBusName': os.environ['EVENT_BUS_NAME'],
            'Detail': json.dumps({'orderId': order_id, 'userId': data['userId']})
        }]
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Order placed', 'orderId': order_id})
    }

```

### **requirements.txt**

```
shell
CopiarEditar
aws-cdk-lib==2.90.0
constructs>=10.0.0

```

Se quiser, posso gerar o zip com tudo pronto.

---

## **2. Deploy Guiado – Passo a Passo com CDK (TypeScript ou Python)**

```bash
# 1. Instale o CDK e CLI AWS
npm install -g aws-cdk
aws configure  # configure suas credenciais

# 2. Instale dependências
npm install  # ou pip install -r requirements.txt para Python

# 3. Compile (TypeScript)
npx tsc

# 4. Bootstrap (só na primeira vez)
cdk bootstrap

# 5. Deploy
cdk deploy

```

---

## **3. Simulação de execução + logs (Local + CloudWatch)**

### **Chamada da API (local ou deployado)**

```bash
curl -X POST https://<API_ID>.execute-api.us-east-1.amazonaws.com/prod/order \
  -H "Content-Type: application/json" \
  -d '{"userId": "123", "items": [{"sku": "item-1", "qty": 2}]}'

```

### **Logs**

```bash
aws logs describe-log-groups
aws logs tail /aws/lambda/OrderHandler --follow

```

---

Quer que eu gere o **zip do projeto CDK em Python** também agora?

Tudo pronto! Aqui está o **projeto AWS CDK em Python completo**:

**Download cdk-order-api-python.zip**

Isso cobre:

- Infraestrutura em Python com CDK
- Lambda functions
- API Gateway
- DynamoDB, EventBridge, S3

Se quiser, posso gerar:

- Versão com Step Functions
- Monitoramento com CloudWatch Dashboards
- CI/CD com GitHub Actions ou CodePipeline