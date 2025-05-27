# # Árvores Balanceadas (AVL, Red-Black)
# AVL Tree Implementation
class AVLNode:
    def __init__(self, key):
        self.key    = key
        self.left   = None
        self.right  = None
        self.height = 1  # altura do nó

def get_height(node):
    return node.height if node else 0

def update_height(node):
    node.height = 1 + max(get_height(node.left), get_height(node.right))

def get_balance(node):
    return get_height(node.left) - get_height(node.right) if node else 0

def right_rotate(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left  = T2
    update_height(y)
    update_height(x)
    return x

def left_rotate(x):
    y = x.right
    T2 = y.left
    y.left  = x
    x.right = T2
    update_height(x)
    update_height(y)
    return y

def avl_insert(node, key):
    """Insere key na AVL e retorna a nova raiz."""
    if not node:
        return AVLNode(key)
    if key < node.key:
        node.left = avl_insert(node.left, key)
    else:
        node.right = avl_insert(node.right, key)

    update_height(node)
    balance = get_balance(node)

    # Left Left
    if balance > 1 and key < node.left.key:
        return right_rotate(node)
    # Right Right
    if balance < -1 and key > node.right.key:
        return left_rotate(node)
    # Left Right
    if balance > 1 and key > node.left.key:
        node.left = left_rotate(node.left)
        return right_rotate(node)
    # Right Left
    if balance < -1 and key < node.right.key:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    return node

def avl_inorder(node):
    return avl_inorder(node.left) + [node.key] + avl_inorder(node.right) if node else []

# Exemplo AVL
if __name__ == "__main__":
    keys = [10, 20, 30, 40, 50, 25]
    root = None
    for k in keys:
        root = avl_insert(root, k)
    print("AVL in-order:", avl_inorder(root))
    # Saída esperada: [10, 20, 25, 30, 40, 50]


# Red-Black Tree Implementation

class RBNode:
    def __init__(self, key, color='red', left=None, right=None, parent=None):
        self.key    = key
        self.color  = color  # 'red' ou 'black'
        self.left   = left
        self.right  = right
        self.parent = parent

class RedBlackTree:
    def __init__(self):
        self.NIL  = RBNode(None, color='black')
        self.root = self.NIL

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not self.NIL:
            y.left.parent = x
        y.parent   = x.parent
        if x.parent is None:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left     = x
        x.parent   = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right is not self.NIL:
            y.right.parent = x
        y.parent    = x.parent
        if x.parent is None:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right    = x
        x.parent   = y

    def insert(self, key):
        node = RBNode(key, left=self.NIL, right=self.NIL)
        y = None
        x = self.root
        while x is not self.NIL:
            y = x
            x = x.left if node.key < x.key else x.right
        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        node.color = 'red'
        self._insert_fixup(node)

    def _insert_fixup(self, z):
        while z.parent and z.parent.color == 'red':
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y and y.color == 'red':
                    z.parent.color = 'black'
                    y.color        = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y and y.color == 'red':
                    z.parent.color = 'black'
                    y.color        = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.left_rotate(z.parent.parent)
        self.root.color = 'black'

    def inorder(self, node=None, res=None):
        if res is None:
            res = []
        if node is None:
            node = self.root
        if node is not self.NIL:
            self.inorder(node.left, res)
            res.append((node.key, node.color))
            self.inorder(node.right, res)
        return res

# Exemplo Red-Black
if __name__ == "__main__":
    rbt = RedBlackTree()
    for k in [10, 20, 30, 15, 25, 5, 1]:
        rbt.insert(k)
    print("RBT in-order (key, color):", rbt.inorder())
    # Exemplo de saída:
    # [(1, 'black'), (5, 'red'), (10, 'black'),
    #  (15, 'red'), (20, 'black'), (25, 'red'), (30, 'black')]


# # Segment Tree e Fenwick Tree (BIT)
class SegmentTree:
    """
    Segment Tree para soma em intervalo [l, r) em O(log n), com atualização em O(log n).
    """
    def __init__(self, data: list[int]):
        self.n = len(data)
        # árvore armazenada linearmente; nós folha em [n..2n)
        self.tree = [0] * (2 * self.n)
        # constrói as folhas
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        # constrói os nós internos
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, idx: int, value: int) -> None:
        """
        Atualiza data[idx] = value e reconstrói a árvore.
        """
        # atualiza a folha
        i = idx + self.n
        self.tree[i] = value
        # sobe atualizando pais
        while i > 1:
            i //= 2
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def query(self, left: int, right: int) -> int:
        """
        Retorna a soma em data[left:right] (right exclusivo).
        """
        res = 0
        l = left + self.n
        r = right + self.n
        while l < r:
            if l & 1:
                res += self.tree[l]
                l += 1
            if r & 1:
                r -= 1
                res += self.tree[r]
            l //= 2
            r //= 2
        return res


class FenwickTree:
    """
    Fenwick Tree (BIT) para soma de prefixo em O(log n), com atualização em O(log n).
    Usa índices 1..n.
    """
    def __init__(self, size: int):
        self.n = size
        self.bit = [0] * (self.n + 1)

    def update(self, idx: int, delta: int) -> None:
        """
        Adiciona delta a data[idx], onde idx é 1-based.
        """
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & -idx

    def prefix_sum(self, idx: int) -> int:
        """
        Retorna soma de data[1:idx] (inclusive), idx 1-based.
        """
        s = 0
        while idx > 0:
            s += self.bit[idx]
            idx -= idx & -idx
        return s

    def range_sum(self, left: int, right: int) -> int:
        """
        Soma em data[left:right], ambos 1-based e inclusive.
        """
        return self.prefix_sum(right) - self.prefix_sum(left - 1)


