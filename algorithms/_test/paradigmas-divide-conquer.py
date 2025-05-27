# Divide and Conquer

# # Merge Sort, Quick Sort
def merge_sort(arr):
    """
    Divide and conquer: split the array, sort each half, then merge.
    """
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    # append remaining
    merged.extend(left[i:] or right[j:])
    return merged

if __name__ == "__main__":
    data = [38, 27, 43, 3, 9, 82, 10]
    print("Merge Sort:", merge_sort(data))
    # Saída: [3, 9, 10, 27, 38, 43, 82]


def quick_sort(arr):
    """
    Escolhe pivô no meio e particiona em <, ==, >, ordenando recursivamente.
    """
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr) // 2]
    left  = [x for x in arr if x <  pivot]
    mid   = [x for x in arr if x == pivot]
    right = [x for x in arr if x >  pivot]
    return quick_sort(left) + mid + quick_sort(right)

if __name__ == "__main__":
    data = [3, 6, 8, 10, 1, 2, 1]
    print("Quick Sort:", quick_sort(data))
    # Saída: [1, 1, 2, 3, 6, 8, 10]



# # Máximo de subarray cruzando o meio
def max_crossing_subarray(arr, low, mid, high):
    """
    Encontra o subarray de soma máxima que cruza o ponto mid.
    Retorna (índice_esquerdo, índice_direito, soma).
    """
    left_sum = float('-inf')
    sum_ = 0
    max_left = mid
    for i in range(mid, low-1, -1):
        sum_ += arr[i]
        if sum_ > left_sum:
            left_sum = sum_
            max_left = i

    right_sum = float('-inf')
    sum_ = 0
    max_right = mid + 1
    for j in range(mid+1, high+1):
        sum_ += arr[j]
        if sum_ > right_sum:
            right_sum = sum_
            max_right = j

    return max_left, max_right, left_sum + right_sum

if __name__ == "__main__":
    arr = [2, -1, 3, -4, 5, 1, -3, 2]
    low, mid, high = 0, len(arr)//2, len(arr)-1
    l, r, s = max_crossing_subarray(arr, low, mid, high)
    print(f"Crossing max-subarray: arr[{l}:{r+1}] = {arr[l:r+1]}, sum = {s}")
    # Por exemplo: arr[2:5] = [3, -4, 5], sum = 4
