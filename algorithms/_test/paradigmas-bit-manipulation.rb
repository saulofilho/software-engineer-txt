# Bit Manipulation em Ruby

# Encontra o elemento que aparece uma vez (xor)
def single_number(nums)
  result = 0
  nums.each { |x| result ^= x }
  result
end

# Conta bits '1' usando Brian Kernighan
def count_bits(n)
  count = 0
  while n != 0
    n &= (n - 1)
    count += 1
  end
  count
end

# Gera todos os subconjuntos via máscara de bits
def subsets(nums)
  n = nums.size
  res = []
  (0...1<<n).each do |mask|
    subset = []
    nums.each_with_index do |num, i|
      subset << num if (mask & (1 << i)) != 0
    end
    res << subset
  end
  res
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  p single_number([2, 1, 4, 5, 2, 4, 1])   # => 5
  p count_bits(13)                         # => 3
  p count_bits(0b101010)                   # => 3
  p subsets([1, 2, 3])                     # => [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
end