if __name__ == "__main__":
    data = [2, 5, 1, 4, 9, 3]

    # Segment Tree
    st = SegmentTree(data)
    print("Soma [1, 5):", st.query(1, 5))  # índice 1 até 4 → 5+1+4+9 = 19
    st.update(3, 6)                        # data[3]=4 → 6
    print("Após update, soma [1, 5):", st.query(1, 5))  # 5+1+6+9 = 21

    # Fenwick Tree
    ft = FenwickTree(len(data))
    # inicializa com os valores
    for i, v in enumerate(data, start=1):
        ft.update(i, v)
    print("Prefix sum até 4:", ft.prefix_sum(4))       # 2+5+1+4 = 12
    print("Range sum 2..5:", ft.range_sum(2, 5))       # 5+1+6+9 = 21


# # Trie (árvore de prefixos)
class TrieNode:
    def __init__(self):
        self.children = {}  # mapa char → TrieNode
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insere uma palavra no Trie."""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        """Retorna True se a palavra exata existe no Trie."""
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Retorna True se existe alguma palavra no Trie que comece com o prefixo."""
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True

# Exemplo de uso:
if __name__ == "__main__":
    trie = Trie()
    palavras = ["carro", "casa", "cachorro", "gato"]
    
    for p in palavras:
        trie.insert(p)
    
    # Busca exata
    print(trie.search("casa"))        # True
    print(trie.search("cas"))         # False
    
    # Busca por prefixo
    print(trie.starts_with("ca"))     # True (carro, casa, cachorro)
    print(trie.starts_with("gat"))    # True (gato)
    print(trie.starts_with("dog"))    # False


# # Union-Find (Disjoint Set)
class UnionFind:
    def __init__(self, n: int):
        """
        Inicializa n conjuntos (0 a n-1), cada um como seu próprio pai.
        Usa union by rank para otimizar.
        """
        self.parent = list(range(n))
        self.rank   = [0] * n

    def find(self, x: int) -> int:
        """
        Encontra o representante (root) do conjunto de x,
        aplicando path compression.
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Une os conjuntos de x e y.
        Retorna True se fusão ocorreu, False se já estavam no mesmo conjunto.
        """
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False
        # Une por rank: raiz de menor rank aponta para maior rank
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[ry] < self.rank[rx]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True

    def connected(self, x: int, y: int) -> bool:
        """Retorna True se x e y estão no mesmo conjunto."""
        return self.find(x) == self.find(y)

# Exemplo de uso:
if __name__ == "__main__":
    uf = UnionFind(5)  # elementos 0,1,2,3,4
    print(uf.connected(0, 1))  # False

    uf.union(0, 1)
    print(uf.connected(0, 1))  # True

    uf.union(1, 2)
    print(uf.connected(2, 0))  # True

    uf.union(3, 4)
    print(uf.connected(3, 4))  # True
    print(uf.connected(0, 4))  # False

    uf.union(2, 4)
    print(uf.connected(0, 4))  # True


# # Grafo de Intervalos (Interval Trees)
class IntervalNode:
    def __init__(self, low: int, high: int):
        self.low   = low       # início do intervalo
        self.high  = high      # fim do intervalo
        self.max   = high      # maior high na subárvore
        self.left  = None      # filho esquerdo
        self.right = None      # filho direito

def insert_interval(root: IntervalNode, low: int, high: int) -> IntervalNode:
    """
    Insere o intervalo [low, high] na Interval Tree e retorna a raiz atualizada.
    """
    if root is None:
        return IntervalNode(low, high)
    # insere em BST pelo campo low
    if low < root.low:
        root.left = insert_interval(root.left, low, high)
    else:
        root.right = insert_interval(root.right, low, high)
    # atualiza o max desse nó
    if root.max < high:
        root.max = high
    return root

def overlap(a_low: int, a_high: int, b_low: int, b_high: int) -> bool:
    """Retorna True se [a_low,a_high] e [b_low,b_high] se sobrepõem."""
    return a_low <= b_high and b_low <= a_high

def search_overlap(root: IntervalNode, low: int, high: int) -> IntervalNode:
    """
    Retorna um nó cujo intervalo se sobrepõe com [low, high], ou None se não houver.
    Usa o fato de que, se não houver sobreposição no nó atual e
    root.left.max < low, então não há sobreposição na subárvore esquerda.
    """
    node = root
    while node:
        if overlap(node.low, node.high, low, high):
            return node
        # decide descer
        if node.left and node.left.max >= low:
            node = node.left
        else:
            node = node.right
    return None

# Exemplo de uso:
if __name__ == "__main__":
    intervals = [(15,20), (10,30), (17,19), (5,20), (12,15), (30,40)]
    root = None
    for low, high in intervals:
        root = insert_interval(root, low, high)

    # busca um intervalo que se sobreponha a [14,16]
    query = (14, 16)
    res = search_overlap(root, *query)
    if res:
        print(f"Encontrou sobreposição: [{res.low},{res.high}] com {query}")
    else:
        print(f"Nenhuma sobreposição com {query}")

    # busca um intervalo que se sobreponha a [21,23]
    query2 = (21, 23)
    res2 = search_overlap(root, *query2)
    if res2:
        print(f"Encontrou sobreposição: [{res2.low},{res2.high}] com {query2}")
    else:
        print(f"Nenhuma sobreposição com {query2}")
    # Saídas esperadas:
    # Encontrou sobreposição: [15,20] com (14, 16)
    # Nenhuma sobreposição com (21, 23)
