# Algoritmos em Grafos em Ruby

# 1. DFS e BFS em grafo não-ponderado
def dfs(graph, start, visited = nil, order = nil)
  visited ||= {}
  order   ||= []
  visited[start] = true
  order << start
  Array(graph[start]).each do |nei|
    dfs(graph, nei, visited, order) unless visited[nei]
  end
  order
end

def bfs(graph, start)
  visited = { start => true }
  queue   = [start]
  order   = []
  until queue.empty?
    v = queue.shift
    order << v
    Array(graph[v]).each do |nei|
      next if visited[nei]
      visited[nei] = true
      queue << nei
    end
  end
  order
end

# 2. Dijkstra (não-negativo) – O(V²)
def dijkstra(graph, src)
  dist = Hash[graph.keys.map { |v| [v, Float::INFINITY] }]
  dist[src] = 0
  visited = {}
  until visited.size == graph.size
    u = (graph.keys - visited.keys).min_by { |v| dist[v] }
    break if u.nil? || dist[u] == Float::INFINITY
    visited[u] = true
    graph[u].each do |v, w|
      nd = dist[u] + w
      dist[v] = nd if nd < dist[v]
    end
  end
  dist
end

# 3. Bellman–Ford – permite pesos negativos, detecta ciclo negativo
def bellman_ford(edges, n, src)
  dist = Hash[(1..n).map { |i| [i, Float::INFINITY] }]
  dist[src] = 0
  (n - 1).times do
    edges.each do |u, v, w|
      nd = dist[u] + w
      dist[v] = nd if nd < dist[v]
    end
  end
  neg = edges.any? { |u, v, w| dist[u] + w < dist[v] }
  [dist, neg]
end

# 4. Floyd–Warshall – todos-pares O(n³)
def floyd_warshall(n, w)
  dist = w.map(&:dup)
  n.times do |k|
    n.times do |i|
      n.times do |j|
        nd = dist[i][k] + dist[k][j]
        dist[i][j] = nd if nd < dist[i][j]
      end
    end
  end
  dist
end

# 5. A* Search (heurística h)
def a_star(graph, start, goal, h)
  open_set = { start => true }
  g = Hash[graph.keys.map { |v| [v, Float::INFINITY] }]
  f = g.dup
  g[start] = 0
  f[start] = h[start]
  parent = {}

  until open_set.empty?
    u = open_set.keys.min_by { |v| f[v] }
    if u == goal
      path = []
      while parent.key?(u)
        path << u
        u = parent[u]
      end
      return [start] + path.reverse
    end

    open_set.delete(u)
    graph[u].each do |v, w|
      tg = g[u] + w
      if tg < g[v]
        parent[v] = u
        g[v] = tg
        f[v] = tg + h[v]
        open_set[v] = true
      end
    end
  end

  []
end

# 6. Kruskal (MST) usando Union-Find
class UF
  def initialize(n)
    @p = (0...n).to_a
    @r = Array.new(n, 0)
  end

  def find(x)
    @p[x] = find(@p[x]) unless @p[x] == x
    @p[x]
  end

  def union(x, y)
    rx, ry = find(x), find(y)
    return false if rx == ry
    if @r[rx] < @r[ry]
      rx, ry = ry, rx
    end
    @p[ry] = rx
    @r[rx] += 1 if @r[rx] == @r[ry]
    true
  end
end

def kruskal(n, edges)
  uf = UF.new(n)
  edges.sort_by { |u, v, w| w }
       .each_with_object([]) { |(u, v, w), mst|
         mst << [u, v, w] if uf.union(u, v)
       }
end

# 7. Prim (MST) – O(V²) sem heap
def prim(n, w)
  key     = Array.new(n, Float::INFINITY)
  parent  = Array.new(n, -1)
  in_mst  = Array.new(n, false)
  key[0]  = 0

  n.times do
    u = (0...n).reject { |i| in_mst[i] }.min_by { |i| key[i] }
    in_mst[u] = true
    (0...n).each do |v|
      if !in_mst[v] && w[u][v] < key[v]
        key[v]    = w[u][v]
        parent[v] = u
      end
    end
  end

  parent
end

