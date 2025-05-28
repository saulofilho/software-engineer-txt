# Guia Completo de Test-Driven Development (TDD)

Este guia aborda o ciclo, práticas, benefícios e exemplos avançados de Test-Driven Development (TDD) em múltiplas linguagens.

---

## 1. O que é TDD?

Test-Driven Development é uma prática de desenvolvimento ágil proposta por Kent Beck, onde os testes são escritos **antes** do código de produção. Segue o ciclo:

1. **Red**: escreva um teste que falhe.
2. **Green**: implemente o código mínimo para passar no teste.
3. **Refactor**: limpe e otimize o código mantendo todos os testes verdes.

---

## 2. Benefícios de TDD

* **Design Orientado a Testes**: força API simples e coesa.
* **Feedback Imediato**: detecta regressões rapidamente.
* **Código com Menos Bugs**: cobertura alta de casos críticos.
* **Documentação Viva**: os testes servem como especificação.

---

## 3. Ciclo Red-Green-Refactor

| Etapa    | Objetivo                                             |
| -------- | ---------------------------------------------------- |
| Red      | Definir comportamento desejado via teste falho.      |
| Green    | Implementar o mínimo para satisfazer o teste.        |
| Refactor | Eliminar duplicação, melhorar legibilidade e design. |

*Dica*: mantenha cada iteração rápida (<5s) para teste + produção.

---

## 4. Tipos de Testes em TDD

1. **Unit Tests**: isolam funções/métodos; rápida execução.
2. **Integration Tests**: testam interação entre módulos (bancos, APIs).
3. **Functional/Acceptance Tests**: validam requisitos de alto nível (BDD).

Mantém-se a regra: **75% unit** : 25% integration.

---

## 5. Mocks, Stubs e Fakes

* **Stub**: retorna dados pré-definidos; não verifica interação.
* **Mock**: objeto espião que verifica comportamentos (métodos chamados, argumentos).
* **Fake**: implementação simplificada (ex: banco em memória).

Use com parcimônia para evitar testes frágeis.

---

## 6. Exemplos Práticos

### 6.1 JavaScript com Jest

```js
// funcoes.js
function sum(a, b) {
  return a + b;
}
module.exports = sum;

// funcoes.test.js
const sum = require('./funcoes');
test('soma 2 + 3 = 5', () => {
  expect(sum(2, 3)).toBe(5);
});
```

Ciclo:

```bash
npm test -- --watch
# Red: falha teste sem funcoes.js
# Green: implementa sum e salva até ficar verde
# Refactor: ajustar formatação, extrair constantes
```

### 6.2 Python com pytest

```py
# calculadora.py
def multiply(a, b):
    return a * b

# test_calculadora.py
import pytest
from calculadora import multiply

def test_multiply():
    assert multiply(3, 4) == 12
```

Executar:

```bash
pytest --maxfail=1 --disable-warnings -q
```

### 6.3 Ruby com RSpec

```ruby
# lib/string_utils.rb
class StringUtils
  def self.reverse(str)
    str.reverse
  end
end

# spec/string_utils_spec.rb
require 'string_utils'

describe StringUtils do
  it 'reverte string' do
    expect(StringUtils.reverse('abc')).to eq 'cba'
  end
end
```

---

## 7. Práticas Avançadas

* **Property-Based Testing**: geradores de dados aleatórios (Hypothesis, QuickCheck).
* **Mutation Testing**: introduz mutações no código para medir efetividade dos testes.
* **Contract Testing**: validar APIs externas (PACT).
* **Acceptance TDD** (ATDD) com Cucumber/Gherkin.

---

## 8. Integração com CI/CD

* Rodar testes em pipeline (GitHub Actions, GitLab CI).
* Falhas bloqueiam merge.
* Indicadores de cobertura (Codecov, Coveralls).

Exemplo GitHub Actions:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with: { 'node-version': '18' }
      - run: npm ci
      - run: npm test
```

---

## 9. Boas Práticas

1. **Teste primeiro o comportamento** (não a implementação).
2. **Mantenha testes pequenos** e de fácil leitura.
3. **Evite lógica complexa nos testes**.
4. **Documente intenções** via nomes claros de testes.
5. **Revisite e refatore testes** junto com código.

---

## 10. Desafios e Contra-Argumentos

* **Sobrecarga inicial**: requer disciplina; pode retardar no curto prazo.
* **Testes frágeis**: uso excessivo de mocks pode levar a mudanças frequentes nos testes.
* **Cobertura não é qualidade**: foco em casos relevantes, não em números.

---

## Conclusão

TDD é uma disciplina que melhora design, confiabilidade e manutenção do software. Com prática constante e revisão crítica, traz agilidade e qualidade ao desenvolvimento de produtos.
