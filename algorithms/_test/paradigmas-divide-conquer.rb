# Divide and Conquer em Ruby

# 1. Merge Sort
def merge_sort(arr)
  return arr.dup if arr.size <= 1
  mid   = arr.size / 2
  left  = merge_sort(arr[0...mid])
  right = merge_sort(arr[mid..-1])
  merged = []
  i = j = 0
  while i < left.size && j < right.size
    if left[i] <= right[j]
      merged << left[i]
      i += 1
    else
      merged << right[j]
      j += 1
    end
  end
  # append restantes
  merged + left[i..-1] + right[j..-1]
end

# 2. Quick Sort
def quick_sort(arr)
  return arr.dup if arr.size <= 1
  pivot = arr[arr.size / 2]
  left  = arr.select { |x| x <  pivot }
  mid   = arr.select { |x| x == pivot }
  right = arr.select { |x| x >  pivot }
  quick_sort(left) + mid + quick_sort(right)
end

# 3. Máximo de subarray cruzando o meio
# Retorna [índice_esquerdo, índice_direito, soma]
def max_crossing_subarray(arr, low, mid, high)
  left_sum  = -Float::INFINITY
  sum = 0
  max_left = mid
  mid.downto(low) do |i|
    sum += arr[i]
    if sum > left_sum
      left_sum = sum
      max_left = i
    end
  end

  right_sum = -Float::INFINITY
  sum = 0
  max_right = mid + 1
  (mid+1).upto(high) do |j|
    sum += arr[j]
    if sum > right_sum
      right_sum = sum
      max_right = j
    end
  end

  [max_left, max_right, left_sum + right_sum]
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  data1 = [38, 27, 43, 3, 9, 82, 10]
  puts "Merge Sort: #{merge_sort(data1).inspect}"
  # => [3, 9, 10, 27, 38, 43, 82]

  data2 = [3, 6, 8, 10, 1, 2, 1]
  puts "Quick Sort: #{quick_sort(data2).inspect}"
  # => [1, 1, 2, 3, 6, 8, 10]

  arr = [2, -1, 3, -4, 5, 1, -3, 2]
  low, mid, high = 0, arr.size/2, arr.size-1
  l, r, s = max_crossing_subarray(arr, low, mid, high)
  puts "Crossing max-subarray: arr[#{l}:#{r+1}] = #{arr[l..r].inspect}, sum = #{s}"
  # exemplo: arr[2:5] = [3, -4, 5], sum = 4
end
