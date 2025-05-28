# Binary Search em Resposta (Parametric Search) em Ruby

# 1. Alocação de Páginas (min_max_pages)
def min_max_pages(pages, students)
  # Verifica se conseguimos alocar com carga máxima max_load
  can_allocate = lambda do |max_load|
    required = 1
    current  = 0
    pages.each do |p|
      return false if p > max_load
      if current + p <= max_load
        current += p
      else
        required += 1
        current = p
        return false if required > students
      end
    end
    true
  end

  lo = pages.max
  hi = pages.sum
  answer = hi

  while lo <= hi
    mid = (lo + hi) / 2
    if can_allocate.call(mid)
      answer = mid
      hi = mid - 1
    else
      lo = mid + 1
    end
  end

  answer
end

# 2. Capacidade de Navio (ship_capacity)
def ship_capacity(weights, days)
  can_ship = lambda do |cap|
    required_days = 1
    current       = 0
    weights.each do |w|
      return false if w > cap
      if current + w <= cap
        current += w
      else
        required_days += 1
        current = w
        return false if required_days > days
      end
    end
    true
  end

  lo = weights.max
  hi = weights.sum
  answer = hi

  while lo <= hi
    mid = (lo + hi) / 2
    if can_ship.call(mid)
      answer = mid
      hi = mid - 1
    else
      lo = mid + 1
    end
  end

  answer
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  books    = [100, 200, 300, 400]
  students = 2
  puts "Mínimo máximo de páginas por estudante: #{min_max_pages(books, students)}"
  # => 500  (divisão ótima: [100,200,300] e [400])

  weights = [3,2,2,4,1,4]
  days    = 3
  puts "Capacidade mínima do navio: #{ship_capacity(weights, days)}"
  # => 6    (rotações diárias: [3,2], [2,4], [1,4])
end
