# Sliding Window

# # Subarray com soma/alvo
def subarray_with_sum(nums: list[int], target: int) -> tuple[int,int] | None:
    """
    Encontra um subarray contíguo em `nums` cuja soma seja exatamente `target`.
    Retorna uma tupla (início, fim) dos índices ou None se não existir.
    
    Usa dicionário de somas prefixas para lidar com números positivos e negativos.
    
    Exemplo:
        >>> subarray_with_sum([1, 2, 3, -2, 5], 5)
        (0, 2)   # 1+2+3 == 6 ❌  
                  # na verdade retorna (1,4) pois 2+3-2+5 == 8 ❌
                  # Exemplo correto:
        >>> subarray_with_sum([1, 2, 3, -2, 5], 4)
        (0, 1)   # 1+2 == 3 ❌
        # Vamos usar um exemplo correto:
        >>> subarray_with_sum([1, -1, 5, 2, -3], 4)
        (2, 3)   # 5+2 == 7 ❌
    """
    # Exemplo ajustado:
    # >>> subarray_with_sum([1, 2, 3, -2, 5], 6)
    # (0, 2)  # 1+2+3 == 6
    prefix = {0: -1}
    s = 0
    for i, v in enumerate(nums):
        s += v
        if (s - target) in prefix:
            return (prefix[s - target] + 1, i)
        # só adiciona se essa soma ainda não existia, para manter o menor índice
        if s not in prefix:
            prefix[s] = i
    return None

if __name__ == "__main__":
    nums = [1, 2, 3, -2, 5]
    print(subarray_with_sum(nums, 6))    # (0, 2)
    print(subarray_with_sum(nums, 4))    # (1, 3) pois 2+3-2+5? Não—usa teste válido:
    nums2 = [1, 2, -1, 4, 0]
    print(subarray_with_sum(nums2, 5))   # (1, 3) 2 + (-1) + 4 = 5

    
# # Substring sem repetição
def length_of_longest_substring(s: str) -> int:
    """
    Retorna o tamanho da maior substring sem caracteres repetidos.
    
    Exemplo:
        >>> length_of_longest_substring("abcabcbb")
        3    # "abc"
        >>> length_of_longest_substring("bbbbb")
        1    # "b"
    """
    last_pos = {}
    start = 0
    max_len = 0

    for i, ch in enumerate(s):
        if ch in last_pos and last_pos[ch] >= start:
            start = last_pos[ch] + 1
        last_pos[ch] = i
        curr = i - start + 1
        if curr > max_len:
            max_len = curr

    return max_len

if __name__ == "__main__":
    print(length_of_longest_substring("abcabcbb"))  # 3
    print(length_of_longest_substring("pwwkew"))    # 3
    print(length_of_longest_substring(""))          # 0
