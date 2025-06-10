# Guia Completo de Access Control Lists (ACL)

Este guia aborda, em nível avançado, o conceito de **Access Control Lists (ACL)**, cobrindo definições, modelos, implementações em diversos sistemas (Unix/Linux, Windows, redes, bancos de dados, aplicações), melhores práticas e exemplos práticos.

---

## 1. O que é ACL?

* **Access Control List (ACL)**: lista que especifica permissões detalhadas para usuários ou grupos em relação a recursos (arquivos, diretórios, objetos de rede, APIs).
* **Diferença de DAC vs. MAC**:

  * **DAC (Discretionary Access Control)**: permissões definidas pelo proprietário do recurso.
  * **MAC (Mandatory Access Control)**: políticas centralizadas, ex.: SELinux, AppArmor.

---

## 2. Tipos e Modelos de ACL

| Modelo              | Descrição                                                                        |
| ------------------- | -------------------------------------------------------------------------------- |
| **Tipo-List**       | ACLs por recurso, listando entradas (usuário/grupo → permissões).                |
| **Role-Based**      | ACLs baseadas em papéis (roles) e atributos (ABAC); mapeia roles a permissões.   |
| **Network ACL**     | Firewall ou router ACLs: regras de permit/deny baseadas em IP, porta, protocolo. |
| **Application ACL** | ACLs em aplicações (RBAC/ABAC), definindo acesso a endpoints ou operações.       |

---

## 3. ACLs em Sistemas de Arquivos

### 3.1 POSIX ACL (Linux/UNIX)

* **Ferramentas**: `setfacl`, `getfacl`, requer sistema de arquivos que suporte ACL (ext4, XFS).
* **Entrada de ACL**:

  ```bash
  # Adicionar permissão de leitura para user 'alice'
  setfacl -m u:alice:r-- file.txt
  # Remover permissão
  setfacl -x u:alice file.txt
  # Definir ACL recursiva
  setfacl -R -m g:devs:rwX /project
  ```
* **Visualizar**:

  ```bash
  getfacl file.txt
  ```
* **Máscara**: entry `mask` define máximo de permissões para usuários e grupos.

### 3.2 ACL em Windows NTFS

* **Ferramentas UI**: aba Segurança nas propriedades.
* **Comandos**:

  ```powershell
  # Exibir ACL
  Get-Acl C:\path\file.txt | Format-List
  # Definir permissão
  $acl = Get-Acl C:\path\file.txt
  $rule = New-Object System.Security.AccessControl.FileSystemAccessRule("DOMAIN\Alice", "ReadData", "Allow")
  $acl.AddAccessRule($rule)
  Set-Acl C:\path\file.txt $acl
  ```
* **Inheritance**: hierarquia de pastas herda ACL a objetos filhos.
* **Audit**: flags para auditar sucesso/fracasso de acessos.

---

## 4. Network ACLs (Firewalls e Roteadores)

* **ACLs em Cisco IOS**:

  ```text
  ip access-list extended BLOCK_HTTP
    deny tcp any any eq 80
    permit ip any any
  interface GigabitEthernet0/1
    ip access-group BLOCK_HTTP in
  ```
* **iptables (Linux)**:

  ```bash
  # Bloquear HTTP inbound
  iptables -A INPUT -p tcp --dport 80 -j DROP
  # Permitir SSH
  iptables -A INPUT -p tcp --dport 22 -j ACCEPT
  ```
* **Cloud Network ACLs**: AWS NACL (stateless), Azure NSG (stateful).

---

## 5. ACLs em Bancos de Dados

### 5.1 MySQL

* **Users e Privileges**:

  ```sql
  CREATE USER 'alice'@'%' IDENTIFIED BY 'pass';
  GRANT SELECT, INSERT ON mydb.* TO 'alice'@'%';
  FLUSH PRIVILEGES;
  ```
* **INFORMATION\_SCHEMA**: tabelas `USER_PRIVILEGES`, `SCHEMA_PRIVILEGES`.

### 5.2 PostgreSQL

* **Roles e Grants**:

  ```sql
  CREATE ROLE alice LOGIN PASSWORD 'pass';
  GRANT SELECT, UPDATE ON TABLE public.orders TO alice;
  ```
* **Row-Level Security (RLS)**: políticas por linha:

  ```sql
  ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
  CREATE POLICY owner_policy ON orders FOR SELECT USING (owner_id = current_user_id());
  ```

---

## 6. ACLs em Aplicações e APIs

### 6.1 RBAC com JWT e Claims

* **JWT** carrega roles/permissions nos claims.
* **Middleware** valida claim e compara com ACL:

  ```js
  function authorize(requiredRole) {
    return (req, res, next) => {
      const roles = req.user.roles;
      if (!roles.includes(requiredRole)) return res.status(403).send('Forbidden');
      next();
    };
  }
  app.get('/admin', authorize('admin'), handler);
  ```

### 6.2 ABAC e Policy Decision

* **Open Policy Agent (OPA)** com Rego:

  ```rego
  package httpapi.authz

  default allow = false
  allow {
    input.user == resource.owner
    input.action == "read"
  }
  ```
* **Request** para OPA:

  ```json
  { "input": { "user": "alice", "resource": { "owner": "alice" }, "action": "read" } }
  ```

---

## 7. Ferramentas de Gerenciamento de ACL

* **LDAP**: atributos `acl` e `accessControlAttribute`.
* **Keycloak**: Admin UI para definir roles, grupos e mappers.
* **AWS IAM**: policies JSON para recursos AWS.
* **Kubernetes RBAC**: `ClusterRole`, `RoleBinding`:

  ```yaml
  apiVersion: rbac.authorization.k8s.io/v1
  kind: Role
  metadata:
    namespace: default
    name: pod-reader
  rules:
    - apiGroups: [""]
      resources: ["pods"]
      verbs: ["get", "watch", "list"]
  ---
  kind: RoleBinding
  apiVersion: rbac.authorization.k8s.io/v1
  metadata:
    name: read-pods
    namespace: default
  subjects:
    - kind: User
      name: alice
      apiGroup: rbac.authorization.k8s.io
  roleRef:
    kind: Role
    name: pod-reader
    apiGroup: rbac.authorization.k8s.io
  ```

---

## 8. Boas Práticas de ACL

1. **Princípio do Menor Privilégio**: permitir apenas permissões necessárias.
2. **Revisão Periódica**: auditar e revogar entradas obsoletas.
3. **Uso de Grupos/Roles** em vez de permissões por usuário.
4. **Políticas Claras e Documentadas**: use convenções de nomenclatura e documentação.
5. **Automação**: aplicar ACL via IaC (Terraform, Ansible).
6. **Monitoramento e Logs**: registrar mudanças de ACL e acessos negados.

---

## 9. Conclusão

ACLs são fundamentais para controle granular de acesso em múltiplos domínios: sistemas de arquivos, redes, bancos e aplicações. Seguir modelos de menor privilégio, revisar periodicamente e automatizar definições garante segurança consistente e compliance.
