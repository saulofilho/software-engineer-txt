# # Torre de Hanói
def hanoi(n, source, aux, target):
    """
    Move n discos de 'source' para 'target' usando 'aux' como auxiliar.
    Imprime cada movimento.
    """
    if n == 0:
        return
    # Move n-1 discos de source → aux
    hanoi(n-1, source, target, aux)
    # Move o disco n de source → target
    print(f"Mover disco {n} de {source} para {target}")
    # Move os n-1 discos de aux → target
    hanoi(n-1, aux, source, target)

if __name__ == "__main__":
    hanoi(3, 'A', 'B', 'C')


# # Jogo dos 8 (8-puzzle)
def astar(start, goal):
    """
    Usa A* com heurística Manhattan para o 8-puzzle.
    Representa estados como tuplas de 9 inteiros (0=buraco).
    """
    def manhattan(state):
        dist = 0
        for i, v in enumerate(state):
            if v == 0: continue
            target_i = (v - 1) // 3
            target_j = (v - 1) % 3
            i0, j0 = divmod(i, 3)
            dist += abs(i0 - target_i) + abs(j0 - target_j)
        return dist

    def neighbors(state):
        i = state.index(0)
        x, y = divmod(i, 3)
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                ni = nx*3 + ny
                lst = list(state)
                lst[i], lst[ni] = lst[ni], lst[i]
                yield tuple(lst)

    open_set = [start]
    g = {start: 0}
    f = {start: manhattan(start)}
    parent = {}
    while open_set:
        # escolhe nó com menor f
        current = min(open_set, key=lambda s: f[s])
        if current == goal:
            # reconstrói caminho
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            return list(reversed(path + [goal]))
        open_set.remove(current)
        for nbr in neighbors(current):
            tentative = g[current] + 1
            if tentative < g.get(nbr, float('inf')):
                parent[nbr] = current
                g[nbr] = tentative
                f[nbr] = tentative + manhattan(nbr)
                if nbr not in open_set:
                    open_set.append(nbr)
    return []

if __name__ == "__main__":
    start = (1,2,3,4,0,5,6,7,8)
    goal  = (1,2,3,4,5,6,7,8,0)
    path = astar(start, goal)
    for state in path:
        print(state)


# # Problema das 8 Rainhas
def solve_n_queens(n):
    cols = set()
    diag1 = set()  # r-c
    diag2 = set()  # r+c
    board = [['.' for _ in range(n)] for _ in range(n)]
    solutions = []

    def backtrack(r):
        if r == n:
            solutions.append([''.join(row) for row in board])
            return
        for c in range(n):
            if c in cols or (r-c) in diag1 or (r+c) in diag2:
                continue
            cols.add(c); diag1.add(r-c); diag2.add(r+c)
            board[r][c] = 'Q'
            backtrack(r+1)
            board[r][c] = '.'
            cols.remove(c); diag1.remove(r-c); diag2.remove(r+c)

    backtrack(0)
    return solutions

if __name__ == "__main__":
    for sol in solve_n_queens(8):
        for row in sol:
            print(row)
        print()


# # Labirinto (DFS/BFS)
# Representa o labirinto como lista de strings, '#' muro, '.' caminho.
def dfs_maze(maze, start, end):
    m, n = len(maze), len(maze[0])
    visited = [[False]*n for _ in range(m)]
    path = []

    def dfs(x,y):
        if not (0<=x<m and 0<=y<n) or visited[x][y] or maze[x][y]=='#':
            return False
        visited[x][y] = True
        path.append((x,y))
        if (x,y) == end:
            return True
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            if dfs(x+dx,y+dy):
                return True
        path.pop()
        return False

    dfs(*start)
    return path

def bfs_maze(maze, start, end):
    m, n = len(maze), len(maze[0])
    visited = [[False]*n for _ in range(m)]
    parent = {}
    queue = [start]
    visited[start[0]][start[1]] = True
    qi = 0
    while qi < len(queue):
        x,y = queue[qi]; qi+=1
        if (x,y) == end:
            break
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny = x+dx,y+dy
            if 0<=nx<m and 0<=ny<n and not visited[nx][ny] and maze[nx][ny]=='.':
                visited[nx][ny] = True
                parent[(nx,ny)] = (x,y)
                queue.append((nx,ny))
    # reconstrói caminho
    if end not in parent:
        return []
    path = []
    cur = end
    while cur != start:
        path.append(cur)
        cur = parent[cur]
    path.append(start)
    return list(reversed(path))


