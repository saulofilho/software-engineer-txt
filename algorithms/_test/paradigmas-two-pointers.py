# Two Pointers

# # Par de soma alvo em array ordenado
def two_sum_sorted(arr: list[int], target: int) -> tuple[int, int] | None:
    """
    Encontra dois números em um array **ordenado** cuja soma seja igual a target,
    usando o método dos dois ponteiros.
    
    Retorna uma tupla (índice_esquerdo, índice_direito) ou None se não existir.

    Exemplo:
        >>> two_sum_sorted([1, 2, 3, 4, 6], 6)
        (1, 3)   # pois arr[1] + arr[3] == 2 + 4 == 6
    """
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return (left, right)
        elif s < target:
            left += 1
        else:
            right -= 1
    return None

if __name__ == "__main__":
    data = [1, 2, 3, 4, 6]
    print(two_sum_sorted(data, 6))    # saída: (1, 3)
    print(two_sum_sorted(data, 10))   # saída: None


# # Palíndromo verificando extremidades
def is_palindrome(s: str) -> bool:
    """
    Verifica se a string s é um palíndromo, comparando os caracteres das extremidades
    em direção ao centro.

    Exemplo:
        >>> is_palindrome("radar")
        True
        >>> is_palindrome("hello")
        False
    """
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True

if __name__ == "__main__":
    print(is_palindrome("radar"))   # True
    print(is_palindrome("level"))   # True
    print(is_palindrome("ChatGPT")) # False
