# Guia Completo de Paralelismo em Computação

Este guia aborda conceitos, arquiteturas, técnicas e ferramentas de paralelismo em sistemas computacionais. Inclui teoria, padrões de projeto paralelo, exemplos práticos e boas práticas.

---

## 1. Concorrência vs. Paralelismo

* **Concorrência**: vários fluxos de execução progridem em intervalos de tempo compartilhados (time-slicing).
* **Paralelismo**: execução simultânea de múltiplas tarefas em diferentes núcleos/processadores.

|              | Concorrência                  | Paralelismo                                      |
| ------------ | ----------------------------- | ------------------------------------------------ |
| Objetivo     | Gerenciar múltiplas tarefas   | Acelerar processamento dividindo carga           |
| Escala       | 1 CPU, múltiplas tarefas      | Múltiplas CPUs/cores                             |
| Complexidade | Context switch, sincronização | Balanceamento de carga, latência de interconexão |

---

## 2. Arquiteturas de Executores Paralelos

1. **Memória Compartilhada** (shared-memory): threads dentro de um mesmo processo acessam memória comum (C/C++ threads, OpenMP, TPL).
2. **Memória Distribuída** (distributed-memory): múltiplos nós comunicam-se via mensagens (MPI, clusters).
3. **Arquiteturas Híbridas**: combinações de shared e distributed (MPI+OpenMP).
4. **SIMD / SIMT**: vetorização de dados (Intel AVX, GPU CUDA).

---

## 3. Modelos de Programação

### 3.1 Threads e Processos

* **Processos**: isolamento de espaço de endereçamento; comunicação via IPC.
* **Threads**: leve, compartilham heap; requer sincronização.

### 3.2 Tasks e Coroutines

* **Task-based**: abstração de trabalho assíncrono (TPL .NET, Java `CompletableFuture`, C++ `std::async`).
* **Coroutines**: unidades cooperativas de execução (Go routines, Python async/await).

### 3.3 Message-Passing

* **MPI**: padrão para HPC em C/C++/Fortran.
* **Actor Model**: Erlang, Akka Java/Scala; mensagens assíncronas entre atores.

### 3.4 Vetorização de Dados

* **SIMD**: instruções vetoriais em CPU (SSE/AVX).
* **SIMT**: Single Instruction Multiple Threads em GPUs (CUDA, OpenCL).

---

## 4. Leis de Escalabilidade

### 4.1 Lei de Amdahl

Estimativa de ganho máximo:

```
Speedup = 1 / ( (1 - P) + P / N )
```

* P = fração paralelizável, N = número de núcleos.

### 4.2 Lei de Gustafson

Considera aumento de carga de trabalho:

```
Speedup = N - (1 - P) * (N - 1)
```

---

## 5. Padrões de Paralelismo

### 5.1 Fork–Join

Divide problema em subtarefas recursivas e combina resultados.

```csharp
// C# TPL
int Sum(int[] data) {
  return Parallel.For(0, data.Length, () => 0,
    (i, loop, subtotal) => subtotal + data[i],
    subtotal => Interlocked.Add(ref result, subtotal)
  );
}
```

### 5.2 Map-Reduce

Map aplica função a dados, Reduce agrega resultados.

```python
# Python multiprocessing
from multiprocessing import Pool

def square(x): return x*x
with Pool(4) as p:
    squares = p.map(square, range(1000))
```

### 5.3 Pipeline

Sequência de estágios independentes conectados por filas.

### 5.4 SPMD (Single Program, Multiple Data)

Mesmo programa executa em múltiplos nós com dados particionados.

---

## 6. Ferramentas e Frameworks

| Tecnologia             | Modelo          | Linguagens                          |
| ---------------------- | --------------- | ----------------------------------- |
| OpenMP                 | Diretivas       | C/C++, Fortran                      |
| MPI                    | Message-passing | C/C++, Fortran, Python via wrappers |
| Intel TBB              | Task-based      | C++                                 |
| .NET TPL               | Task-based      | C#                                  |
| Java Fork/Join         | Task-based      | Java                                |
| Python threading       | Threads (GIL)   | Python                              |
| Python multiprocessing | Processes       | Python                              |
| CUDA / OpenCL          | SIMT            | C/C++, Python                       |
| Akka                   | Actor           | Java/Scala                          |

---

## 7. Sincronização e Consistência

* **Mutex / Lock**: exclusão mútua.
* **Semaphore**: contador de acessos.
* **Barrier**: sincroniza fases.
* **Atomic**: operações indivisíveis (C++ `std::atomic`, Java `AtomicInteger`).
* **Memory Model**: regras de visibilidade de memória (C++11, Java Memory Model).

---

## 8. Considerações de Desempenho

1. **Granularidade**: tarefas muito pequenas criam overhead de scheduling.
2. **Balanceamento de Carga**: evite hotspots; use work-stealing.
3. **Localidade de Dados**: minimize cache misses e comunicação remota (NUMA).
4. **False Sharing**: variáveis independentes compartilhando cache line provocam invalidações.

---

## 9. Exemplos Práticos

### 9.1 C++ com OpenMP

```cpp
#include <omp.h>
int main(){
  #pragma omp parallel for reduction(+:sum)
  for(int i=0; i<1000000; ++i) sum += i;
}
```

### 9.2 C# com Parallel.For

```csharp
int sum = 0;
Parallel.For(0, data.Length, i => {
  Interlocked.Add(ref sum, data[i]);
});
```

### 9.3 Java Streams Paralelos

```java
long count = list.parallelStream()
  .filter(x -> x % 2 == 0)
  .count();
```

---

## 10. Erros Comuns e Como Evitar

* **Race Conditions**: proteger seções críticas.
* **Deadlocks**: evitar ordem circular de locks.
* **Starvation**: garantir justa distribuição de recursos.
* **Oversubscription**: criar mais threads/cores que disponível.

---

## 11. Profiling e Debugging

* **Perf**, **VTune**, **gprof** para CPU.
* **Thread Sanitizer**, **Helgrind** para detectar data races.
* Logs de tempo e contadores de eventos (hardware counters).

---

## Conclusão

Paralelismo é essencial para aproveitar arquiteturas modernas multicore e distribuídas. Compreender modelo, overhead, padrões e ferramentas é crucial para escrever código paralelo correto e performático.
