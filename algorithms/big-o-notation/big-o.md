# Guia Completo de Notação Big O

Este guia aborda, em nível avançado, a notação Big O e outras notações assintóticas, incluindo definições formais, classes de complexidade, técnicas de análise e exemplos práticos.

---

## 1. Introdução a Análise de Algoritmos

* **Objetivo**: medir o crescimento do tempo de execução ou do uso de memória de um algoritmo em função do tamanho da entrada (n).
* **Métricas comuns**:

  * **Tempo**: número de operações elementares.
  * **Espaço**: quantidade de memória adicional.

---

## 2. Notações Assintóticas

| Notação     | Definição Formal                                         | Interpretação                          |
| ----------- | -------------------------------------------------------- | -------------------------------------- |
| **O(g(n))** | f(n) = O(g(n)) se ∃c>0 e n₀ tal que ∀n≥n₀, f(n) ≤ c·g(n) | Limite superior assintótico            |
| **Ω(g(n))** | f(n) = Ω(g(n)) se ∃c>0 e n₀ tal que ∀n≥n₀, f(n) ≥ c·g(n) | Limite inferior assintótico            |
| **Θ(g(n))** | f(n) = Θ(g(n)) se f(n) = O(g(n)) e f(n) = Ω(g(n))        | Limite superior e inferior simultâneos |
| **o(g(n))** | f(n) = o(g(n)) se ∀c>0 ∃n₀ tal que ∀n≥n₀, f(n) < c·g(n)  | Crescimento estritamente menor         |
| **ω(g(n))** | f(n) = ω(g(n)) se ∀c>0 ∃n₀ tal que ∀n≥n₀, f(n) > c·g(n)  | Crescimento estritamente maior         |

---

## 3. Classes de Complexidade Comuns

| Classe         | Crescimento  | Exemplos de Algoritmos                      |
| -------------- | ------------ | ------------------------------------------- |
| **O(1)**       | Constante    | Acesso a array, operações aritméticas       |
| **O(log n)**   | Logarítmica  | Busca binária, operações em heaps           |
| **O(n)**       | Linear       | Busca sequencial, enumeração de listas      |
| **O(n log n)** | Linearítmica | Merge Sort, Quick Sort (média), Heap Sort   |
| **O(n²)**      | Quadrática   | Bubble Sort, Insertion Sort, Selection Sort |
| **O(n³)**      | Cúbica       | Floyd-Warshall                              |
| **O(2ⁿ)**      | Exponencial  | Subconjuntos, Fibonacci recursivo           |
| **O(n!)**      | Fatorial     | Permutações completas                       |

---

## 4. Técnicas de Análise

### 4.1 Análise de Loops

* **Loops simples**: `for i in 1..n` → O(n).
* **Loops aninhados**: `for i in 1..n { for j in 1..n }` → O(n²).

### 4.2 Recorrências e Master Theorem

* Recorrência genérica: T(n) = a·T(n/b) + f(n).
* **Master Theorem**:

  1. Se f(n) = O(n^{log\_b a - ε}), então T(n) = Θ(n^{log\_b a}).
  2. Se f(n) = Θ(n^{log\_b a}·log^k n), então T(n) = Θ(n^{log\_b a}·log^{k+1} n).
  3. Se f(n) = Ω(n^{log\_b a + ε}) e regularidade, então T(n) = Θ(f(n)).

### 4.3 Análise Amortizada

* Custos dispersos ao longo de várias operações: p.ex., expansão de vetor dinâmico.
* **Métodos**: agregação, contabilidade, potencial.

### 4.4 Melhor, Médio e Pior Caso

* **Pior caso (worst-case)**: limite superior garantido.
* **Melhor caso (best-case)**: limite inferior trivial.
* **Caso médio (average-case)**: análise probabilística, assume distribuição de entradas.

---

## 5. Espaço de Complexidade

* **Espaço Extra**: memória adicional além da entrada.
* Exemplos:

  * Algoritmo in-place: O(1).
  * Merge Sort: O(n) espaço adicional.

---

## 6. Exemplo de Análise Detalhada

```python
def example(arr):
    n = len(arr)
    for i in range(n):               # O(n)
        j = 1
        while j < n:                 # O(log n) em potências de 2
            j *= 2
    return arr[0]                   # O(1)
```

* Loop externo: O(n).
* Loop interno: j dobra, executa \~log₂n vezes.
* Total: O(n·log n).

---

## 7. Complexidade em Estruturas de Dados

| Estrutura       | Acesso    | Busca     | Inserção  | Remoção             |
| --------------- | --------- | --------- | --------- | ------------------- |
| Array           | O(1)      | O(n)      | O(n)      | O(n)                |
| Lista Encadeada | O(n)      | O(n)      | O(1)      | O(1) (nó conhecido) |
| Stack/Queue     | O(1)      | O(n)      | O(1)      | O(1)                |
| Hash Table      | O(1) avg. | O(1) avg. | O(1) avg. | O(1) avg.           |
| BST Balanceada  | O(log n)  | O(log n)  | O(log n)  | O(log n)            |
| Heap            | O(1)      | O(n)      | O(log n)  | O(log n)            |

---

## 8. Notações Relacionadas

* **Big Θ**: limite tempo de execução “teto” e “piso”.
* **Big Ω**: limite inferior.
* **Little o** e **ω**: crescimento estritamente menor/maior.

---

## 9. Dicas de Aprimoramento

1. **Simplificar expressões**: descartar termos de menor ordem e constantes.
2. **Comparar algoritmos** no mesmo domínio de entrada.
3. **Testar em grandes n** para observar comportamento prático.
4. **Profiling**: identificar gargalos reais, não apenas teóricos.

---

## Conclusão

A notação Big O é fundamental para entender a escalabilidade e performance de algoritmos. Combinando análise assintótica com testes práticos e profiling, é possível escolher e otimizar soluções eficientes para diferentes problemas.
