# Math Utilities em Ruby

# 1. GCD e LCM (Euclides)
def gcd(a, b)
  a, b = b, a % b while b != 0
  a.abs
end

def lcm(a, b)
  return 0 if a == 0 || b == 0
  (a.abs / gcd(a, b) * b.abs)
end

# 2. Crivo de Eratóstenes
def sieve(n)
  return [] if n < 2
  is_prime = Array.new(n+1, true)
  is_prime[0] = is_prime[1] = false
  p = 2
  while p * p <= n
    if is_prime[p]
      (p*p).step(n, p) { |m| is_prime[m] = false }
    end
    p += 1
  end
  (2..n).select { |i| is_prime[i] }
end

# 3. Teste de Primalidade e Fatoração
def is_prime(n)
  return false if n <= 1
  return true  if n <= 3
  return false if n % 2 == 0
  i = 3
  while i * i <= n
    return false if n % i == 0
    i += 2
  end
  true
end

def prime_factors(n)
  factors = []
  # extrai fatores 2
  while n % 2 == 0
    factors << 2
    n /= 2
  end
  # extrai fatores ímpares
  f = 3
  while f * f <= n
    while n % f == 0
      factors << f
      n /= f
    end
    f += 2
  end
  factors << n if n > 1
  factors
end

# 4. Potenciação Modular e Inverso (Fermat)
def mod_pow(base, exp, mod)
  result = 1
  base %= mod
  while exp > 0
    result = (result * base) % mod if (exp & 1) == 1
    base = (base * base) % mod
    exp >>= 1
  end
  result
end

def mod_inverse(a, p)
  # assume p é primo
  mod_pow(a, p - 2, p)
end

# 5. Combinatória (nCr)
def nCr(n, r)
  return 0 if r < 0 || r > n
  r = [r, n - r].min
  numer = 1
  denom = 1
  (1..r).each do |i|
    numer *= (n - r + i)
    denom *= i
  end
  numer / denom
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  puts "--- GCD e LCM ---"
  puts "GCD de 48 e 18: #{gcd(48, 18)}"   # => 6
  puts "LCM de 48 e 18: #{lcm(48, 18)}"   # => 144

  puts "\n--- Primos até 30 ---"
  p sieve(30)                           # => [2,3,5,7,11,13,17,19,23,29]

  puts "\n--- Primalidade e Fatores ---"
  puts "17 é primo? #{is_prime(17)}"     # => true
  puts "18 é primo? #{is_prime(18)}"     # => false
  p prime_factors(360)                  # => [2,2,2,3,3,5]

  puts "\n--- Potenciação Modular e Inverso ---"
  puts "3^13 mod 17 = #{mod_pow(3, 13, 17)}"      # => 12
  puts "Inverso de 3 mod 17: #{mod_inverse(3, 17)}" # => 6

  puts "\n--- Combinatória ---"
  puts "C(5,2) = #{nCr(5,2)}"              # => 10
  puts "C(10,3) = #{nCr(10,3)}"            # => 120
end
