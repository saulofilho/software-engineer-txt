O que é o Repository Pattern?

É um padrão de projeto que isola a lógica de acesso a dados da lógica de negócios. Com isso, o código fica mais organizado, testável e flexível.

Sem Repository Pattern: você acessa o banco de dados diretamente nos serviços ou controladores.
Sem Repository:
1 - Acoplamento forte com o banco de dados
2 - Dificuldade para testar
3 - Repetição de código
4 - Responsabilidades misturadas
5- Baixa reutilização
6 - Dificuldade de manutenção

Com Repository Pattern: você usa uma camada intermediária (o repositório) para manipular os dados.
Com Repository:
1 - Separação de responsabilidades
2 - Facilita testes (mockar repositório)
3 - Possível trocar implementação do repositório sem alterar a lógica de negócio
