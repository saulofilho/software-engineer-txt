### **Adição de elementos**

- `push(obj)` → Adiciona um elemento ao final do array.
- `<< obj` → Atalho para `push`.
- `unshift(obj)` → Adiciona um elemento no início do array.
- `insert(index, obj)` → Insere um elemento em uma posição específica.

### **Remoção de elementos**

- `pop` → Remove e retorna o último elemento do array.
- `shift` → Remove e retorna o primeiro elemento do array.
- `delete(obj)` → Remove todas as ocorrências de um objeto.
- `delete_at(index)` → Remove o elemento no índice especificado.
- `compact` → Remove valores `nil` (não modifica o original).
- `compact!` → Remove `nil` diretamente no array original.

### **Consulta e acesso**

- `first` → Retorna o primeiro elemento.
- `last` → Retorna o último elemento.
- `at(index)` → Retorna o elemento no índice especificado.
- `fetch(index, default)` → Retorna o valor no índice, ou um valor padrão se não existir.
- `include?(obj)` → Verifica se o array contém o objeto.
- `index(obj)` → Retorna o índice do primeiro elemento igual ao `obj`.
- `rindex(obj)` → Retorna o índice da última ocorrência do `obj`.

### **Iteração e manipulação**

- `each { |el| bloco }` → Itera sobre os elementos do array.
- `map { |el| bloco }` → Retorna um novo array com os elementos transformados.
- `map! { |el| bloco }` → Modifica o próprio array.
- `select { |el| bloco }` → Retorna um novo array com os elementos que atendem à condição.
- `reject { |el| bloco }` → Retorna um array sem os elementos que atendem à condição.
- `reduce { |memo, el| bloco }` → Acumula um valor aplicando uma operação em sequência.

### **Ordenação e modificação**

- `sort` → Retorna um novo array ordenado.
- `sort!` → Ordena o array original.
- `reverse` → Retorna um novo array com a ordem invertida.
- `reverse!` → Inverte a ordem do próprio array.
- `uniq` → Remove elementos duplicados sem modificar o original.
- `uniq!` → Remove duplicatas no array original.

### **Conversões e manipulação de conteúdo**

- `join(separador)` → Converte o array em string, separando por `separador`.
- `split(separador)` → Transforma uma string em array.
- `flatten` → Achata arrays aninhados em um só nível.
- `flatten!` → Modifica o array original para ser achatado.
- `zip(outro_array)` → Junta dois arrays em pares.

### **Operações matemáticas e de agregação**

- `sum` → Soma os elementos do array.
- `min` → Retorna o menor valor.
- `max` → Retorna o maior valor.
- `count(obj)` → Conta quantas vezes o objeto aparece.