# Sliding Window em Ruby

# 1. Subarray com soma alvo usando prefix sums (suporta negativos)
# Retorna [início, fim] ou nil
def subarray_with_sum(nums, target)
  prefix = { 0 => -1 }  # soma_prefixa => índice
  sum = 0

  nums.each_with_index do |v, i|
    sum += v
    if prefix.key?(sum - target)
      return [ prefix[sum - target] + 1, i ]
    end
    # armazena apenas a primeira ocorrência para menor subarray
    prefix[sum] ||= i
  end

  nil
end

# 2. Maior substring sem caracteres repetidos
# Retorna comprimento
def length_of_longest_substring(s)
  last_pos = {}  # caractere => última posição vista
  start = 0
  max_len = 0

  s.chars.each_with_index do |ch, i|
    if last_pos.key?(ch) && last_pos[ch] >= start
      start = last_pos[ch] + 1
    end
    last_pos[ch] = i
    curr_len = i - start + 1
    max_len = curr_len if curr_len > max_len
  end

  max_len
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  nums  = [1, 2, 3, -2, 5]
  p subarray_with_sum(nums, 6)       # => [0, 2]  (1+2+3 = 6)
  nums2 = [1, 2, -1, 4, 0]
  p subarray_with_sum(nums2, 5)      # => [1, 3]  (2 + -1 + 4 = 5)

  p length_of_longest_substring("abcabcbb")  # => 3 ("abc")
  p length_of_longest_substring("pwwkew")    # => 3 ("wke")
  p length_of_longest_substring("")          # => 0
end
