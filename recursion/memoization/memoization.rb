def fibonacci(n, memo = {})
  return n if n <= 1
  memo[n] ||= fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
end

puts fibonacci(10) # => 55
