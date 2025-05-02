# Kubernets

Kubernetes (ou **K8s**) é uma plataforma de orquestração de **containers**. Ele automatiza o **deploy**, o **escalonamento** (aumento ou diminuição de recursos), o **monitoramento** e a **gestão de aplicações containerizadas**, como as que rodam em **Docker**.

Em termos simples: se você tem várias aplicações rodando em containers, o Kubernetes ajuda a organizá-las, distribuir a carga, garantir que fiquem no ar (mesmo se algo falhar), escalar conforme a demanda e facilitar atualizações.

Alguns conceitos importantes no Kubernetes:

- **Pod**: a menor unidade de execução, geralmente contém um ou mais containers.
- **Node**: uma máquina (física ou virtual) onde os Pods são executados.
- **Cluster**: conjunto de nodes gerenciado pelo Kubernetes.
- **Deployment**: define como sua aplicação deve ser executada, atualizada, etc.
- **Service**: expõe a aplicação para o mundo externo ou dentro do cluster.

Imagina que você tem uma aplicação web feita em Node.js, empacotada em um **container Docker**. Agora você quer rodar essa aplicação em produção com **alta disponibilidade** (ou seja, não cair se uma instância der pau) e com possibilidade de **escalar** quando tiver muito acesso.

### Sem Kubernetes:

Você teria que subir vários containers manualmente, configurar balanceamento de carga, garantir que tudo volte ao ar se algum container parar, e fazer atualizações sem derrubar o serviço. Um baita trampo.

### Com Kubernetes:

Você só precisa dizer algo como:

> “Quero 3 réplicas da minha aplicação Node.js rodando nesse container, com um serviço exposto na porta 80, e se algum Pod morrer, suba outro.”
> 

E o Kubernetes faz tudo isso automaticamente.

### Exemplo (Deployment YAML):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: minha-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: minha-app
  template:
    metadata:
      labels:
        app: minha-app
    spec:
      containers:
      - name: minha-app
        image: meu-usuario/meu-container:latest
        ports:
        - containerPort: 3000

```

Esse arquivo diz para o Kubernetes:

> “Suba 3 instâncias do container meu-usuario/meu-container, que escuta na porta 3000”.
> 

Depois disso, você ainda criaria um **Service** para expor isso pra fora do cluster:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: minha-app-service
spec:
  type: LoadBalancer
  selector:
    app: minha-app
  ports:
    - port: 80
      targetPort: 3000

```

Esse Service diz:

> “Redirecione o tráfego da porta 80 para os Pods da minha app, que escutam na 3000”.
> 

Quer que eu te mostre como testar algo assim localmente com o **Minikube** ou **Kind** (ferramentas pra simular um cluster Kubernetes no seu computador)?
