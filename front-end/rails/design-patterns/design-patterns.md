No Ruby on Rails, vários design patterns são utilizados para organizar o código e facilitar a manutenção. Aqui estão alguns dos principais padrões usados na framework:

1. MVC (Model-View-Controller) - Arquitetural
Modelo (Model): Representa os dados e a lógica de negócio.

Visão (View): Responsável pela apresentação da informação.

Controlador (Controller): Intermedia entre o modelo e a visão.

2. Active Record - Padrão ORM
Utilizado pelo Rails para mapear tabelas do banco de dados para objetos Ruby.

Implementa o padrão Active Record, facilitando operações CRUD.

3. Service Objects - Padrão de Serviço
Organiza a lógica de negócio fora dos modelos e controladores.

Exemplo: Criar um objeto ProcessPaymentService para lidar com pagamentos.

4. Decorator - Padrão de Apresentação
Utilizado para estender funcionalidades de objetos sem modificar suas classes originais.

Gems como Draper facilitam a implementação desse padrão.

5. Presenter - Separação de Lógica de Apresentação
Similar ao Decorator, mas foca na formatação de dados para a view.

Geralmente, encapsula métodos auxiliares complexos.

6. View Components - Reutilização de Elementos na View
Permite criar componentes reutilizáveis nas views do Rails.

O Rails 6 introduziu o ViewComponent, inspirado no conceito do React.

7. Form Object - Padrão de Organização de Formulários
Centraliza a lógica de validação e manipulação de formulários.

Evita sobrecarregar modelos com regras de validação complexas.

8. Query Object - Padrão de Consulta ao Banco
Isola consultas complexas em classes separadas.

Exemplo: UsersWithActiveSubscriptionQuery.call

9. Repository - Camada de Abstração do Banco
Cria uma camada intermediária entre o banco de dados e os modelos.

10. Policy Object - Controle de Permissões
Implementado com a gem Pundit para controlar regras de autorização.

11. Observer - Monitoramento de Mudanças no Modelo
Permite executar ações automaticamente quando um modelo é alterado.

Implementado com ActiveSupport::Observers.

12. Factory - Criação de Objetos para Testes
Utilizado com gems como FactoryBot para gerar dados de teste.

13. Singleton - Garantia de Instância Única
Implementado com self.instance dentro de classes.