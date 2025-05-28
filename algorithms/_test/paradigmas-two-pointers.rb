# Two Pointers em Ruby

# Par de soma alvo em array ordenado
# Retorna [índice_esquerdo, índice_direito] ou nil
def two_sum_sorted(arr, target)
  left = 0
  right = arr.size - 1
  while left < right
    s = arr[left] + arr[right]
    return [left, right] if s == target
    s < target ? left += 1 : right -= 1
  end
  nil
end

# Verifica se string é palíndromo comparando extremidades
def is_palindrome(s)
  i = 0
  j = s.size - 1
  while i < j
    return false if s[i] != s[j]
    i += 1
    j -= 1
  end
  true
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  data = [1, 2, 3, 4, 6]
  p two_sum_sorted(data, 6)    # => [1, 3]
  p two_sum_sorted(data, 10)   # => nil

  p is_palindrome("radar")     # => true
  p is_palindrome("level")     # => true
  p is_palindrome("ChatGPT")   # => false
end
