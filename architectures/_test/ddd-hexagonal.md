DDD + Arquitetura Hexagonal: Sempre vale a pena?
Recentemente trabalhei num projeto de pagamento onde, mesmo com poucos usuários e requisitos relativamente simples, optaram por aplicar DDD (Domain-Driven Design) e Arquitetura Hexagonal logo de cara.

DDD e arquitetura hexagonal são excelentes... MAS em contextos certos.

QUANDO VALE A PENA USAR?
-> Domínio complexo, cheio de regras e exceções.
-> Regras de negócio que mudam com frequência.
-> Muitos pontos de integração (bancos, APls, filas).
-> Necessidade de testes mais robustos e isolamento de dependências.

QUANDO NÃO VALE A PENA?
-> Projeto simples ou MVP.
-> Poucos usuários, baixo escopo e prazo curto.
-> Sem regras de negócio relevantes.
-> Time pequeno ou sem familiaridade com essas abordagens.
No fim das contas, arquitetura é uma decisão estratégica. Ela deve servir ao projeto e não o contrário.
