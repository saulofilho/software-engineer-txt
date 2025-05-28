# Algoritmos Populares para Entrevistas de System Design

Este guia apresenta 12 algoritmos e estruturas de dados amplamente cobrados em entrevistas de System Design, com descrição, funcionamento, complexidade e casos de uso.

---

## 1. Bloom Filter

**O que é:** Estrutura probabilística para testar se um elemento pertence a um conjunto, permitindo falsos positivos mas nunca falsos negativos.

**Como funciona:**

1. Um array de bits `m` inicializado a 0.
2. `k` funções de hash independentes.
3. Ao inserir um item, calcula-se cada hash e seta-se o bit correspondente.
4. Ao consultar, verifica-se se todos os `k` bits estão 1; se algum for 0, o item não está no conjunto.

**Complexidade:**

* Inserção/consulta: O(k) hashes.
* Espaço: O(m).

**Casos de uso:**

* Cache pré-verificação antes de operações de disco ou rede (por ex., verificar URLs).
* Filtros de spam, sistemas de recomendação.

---

## 2. Geohash

**O que é:** Codificação de coordenadas geográficas em strings base-32, facilitando indexação e consulta espacial.

**Como funciona:**

1. Intercala bits de latitude e longitude.
2. Divide recursivamente o espaço em retângulos.
3. Cada caractere da string reduz a área de busca.

**Complexidade:**

* Cálculo: O(precision) operações bitwise.
* Pesquisa de vizinhança: consultas prefix-based em trie ou B-tree.

**Casos de uso:**

* Bancos de dados geoespaciais para consultas de proximidade.
* Armazenamento em key-value stores para geocoding.

---

## 3. HyperLogLog

**O que é:** Algoritmo para estimar cardinalidade (número de elementos distintos) de grandes volumes de dados com alta precisão e baixo uso de memória.

**Como funciona:**

1. Hash uniforme de cada elemento.
2. Divide o hash em `p` bits de prefixo (escolhe registrador) e restante para contagem de zeros à esquerda.
3. Mantém máximo de zeros em cada registrador e aplica média harmônica.

**Complexidade:**

* Inserção: O(1).
* Espaço: O(2^p) registradores (\~kilobytes).

**Casos de uso:**

* Contagem de visitantes únicos, consultas de big data em tempo real.

---

## 4. Consistent Hashing

**O que é:** Técnica de balanceamento que minimiza realocações de chaves quando nodos são adicionados/remoção.

**Como funciona:**

1. Usa um círculo hash (0..2^32−1).
2. Mapeia nós e chaves no círculo via hash.
3. Cada chave é atribuída ao próximo nó no sentido horário.

**Complexidade:**

* Inserção/remoção de nó: O(log N) com árvore balanceada.
* Lookup de chave: O(log N) ou O(1) com hash ring e tabela.

**Casos de uso:**

* Sharding de caches distribuídos (Memcached), sistemas de armazenamento.

---

## 5. Merkle Tree

**O que é:** Árvore binária de hashes que permite verificação eficiente de integridade de grandes conjuntos de dados.

**Como funciona:**

1. Folhas contêm hashes de blocos de dados.
2. Cada nó pai armazena hash concatenado de filhos.
3. Raiz (root hash) representa todo o dataset.

**Complexidade:**

* Construção: O(n).
* Verificação de prova (Merkle proof): O(log n).

**Casos de uso:**

* Blockchain (Bitcoin, Ethereum) para validação de transações.
* Sistemas de replicação de dados.

---

## 6. Raft Algorithm

**O que é:** Algoritmo de consenso para replicar logs de forma segura em clusters distribuídos.

**Como funciona:**

1. Eleição de líder via timeout randômico.
2. Líder recebe comandos e replica logs para seguidores.
3. Comando é aplicado quando commit index atinge maioria.

**Complexidade:**

* Latência de consenso: O(f + 1) RTTs, onde f é número de falhas toleradas.

**Casos de uso:**

* Sistemas de armazenamento distribuído (etcd, Consul).
* Bancos de dados replicados.

---

## 7. Lossy Counting

**O que é:** Algoritmo para identificar itens frequentes em streams de dados usando memória limitada.

**Como funciona:**

1. Define parâmetro ε (erro tolerado).
2. Stream dividido em buckets de largura ⌈1/ε⌉.
3. Mantém contador estimado e erro para cada item.
4. A cada bucket, elimina itens cujo contador + erro ≤ bucket atual.

**Complexidade:**

* Espaço: O(1/ε).
* Atualização por item: O(1)

**Casos de uso:**

* Monitoramento de heavy hitters em logs, análise de tráfego.

---

## 8. QuadTree

**O que é:** Estrutura de dados de particionamento espacial que divide recursivamente o espaço em quatro quadrantes.

**Como funciona:**

1. Cada nó representa uma região retangular.
2. Se a capacidade (pontos) excede limite, subdivide em 4 filhos.
3. Busca e inserção descem até o quadrante apropriado.

**Complexidade:**

* Inserção/consulta: O(log n) em distribuição uniforme.
* Espaço: O(n).

**Casos de uso:**

* Indexação geoespacial, colisão em jogos, visibilidade em renderização.

---

## 9. Operational Transformation

**O que é:** Técnica para manter consistência em edição colaborativa em tempo real (Google Docs).

**Como funciona:**

1. Cada operação recebe timestamp/ID de cliente.
2. Operações concorrentes são transformadas umas pelas outras antes de aplicação.
3. Garantia de convergência: resultado idêntico em todos os clientes.

**Complexidade:**

* Aplicação por operação: O(k) onde k é número de operações concorrentes ativas.

**Casos de uso:**

* Editores colaborativos, CRDTs (Conflict-free Replicated Data Types).

---

## 10. Leaky Bucket

**O que é:** Algoritmo de rate limiting que controla fluxo de requisições com buffer e vazão constante.

**Como funciona:**

1. Requisições entram em um buffer (tanque).
2. Líquido (tokens) vazam a uma taxa fixa.
3. Se buffer cheio, novas requisições são rejeitadas ou bloqueadas.

**Complexidade:**

* Inserção: O(1).
* Espaço: O(capacidade do bucket).

**Casos de uso:**

* Proteção de APIs, controle de tráfego de rede.

---

## 11. Rsync Algorithm

**O que é:** Algoritmo para sincronização eficiente de arquivos, transferindo apenas diferenças.

**Como funciona:**

1. Divide arquivo em blocos e calcula checksums (rolling hash + hash forte).
2. Remoto compara checksums para identificar blocos alterados.
3. Transfere apenas blocos diferentes e aplica patch.

**Complexidade:**

* Tempo: O(n + D) onde D é tamanho delta.
* Espaço: O(n) checksums.

**Casos de uso:**

* Ferramentas de backup e sincronização (rsync, Dropbox internals).

---

## 12. Ray Casting

**O que é:** Algoritmo para detectar se um ponto está dentro de um polígono, usado em gráficos e geoprocessamento.

**Como funciona:**

1. Traça um raio horizontal desde o ponto.
2. Conta quantas vezes o raio intersecta arestas do polígono.
3. Se o número de interseções for ímpar, o ponto está dentro; se par, fora.

**Complexidade:**

* Tempo: O(n) onde n é número de vértices do polígono.

**Casos de uso:**

* Sistemas GIS, colisões em jogos, testes de inclusão espacial.

---

## Conclusão

Estes algoritmos e estruturas são fundamentais para projetar sistemas escaláveis, eficientes e resilientes. Estude implementações, variações e trade-offs de cada um para entrevistas de System Design e produção em larga escala.
