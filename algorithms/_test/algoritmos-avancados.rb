# Algoritmos Avançados em Ruby

# 1. Mo's Algorithm (queries offline)
class Mo
  def initialize(arr, queries)
    @arr   = arr
    n      = arr.size
    @block = Math.sqrt(n).to_i
    # queries: array de [l, r, idx]
    @queries = queries.sort_by { |l, r, idx| [l / @block, r] }
    @ans     = Array.new(queries.size)
  end

  def process
    cur_l = 0; cur_r = -1; cur_sum = 0
    @queries.each do |l, r, idx|
      while cur_r < r
        cur_r += 1
        cur_sum += @arr[cur_r]
      end
      while cur_r > r
        cur_sum -= @arr[cur_r]
        cur_r -= 1
      end
      while cur_l < l
        cur_sum -= @arr[cur_l]
        cur_l += 1
      end
      while cur_l > l
        cur_l -= 1
        cur_sum += @arr[cur_l]
      end
      @ans[idx] = cur_sum
    end
    @ans
  end
end

# 2. Convex Hull – Graham Scan
def cross(o, a, b)
  (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
end

def graham_scan(points)
  pts = points.uniq.sort
  return pts if pts.size < 3
  lower = []
  pts.each do |p|
    while lower.size >= 2 && cross(lower[-2], lower[-1], p) <= 0
      lower.pop
    end
    lower << p
  end
  upper = []
  pts.reverse_each do |p|
    while upper.size >= 2 && cross(upper[-2], upper[-1], p) <= 0
      upper.pop
    end
    upper << p
  end
  lower[0...-1] + upper[0...-1]
end

# 3. FFT (Cooley–Tuk)
require 'complex'
def fft(a)
  n = a.size
  # bit-reversal reorder
  j = 0
  (1...n).each do |i|
    bit = n >> 1
    while (j & bit) != 0
      j ^= bit
      bit >>= 1
    end
    j |= bit
    a[i], a[j] = a[j], a[i] if i < j
  end
  # Danielson–Lanczos
  m = 2
  while m <= n
    ang  = 2 * Math::PI / m
    wlen = Complex(Math.cos(ang), Math.sin(ang))
    (0...n).step(m) do |i|
      w = Complex(1, 0)
      (0...(m / 2)).each do |k|
        u = a[i + k]
        v = a[i + k + m/2] * w
        a[i + k]         = u + v
        a[i + k + m/2] = u - v
        w *= wlen
      end
    end
    m <<= 1
  end
  a
end

# 4. Edmonds–Karp (fluxo máximo)
def edmonds_karp(cap, s, t)
  n = cap.size
  flow = 0
  parent = Array.new(n)
  loop do
    parent.fill(-1)
    parent[s] = s
    queue = [s]; qi = 0
    while qi < queue.size && parent[t] == -1
      u = queue[qi]; qi += 1
      (0...n).each do |v|
        if cap[u][v] > 0 && parent[v] == -1
          parent[v] = u
          queue << v
        end
      end
    end
    break if parent[t] == -1
    # encontra gargalo
    aug = Float::INFINITY
    v = t
    while v != s
      u = parent[v]
      aug = [aug, cap[u][v]].min
      v = u
    end
    # aplica fluxo
    v = t
    while v != s
      u = parent[v]
      cap[u][v] -= aug
      cap[v][u] += aug
      v = u
    end
    flow += aug
  end
  flow
end

# 5. Dinic (fluxo máximo)
class Dinic
  def initialize(n)
    @n    = n
    @adj  = Array.new(n) { [] }
    @level = Array.new(n)
    @it    = Array.new(n)
  end

  def add_edge(u, v, w)
    @adj[u] << [v, w, @adj[v].size]
    @adj[v] << [u, 0, @adj[u].size - 1]
  end

  def bfs(s, t)
    @level.fill(-1)
    @level[s] = 0
    queue = [s]; qi = 0
    while qi < queue.size
      u = queue[qi]; qi += 1
      @adj[u].each do |v, w, _|
        if w > 0 && @level[v] < 0
          @level[v] = @level[u] + 1
          queue << v
        end
      end
    end
    @level[t] >= 0
  end

  def dfs(u, t, f)
    return f if u == t
    while @it[u] < @adj[u].size
      v, w, rev = @adj[u][@it[u]]
      if w > 0 && @level[v] == @level[u] + 1
        ret = dfs(v, t, [f, w].min)
        if ret > 0
          @adj[u][@it[u]][1] -= ret
          @adj[v][rev][1]       += ret
          return ret
        end
      end
      @it[u] += 1
    end
    0
  end

  def max_flow(s, t)
    flow = 0
    inf = Float::INFINITY
    while bfs(s, t)
      @it.fill(0)
      while (f = dfs(s, t, inf)) > 0
        flow += f
      end
    end
    flow
  end
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  # Mo's Algorithm
  arr = [1,2,3,4,5,6,7,8,9]
  qs  = [[0,2,0], [4,7,1], [1,5,2]]
  p Mo.new(arr, qs).process      # => [6, 26, 20]

  # Convex Hull
  pts = [[0,0],[1,1],[2,2],[2,0],[0,2],[1,2],[2,1]]
  p graham_scan(pts)             # => [[0,0],[2,0],[2,2],[0,2]]

  # FFT
  data = (0...8).map { |x| Complex(x, 0) }
  p fft(data.dup)

  # Edmonds–Karp
  cap = [
    [0,3,2,0],
    [0,0,5,2],
    [0,0,0,3],
    [0,0,0,0]
  ]
  p edmonds_karp(cap.map(&:dup), 0, 3)  # => 4

  # Dinic
  d = Dinic.new(4)
  d.add_edge(0,1,3)
  d.add_edge(0,2,2)
  d.add_edge(1,2,5)
  d.add_edge(1,3,2)
  d.add_edge(2,3,3)
  p d.max_flow(0,3)                   # => 4
end
