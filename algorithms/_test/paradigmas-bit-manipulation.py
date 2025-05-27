# Bit Manipulation

# # Encontrar elemento único (XOR)
def single_number(nums: list[int]) -> int:
    """
    Encontra o elemento que aparece apenas uma vez em uma lista onde todos os outros
    aparecem exatamente duas vezes, usando XOR.
    
    Exemplo:
        >>> single_number([2, 1, 4, 5, 2, 4, 1])
        5
    """
    result = 0
    for x in nums:
        result ^= x
    return result

if __name__ == "__main__":
    print(single_number([2, 1, 4, 5, 2, 4, 1]))  # Saída: 5


# # Contagem de bits
def count_bits(n: int) -> int:
    """
    Conta quantos bits '1' existem na representação binária de n,
    usando o algoritmo de Brian Kernighan (remove o último bit 1 a cada iteração).
    
    Exemplo:
        >>> count_bits(13)  # 13 = 0b1101
        3
    """
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count

if __name__ == "__main__":
    print(count_bits(13))  # Saída: 3
    print(count_bits(0b101010))  # Saída: 3


# # Subsets via máscara de bits
def subsets(nums: list[int]) -> list[list[int]]:
    """
    Gera todos os subconjuntos de nums usando máscara de bits.
    
    Exemplo:
        >>> subsets([1, 2, 3])
        [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
    """
    n = len(nums)
    res = []
    for mask in range(1 << n):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        res.append(subset)
    return res

if __name__ == "__main__":
    print(subsets([1, 2, 3]))
    # Saída:
    # [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
