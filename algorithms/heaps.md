Heaps (ou heaps binários) são estruturas de dados baseadas em árvores binárias que satisfazem uma propriedade específica chamada propriedade do heap. Eles são comumente usados para implementar filas de prioridade e algoritmos como o heapsort.

Tipos de heaps
Max-heap:
- A chave de cada nó é maior ou igual às chaves dos seus filhos.
- O maior valor está sempre na raiz da árvore.

Min-heap:
- A chave de cada nó é menor ou igual às chaves dos seus filhos.
- O menor valor está na raiz.

```python
       2
     /   \
    4     5
   / \   /
  10  8  15

```

Propriedades
- A estrutura é completa, ou seja, todos os níveis estão preenchidos, exceto talvez o último, que é preenchido da esquerda para a direita.

- Pode ser implementado de forma eficiente usando vetores/arrays, o que facilita a navegação entre pais e filhos:

- Pai de i: ⌊(i - 1) / 2⌋
- Filho esquerdo de i: 2i + 1
- Filho direito de i: 2i + 2

Operações comuns

| Operação       | Complexidade |
| -------------- | ------------ |
| Inserir        | O(log n)     |
| Remover raiz   | O(log n)     |
| Obter raiz     | O(1)         |
| Construir heap | O(n)         |

Aplicações
- Filas de prioridade
- Algoritmo de Dijkstra (caminho mais curto)
- Heapsort
- Agendamento de tarefas
