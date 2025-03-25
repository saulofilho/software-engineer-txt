def fatorial(n)
  return 1 if n == 0
  n * fatorial(n - 1)
end

p fatorial(5)  # 120
