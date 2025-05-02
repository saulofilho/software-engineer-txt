Problema: 
Você quer gerenciar um conjunto de mudanças em objetos de forma transacional, garantindo que todas as alterações sejam persistidas de forma consistente (ex: múltiplas alterações em um sistema de ORM).

Solução: 
Registrar objetos modificados durante uma transação e coordenar a persistência com um repositório.

Benefícios dessa abordagem
- Baixo acoplamento entre entidades e banco (graças aos repositórios)
- Transações centralizadas e explícitas (Unit of Work)
- Serviços focados em orquestração de regras de negócio
- Testabilidade: fácil de mockar repositórios e unit of work
