O que é arquitetura orientada a serviços?
Arquitetura orientada a serviços (SOA) é um método de desenvolvimento de software que usa componentes de software chamados de serviços para criar aplicações de negócios. Cada serviço fornece um recurso de negócios, e todos eles também podem se comunicar entre si em diferentes plataformas e linguagens. Os desenvolvedores usam a SOA para reutilizar serviços em sistemas diferentes ou combinar vários serviços independentes para realizar tarefas complexas.

Por exemplo, vários processos de negócios em uma organização exigem a funcionalidade de autenticação de usuários. Em vez de reescrever o código de autenticação para todos os processos de negócios, você pode criar um único serviço de autenticação e reutilizá-lo para todas as aplicações. Da mesma maneira, quase todos os sistemas em uma organização de saúde, como sistemas de gerenciamento de pacientes e sistemas de prontuário eletrônico de saúde (EHR), precisam registrar pacientes. Eles podem chamar um único serviço comum para realizar essa tarefa.

Quais são os benefícios da arquitetura orientada a serviços?
A SOA tem vários benefícios em relação às arquiteturas monolíticas tradicionais, nas quais todos os processos são executados como uma única unidade. Alguns dos principais benefícios da SOA incluem:

Mais rapidez para entrada no mercado
Os desenvolvedores reutilizam serviços em diferentes processos de negócios para poupar tempo e economizar custos. Eles podem estruturar aplicações muito mais rapidamente com a SOA do que escrevendo código e realizando integrações do zero.

Manutenção eficiente
É mais fácil criar, atualizar e depurar pequenos serviços do que grandes blocos de código em aplicações monolíticas. A modificação de qualquer serviço na SOA não afeta a funcionalidade geral do processo de negócios.

Maior adaptabilidade
A SOA é mais adaptável aos avanços da tecnologia. Você pode modernizar suas aplicações de maneira eficiente e econômica. Por exemplo, as organizações de saúde podem usar a funcionalidade de sistemas de EHR mais antigos em aplicações baseadas na nuvem mais recentes.

Quais são os princípios básicos da arquitetura orientada a serviços?
Não há diretrizes padrão bem definidas para implementar a arquitetura orientada a serviços (SOA). Porém, alguns princípios básicos são comuns em todas as implementações da SOA.

Interoperabilidade
Cada serviço na SOA inclui documentos de descrição que especificam a funcionalidade do serviço e os termos e condições relacionados. Qualquer sistema cliente pode executar um serviço, independentemente da plataforma de base ou da linguagem de programação. Por exemplo, processos de negócios podem usar serviços escritos em C# e Python. Como não há interações diretas, as alterações em um serviço não afetam outros componentes que usam esse serviço.

Acoplamento fraco
Os serviços na SOA devem ter acoplamento fraco, tendo a menor dependência possível de recursos externos, como modelos de dados ou sistemas de informações. Eles também devem ser stateless, sem reter informações de sessões ou transações anteriores. Dessa forma, se você modificar um serviço, ele não afetará significativamente as aplicações cliente e outros serviços que o utilizam.

Abstração
Os clientes ou usuários de serviços na SOA não precisam conhecer a lógica do código ou os detalhes de implementação do serviço. Para eles, os serviços devem parecer uma caixa preta. Os clientes obtêm as informações necessárias sobre o que o serviço faz e como utilizá-lo por meio de contratos de serviço e outros documentos de descrição de serviços.

Granularidade
Os serviços na SOA devem ter um tamanho e escopo apropriados, idealmente empacotando uma única
função de negócios distinta por serviço. Os desenvolvedores podem então usar vários serviços a fim de criar um serviço composto para realizar operações complexas.

Quais são os componentes da arquitetura orientada a serviços?
Existem quatro componentes principais na arquitetura orientada a serviços (SOA).

Serviço
Serviços são os alicerces básicos da SOA. Eles podem ser privados (disponíveis apenas para usuários internos de uma organização) ou públicos (acessíveis pela Internet a todos). Individualmente, cada serviço tem três características principais.

Implementação do serviço
A implementação do serviço é o código que cria a lógica para realizar a função de serviço específica, como a autenticação de um usuário ou o cálculo de uma fatura.

Contrato de serviço
O contrato de serviço define a natureza do serviço e seus termos e condições associados, como os pré-requisitos para usar o serviço, o custo do serviço e a qualidade do serviço prestado.
 
Interface de serviço
Na SOA, outros serviços ou sistemas se comunicam com um serviço por meio de sua interface de serviço. A interface define como você pode chamar o serviço para realizar atividades ou trocar dados. Ele reduz as dependências entre os serviços e aquele que os solicita. Por exemplo, até mesmo usuários com pouca ou nenhuma compreensão da lógica do código subjacente podem usar um serviço por meio de sua interface.
Provedor de serviços
O provedor de serviços cria, mantém e fornece um ou mais serviços que outros usuários podem utilizar. Organizações podem criar seus próprios serviços ou comprá-los de provedores de serviços terceirizados.

Consumidor de serviços
O consumidor de serviços solicita que o provedor de serviços execute um serviço específico. Pode ser um sistema inteiro, uma aplicação ou outro serviço. O contrato de serviço especifica as regras que o provedor e o consumidor de serviços devem seguir ao interagirem entre si. Provedores e consumidores de serviços podem pertencer a diferentes departamentos, organizações e até mesmo setores.

Registro de serviços
Um registro de serviços, ou repositório de serviços, é um diretório de serviços disponíveis acessível pela rede. Ele armazena documentos de descrição de serviço de provedores de serviços. Documentos de descrição contêm informações sobre o serviço e como se comunicar com ele. Os consumidores de serviços podem descobrir facilmente os serviços de que precisam usando o registro de serviços.

Como funciona a arquitetura orientada a serviços?
Na arquitetura orientada a serviços (SOA), os serviços funcionam de maneira independente e fornecem funcionalidades ou troca de dados aos seus consumidores. O consumidor solicita informações e envia dados de entrada ao serviço. O serviço processa esses dados, realiza a tarefa e retorna uma resposta. Por exemplo, se uma aplicação usa um serviço de autorização, ela fornece ao serviço o nome de usuário e a senha. O serviço verifica esses dados e retorna uma resposta apropriada.

Protocolos de comunicação
Serviços se comunicam usando regras estabelecidas que determinam a transmissão de dados em uma rede. Essas regras são chamadas de protocolos de comunicação. Alguns protocolos padrão para implementar a SOA incluem:

• Protocolo Simples de Acesso a Objetos (SOAP)
• HTTP RESTful
• Apache Thrift
• Apache ActiveMQ
• Serviço de Mensagens Java (JMS)

Você pode até mesmo usar mais de um protocolo na sua implementação da SOA.
