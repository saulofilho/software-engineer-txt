### Principais Modelos e Atributos do Redmine

1. **User (Usuário)**
    - id
    - login
    - hashed_password
    - firstname
    - lastname
    - mail
    - admin
    - status
    - created_on
    - updated_on
2. **Project (Projeto)**
    - id
    - name
    - identifier
    - description
    - homepage
    - is_public
    - parent_id
    - created_on
    - updated_on
3. **Issue (Tarefa)**
    - id
    - project_id
    - subject
    - description
    - tracker_id
    - status_id
    - priority_id
    - assigned_to_id
    - author_id
    - start_date
    - due_date
    - created_on
    - updated_on
4. **Tracker (Rastreadores)**
    - id
    - name
    - position
    - is_in_chlog
    - default_status_id
5. **Status**
    - id
    - name
    - is_default
    - is_closed
6. **Priority**
    - id
    - name
    - position
7. **Version (Versão)**
    - id
    - project_id
    - name
    - description
    - effective_date
    - created_on
    - updated_on
8. **TimeEntry (Registro de Tempo)**
    - id
    - project_id
    - issue_id
    - user_id
    - hours
    - comments
    - spent_on
    - created_on
    - updated_on
9. **Membership (Membro)**
    - id
    - project_id
    - user_id
    - role_ids (pode ser uma lista de IDs de funções)
10. **Role (Função)**
    - id
    - name
    - position
    - assignable

### Diagrama ER (Entidade-Relacionamento)

Abaixo está uma descrição textual simplificada de como você poderia estruturar um diagrama ER:

- **User** pode estar associado a várias **Memberships**.
- **Project** pode ter várias **Memberships** e **Issues**.
- **Issue** pode ter um **User** atribuído, um **Status**, um **Tracker**, uma **Priority** e pode estar relacionada a um **Version**.
- **TimeEntry** é associado a um **User**, um **Project** e uma **Issue**.

Para visualizar isso graficamente, você pode usar ferramentas como Lucidchart, Draw.io ou qualquer software de modelagem de dados para criar um diagrama ER.
