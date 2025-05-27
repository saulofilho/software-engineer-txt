# Programação Dinâmica (DP)
# # Fibonacci, Subsequência comum (LCS)
# 1. Fibonacci (DP / memoização)
def fib(n, memo=None):
    """
    Retorna o n-ésimo Fibonacci usando memoização (top-down DP).
    Exemplo:
        >>> fib(10)
        55
    """
    if memo is None:
        memo = {}
    if n < 2:
        return n
    if n not in memo:
        memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]

if __name__ == "__main__":
    print(fib(10))  # 55


# 2. Subsequência comum máxima (LCS) – bottom-up DP
def lcs(a: str, b: str) -> int:
    """
    Retorna o tamanho da maior subsequência comum entre a e b.
    Exemplo:
        >>> lcs("AGGTAB", "GXTXAYB")
        4  # "GTAB"
    """
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

if __name__ == "__main__":
    print(lcs("AGGTAB", "GXTXAYB"))  # 4


# # Knapsack (0/1 e fracionário)
# 3a. Knapsack 0/1 – DP de valor máximo em peso limitado
def knapsack_01(values: list[int], weights: list[int], W: int) -> int:
    """
    Retorna valor máximo com capacidade W, cada item usado 0 ou 1 vez.
    Exemplo:
        >>> knapsack_01([60,100,120], [10,20,30], 50)
        220
    """
    n = len(values)
    dp = [[0]*(W+1) for _ in range(n+1)]
    for i in range(1, n+1):
        v, w = values[i-1], weights[i-1]
        for cap in range(W+1):
            dp[i][cap] = dp[i-1][cap]
            if w <= cap:
                dp[i][cap] = max(dp[i][cap], dp[i-1][cap-w] + v)
    return dp[n][W]

# 3b. Knapsack fracionário – greedy por razão valor/peso
def knapsack_fractional(values: list[int], weights: list[int], W: int) -> float:
    """
    Retorna valor máximo permitindo frações de itens.
    Exemplo:
        >>> knapsack_fractional([60,100,120], [10,20,30], 50)
        240.0
    """
    items = sorted(zip(values, weights), key=lambda x: x[0]/x[1], reverse=True)
    total = 0.0
    for v, w in items:
        if W == 0:
            break
        take = min(w, W)
        total += take * (v/w)
        W -= take
    return total

if __name__ == "__main__":
    print(knapsack_01([60,100,120],[10,20,30],50))        # 220
    print(knapsack_fractional([60,100,120],[10,20,30],50))# 240.0


# # Caminho mínimo em grade (Grid DP)
# 4. Caminho mínimo em grade (Grid DP – soma mínima de cima-esquerda até baixo-direita)
def min_path_sum(grid: list[list[int]]) -> int:
    """
    Exemplo:
        >>> min_path_sum([[1,3,1],[1,5,1],[4,2,1]])
        7  # 1→3→1→1→1
    """
    m, n = len(grid), len(grid[0])
    dp = [[0]*n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for i in range(1, m):
        dp[i][0] = dp[i-1][0] + grid[i][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j-1] + grid[0][j]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
    return dp[m-1][n-1]

if __name__ == "__main__":
    print(min_path_sum([[1,3,1],[1,5,1],[4,2,1]]))  # 7


# # Edit Distance (Levenshtein)
# 5. Edit Distance (Levenshtein) – bottom-up DP
def edit_distance(a: str, b: str) -> int:
    """
    Retorna número mínimo de inserções/deleções/substituições de a→b.
    Exemplo:
        >>> edit_distance("kitten","sitting")
        3
    """
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if a[i-1]==b[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,    # delete
                dp[i][j-1] + 1,    # insert
                dp[i-1][j-1] + cost  # replace or match
            )
    return dp[m][n]

if __name__ == "__main__":
    print(edit_distance("kitten","sitting"))  # 3


# # Palíndromos e corte mínimo
# 6. Palíndromos e corte mínimo (min cut para tornar toda string em palíndromo)
def min_cut_palindrome(s: str) -> int:
    """
    Retorna número mínimo de cortes para que cada substring seja palíndroma.
    Exemplo:
        >>> min_cut_palindrome("aab")
        1  # "aa"|"b"
    """
    n = len(s)
    # is_pal[i][j] = True se s[i:j+1] é palíndromo
    is_pal = [[False]*n for _ in range(n)]
    for i in range(n-1, -1, -1):
        for j in range(i, n):
            if s[i]==s[j] and (j-i<2 or is_pal[i+1][j-1]):
                is_pal[i][j] = True
    # dp[i] = min cortes para s[:i]
    dp = [0]*(n+1)
    dp[0] = -1  # para compensar o primeiro corte
    for i in range(1, n+1):
        dp[i] = i-1
        for j in range(i):
            if is_pal[j][i-1]:
                dp[i] = min(dp[i], dp[j]+1)
    return dp[n]

if __name__ == "__main__":
    print(min_cut_palindrome("aab"))   # 1
    print(min_cut_palindrome("a"))     # 0
    print(min_cut_palindrome("ab"))    # 1


# # DP com Bitmask, DP com Trie
# 7. DP com Bitmask – Assignment problem (n pessoas ↔ n tarefas)
def assignment_min_cost(cost: list[list[int]]) -> int:
    """
    Dada matriz cost[n][n], retorna custo mínimo de atribuir cada pessoa a uma tarefa distinta.
    Usa DP de 2^n estados.
    """
    n = len(cost)
    size = 1 << n
    dp = [float('inf')] * size
    dp[0] = 0
    for mask in range(size):
        i = mask.bit_count()  # quantas pessoas já atribuídas
        if i >= n: continue
        for j in range(n):
            if not (mask & (1 << j)):
                nxt = mask | (1 << j)
                dp[nxt] = min(dp[nxt], dp[mask] + cost[i][j])
    return dp[size-1]

if __name__ == "__main__":
    cost = [
        [9,2,7,8],
        [6,4,3,7],
        [5,8,1,8],
        [7,6,9,4]
    ]
    print(assignment_min_cost(cost))  # 13


# 8. DP com Trie – Word Break (segmentação de string usando dicionário)
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

def build_trie(words: list[str]) -> TrieNode:
    root = TrieNode()
    for w in words:
        node = root
        for ch in w:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True
    return root

def word_break(s: str, word_dict: list[str]) -> bool:
    """
    Retorna True se s pode ser segmentada em palavras do dicionário.
    Exemplo:
        >>> word_break("leetcode", ["leet","code"])
        True
    """
    root = build_trie(word_dict)
    n = len(s)
    dp = [False]*(n+1)
    dp[0] = True
    for i in range(n):
        if not dp[i]:
            continue
        node = root
        for j in range(i, n):
            ch = s[j]
            if ch not in node.children:
                break
            node = node.children[ch]
            if node.is_end:
                dp[j+1] = True
    return dp[n]

if __name__ == "__main__":
    print(word_break("leetcode", ["leet","code"]))   # True
    print(word_break("applepenapple", ["apple","pen"]))  # True
    print(word_break("catsandog", ["cats","dog","sand","and","cat"]))  # False