if __name__ == "__main__":
    lab = [
        "S..#",
        ".##.",
        ".#E.",
        "...."
    ]
    start = (0,0)
    end   = (2,2)
    print("DFS path:", dfs_maze(lab, start, end))
    print("BFS path:", bfs_maze(lab, start, end))


# # Sudoku Solver
def solve_sudoku(board):
    def find_empty():
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def valid(i, j, v):
        for k in range(9):
            if board[i][k]==v or board[k][j]==v:
                return False
        bi, bj = (i//3)*3, (j//3)*3
        for r in range(bi,bi+3):
            for c in range(bj,bj+3):
                if board[r][c]==v:
                    return False
        return True

    empty = find_empty()
    if not empty:
        return True
    i,j = empty
    for v in range(1,10):
        if valid(i,j,v):
            board[i][j] = v
            if solve_sudoku(board):
                return True
            board[i][j] = 0
    return False

if __name__ == "__main__":
    puzzle = [
      [5,3,0,0,7,0,0,0,0],
      [6,0,0,1,9,5,0,0,0],
      [0,9,8,0,0,0,0,6,0],
      [8,0,0,0,6,0,0,0,3],
      [4,0,0,8,0,3,0,0,1],
      [7,0,0,0,2,0,0,0,6],
      [0,6,0,0,0,0,2,8,0],
      [0,0,0,4,1,9,0,0,5],
      [0,0,0,0,8,0,0,7,9],
    ]
    solve_sudoku(puzzle)
    for row in puzzle:
        print(row)


# # LRU Cache
class Node:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}  # key → node
        # sentinelas
        self.head = Node(0,0)
        self.tail = Node(0,0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        p = node.prev; n = node.next
        p.next = n; n.prev = p

    def _add_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_front(node)
            return node.val
        return -1

    def put(self, key, val):
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, val)
        self._add_front(node)
        self.cache[key] = node
        if len(self.cache) > self.cap:
            # remove LRU (no fim)
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

if __name__ == "__main__":
    c = LRUCache(2)
    c.put(1,1)
    c.put(2,2)
    print(c.get(1))  # 1
    c.put(3,3)       # evict key=2
    print(c.get(2))  # -1


# # Autocompletar com Trie
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Autocomplete:
    def __init__(self, words):
        self.root = TrieNode()
        for w in words:
            node = self.root
            for ch in w:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.is_end = True

    def suggest(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        results = []
        self._dfs(node, prefix, results)
        return results

    def _dfs(self, node, path, res):
        if node.is_end:
            res.append(path)
        for ch, nxt in node.children.items():
            self._dfs(nxt, path+ch, res)

if __name__ == "__main__":
    ac = Autocomplete(["auto","autocomplete","author","aux","banana"])
    print(ac.suggest("au"))  # ['auto','autocomplete','author','aux']


# # Algoritmo de compressão (Huffman)
class Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char, self.freq = char, freq
        self.left, self.right = left, right

def build_huffman(freqs):
    nodes = [Node(c,f) for c,f in freqs.items()]
    while len(nodes) > 1:
        nodes.sort(key=lambda n: n.freq)
        a, b = nodes.pop(0), nodes.pop(0)
        nodes.append(Node(None, a.freq+b.freq, a, b))
    return nodes[0]

def make_codes(root):
    codes = {}
    def dfs(node, path):
        if node.char is not None:
            codes[node.char] = path or "0"
        else:
            dfs(node.left,  path+"0")
            dfs(node.right, path+"1")
    dfs(root, "")
    return codes

if __name__ == "__main__":
    freqs = {'a':5,'b':9,'c':12,'d':13,'e':16,'f':45}
    root = build_huffman(freqs)
    print(make_codes(root))


# # Encontrar ciclos negativos (Bellman-Ford)
def bellman_ford(edges, n, src):
    """
    edges: lista de (u,v,w)
    n: # de vértices 0..n-1
    src: vértice fonte
    Retorna (dist, has_negative_cycle)
    """
    dist = [float('inf')]*n
    dist[src] = 0
    for _ in range(n-1):
        for u,v,w in edges:
            if dist[u]+w < dist[v]:
                dist[v] = dist[u]+w
    # check negative cycle
    neg = False
    for u,v,w in edges:
        if dist[u]+w < dist[v]:
            neg = True
            break
    return dist, neg

if __name__ == "__main__":
    e = [(0,1,1),(1,2,-1),(2,0,-1)]
    d, has_neg = bellman_ford(e, 3, 0)
    print(d, "neg_cycle?", has_neg)  # [0,1,0] neg_cycle? True
