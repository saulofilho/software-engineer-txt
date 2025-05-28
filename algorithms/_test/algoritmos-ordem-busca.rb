# Ordenação e Busca em Ruby

# Bubble Sort
# Percorre o array várias vezes, trocando elementos adjacentes fora de ordem.
# Complexidade: O(n²)
def bubble_sort(arr)
  a = arr.dup
  n = a.size
  n.times do |i|
    (0...n - i - 1).each do |j|
      if a[j] > a[j + 1]
        a[j], a[j + 1] = a[j + 1], a[j]
      end
    end
  end
  a
end

# Selection Sort
# Em cada iteração, seleciona o menor elemento do restante e o coloca na posição correta.
# Complexidade: O(n²)
def selection_sort(arr)
  a = arr.dup
  n = a.size
  (0...n).each do |i|
    min_idx = i
    ((i + 1)...n).each do |j|
      min_idx = j if a[j] < a[min_idx]
    end
    a[i], a[min_idx] = a[min_idx], a[i]
  end
  a
end

# Insertion Sort
# Constrói o array ordenado inserindo cada elemento na posição correta.
# Complexidade: O(n²) (ótimo O(n) se quase ordenado)
def insertion_sort(arr)
  a = arr.dup
  (1...a.size).each do |i|
    key = a[i]
    j = i - 1
    while j >= 0 && a[j] > key
      a[j + 1] = a[j]
      j -= 1
    end
    a[j + 1] = key
  end
  a
end

# Merge Sort
# Divide e conquista: divide o array, ordena cada metade e intercala.
# Complexidade: O(n log n)
def merge_sort(arr)
  return arr.dup if arr.size <= 1

  mid = arr.size / 2
  left  = merge_sort(arr[0...mid])
  right = merge_sort(arr[mid..-1])

  merged = []
  until left.empty? || right.empty?
    if left.first <= right.first
      merged << left.shift
    else
      merged << right.shift
    end
  end
  merged + left + right
end

# Quick Sort
# Escolhe um pivô e particiona em menores e maiores, então ordena recursivamente.
# Complexidade média: O(n log n), pior caso O(n²)
def quick_sort(arr)
  return arr.dup if arr.size <= 1

  pivot = arr[arr.size / 2]
  left  = arr.select { |x| x < pivot }
  mid   = arr.select { |x| x == pivot }
  right = arr.select { |x| x > pivot }

  quick_sort(left) + mid + quick_sort(right)
end

# Counting Sort
# Para inteiros no intervalo [0..k], conta ocorrências e reconstrói o array.
# Complexidade: O(n + k)
def counting_sort(arr, k)
  count = Array.new(k + 1, 0)
  arr.each { |x| count[x] += 1 }

  res = []
  count.each_with_index do |freq, val|
    freq.times { res << val }
  end
  res
end

# Radix Sort (base 10)
# Ordena por dígitos, usando Counting Sort como sub-rotina estável.
# Complexidade: O(d·(n + b)), d = dígitos, b = base
def radix_sort(arr)
  return [] if arr.empty?

  max_val = arr.max
  exp = 1
  res = arr.dup

  while max_val / exp > 0
    # Counting sort por dígito
    count = Array.new(10, 0)
    output = Array.new(res.size)

    res.each do |num|
      digit = (num / exp) % 10
      count[digit] += 1
    end
    (1...10).each { |i| count[i] += count[i - 1] }

    res.reverse_each do |num|
      digit = (num / exp) % 10
      count[digit] -= 1
      output[count[digit]] = num
    end

    res = output
    exp *= 10
  end

  res
end

# Bucket Sort
# Distribui em buckets, ordena cada um com Insertion Sort e concatena.
# Complexidade média: O(n + k)
def bucket_sort(arr, bucket_count = 10)
  buckets = Array.new(bucket_count) { [] }
  arr.each do |x|
    idx = [(x * bucket_count).to_i, bucket_count - 1].min
    buckets[idx] << x
  end

  res = []
  buckets.each do |bucket|
    # Reuso de insertion_sort
    bucket = insertion_sort(bucket)
    res.concat(bucket)
  end
  res
end

# Binary Search
# Retorna índice de `target` em `arr` (assumido ordenado) ou -1 se não existe.
# Complexidade: O(log n)
def binary_search(arr, target)
  lo = 0
  hi = arr.size - 1
  while lo <= hi
    mid = (lo + hi) / 2
    if arr[mid] == target
      return mid
    elsif arr[mid] < target
      lo = mid + 1
    else
      hi = mid - 1
    end
  end
  -1
end

# Busca do primeiro elemento igual a target
def find_first(arr, target)
  lo = 0
  hi = arr.size - 1
  res = -1
  while lo <= hi
    mid = (lo + hi) / 2
    if arr[mid] == target
      res = mid
      hi = mid - 1
    elsif arr[mid] < target
      lo = mid + 1
    else
      hi = mid - 1
    end
  end
  res
end

# Busca do último elemento igual a target
def find_last(arr, target)
  lo = 0
  hi = arr.size - 1
  res = -1
  while lo <= hi
    mid = (lo + hi) / 2
    if arr[mid] == target
      res = mid
      lo = mid + 1
    elsif arr[mid] < target
      lo = mid + 1
    else
      hi = mid - 1
    end
  end
  res
end

# Busca em matriz ordenada
# Matriz onde cada linha é ordenada e o 1º elemento de cada linha >
# último da linha anterior.
# Usa busca binária considerando o array concatenado.
def search_matrix(matrix, target)
  return false if matrix.empty? || matrix.first.empty?
  rows = matrix.size
  cols = matrix.first.size
  lo = 0
  hi = rows * cols - 1

  while lo <= hi
    mid = (lo + hi) / 2
    r, c = mid.divmod(cols)
    val = matrix[r][c]
    if val == target
      return true
    elsif val < target
      lo = mid + 1
    else
      hi = mid - 1
    end
  end

  false
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  p bubble_sort([5,1,4,2,8])              # => [1,2,4,5,8]
  p selection_sort([64,25,12,22,11])      # => [11,12,22,25,64]
  p insertion_sort([12,11,13,5,6])        # => [5,6,11,12,13]
  p merge_sort([38,27,43,3,9,82,10])      # => [3,9,10,27,38,43,82]
  p quick_sort([3,6,8,10,1,2,1])          # => [1,1,2,3,6,8,10]
  p counting_sort([1,4,1,2,7,5,2], 7)     # => [1,1,2,2,4,5,7]
  p radix_sort([170,45,75,90,802,24,2,66])
  p bucket_sort([0.897,0.565,0.656,0.1234,0.665,0.3434])
  p binary_search([1,2,3,4,5,6], 4)       # => 3
  p binary_search([1,2,3,4,5,6], 7)       # => -1
  arr = [1,2,2,2,3,4]
  p find_first(arr, 2), find_last(arr, 2) # => 1, 3
  mat = [
    [1,3,5,7],
    [10,11,16,20],
    [23,30,34,60]
  ]
  p search_matrix(mat, 3)                 # => true
  p search_matrix(mat, 13)                # => false
end
