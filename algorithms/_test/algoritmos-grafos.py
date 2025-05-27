# Algoritmos em Grafos
# # DFS, BFS
# 1. DFS e BFS em grafo não-ponderado

def dfs(graph: dict[int, list[int]], start: int, visited=None) -> list[int]:
    """
    Depth-First Search recursiva.
    graph: adjacência {v: [u1, u2, ...]}
    """
    if visited is None:
        visited = set()
    visited.add(start)
    order = [start]
    for nei in graph.get(start, []):
        if nei not in visited:
            order += dfs(graph, nei, visited)
    return order

def bfs(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    Breadth-First Search usando lista como fila.
    """
    visited = {start}
    queue = [start]
    order = []
    idx = 0
    while idx < len(queue):
        v = queue[idx]; idx += 1
        order.append(v)
        for nei in graph.get(v, []):
            if nei not in visited:
                visited.add(nei)
                queue.append(nei)
    return order

# Exemplo:
if __name__ == "__main__":
    g = {
        1: [2, 3],
        2: [4],
        3: [4, 5],
        4: [],
        5: []
    }
    print("DFS:", dfs(g, 1))  # e.g. [1,2,4,3,5]
    print("BFS:", bfs(g, 1))  # [1,2,3,4,5]


# # Dijkstra e Bellman-Ford (caminho mínimo)
# 2. Dijkstra (não-negativo) – O(V²)

def dijkstra(graph: dict[int, list[tuple[int,int]]], src: int) -> dict[int,int]:
    """
    graph: {v: [(u, w), ...]} com w ≥ 0
    Retorna distâncias mínimas de src a todos.
    """
    dist = {v: float('inf') for v in graph}
    dist[src] = 0
    visited = set()
    while len(visited) < len(graph):
        # escolhe não visitado com menor dist
        u = min((v for v in graph if v not in visited), key=lambda x: dist[x], default=None)
        if u is None or dist[u] == float('inf'):
            break
        visited.add(u)
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist

# Exemplo:
if __name__ == "__main__":
    wg = {
        1: [(2,2),(3,5)],
        2: [(3,1),(4,2)],
        3: [(4,3)],
        4: []
    }
    print(dijkstra(wg, 1))  # {1:0,2:2,3:3,4:4}


# # Floyd-Warshall, A*
# 3. Bellman–Ford – permite pesos negativos, detecta ciclo negativo

def bellman_ford(graph: list[tuple[int,int,int]], n: int, src: int) -> tuple[dict[int,int], bool]:
    """
    graph: lista de arestas (u, v, w)
    n: número de vértices (1..n)
    Retorna (dist, has_negative_cycle)
    """
    dist = {i: float('inf') for i in range(1, n+1)}
    dist[src] = 0
    for _ in range(n-1):
        for u, v, w in graph:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    # verifica ciclo negativo
    neg = False
    for u, v, w in graph:
        if dist[u] + w < dist[v]:
            neg = True
            break
    return dist, neg

# Exemplo:
if __name__ == "__main__":
    edges = [(1,2,4),(1,3,5),(2,3,-3),(3,4,2)]
    dist, neg = bellman_ford(edges, 4, 1)
    print(dist, "neg_cycle?", neg)  # {1:0,2:4,3:1,4:3} False


# 4. Floyd–Warshall – todos-pares O(n³)

def floyd_warshall(n: int, w: list[list[float]]) -> list[list[float]]:
    """
    n: número de vértices (0..n-1)
    w: matriz de adjacência com w[i][j]=peso ou inf
    Retorna distância[i][j] mínima.
    """
    dist = [row[:] for row in w]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

# Exemplo:
if __name__ == "__main__":
    INF = float('inf')
    W = [
        [0,3,INF,7],
        [8,0,2,INF],
        [5,INF,0,1],
        [2,INF,INF,0]
    ]
    print(floyd_warshall(4, W))


# 5. A* Search (heurística h)

def a_star(graph: dict[int, list[tuple[int,int]]],
           start: int, goal: int,
           h: dict[int,int]) -> list[int]:
    """
    graph: {v: [(u,w),...]}
    h: heurística h[v] estimativa até goal
    Retorna caminho de start a goal ou [].
    """
    open_set = {start}
    g = {v: float('inf') for v in graph}
    g[start] = 0
    f = {v: float('inf') for v in graph}
    f[start] = h[start]
    parent = {}
    while open_set:
        u = min(open_set, key=lambda x: f[x])
        if u == goal:
            # reconstrói caminho
            path = []
            while u in parent:
                path.append(u)
                u = parent[u]
            return [start] + path[::-1]
        open_set.remove(u)
        for v, w in graph[u]:
            tentative = g[u] + w
            if tentative < g[v]:
                parent[v] = u
                g[v] = tentative
                f[v] = tentative + h[v]
                open_set.add(v)
    return []

# Exemplo:
if __name__ == "__main__":
    graph = {
        1: [(2,1),(3,4)],
        2: [(3,2),(4,5)],
        3: [(4,1)],
        4: []
    }
    # heurística trivial (zero)
    h = {v: 0 for v in graph}
    print(a_star(graph, 1, 4, h))  # [1,2,3,4]


# # Kruskal e Prim (MST)
# 6. Kruskal (MST) usando Union-Find

class UF:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0]*n
    def find(self,x):
        if self.p[x]!=x: self.p[x]=self.find(self.p[x])
        return self.p[x]
    def union(self,x,y):
        rx,ry=self.find(x),self.find(y)
        if rx==ry: return False
        if self.r[rx]<self.r[ry]: rx,ry=ry,rx
        self.p[ry]=rx
        if self.r[rx]==self.r[ry]: self.r[rx]+=1
        return True

def kruskal(n: int, edges: list[tuple[int,int,int]]) -> list[tuple[int,int,int]]:
    """
    n vértices 0..n-1, edges (u,v,w).
    Retorna lista de arestas MST.
    """
    mst = []
    uf = UF(n)
    for u,v,w in sorted(edges, key=lambda x: x[2]):
        if uf.union(u,v):
            mst.append((u,v,w))
    return mst

# Exemplo:
if __name__ == "__main__":
    es = [(0,1,4),(0,2,3),(1,2,1),(1,3,2),(2,3,4),(3,4,2)]
    print(kruskal(5, es))
    # e.g. [(1,2,1),(1,3,2),(3,4,2),(0,2,3)]


# 7. Prim (MST) – O(V²) sem heap

def prim(n: int, w: list[list[float]]) -> list[int]:
    """
    n vértices 0..n-1, w matriz de pesos (inf se não adj).
    Retorna parent[v] da árvore.
    """
    import math
    key = [math.inf]*n
    parent = [-1]*n
    in_mst = [False]*n
    key[0] = 0
    for _ in range(n):
        # escolhe v não em MST com menor key
        u = min((i for i in range(n) if not in_mst[i]), key=lambda x: key[x])
        in_mst[u] = True
        for v in range(n):
            if not in_mst[v] and w[u][v] < key[v]:
                key[v] = w[u][v]
                parent[v] = u
    return parent

# Exemplo:
if __name__ == "__main__":
    INF = float('inf')
    W = [
        [0,2,INF,6,INF],
        [2,0,3,8,5],
        [INF,3,0,INF,7],
        [6,8,INF,0,9],
        [INF,5,7,9,0]
    ]
    print(prim(5, W))  # e.g. [-1,0,1,0,1]


# # Topological Sort
# 8. Topological Sort (grafo dirigido acíclico)

def topological_sort(graph: dict[int,list[int]]) -> list[int]:
    visited = set()
    stack = []
    def dfs(v):
        visited.add(v)
        for nei in graph.get(v, []):
            if nei not in visited:
                dfs(nei)
        stack.append(v)
    for v in graph:
        if v not in visited:
            dfs(v)
    return stack[::-1]

# Exemplo:
if __name__ == "__main__":
    dg = {5:[2,0],4:[0,1],2:[3],3:[],1:[],0:[]}
    print(topological_sort(dg))  # e.g. [4,5,1,2,3,0]


# # Detecção de ciclo (grafo dirigido e não dirigido)
# 9. Detecção de ciclo
# 9a. Grafo dirigido
def has_cycle_directed(graph: dict[int,list[int]]) -> bool:
    visited = set()
    stack = set()
    def dfs(v):
        visited.add(v)
        stack.add(v)
        for nei in graph.get(v, []):
            if nei not in visited:
                if dfs(nei): return True
            elif nei in stack:
                return True
        stack.remove(v)
        return False
    return any(dfs(v) for v in graph if v not in visited)

# 9b. Grafo não-dirigido
def has_cycle_undirected(graph: dict[int,list[int]]) -> bool:
    visited = set()
    def dfs(v, parent):
        visited.add(v)
        for nei in graph.get(v, []):
            if nei not in visited:
                if dfs(nei, v): return True
            elif nei != parent:
                return True
        return False
    return any(dfs(v, -1) for v in graph if v not in visited)

# Exemplos:
if __name__ == "__main__":
    dg = {1:[2],2:[3],3:[1]}      # ciclo
    ug = {1:[2],2:[1,3],3:[2]}    # sem ciclo
    print(has_cycle_directed(dg))     # True
    print(has_cycle_undirected(ug))   # False


# # SCC (Kosaraju/Tarjan)
# 10. SCC – Kosaraju

def kosaraju(graph: dict[int,list[int]]) -> list[list[int]]:
    """
    Retorna lista de componentes fortemente conectados.
    """
    visited = set()
    order = []
    def dfs1(v):
        visited.add(v)
        for nei in graph.get(v, []):
            if nei not in visited:
                dfs1(nei)
        order.append(v)

    for v in graph:
        if v not in visited:
            dfs1(v)

    # transposto
    gt = {v: [] for v in graph}
    for u in graph:
        for v in graph[u]:
            gt[v].append(u)

    visited.clear()
    comps = []
    def dfs2(v, comp):
        visited.add(v)
        comp.append(v)
        for nei in gt.get(v, []):
            if nei not in visited:
                dfs2(nei, comp)

    for v in reversed(order):
        if v not in visited:
            comp = []
            dfs2(v, comp)
            comps.append(comp)
    return comps

# Exemplo:
if __name__ == "__main__":
    g = {1:[2],2:[3],3:[1,4],4:[5],5:[4]}
    print(kosaraju(g))  # [[4,5], [1,3,2]]
