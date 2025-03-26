O **Redis** (Remote Dictionary Server) é um banco de dados NoSQL baseado em chave-valor, altamente performático, que armazena dados na memória RAM. Ele é frequentemente utilizado como **cache**, **fila de mensagens**, **contador**, **armazenamento de sessões** e até mesmo como banco de dados primário para determinadas aplicações.

## **Principais Características do Redis**

1. **Armazenamento em Memória**
    - Diferente de bancos relacionais (como MySQL e PostgreSQL), o Redis mantém os dados na memória RAM, o que torna as operações extremamente rápidas.
2. **Modelo Chave-Valor**
    - Os dados são armazenados como pares `chave: valor`, similar a um dicionário em Python ou um objeto em JavaScript.
3. **Tipos de Dados**
    - Além de strings simples, o Redis suporta listas, conjuntos, hashes, conjuntos ordenados e até estruturas mais avançadas como **HyperLogLogs** e **Streams**.
4. **Persistência Opcional**
    - Embora funcione na memória, o Redis pode salvar dados no disco periodicamente (AOF e RDB) para evitar perda de informações em caso de reinício do servidor.
5. **Alta Disponibilidade e Escalabilidade**
    - Suporte a replicação mestre-escravo, clusterização e **sentinels** para garantir alta disponibilidade e balanceamento de carga.
6. **Operações Atômicas**
    - Todas as operações no Redis são atômicas, garantindo consistência ao lidar com concorrência.

## **Casos de Uso do Redis**

- **Cache de páginas ou objetos** (reduz a carga em bancos tradicionais)
- **Armazenamento de sessões de usuários**
- **Filas e mensageria** (exemplo: implementação de filas com listas ou streams)
- **Contadores e rankings** (exemplo: sistemas de likes ou upvotes)
- **Rate Limiting** (limitação de requisições por segundo)

## **Exemplo de Uso**