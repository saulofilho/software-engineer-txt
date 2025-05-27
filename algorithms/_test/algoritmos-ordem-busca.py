# Ordenação e Busca
# # Bubble, Selection, Insertion Sort
def bubble_sort(arr: list[int]) -> list[int]:
    """
    Percorre o array várias vezes, trocando elementos adjacentes fora de ordem.
    Complexidade: O(n²)
    """
    n = len(arr)
    a = arr[:]  # faz cópia para não alterar original
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

if __name__ == "__main__":
    print(bubble_sort([5, 1, 4, 2, 8]))  # [1, 2, 4, 5, 8]


def selection_sort(arr: list[int]) -> list[int]:
    """
    Em cada iteração, seleciona o menor elemento do restante e o coloca na posição correta.
    Complexidade: O(n²)
    """
    n = len(arr)
    a = arr[:]
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

if __name__ == "__main__":
    print(selection_sort([64, 25, 12, 22, 11]))  # [11, 12, 22, 25, 64]


def insertion_sort(arr: list[int]) -> list[int]:
    """
    Constrói o array ordenado inserindo cada elemento na posição correta.
    Complexidade: O(n²) (ótimo O(n) se já estiver quase ordenado)
    """
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

if __name__ == "__main__":
    print(insertion_sort([12, 11, 13, 5, 6]))  # [5, 6, 11, 12, 13]


# # Merge Sort, Quick Sort
def merge_sort(arr: list[int]) -> list[int]:
    """
    Divide e conquista: divide o array, ordena cada metade e intercala.
    Complexidade: O(n log n)
    """
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    # intercala
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i]); i += 1
        else:
            res.append(right[j]); j += 1
    res.extend(left[i:] or right[j:])
    return res

if __name__ == "__main__":
    print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
    # [3, 9, 10, 27, 38, 43, 82]


def quick_sort(arr: list[int]) -> list[int]:
    """
    Escolhe um pivô e particiona em menores e maiores, então ordena recursivamente.
    Complexidade média: O(n log n), pior caso O(n²).
    """
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid  = [x for x in arr if x == pivot]
    right= [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

if __name__ == "__main__":
    print(quick_sort([3,6,8,10,1,2,1]))
    # [1,1,2,3,6,8,10]


# # Counting/Radix/Bucket Sort
def counting_sort(arr: list[int], k: int) -> list[int]:
    """
    Para inteiros no intervalo [0..k], conta ocorrências e reconstrói o array.
    Complexidade: O(n + k)
    """
    count = [0] * (k + 1)
    for x in arr:
        count[x] += 1
    res = []
    for val, freq in enumerate(count):
        res.extend([val] * freq)
    return res

if __name__ == "__main__":
    print(counting_sort([1,4,1,2,7,5,2], 7))
    # [1,1,2,2,4,5,7]


def radix_sort(arr: list[int]) -> list[int]:
    """
    Ordena por dígitos, usando Counting Sort como sub-rotina estável.
    Complexidade: O(d·(n + b)), d = dígitos, b = base (10).
    """
    def counting_sort_by_digit(a, exp):
        n = len(a)
        output = [0]*n
        count = [0]*10
        for num in a:
            digit = (num // exp) % 10
            count[digit] += 1
        for i in range(1,10):
            count[i] += count[i-1]
        for num in reversed(a):
            digit = (num // exp) % 10
            count[digit] -= 1
            output[count[digit]] = num
        return output

    res = arr[:]
    max_val = max(res) if res else 0
    exp = 1
    while max_val // exp > 0:
        res = counting_sort_by_digit(res, exp)
        exp *= 10
    return res

if __name__ == "__main__":
    print(radix_sort([170,45,75,90,802,24,2,66]))
    # [2,24,45,66,75,90,170,802]


def bucket_sort(arr: list[float], bucket_count: int = 10) -> list[float]:
    """
    Distribui em buckets, ordena cada um com Insertion Sort e concatena.
    Complexidade média: O(n + k), onde k = número de buckets.
    """
    buckets = [[] for _ in range(bucket_count)]
    for x in arr:
        idx = int(x * bucket_count)
        buckets[min(idx, bucket_count-1)].append(x)

    def insertion_sort(a):
        for i in range(1, len(a)):
            key = a[i]
            j = i - 1
            while j >= 0 and a[j] > key:
                a[j+1] = a[j]; j -= 1
            a[j+1] = key

    res = []
    for b in buckets:
        insertion_sort(b)
        res.extend(b)
    return res

if __name__ == "__main__":
    data = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
    print(bucket_sort(data))
    # e.g. [0.1234, 0.3434, 0.565, 0.656, 0.665, 0.897]


# # Binary Search e variações:
def binary_search(arr: list[int], target: int) -> int:
    """
    Retorna índice de `target` em `arr` ou -1 se não existe.
    Complexidade: O(log n)
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

if __name__ == "__main__":
    print(binary_search([1,2,3,4,5,6], 4))  # 3
    print(binary_search([1,2,3,4,5,6], 7))  # -1


# # Busca do primeiro/último elemento
def find_first(arr: list[int], target: int) -> int:
    lo, hi, res = 0, len(arr) - 1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            res = mid
            hi = mid - 1
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return res

def find_last(arr: list[int], target: int) -> int:
    lo, hi, res = 0, len(arr) - 1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            res = mid
            lo = mid + 1
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return res

if __name__ == "__main__":
    a = [1,2,2,2,3,4]
    print(find_first(a, 2), find_last(a, 2))  # 1 3


# # Busca em matriz ordenada
def search_matrix(matrix: list[list[int]], target: int) -> bool:
    """
    Matriz onde cada linha é ordenada e o 1º elemento de cada linha >
    último da linha anterior.
    Usa busca binária considerando o array concatenado.
    """
    if not matrix or not matrix[0]:
        return False
    rows, cols = len(matrix), len(matrix[0])
    lo, hi = 0, rows * cols - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        r, c = divmod(mid, cols)
        val = matrix[r][c]
        if val == target:
            return True
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False

if __name__ == "__main__":
    mat = [
        [1, 3, 5, 7],
        [10,11,16,20],
        [23,30,34,60]
    ]
    print(search_matrix(mat, 3))   # True
    print(search_matrix(mat, 13))  # False
