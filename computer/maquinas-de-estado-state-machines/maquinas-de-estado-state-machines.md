# Guia Completo de Máquinas de Estado

Este guia aborda, em nível avançado, as **Máquinas de Estado** (State Machines): modelos formais para controle de fluxo de sistemas, incluindo autômatos finitos, máquinas de estado hierárquicas, statecharts, redes de Petri e implementações em software.

---

## 1. Conceito e Motivação

* **Máquina de Estado**: modelo computacional que, em resposta a eventos, transita entre estados definidos e executa ações associadas.
* **Motivação**:

  1. Clarificar lógica de controle em sistemas reativos.
  2. Facilitar verificação e teste de comportamento.
  3. Modularizar fluxos complexos e garantir robustez.

---

## 2. Autômatos Finitos (Finite State Machines)

### 2.1 Definição Formal

Um **AFD (Autômato Finito Determinístico)** é a 5-tupla $(Q, Σ, δ, q₀, F)$:

* $Q$: conjunto finito de estados.
* $Σ$: alfabeto de símbolos/eventos.
* $δ: Q × Σ → Q$: função de transição.
* $q₀ ∈ Q$: estado inicial.
* $F ⊆ Q$: estados finais ou de aceitação.

### 2.2 Exemplo de AFD

```text
Q = {Locked, Unlocked}
Σ = {coin, push}
q₀ = Locked
F = {Unlocked}
δ:
  (Locked, coin) → Unlocked
  (Locked, push) → Locked
  (Unlocked, coin) → Unlocked
  (Unlocked, push) → Locked
```

---

## 3. Máquinas de Estado Hierárquicas (Statecharts)

* **Statecharts (Harel)**: estendem FSM com hierarquia, paralelismo e histórico.
* **Componentes**:

  * Estados compostos (contêm subestados).
  * Transições hierárquicas que atravessam níveis.
  * Estados ortogonais (regiões paralelas).
  * Pseudostados (`initial`, `history`).

### 3.1 Benefícios

1. Reduz explosão de estados (composição em árvore).
2. Modela sistemas concorrentes (regiões paralelas).
3. Facilita design visual e compartilhamento.

---

## 4. Redes de Petri

* **Petri Nets**: grafo bipartido com lugares (states) e transições.
* **Marcação**: distribuição de tokens define o estado atual.
* **Disparo de Transição**: consome tokens de lugares de entrada e produz em lugares de saída.

### 4.1 Uso Avançado

* Modelagem de concorrência, sincronização e recursos limitados.
* Análise formal de propriedades: vivacidade, alcance, deadlock.

---

## 5. Streams de Eventos e Máquinas de Estado

* **Event Sourcing** e **CQRS** geralmente usam máquinas de estado para derivar estado de agregados a partir de logs de eventos.
* **Workflow Engines** (Zeebe, Temporal) empregam state machines para orquestração de tarefas e estados de workflow.

---

## 6. Implementações em Código

### 6.1 JavaScript (xstate)

```js
import { createMachine, interpret } from 'xstate';

const turnstile = createMachine({
  id: 'turnstile',
  initial: 'locked',
  states: {
    locked: { on: { COIN: 'unlocked', PUSH: 'locked' } },
    unlocked: { on: { PUSH: 'locked', COIN: 'unlocked' } }
  }
});

const service = interpret(turnstile).start();
service.subscribe(state => console.log(state.value));
service.send('COIN'); // unlocked
```

### 6.2 Python (transitions)

```python
from transitions import Machine

class Turnstile:
    pass

turnstile = Turnstile()
states = ['locked', 'unlocked']
transitions = [
    {'trigger': 'coin', 'source': 'locked', 'dest': 'unlocked'},
    {'trigger': 'push', 'source': 'unlocked', 'dest': 'locked'}
]

machine = Machine(model=turnstile, states=states, transitions=transitions, initial='locked')
print(turnstile.state)  # 'locked'
turnstile.coin()
print(turnstile.state)  # 'unlocked'
```

### 6.3 Ruby (state\_machine gem)

```ruby
require 'state_machine'

class Turnstile
  state_machine initial: :locked do
    event :coin do
      transition locked: :unlocked
    end

    event :push do
      transition unlocked: :locked, locked: :locked
    end

    state :locked do
      # Ação ao entrar em :locked
      before_transition any => :locked do |obj, _|
        puts 'Transitioning to locked state'
      end
    end

    state :unlocked do
      # Ação ao entrar em :unlocked
      before_transition any => :unlocked do |obj, _|
        puts 'Transitioning to unlocked state'
      end
    end
  end
end

# Uso
t = Turnstile.new
puts t.state   # => "locked"
t.coin         # => "Transitioning to unlocked state"
puts t.state   # => "unlocked"
t.push         # => "Transitioning to locked state"
puts t.state   # => "locked"
```

**Explicação**:

1. `state_machine initial: :locked` define o estado inicial.
2. `event :coin` e `:push` configuram transições de estados.
3. `state :locked` e `:unlocked` permitem hooks como `before_transition` para executar código.
4. Chamadas `t.coin` e `t.push` acionam transições e ações associadas.

---

## 7. Verificação e Testes

* **Cobertura** de transições e estados através de testes unitários.
* **Model Checking**: usar SPIN, NuSMV para autômatos formais.
* **Test Driven Design**: definir testes de comportamento antes da implementação.

---

## 8. Padrões de Projeto Relacionados

* **State Pattern**: encapsula comportamentos em classes por estado, permitindo mudança de comportamento em tempo de execução.
* **Strategy Pattern**: similar ao State, mas foca seleção de algoritmo.

---

## 9. Boas Práticas

1. **Manter FSM Simples**: use hierarquia para modularizar.
2. **Documentar Visualmente**: diagramas UML e statecharts.
3. **Modularizar Implementação**: separar definição de máquina do domínio de aplicação.
4. **Definir Ações de Erro**: transições dedicadas para estados de falha.
5. **Monitorar Transições**: logs e métricas para diagnóstico.

---

## Conclusão

Máquinas de estado são fundamentais para modelar lógica de controle em sistemas reativos, oferecendo clareza e previsibilidade. Utilizando autômatos, statecharts e implementações em linguagens como Ruby, Python e JavaScript, você pode construir sistemas escaláveis, testáveis e confiáveis.
