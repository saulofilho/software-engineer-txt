# Algoritmos Avançados
# # Algoritmo de Mo (queries offline)
# 1. Algoritmo de Mo (queries offline sem usar math.sqrt nem collections)
class Mo:
    def __init__(self, arr, queries):
        """
        arr: lista de inteiros
        queries: lista de tuplas (l, r, idx)
        idx é a posição original da query
        """
        self.arr = arr
        n = len(arr)
        # bloco de tamanho ~√n usando **0.5
        self.block = int(n ** 0.5)
        # ordena por (bloco de l, r)
        self.queries = sorted(queries, key=lambda x: (x[0]//self.block, x[1]))
        self.ans = [0] * len(queries)

    def process(self):
        cur_l, cur_r, cur_sum = 0, -1, 0
        for l, r, idx in self.queries:
            # estende/diminui a direita
            while cur_r < r:
                cur_r += 1
                cur_sum += self.arr[cur_r]
            while cur_r > r:
                cur_sum -= self.arr[cur_r]
                cur_r -= 1
            # estende/diminui a esquerda
            while cur_l < l:
                cur_sum -= self.arr[cur_l]
                cur_l += 1
            while cur_l > l:
                cur_l -= 1
                cur_sum += self.arr[cur_l]
            self.ans[idx] = cur_sum
        return self.ans

# Exemplo
if __name__ == "__main__":
    arr = [1,2,3,4,5,6,7,8,9]
    # queries: soma de arr[l..r]
    qs = [(0,2,0),(4,7,1),(1,5,2)]
    mo = Mo(arr, qs)
    print(mo.process())  # [6,26,20]


# # Convex Hull (Graham Scan, Jarvis March)
# 2. Convex Hull – Graham Scan sem imports
def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def graham_scan(points):
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts
    # monta lower
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    # monta upper
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    # remove duplicatas de ponta
    return lower[:-1] + upper[:-1]

# Exemplo
if __name__ == "__main__":
    pts = [(0,0),(1,1),(2,2),(2,0),(0,2),(1,2),(2,1)]
    print(graham_scan(pts))  # [(0,0),(2,0),(2,2),(0,2)]


# # FFT (Fast Fourier Transform)
# 3. FFT Cooley–Tuk (usa apenas math do stdlib para cos/sin)
import math

def fft(a):
    n = len(a)
    # reordenação por bit-reversal
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    # Danielson–Lanczos
    m = 2
    while m <= n:
        ang = 2 * math.pi / m
        wlen = complex(math.cos(ang), math.sin(ang))
        for i in range(0, n, m):
            w = 1+0j
            for k in range(i, i + m//2):
                u = a[k]
                v = a[k + m//2] * w
                a[k] = u + v
                a[k + m//2] = u - v
                w *= wlen
        m <<= 1
    return a

# Exemplo
if __name__ == "__main__":
    data = [complex(x, 0) for x in range(8)]
    print(fft(data.copy()))


# # Algoritmo de Dínic e Edmonds-Karp (fluxo máximo)
# 4. Fluxo Máximo – Edmonds–Karp e Dinic sem collections nem heapq

# Edmonds–Karp
def edmonds_karp(cap, s, t):
    n = len(cap)
    flow = 0
    parent = [-1]*n
    while True:
        # BFS usando lista como fila
        for i in range(n):
            parent[i] = -1
        parent[s] = s
        queue = [s]
        qi = 0
        while qi < len(queue) and parent[t] == -1:
            u = queue[qi]; qi += 1
            for v in range(n):
                if cap[u][v] > 0 and parent[v] == -1:
                    parent[v] = u
                    queue.append(v)
        if parent[t] == -1:
            break
        # encontra gargalo
        aug = float('inf')
        v = t
        while v != s:
            u = parent[v]
            if cap[u][v] < aug:
                aug = cap[u][v]
            v = u
        # aplica fluxo
        v = t
        while v != s:
            u = parent[v]
            cap[u][v] -= aug
            cap[v][u] += aug
            v = u
        flow += aug
    return flow

# Dinic
class Dinic:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.level = [0]*n
        self.it = [0]*n

    def add_edge(self, u, v, w):
        self.adj[u].append([v, w, len(self.adj[v])])
        self.adj[v].append([u, 0, len(self.adj[u]) - 1])

    def bfs(self, s, t):
        for i in range(self.n):
            self.level[i] = -1
        self.level[s] = 0
        queue = [s]; qi = 0
        while qi < len(queue):
            u = queue[qi]; qi += 1
            for v, w, _ in self.adj[u]:
                if w > 0 and self.level[v] < 0:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)
        return self.level[t] >= 0

    def dfs(self, u, t, f):
        if u == t:
            return f
        for i in range(self.it[u], len(self.adj[u])):
            v, w, rev = self.adj[u][i]
            if w > 0 and self.level[v] == self.level[u] + 1:
                ret = self.dfs(v, t, f if f < w else w)
                if ret > 0:
                    self.adj[u][i][1] -= ret
                    self.adj[v][rev][1] += ret
                    return ret
            self.it[u] += 1
        return 0

    def max_flow(self, s, t):
        flow = 0
        INF = float('inf')
        while self.bfs(s, t):
            self.it = [0]*self.n
            f = self.dfs(s, t, INF)
            while f:
                flow += f
                f = self.dfs(s, t, INF)
        return flow

# Exemplos
if __name__ == "__main__":
    cap = [
        [0,3,2,0],
        [0,0,5,2],
        [0,0,0,3],
        [0,0,0,0]
    ]
    print(edmonds_karp([row[:] for row in cap], 0, 3))  # 4

    d = Dinic(4)
    d.add_edge(0,1,3)
    d.add_edge(0,2,2)
    d.add_edge(1,2,5)
    d.add_edge(1,3,2)
    d.add_edge(2,3,3)
    print(d.max_flow(0,3))  # 4
