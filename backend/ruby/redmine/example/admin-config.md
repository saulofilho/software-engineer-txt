### 1. Projetos

- **Modelo**: `Project`
- **Descrição**: Representa um projeto específico no Redmine. Cada projeto pode ter suas próprias tarefas, membros, versões, etc.

### 2. Usuários

- **Modelo**: `User`
- **Descrição**: Representa os usuários do sistema. Os usuários podem ser atribuídos a projetos, tarefas e podem ter diferentes papéis.

### 3. Grupos

- **Modelo**: `Group`
- **Descrição**: Os grupos são utilizados para organizar usuários. Embora o Redmine não tenha um modelo `Group` explícito, os grupos podem ser representados através de associações de usuários e permissões em projetos.

### 4. Papéis e permissões

- **Modelo**: `Role`
- **Descrição**: Define os papéis que um usuário pode assumir dentro de um projeto, bem como as permissões associadas a esse papel.

### 5. Tipos de tarefas

- **Modelo**: `Tracker`
- **Descrição**: Representa diferentes tipos de tarefas (ou rastreadores) que podem ser criadas, como bugs, melhorias, tarefas, etc.

### 6. Situação das tarefas

- **Modelo**: `Status`
- **Descrição**: Representa o estado atual de uma tarefa, como "Novo", "Em andamento", "Concluído", etc.

### 7. Fluxo de trabalho

- **Modelo**: `Workflow`
- **Descrição**: Define as transições possíveis entre os status das tarefas e as permissões para esses estados dentro de um projeto.

### 8. Campos personalizados

- **Modelo**: `CustomField`
- **Descrição**: Permitem que os usuários adicionem campos adicionais a diferentes modelos (como tarefas, projetos, etc.) para capturar informações específicas que não estão disponíveis nos campos padrão.

### 9. Tipos & Categorias

- **Modelos**: `Category` (para tarefas) e `Version` (para versões de projeto)
- **Descrição**: Categorias podem ser usadas para classificar tarefas dentro de um projeto, enquanto versões representam marcos ou lançamentos de um projeto.

### 10. Configurações

- **Modelo**: O Redmine possui um conjunto de configurações no banco de dados, mas não há um modelo específico chamado `Configuration`. As configurações incluem preferências do sistema, configurações de e-mail, entre outras.

### 11. Autenticação LDAP

- **Modelo**: O Redmine não possui um modelo específico para LDAP, mas permite configuração de autenticação via LDAP nas configurações do sistema.
- **Descrição**: Permite que os usuários façam login usando credenciais de um diretório LDAP.

### 12. Plugins

- **Modelo**: Não há um modelo específico, mas os plugins podem adicionar novos modelos e funcionalidades ao Redmine.
- **Descrição**: Extensões que adicionam funcionalidades ao Redmine, como novos tipos de relatórios, integrações com outras ferramentas, etc.

### 13. Informações

- **Descrição**: Isso pode se referir a várias informações gerais que podem ser armazenadas em diferentes modelos, como relatórios, histórico de atividades, etc.
