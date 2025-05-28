require 'set'

# 1. Torre de Hanói
def hanoi(n, source, aux, target)
  return if n.zero?
  hanoi(n-1, source, target, aux)
  puts "Move disk #{n} from #{source} to #{target}"
  hanoi(n-1, aux, source, target)
end

# 2. A* para 8-puzzle
def astar(start, goal)
  manhattan = ->(state) {
    dist = 0
    state.each_with_index do |v,i|
      next if v.zero?
      ti, tj = (v-1).divmod(3)
      i0, j0 = i.divmod(3)
      dist += (i0 - ti).abs + (j0 - tj).abs
    end
    dist
  }
  neighbors = ->(state) {
    i = state.index(0)
    x, y = i.divmod(3)
    [[1,0],[-1,0],[0,1],[0,-1]].each do |dx,dy|
      nx, ny = x+dx, y+dy
      if (0...3).cover?(nx) && (0...3).cover?(ny)
        ni = nx*3+ny
        new_st = state.dup
        new_st[i], new_st[ni] = new_st[ni], new_st[i]
        yield new_st
      end
    end
  }

  open_set = [start]
  g = { start => 0 }
  f = { start => manhattan.call(start) }
  parent = {}

  until open_set.empty?
    current = open_set.min_by { |s| f[s] }
    if current == goal
      path = []
      while parent.key?(current)
        path << current
        current = parent[current]
      end
      return (path << start).reverse
    end
    open_set.delete(current)
    neighbors.call(current) do |nbr|
      tg = g[current] + 1
      if tg < (g[nbr] || Float::INFINITY)
        g[nbr] = tg
        f[nbr] = tg + manhattan.call(nbr)
        parent[nbr] = current
        open_set << nbr unless open_set.include?(nbr)
      end
    end
  end

  []
end

# 3. Problema das N Rainhas
def solve_n_queens(n)
  cols, diag1, diag2 = Set.new, Set.new, Set.new
  board = Array.new(n) { Array.new(n, '.') }
  solutions = []

  backtrack = lambda do |r|
    if r == n
      solutions << board.map(&:join)
      return
    end
    (0...n).each do |c|
      next if cols.include?(c) || diag1.include?(r-c) || diag2.include?(r+c)
      cols.add(c); diag1.add(r-c); diag2.add(r+c); board[r][c] = 'Q'
      backtrack.call(r+1)
      board[r][c] = '.'; cols.delete(c); diag1.delete(r-c); diag2.delete(r+c)
    end
  end

  backtrack.call(0)
  solutions
end

# 4. Labirinto DFS/BFS
def dfs_maze(maze, start, finish)
  m, n = maze.size, maze.first.size
  visited = Array.new(m) { Array.new(n, false) }
  path = []

  dfs = lambda do |x,y|
    return false if x<0||y<0||x>=m||y>=n||visited[x][y]||maze[x][y]=='#'
    visited[x][y] = true
    path << [x,y]
    return true if [x,y]==finish
    [[1,0],[-1,0],[0,1],[0,-1]].each { |dx,dy|
      return true if dfs.call(x+dx,y+dy)
    }
    path.pop
    false
  end

  dfs.call(*start)
  path
end

def bfs_maze(maze, start, finish)
  m, n = maze.size, maze.first.size
  visited = Array.new(m) { Array.new(n, false) }
  parent = {}
  queue = [start]
  visited[start[0]][start[1]] = true

  until queue.empty?
    x, y = queue.shift
    break if [x,y] == finish
    [[1,0],[-1,0],[0,1],[0,-1]].each do |dx,dy|
      nx, ny = x+dx, y+dy
      if (0...m).cover?(nx) && (0...n).cover?(ny) && !visited[nx][ny] && maze[nx][ny]=='.'
        visited[nx][ny] = true
        parent[[nx,ny]] = [x,y]
        queue << [nx,ny]
      end
    end
  end

  return [] unless parent.key?(finish)
  path = []
  cur = finish
  until cur == start
    path << cur
    cur = parent[cur]
  end
  (path << start).reverse
end

# 5. Sudoku Solver
def solve_sudoku(board)
  find_empty = -> {
    board.each_with_index { |row,i|
      row.each_with_index { |v,j|
        return [i,j] if v.zero?
      }
    }
    nil
  }
  valid = ->(i,j,v) {
    9.times { |k|
      return false if board[i][k]==v || board[k][j]==v
    }
    bi, bj = (i/3)*3, (j/3)*3
    (bi...(bi+3)).each { |r|
      (bj...(bj+3)).each { |c|
        return false if board[r][c]==v
      }
    }
    true
  }

  empty = find_empty.call
  return true unless empty
  i, j = empty
  (1..9).each do |v|
    if valid.call(i,j,v)
      board[i][j] = v
      return true if solve_sudoku(board)
      board[i][j] = 0
    end
  end
  false
end

