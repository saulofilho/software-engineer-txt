# Árvores:

# # Travessias (pré, in, pós-ordem, BFS)
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val   = val
        self.left  = left
        self.right = right

def preorder(root):
    """Pré-ordem: Root → Left → Right"""
    if root is None:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

def inorder(root):
    """In-ordem: Left → Root → Right"""
    if root is None:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def postorder(root):
    """Pós-ordem: Left → Right → Root"""
    if root is None:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]

def bfs(root):
    """Busca em largura (BFS) usando lista como fila."""
    if root is None:
        return []
    queue = [root]  # nossa fila
    result = []
    idx = 0
    while idx < len(queue):
        node = queue[idx]
        idx += 1
        result.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result

# Exemplo de uso:
if __name__ == "__main__":
    # Construindo a árvore:
    #       10
    #      /  \
    #     5    15
    #    / \     \
    #   3   7     18
    n3  = TreeNode(3)
    n7  = TreeNode(7)
    n5  = TreeNode(5, n3, n7)
    n18 = TreeNode(18)
    n15 = TreeNode(15, None, n18)
    root = TreeNode(10, n5, n15)

    print("Pré-ordem:", preorder(root))   # [10, 5, 3, 7, 15, 18]
    print("In-ordem: ", inorder(root))    # [3, 5, 7, 10, 15, 18]
    print("Pós-ordem:", postorder(root))  # [3, 7, 5, 18, 15, 10]
    print("BFS:      ", bfs(root))        # [10, 5, 15, 3, 7, 18]


# # Verificar árvore balanceada
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val   = val
        self.left  = left
        self.right = right

def is_balanced(root):
    """
    Retorna True se a árvore for height-balanced:
    para todo nó, altura das subárvores difere em no máximo 1.
    """
    def height(node):
        if node is None:
            return 0
        lh = height(node.left)
        if lh == -1:
            return -1
        rh = height(node.right)
        if rh == -1 or abs(lh - rh) > 1:
            return -1
        return max(lh, rh) + 1

    return height(root) != -1

# Exemplo de uso:
if __name__ == "__main__":
    # Árvore balanceada:
    #      4
    #     / \
    #    2   6
    #   / \ / \
    #  1  3 5  7
    n1 = TreeNode(1)
    n3 = TreeNode(3)
    n5 = TreeNode(5)
    n7 = TreeNode(7)
    n2 = TreeNode(2, n1, n3)
    n6 = TreeNode(6, n5, n7)
    root_bal = TreeNode(4, n2, n6)

    print(is_balanced(root_bal))  # True

    # Árvore não balanceada (cadeia à esquerda):
    #    1
    #   /
    #  2
    # /
    #3
    unb = TreeNode(3)
    unb = TreeNode(2, unb)
    root_unb = TreeNode(1, unb)

    print(is_balanced(root_unb))  # False


# # Menor ancestral comum (LCA)
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val   = val
        self.left  = left
        self.right = right

def lowest_common_ancestor(root, p, q):
    """
    Retorna o menor ancestral comum (LCA) dos nós p e q em uma árvore binária.
    Assume que ambos existem na árvore.
    """
    if root is None or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right

# Exemplo de uso:
if __name__ == "__main__":
    # Monta a árvore:
    #         3
    #       /   \
    #      5     1
    #     / \   / \
    #    6   2 0   8
    #       / \
    #      7   4
    n6 = TreeNode(6)
    n7 = TreeNode(7)
    n4 = TreeNode(4)
    n2 = TreeNode(2, n7, n4)
    n5 = TreeNode(5, n6, n2)
    n0 = TreeNode(0)
    n8 = TreeNode(8)
    n1 = TreeNode(1, n0, n8)
    root = TreeNode(3, n5, n1)

    a = n5  # nó com valor 5
    b = n1  # nó com valor 1
    lca = lowest_common_ancestor(root, a, b)
    print("LCA de", a.val, "e", b.val, "é:", lca.val)  # saída: 3

    a = n7  # nó com valor 7
    b = n4  # nó com valor 4
    lca = lowest_common_ancestor(root, a, b)
    print("LCA de", a.val, "e", b.val, "é:", lca.val)  # saída: 2


# # Conversão árvore-binária ↔ lista ligada
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val   = val
        self.left  = left
        self.right = right

class ListNode:
    def __init__(self, val, prev=None, next=None):
        self.val  = val
        self.prev = prev
        self.next = next

def tree_to_dll(root):
    """
    Converte uma BST em uma lista duplamente ligada ordenada (in-order).
    Retorna o head da lista.
    """
    def helper(node):
        nonlocal last, head
        if node is None:
            return
        # processa subárvore esquerda
        helper(node.left)
        # cria e encadeia o nó de lista
        curr = ListNode(node.val)
        if last:
            last.next = curr
            curr.prev = last
        else:
            head = curr
        last = curr
        # processa subárvore direita
        helper(node.right)

    last = None
    head = None
    helper(root)
    return head

