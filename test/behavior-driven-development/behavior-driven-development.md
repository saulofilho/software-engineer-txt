# Guia Completo de BDD (Behavior-Driven Development)

Este guia aborda em profundidade o BDD (Behavior-Driven Development): conceitos, ciclo, ferramentas, sintaxe Gherkin, exemplos práticos e boas práticas.

---

## 1. O que é BDD?

Behavior-Driven Development (BDD) é uma evolução do TDD que enfatiza a colaboração entre desenvolvedores, QA e stakeholders de negócio através de linguagem ubíqua e cenários executáveis. BDD foca em comportamentos do sistema, não em implementações.

**Objetivos**:

* Garantir entendimento compartilhado de requisitos.
* Gerar documentação viva com exemplos concretos.
* Automatizar testes de aceitação de alto nível.

---

## 2. Principais Características

1. **Linguagem Ubíqua**: termos de negócio usados em especificações.
2. **Cenários Executáveis**: exemplos escritos em formato estruturado (Gherkin).
3. **Colaboração**: envolvimento de times multidisciplinares.

---

## 3. Sintaxe Gherkin

Gherkin é a linguagem de domínio específico usada para escrever cenários BDD.

* **Feature**: descrição de funcionalidade.
* **Scenario**: caso de uso específico.
* **Given / When / Then / And / But**: passos do cenário.

```gherkin
Feature: Login de usuário
  Como usuário autenticado
  Quero acessar minha conta
  Para visualizar meu dashboard

  Scenario: Login bem-sucedido
    Given que estou na página de login
    When insiro credenciais válidas
    Then devo ser redirecionado para o dashboard
    And devo ver minha foto de perfil
```

---

## 4. Ciclo de BDD

1. **Discovery**: workshops de 3 amigos (dev, QA, PO) discutem comportamentos.
2. **Formação de cenários**: escrever exemplos em Gherkin.
3. **Automação**: implementar passos dos cenários nos testes.
4. **Implementação de código**: TDD para tornar cenários verdes.
5. **Refatoração**: melhorar código e cenários.

---

## 5. Ferramentas Populares

| Ferramenta | Linguagem       | Descrição                      |
| ---------- | --------------- | ------------------------------ |
| Cucumber   | Ruby, Java, JS  | CLI e bibliotecas para Gherkin |
| SpecFlow   | .NET            | BDD para C# e VB.NET           |
| Behave     | Python          | Simples, integrado com pytest  |
| JBehave    | Java            | Framework BDD para Java        |
| Gauge      | Multi-linguagem | DSL flexível, plugins          |

---

## 6. Exemplos Práticos

### 6.1 JavaScript com Cucumber.js

```gherkin
# features/login.feature
Feature: Login
  Scenario: Usuário faz login com sucesso
    Given estou na página de login
    When preencho "username" com "user1"
    And preencho "password" com "pass123"
    And clico em "Login"
    Then devo ver "Bem-vindo, user1!"
```

```js
// steps/login.steps.js
const { Given, When, Then } = require('@cucumber/cucumber');
const assert = require('assert');

Given('estou na página de login', async () => {
  await browser.url('/login');
});
When('preencho {string} com {string}', async (field, value) => {
  await $(`#${field}`).setValue(value);
});
When('clico em {string}', async (btn) => {
  await $(`button=${btn}`).click();
});
Then('devo ver {string}', async (msg) => {
  const text = await $('body').getText();
  assert(text.includes(msg));
});
```

### 6.2 Python com Behave

```gherkin
# features/calculator.feature
Feature: Operations
  Scenario: Somar dois números
    Given que eu tenho 2 e 3
    When eu somo esses números
    Then o resultado deve ser 5
```

```python
# features/steps/calculator_steps.py
from behave import given, when, then
from calculator import Calculator

given('que eu tenho {a:d} e {b:d}')
def step_impl(context, a, b):
    context.calc = Calculator()
    context.a = a
    context.b = b

@when('eu somo esses números')
def step_impl(context):
    context.result = context.calc.add(context.a, context.b)

@then('o resultado deve ser {expected:d}')
def step_impl(context, expected):
    assert context.result == expected
```

### 6.3 C# com SpecFlow

```gherkin
Feature: Checkout
  Scenario: Finalizar compra
    Given o carrinho tem 2 itens
    When eu finalizar a compra
    Then o pedido deve ser criado
```

```csharp
[Binding]
public class CheckoutSteps {
  Cart cart;

  [Given("o carrinho tem (\d+) itens")]
  public void GivenCartHasItems(int count) {
    cart = new Cart();
    cart.AddItems(count);
  }

  [When("eu finalizar a compra")]
  public void WhenCheckout() {
    cart.Checkout();
  }

  [Then("o pedido deve ser criado")]
  public void ThenOrderCreated() {
    Assert.IsTrue(cart.OrderCreated);
  }
}
```

---

## 7. Boas Práticas em BDD

1. **Escrever cenários de negócio**, não de UI.
2. **Evitar detalhes de implementação** nos passos (mantenha passos de alto nível).
3. **Reutilizar passos**: DRY nos step definitions.
4. **Manter o backlog de features organizado** e versionado.
5. **Revisar cenários regularmente** no comportamento de negócio.

---

## 8. Dificuldades Comuns

* **Cenários inflados** com detalhes técnicos.
* **Passos demasiadamente genéricos** que escondem lógica.
* **Manutenção dos steps** quando o sistema muda.

---

## 9. Integração com CI/CD

* Executar testes BDD no pipeline.
* Gerar relatórios legíveis para stakeholders (HTML, JSON).
* Bloquear merges se cenários falharem.

---

## Conclusão

BDD fortalece a comunicação e a qualidade do software, alinhando código e requisitos de negócio. Use cenários claros, ferramentas adequadas e mantenha o foco no comportamento desejado.