# 6. LRU Cache
class Node
  attr_accessor :key, :val, :prev, :next
  def initialize(key,val)
    @key,@val=key,val;@prev=@next=nil
  end
end

class LRUCache
  def initialize(capacity)
    @cap = capacity
    @cache = {}
    @head = Node.new(nil,nil)
    @tail = Node.new(nil,nil)
    @head.next = @tail
    @tail.prev = @head
  end

  def get(key)
    if @cache[key]
      node = @cache[key]
      remove(node)
      add_front(node)
      return node.val
    end
    -1
  end

  def put(key,val)
    if @cache[key]
      remove(@cache[key])
    end
    node = Node.new(key,val)
    add_front(node)
    @cache[key] = node
    if @cache.size > @cap
      lru = @tail.prev
      remove(lru)
      @cache.delete(lru.key)
    end
  end

  private

  def remove(node)
    node.prev.next = node.next
    node.next.prev = node.prev
  end

  def add_front(node)
    node.next = @head.next
    node.prev = @head
    @head.next.prev = node
    @head.next = node
  end
end

# 7. Autocomplete com Trie
class TrieNode
  attr_accessor :children, :is_end
  def initialize
    @children = {}
    @is_end = false
  end
end

class Autocomplete
  def initialize(words)
    @root = TrieNode.new
    words.each { |w| insert(w) }
  end

  def insert(word)
    node = @root
    word.each_char { |ch|
      node.children[ch] ||= TrieNode.new
      node = node.children[ch]
    }
    node.is_end = true
  end

  def suggest(prefix)
    node = @root
    prefix.each_char { |ch|
      return [] unless node.children[ch]
      node = node.children[ch]
    }
    res = []
    dfs = ->(n, path) {
      res << path if n.is_end
      n.children.each { |ch, nxt| dfs.call(nxt, path + ch) }
    }
    dfs.call(node, prefix)
    res
  end
end

# 8. Huffman Coding
class HuffmanNode
  attr_accessor :char, :freq, :left, :right
  def initialize(char=nil, freq=0, left=nil, right=nil)
    @char, @freq, @left, @right = char, freq, left, right
  end
end

def build_huffman(freqs)
  nodes = freqs.map { |c,f| HuffmanNode.new(c,f) }
  until nodes.size == 1
    nodes.sort_by!(&:freq)
    a, b = nodes.shift, nodes.shift
    nodes << HuffmanNode.new(nil, a.freq + b.freq, a, b)
  end
  nodes.first
end

def make_codes(root)
  codes = {}
  dfs = ->(node, path) {
    if node.char
      codes[node.char] = path.empty? ? "0" : path
    else
      dfs.call(node.left,  path + "0")
      dfs.call(node.right, path + "1")
    end
  }
  dfs.call(root, "")
  codes
end

# 9. Bellman-Ford com detecção de ciclo negativo
def bellman_ford(edges, n, src)
  dist = Array.new(n, Float::INFINITY)
  dist[src] = 0
  (n-1).times {
    edges.each { |u,v,w|
      dist[v] = dist[u] + w if dist[u] + w < dist[v]
    }
  }
  neg = edges.any? { |u,v,w| dist[u] + w < dist[v] }
  [dist, neg]
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  puts "--- Torre de Hanói ---"
  hanoi(3, 'A','B','C')

  puts "\n--- 8-Puzzle A* ---"
  start = [1,2,3,4,0,5,6,7,8]
  goal  = [1,2,3,4,5,6,7,8,0]
  path = astar(start, goal)
  path.each { |st| p st }

  puts "\n--- N Rainhas (n=4) ---"
  solve_n_queens(4).each { |sol| sol.each { |row| puts row }; puts }

  maze = ["S..#",".##.",".#E.","...."]
  puts "\n--- Labirinto DFS path ---"
  p dfs_maze(maze, [0,0], [2,2])
  puts "--- Labirinto BFS path ---"
  p bfs_maze(maze, [0,0], [2,2])

  board = [
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
  solve_sudoku(board)
  puts "\n--- Sudoku Solved ---"
  board.each { |r| p r }

  puts "\n--- LRU Cache ---"
  lc = LRUCache.new(2)
  lc.put(1,1); lc.put(2,2)
  p lc.get(1)     # => 1
  lc.put(3,3)
  p lc.get(2)     # => -1

  puts "\n--- Autocomplete ---"
  ac = Autocomplete.new(%w[auto autocomplete author aux banana])
  p ac.suggest("au")

  puts "\n--- Huffman Codes ---"
  freqs = {'a'=>5,'b'=>9,'c'=>12,'d'=>13,'e'=>16,'f'=>45}
  root = build_huffman(freqs)
  p make_codes(root)

  puts "\n--- Bellman-Ford ---"
  edges = [[0,1,1],[1,2,-1],[2,0,-1]]
  dist, neg = bellman_ford(edges, 3, 0)
  p dist, neg
end