# 8. Topological Sort (DAG)
def topological_sort(graph)
  visited = {}
  stack   = []

  visit = lambda do |v|
    visited[v] = true
    Array(graph[v]).each { |nei| visit.call(nei) unless visited[nei] }
    stack << v
  end

  graph.keys.each { |v| visit.call(v) unless visited[v] }
  stack.reverse
end

# 9. Detecção de ciclo
def has_cycle_directed(graph)
  visited = {}
  stack   = {}

  dfs = lambda do |v|
    visited[v] = true
    stack[v]   = true
    Array(graph[v]).each do |nei|
      return true if !visited[nei] && dfs.call(nei)
      return true if stack[nei]
    end
    stack.delete(v)
    false
  end

  graph.keys.any? { |v| !visited[v] && dfs.call(v) }
end

def has_cycle_undirected(graph)
  visited = {}

  dfs = lambda do |v, parent|
    visited[v] = true
    Array(graph[v]).each do |nei|
      next if nei == parent
      return true if visited[nei] || dfs.call(nei, v)
    end
    false
  end

  graph.keys.any? { |v| !visited[v] && dfs.call(v, nil) }
end

# 10. SCC – Kosaraju
def kosaraju(graph)
  visited = {}
  order   = []

  dfs1 = lambda do |v|
    visited[v] = true
    Array(graph[v]).each { |nei| dfs1.call(nei) unless visited[nei] }
    order << v
  end

  graph.keys.each { |v| dfs1.call(v) unless visited[v] }

  gt = Hash[graph.keys.map { |v| [v, []] }]
  graph.each { |u, vs| vs.each { |v| gt[v] << u } }

  visited.clear
  comps = []

  dfs2 = lambda do |v, comp|
    visited[v] = true
    comp << v
    gt[v].each { |nei| dfs2.call(nei, comp) unless visited[nei] }
  end

  order.reverse.each do |v|
    if !visited[v]
      comp = []
      dfs2.call(v, comp)
      comps << comp
    end
  end

  comps
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  g_unw = {
    1 => [2,3],
    2 => [4],
    3 => [4,5],
    4 => [],
    5 => []
  }
  puts "DFS: #{dfs(g_unw, 1).inspect}"   # e.g. [1,2,4,3,5]
  puts "BFS: #{bfs(g_unw, 1).inspect}"   # => [1,2,3,4,5]

  wg = {
    1 => [[2,2],[3,5]],
    2 => [[3,1],[4,2]],
    3 => [[4,3]],
    4 => []
  }
  p dijkstra(wg, 1)                     # => {1=>0, 2=>2, 3=>3, 4=>4}

  edges = [[1,2,4],[1,3,5],[2,3,-3],[3,4,2]]
  p bellman_ford(edges, 4, 1)           # => [{...}, false]

  INF = Float::INFINITY
  w = [
    [0,3,INF,7],
    [8,0,2,INF],
    [5,INF,0,1],
    [2,INF,INF,0]
  ]
  p floyd_warshall(4, w)

  # A* com heurística zero
  ast_g = {
    1 => [[2,1],[3,4]],
    2 => [[3,2],[4,5]],
    3 => [[4,1]],
    4 => []
  }
  h_zero = Hash[ast_g.keys.map { |v| [v, 0] }]
  p a_star(ast_g, 1, 4, h_zero)         # => [1,2,3,4]

  es = [[0,1,4],[0,2,3],[1,2,1],[1,3,2],[2,3,4],[3,4,2]]
  p kruskal(5, es)                      # e.g. [[1,2,1],[1,3,2],[3,4,2],[0,2,3]]

  w2 = [
    [0,2,INF,6,INF],
    [2,0,3,8,5],
    [INF,3,0,INF,7],
    [6,8,INF,0,9],
    [INF,5,7,9,0]
  ]
  p prim(5, w2)                         # e.g. [-1,0,1,0,1]

  dg = {1=>[2],2=>[3],3=>[1]}
  ug = {1=>[2],2=>[1,3],3=>[2]}
  p has_cycle_directed(dg)             # => true
  p has_cycle_undirected(ug)           # => false

  dag = {5=>[2,0],4=>[0,1],2=>[3],3=>[],1=>[],0=>[]}
  p topological_sort(dag)              # e.g. [4,5,1,2,3,0]

  scc_g = {1=>[2],2=>[3],3=>[1,4],4=>[5],5=>[4]}
  p kosaraju(scc_g)                    # => [[4,5],[1,3,2]]
end
