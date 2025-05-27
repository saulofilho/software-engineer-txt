# Heaps:

# # Heap mínimo/máximo
class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, val):
        # Insere no final e corrige posição
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        # Remove e retorna o menor elemento (root)
        if not self.heap:
            return None
        root = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return root

    def top(self):
        return self.heap[0] if self.heap else None

    def size(self):
        return len(self.heap)

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i] < self.heap[parent]:
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self.heap)
        while 2*i + 1 < n:
            left = 2*i + 1
            right = left + 1
            smallest = left
            if right < n and self.heap[right] < self.heap[left]:
                smallest = right
            if self.heap[smallest] < self.heap[i]:
                self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
                i = smallest
            else:
                break


class MaxHeap:
    def __init__(self):
        self.heap = []

    def push(self, val):
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        root = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return root

    def top(self):
        return self.heap[0] if self.heap else None

    def size(self):
        return len(self.heap)

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i] > self.heap[parent]:
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self.heap)
        while 2*i + 1 < n:
            left = 2*i + 1
            right = left + 1
            largest = left
            if right < n and self.heap[right] > self.heap[left]:
                largest = right
            if self.heap[largest] > self.heap[i]:
                self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
                i = largest
            else:
                break


# Exemplo de uso
if __name__ == "__main__":
    data = [5, 3, 8, 1, 2]

    # Min-Heap
    min_heap = MinHeap()
    for x in data:
        min_heap.push(x)
    print("MinHeap top:", min_heap.top())                # 1
    print("MinHeap pop sequence:", [min_heap.pop() for _ in range(len(data))])
    # saída: [1, 2, 3, 5, 8]

    # Max-Heap
    max_heap = MaxHeap()
    for x in data:
        max_heap.push(x)
    print("MaxHeap top:", max_heap.top())                # 8
    print("MaxHeap pop sequence:", [max_heap.pop() for _ in range(len(data))])
    # saída: [8, 5, 3, 2, 1]


# # K maiores/menores elementos
def k_largest(nums: list[int], k: int) -> list[int]:
    """
    Retorna os k maiores elementos em ordem decrescente.

    Exemplo:
        >>> k_largest([7, 2, 9, 4, 3, 8, 1], 3)
        [9, 8, 7]
    """
    return sorted(nums, reverse=True)[:k]

def k_smallest(nums: list[int], k: int) -> list[int]:
    """
    Retorna os k menores elementos em ordem crescente.

    Exemplo:
        >>> k_smallest([7, 2, 9, 4, 3, 8, 1], 3)
        [1, 2, 3]
    """
    return sorted(nums)[:k]

if __name__ == "__main__":
    data = [7, 2, 9, 4, 3, 8, 1]
    print("K maiores:", k_largest(data, 3))   # [9, 8, 7]
    print("K menores:", k_smallest(data, 3)) # [1, 2, 3]


# # Stream de dados (mediana em tempo real)
import heapq

class MedianFinder:
    """
    Mantém dois heaps (max-heap small e min-heap large) para calcular a mediana em tempo real.
    """
    def __init__(self):
        # small é um max-heap implementado com valores negativos
        self.small: list[int] = []
        # large é um min-heap
        self.large: list[int] = []

    def add_num(self, num: int) -> None:
        # Insere em small (como max-heap via -num)
        heapq.heappush(self.small, -num)
        # Garante que todo elemento de small ≤ todo elemento de large
        if self.large and -self.small[0] > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Balanceia os tamanhos: small pode ter no máximo 1 elemento a mais que large
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self) -> float:
        # Se small tiver 1 elemento a mais, é a mediana
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        # Senão, é a média das raízes dos dois heaps
        return (-self.small[0] + self.large[0]) / 2.0


if __name__ == "__main__":
    mf = MedianFinder()
    stream = [5, 15, 1, 3, 8]
    for num in stream:
        mf.add_num(num)
        print(f"Após inserir {num}, mediana = {mf.find_median()}")
    # Saída esperada:
    # Após inserir 5, mediana = 5.0
    # Após inserir 15, mediana = 10.0
    # Após inserir 1, mediana = 5.0
    # Após inserir 3, mediana = 4.0
    # Após inserir 8, mediana = 5.0