def dll_to_bst(head):
    """
    Converte uma lista duplamente ligada ordenada em uma BST balanceada.
    Usa abordagem de contagem + construção recursiva.
    """
    # conta nós
    def count_nodes(n):
        cnt = 0
        while n:
            cnt += 1
            n = n.next
        return cnt

    def build(n):
        nonlocal head_ref
        if n == 0:
            return None
        # constrói metade esquerda
        left = build(n // 2)
        # nó raiz
        root = TreeNode(head_ref.val)
        head_ref = head_ref.next
        # constrói metade direita
        root.left  = left
        root.right = build(n - n // 2 - 1)
        return root

    size = count_nodes(head)
    head_ref = head
    return build(size)

# Exemplo de uso:
if __name__ == "__main__":
    # Monta uma BST de exemplo:
    #      4
    #     / \
    #    2   6
    #   / \ / \
    #  1  3 5  7
    n1 = TreeNode(1)
    n3 = TreeNode(3)
    n5 = TreeNode(5)
    n7 = TreeNode(7)
    n2 = TreeNode(2, n1, n3)
    n6 = TreeNode(6, n5, n7)
    root = TreeNode(4, n2, n6)

    # Árvore → DLL
    head = tree_to_dll(root)
    vals = []
    cur = head
    while cur:
        vals.append(cur.val)
        cur = cur.next
    print("DLL in-order:", vals)  # [1,2,3,4,5,6,7]

    # DLL → Árvore
    new_root = dll_to_bst(head)
    # imprime in-ordem para verificar
    def inorder(r):
        return inorder(r.left) + [r.val] + inorder(r.right) if r else []
    print("BST in-ordem:", inorder(new_root))  # [1,2,3,4,5,6,7]


# # Hash Tables (Mapas, Sets):
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Retorna os índices de dois números em `nums` cuja soma é igual a `target`.
    
    Exemplo:
        >>> two_sum([2, 7, 11, 15], 9)
        [0, 1]  # pois nums[0] + nums[1] == 9
    """
    seen = {}  # valor → índice
    for i, v in enumerate(nums):
        diff = target - v
        if diff in seen:
            return [seen[diff], i]
        seen[v] = i
    return []

if __name__ == "__main__":
    print(two_sum([2, 7, 11, 15], 9))      # [0, 1]
    print(two_sum([3, 2, 4], 6))           # [1, 2]
    print(two_sum([3, 3], 6))              # [0, 1]


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Agrupa as palavras que são anagramas.
    
    Exemplo:
        >>> group_anagrams(["eat","tea","tan","ate","nat","bat"])
        [["eat","tea","ate"], ["tan","nat"], ["bat"]]
    """
    buckets = {}  # chave ordenada → lista de strings
    for s in strs:
        key = "".join(sorted(s))
        if key not in buckets:
            buckets[key] = []
        buckets[key].append(s)
    return list(buckets.values())

if __name__ == "__main__":
    words = ["eat","tea","tan","ate","nat","bat"]
    print(group_anagrams(words))
    # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]


def length_of_longest_substring(s: str) -> int:
    """
    Retorna o comprimento da maior substring sem caracteres repetidos.
    
    Exemplo:
        >>> length_of_longest_substring("abcabcbb")
        3  # a,b,c
    """
    last_pos = {}      # registra a última posição de cada caractere
    start = 0          # início da janela corrente
    max_len = 0
    for i, ch in enumerate(s):
        if ch in last_pos and last_pos[ch] >= start:
            start = last_pos[ch] + 1
        last_pos[ch] = i
        cur_len = i - start + 1
        if cur_len > max_len:
            max_len = cur_len
    return max_len

if __name__ == "__main__":
    print(length_of_longest_substring("abcabcbb"))  # 3
    print(length_of_longest_substring("bbbbb"))     # 1
    print(length_of_longest_substring("pwwkew"))    # 3



# # Dois números somam um alvo (Two Sum)
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Retorna os índices de dois números em `nums` cuja soma é igual a `target`.
    
    Exemplo:
        >>> two_sum([2, 7, 11, 15], 9)
        [0, 1]  # pois nums[0] + nums[1] == 9
    """
    seen = {}  # mapa: valor → índice
    for i, v in enumerate(nums):
        diff = target - v
        if diff in seen:
            return [seen[diff], i]
        seen[v] = i
    return []

if __name__ == "__main__":
    # Testes
    print(two_sum([2, 7, 11, 15], 9))  # saída: [0, 1]
    print(two_sum([3, 2, 4], 6))       # saída: [1, 2]
    print(two_sum([3, 3], 6))          # saída: [0, 1]


# # Anagramas
def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Agrupa as palavras que são anagramas.

    Exemplo:
        >>> group_anagrams(["eat","tea","tan","ate","nat","bat"])
        [["eat","tea","ate"], ["tan","nat"], ["bat"]]
    """
    buckets: dict[str, list[str]] = {}
    for s in strs:
        # chave é a string ordenada
        key = "".join(sorted(s))
        if key not in buckets:
            buckets[key] = []
        buckets[key].append(s)
    return list(buckets.values())

if __name__ == "__main__":
    palavras = ["eat","tea","tan","ate","nat","bat"]
    grupos = group_anagrams(palavras)
    print(grupos)
    # Saída esperada (ordem dos grupos ou elementos pode variar):
    # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]


# # Substring sem caracteres repetidos
def length_of_longest_substring(s: str) -> int:
    """
    Retorna o comprimento da maior substring sem caracteres repetidos.

    Exemplo:
        >>> length_of_longest_substring("abcabcbb")
        3   # "abc"
        >>> length_of_longest_substring("bbbbb")
        1   # "b"
        >>> length_of_longest_substring("pwwkew")
        3   # "wke"
    """
    last_index = {}      # mapa: caractere → última posição vista
    start = 0            # início da janela corrente
    max_len = 0

    for i, ch in enumerate(s):
        # se já vimos o caractere dentro da janela atual,
        # movemos o início para a direita de sua posição anterior
        if ch in last_index and last_index[ch] >= start:
            start = last_index[ch] + 1
        last_index[ch] = i
        # atualiza máximo
        curr_len = i - start + 1
        if curr_len > max_len:
            max_len = curr_len

    return max_len


if __name__ == "__main__":
    print(length_of_longest_substring("abcabcbb"))  # 3
    print(length_of_longest_substring("bbbbb"))     # 1
    print(length_of_longest_substring("pwwkew"))    # 3
    print(length_of_longest_substring(""))          # 0
