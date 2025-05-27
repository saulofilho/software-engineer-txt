# Guia de Deadlocks em TI (Interbloqueio)

Este guia apresenta de forma avançada o conceito de *deadlock* (interbloqueio) em sistemas computacionais, cobrindo definição, condições, modelagem, detecção, prevenção, evitação, recuperação e exemplos práticos.

---

## 1. Definição

*Deadlock* é uma situação em que dois ou mais processos ou threads ficam indefinidamente bloqueados, cada um aguardando que outro libere um recurso que necessita, sem possibilidade de prosseguir.

## 2. Condições Necessárias (Condições de Coffman)

Para que ocorra *deadlock*, é preciso que simultaneamente existam estas quatro condições:

1. **Exclusão Mútua**: o recurso não pode ser compartilhado; apenas um processo por vez o utiliza.
2. **Posse e Espera (Hold and Wait)**: processos seguram recursos já alocados enquanto solicitam novos recursos.
3. **Sem Preempção**: recursos não podem ser retirados de um processo; só são liberados voluntariamente.
4. **Espera Circular**: existe um ciclo de processos $P₀, P₁, …, Pₙ$ tal que $Pᵢ$ aguarda recurso detido por $Pᵢ₊₁$, e $Pₙ$ aguarda recurso de $P₀$.

---

## 3. Modelagem com Grafos de Alocação de Recursos

* **Grafos de Recursos**: vértices representam processos (círculos) e recursos (quadrados).
* **Arestas**: de processo → recurso (pedido) e recurso → processo (alocado).
* **Deadlock** detectado se existir ciclo no grafo.

```text
draw.io: [P0] -> [R1]
[R1] -> [P1]
[P1] -> [R2]
[R2] -> [P0]  <-- ciclo, deadlock
```

---

## 4. Detecção de Deadlocks

### 4.1 Em Sistemas Operacionais

* **Algoritmo do Bancário (banker's)**: também detecta estados seguros/inseguros.
* **Grafo de Espera (Wait-for Graph)**: simplificação do grafo de recursos; arestas diretas entre processos.
* **Análise Periódica**: o SO verifica grafo e identifica ciclos.

### 4.2 Em Bancos de Dados

* **Tabela de Locks**: lock table mantém quem detém e quem aguarda; busca ciclo.
* Ferramentas monitoram transações bloqueadas (e.g., Oracle v\$lock, SQL Server sp\_lock).

---

## 5. Prevenção de Deadlocks

Quebrar pelo menos uma condição de Coffman:

1. **Negar Exclusão Mútua**: nem sempre viável (recursos não compartilháveis).
2. **Evitar Posse e Espera**: requer que processos solicitem *todos* recursos de uma vez.
3. **Permitir Preempção**: forçar retirada de recurso de processo, abortando ou revertendo.
4. **Evitar Espera Circular**: impor ordem total nos recursos e só solicitar em ordem crescente.

---

## 6. Evitação de Deadlocks: Algoritmo do Banqueiro

* Mantém monitoramento de **estado seguro**: existe sequência de execução que satisfaz demandas.
* Dados:

  * `Available[R]`: quantidade disponível de cada recurso.
  * `Max[P][R]`: demanda máxima de cada processo.
  * `Allocation[P][R]`: recursos atualmente alocados.
  * `Need[P][R] = Max[P][R] - Allocation[P][R]`.
* **Teste de Segurança**: simular concessão e verificar se todos podem finalizar.

---

## 7. Recuperação de Deadlocks

* **Abortar Processo**: escolher e encerrar processo(s) envolvidos no ciclo.
* **Preempção de Recursos**: retirar (rollback) recursos de processos e reiniciar.
* **Tratamento de Timeout**: abortar após período de espera.

---

## 8. Exemplos Práticos

### 8.1 Em Java (Threads)

```java
Object resourceA = new Object();
Object resourceB = new Object();

// Thread 1 tenta A então B
new Thread(() -> {
    synchronized(resourceA) {
        sleep(100); // garante sequência
        synchronized(resourceB) {
            // faz algo
        }
    }
}).start();

// Thread 2 tenta B então A
new Thread(() -> {
    synchronized(resourceB) {
        sleep(100);
        synchronized(resourceA) {
            // faz algo
        }
    }
}).start();
// Possível deadlock se ambos adquirem o primeiro lock simultaneamente
```

### 8.2 Em Banco de Dados (SQL)

```sql
-- Transação T1
BEGIN;
SELECT * FROM contas WHERE id=1 FOR UPDATE;  -- lock exclusivo em conta 1
-- ...
SELECT * FROM contas WHERE id=2 FOR UPDATE;  -- bloqueia espera por conta 2

-- Transação T2 (concorrente)
BEGIN;
SELECT * FROM contas WHERE id=2 FOR UPDATE;  -- lock em conta 2
-- ...
SELECT * FROM contas WHERE id=1 FOR UPDATE;  -- deadlock!
```

---

## 9. Ferramentas de Monitoramento

* **Linux**: `lsof`, `ps -eo state,pid,ppid,cmd`, `pstree`.
* **Java**: `jstack` e análise de *thread dump*.
* **DB**: `SHOW ENGINE INNODB STATUS;` (MySQL), `v$lock` (Oracle).

---

## 10. Conclusão

Deadlock é um problema crítico em sistemas concorrentes e distribuídos. A compreensão profunda de suas condições, técnicas de prevenção, evitação, detecção e recuperação é essencial para projetar software robusto e sistemas confiáveis.
