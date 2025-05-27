# Greedy

# # Interval Scheduling
# 1. Interval Scheduling (máximo de atividades não sobrepostas)
def interval_scheduling(intervals):
    """
    intervals: lista de tuplas (start, end)
    Retorna o subconjunto máximo de intervalos que não se sobrepõem.
    """
    # ordena por tempo de término
    sorted_intervals = sorted(intervals, key=lambda x: x[1])
    result = []
    last_end = -float('inf')
    for start, end in sorted_intervals:
        if start >= last_end:
            result.append((start, end))
            last_end = end
    return result

if __name__ == "__main__":
    activities = [(1,4), (3,5), (0,6), (5,7), (3,9), (5,9), (6,10), (8,11), (8,12), (2,14), (12,16)]
    chosen = interval_scheduling(activities)
    print("Atividades escolhidas:", chosen)
    # saída esperada:
    # Atividades escolhidas: [(1,4), (5,7), (8,11), (12,16)]


# # Troco com moedas
# 2. Troco com moedas (mínimo de moedas via programação dinâmica)
def min_coins(coins, amount):
    """
    coins: lista de valores de moedas (inteiros positivos)
    amount: alvo
    Retorna o número mínimo de moedas para compor `amount`, ou -1 se não for possível.
    """
    INF = amount + 1
    dp = [0] + [INF] * amount
    for i in range(1, amount + 1):
        for c in coins:
            if c <= i and dp[i - c] + 1 < dp[i]:
                dp[i] = dp[i - c] + 1
    return dp[amount] if dp[amount] != INF else -1

if __name__ == "__main__":
    moedas = [1, 3, 4]
    valor = 6
    print("Min moedas para", valor, ":", min_coins(moedas, valor))
    # saída esperada: Min moedas para 6 : 2  (por exemplo, 3+3 ou 4+1+1)


# # Huffman Coding
# 3. Huffman Coding (construção de árvore sem heapq)
class Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char  = char
        self.freq  = freq
        self.left  = left
        self.right = right

def build_huffman(freqs):
    """
    freqs: dicionário {char: frequência}
    Retorna raiz da árvore de Huffman.
    """
    # cria nós iniciais
    nodes = [Node(c, f) for c, f in freqs.items()]
    # itera até sobrar um nó
    while len(nodes) > 1:
        # encontra os dois nós de menor frequência
        nodes.sort(key=lambda n: n.freq)
        a = nodes.pop(0)
        b = nodes.pop(0)
        # combina em novo nó
        merged = Node(None, a.freq + b.freq, a, b)
        nodes.append(merged)
    return nodes[0]

def make_codes(root):
    """
    root: raiz da árvore de Huffman
    Retorna dicionário {char: código em bits (string)}.
    """
    codes = {}
    def dfs(node, prefix):
        if node is None:
            return
        # folha
        if node.char is not None:
            codes[node.char] = prefix or "0"
        else:
            dfs(node.left,  prefix + "0")
            dfs(node.right, prefix + "1")
    dfs(root, "")
    return codes

if __name__ == "__main__":
    freq_map = {'a': 5, 'b': 9, 'c': 12, 'd': 13, 'e': 16, 'f': 45}
    root = build_huffman(freq_map)
    huff_codes = make_codes(root)
    print("Códigos de Huffman:")
    for ch, code in huff_codes.items():
        print(f" {ch}: {code}")
    # exemplo de saída (códigos podem variar em estrutura):
    #  f: 0
    #  c: 100
    #  d: 101
    #  a: 1100
    #  b: 1101
    #  e: 111
