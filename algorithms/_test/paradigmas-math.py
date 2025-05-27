# Math

# # GCD, LCM
# 1. GCD e LCM (Euclides)

def gcd(a: int, b: int) -> int:
    """
    Computa o Máximo Divisor Comum usando algoritmo de Euclides.
    """
    while b:
        a, b = b, a % b
    return abs(a)

def lcm(a: int, b: int) -> int:
    """
    Computa o Mínimo Múltiplo Comum via gcd.
    """
    return abs(a // gcd(a, b) * b)

if __name__ == "__main__":
    print("GCD de 48 e 18:", gcd(48, 18))   # 6
    print("LCM de 48 e 18:", lcm(48, 18))   # 144


# # Crivo de Eratóstenes
# 2. Crivo de Eratóstenes

def sieve(n: int) -> list[int]:
    """
    Retorna todos os primos ≤ n.
    """
    if n < 2:
        return []
    is_prime = [True] * (n+1)
    is_prime[0] = is_prime[1] = False
    p = 2
    while p*p <= n:
        if is_prime[p]:
            for multiple in range(p*p, n+1, p):
                is_prime[multiple] = False
        p += 1
    return [i for i, prime in enumerate(is_prime) if prime]

if __name__ == "__main__":
    print("Primos até 30:", sieve(30))
    # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


# # Números primos, fatoração
# 3. Teste de primalidade e fatoração

def is_prime(n: int) -> bool:
    """
    Testa primalidade simples em O(√n).
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i*i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def prime_factors(n: int) -> list[int]:
    """
    Retorna a lista dos fatores primos de n (com multiplicidade).
    """
    factors = []
    # extrai fatores 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    # extrai fatores ímpares
    f = 3
    while f*f <= n:
        while n % f == 0:
            factors.append(f)
            n //= f
        f += 2
    if n > 1:
        factors.append(n)
    return factors

if __name__ == "__main__":
    print("17 é primo?", is_prime(17))                 # True
    print("18 é primo?", is_prime(18))                 # False
    print("Fatores primos de 360:", prime_factors(360))  # [2, 2, 2, 3, 3, 5]


# # Teorema de Fermat / Modular Inverse
# 4. Potenciação modular e inverso modular (Fermat)

def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Calcula (base^exp) % mod em O(log exp).
    """
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result

def mod_inverse(a: int, p: int) -> int:
    """
    Retorna inverso de a mod p, assumindo p primo (a^(p-2) mod p).
    """
    # Fermat: a^(p-1) ≡ 1 (mod p) ⇒ a^(p-2) ≡ a⁻¹
    return mod_pow(a, p-2, p)

if __name__ == "__main__":
    print("3^13 mod 17 =", mod_pow(3, 13, 17))       # 12
    print("Inverso de 3 mod 17:", mod_inverse(3, 17)) # 6 (pois 3*6 ≡1 mod17)


# # Combinatória (nCr)
# 5. Combinatória (nCr)

def nCr(n: int, r: int) -> int:
    """
    Calcula C(n, r) sem overflow grande, usando multiplicativo.
    """
    if r < 0 or r > n:
        return 0
    # aproveita simetria
    r = min(r, n - r)
    numer = 1
    denom = 1
    for i in range(1, r+1):
        numer *= n - r + i
        denom *= i
    return numer // denom

if __name__ == "__main__":
    print("C(5,2) =", nCr(5,2))   # 10
    print("C(10,3) =", nCr(10,3)) # 120
