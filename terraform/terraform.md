# Terraform

Terraform é uma ferramenta de **infraestrutura como código (IaC)** criada pela HashiCorp. Ela permite que você defina, provisione e gerencie recursos de infraestrutura (como servidores, redes, bancos de dados, etc.) usando **arquivos de configuração em texto**, geralmente escritos em uma linguagem chamada **HCL (HashiCorp Configuration Language)**.

### Em termos simples:

Em vez de criar servidores manualmente em um painel como o da AWS, você escreve um arquivo descrevendo o que você quer, e o Terraform faz isso pra você automaticamente.

### Exemplos do que você pode criar com Terraform:

- Instâncias EC2 na AWS
- Buckets no S3
- Máquinas virtuais no Google Cloud ou Azure
- Configuração de redes, firewalls, load balancers
- E muito mais (Terraform tem muitos provedores, além de cloud)

### Vantagens:

- **Automação**: menos chance de erro humano.
- **Versionamento**: você pode versionar sua infraestrutura como código.
- **Reutilização**: criar módulos para reaproveitar em diferentes projetos.
- **Provisionamento em múltiplas nuvens**: AWS, Azure, Google Cloud, etc.

Se quiser, posso te mostrar um exemplo básico de um arquivo Terraform. Quer ver?

4o

### Você disse:

Sim

### O ChatGPT disse:

Show! Aqui vai um exemplo bem simples de um arquivo Terraform que cria uma instância EC2 na AWS:

```hcl
hcl
CopiarEditar
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "exemplo" {
  ami           = "ami-0c55b159cbfafe1f0" # AMI do Ubuntu, por exemplo
  instance_type = "t2.micro"

  tags = {
    Name = "MinhaInstanciaTerraform"
  }
}

```

### O que esse código faz:

1. **Define o provedor**: Diz que vamos usar a AWS e em qual região (`us-east-1`).
2. **Cria um recurso**: Uma instância EC2 com uma AMI específica e tipo `t2.micro`.
3. **Adiciona tags**: Nesse caso, só o nome da instância.

### Como usar:

1. Instale o Terraform.
2. Crie um arquivo chamado `main.tf` com esse conteúdo.
3. No terminal, rode:
    - `terraform init` (inicializa o projeto)
    - `terraform plan` (mostra o que será feito)
    - `terraform apply` (executa e cria a infra)

Quer que eu te ajude a criar um projeto Terraform do zero com algo específico? Tipo uma instância, bucket S3, ou rede?
