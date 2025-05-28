# Árvores Balanceadas e Estruturas Avançadas em Ruby

# 1. AVL Tree
class AVLNode
  attr_accessor :key, :height, :left, :right
  def initialize(key)
    @key    = key
    @height = 1
    @left   = nil
    @right  = nil
  end
end

def avl_height(node)
  node ? node.height : 0
end

def avl_update_height(node)
  node.height = 1 + [avl_height(node.left), avl_height(node.right)].max
end

def avl_balance(node)
  avl_height(node.left) - avl_height(node.right)
end

def avl_right_rotate(y)
  x  = y.left
  t2 = x.right
  x.right = y
  y.left  = t2
  avl_update_height(y)
  avl_update_height(x)
  x
end

def avl_left_rotate(x)
  y  = x.right
  t2 = y.left
  y.left  = x
  x.right = t2
  avl_update_height(x)
  avl_update_height(y)
  y
end

def avl_insert(node, key)
  return AVLNode.new(key) unless node
  if key < node.key
    node.left  = avl_insert(node.left, key)
  else
    node.right = avl_insert(node.right, key)
  end
  avl_update_height(node)
  balance = avl_balance(node)
  # LL
  return avl_right_rotate(node) if balance > 1 && key < node.left.key
  # RR
  return avl_left_rotate(node)  if balance < -1 && key > node.right.key
  # LR
  if balance > 1 && key > node.left.key
    node.left = avl_left_rotate(node.left)
    return avl_right_rotate(node)
  end
  # RL
  if balance < -1 && key < node.right.key
    node.right = avl_right_rotate(node.right)
    return avl_left_rotate(node)
  end
  node
end

def avl_inorder(node, res = [])
  return res unless node
  avl_inorder(node.left, res)
  res << node.key
  avl_inorder(node.right, res)
  res
end

# 2. Red-Black Tree
class RBNode
  attr_accessor :key, :color, :left, :right, :parent
  def initialize(key, color = :red, nil_node = nil)
    @key    = key
    @color  = color
    @left   = nil_node
    @right  = nil_node
    @parent = nil_node
  end
end

class RedBlackTree
  attr_reader :root, :nil_node

  def initialize
    @nil_node = RBNode.new(nil, :black, nil)  # sentinel
    @root     = @nil_node
  end

  def left_rotate(x)
    y = x.right
    x.right = y.left
    y.left.parent = x if y.left != nil_node
    y.parent = x.parent
    if x.parent == nil_node
      @root = y
    elsif x == x.parent.left
      x.parent.left = y
    else
      x.parent.right = y
    end
    y.left   = x
    x.parent = y
  end

  def right_rotate(x)
    y = x.left
    x.left = y.right
    y.right.parent = x if y.right != nil_node
    y.parent = x.parent
    if x.parent == nil_node
      @root = y
    elsif x == x.parent.right
      x.parent.right = y
    else
      x.parent.left = y
    end
    y.right  = x
    x.parent = y
  end

  def insert(key)
    z = RBNode.new(key, :red, nil_node)
    y = nil_node
    x = root
    while x != nil_node
      y = x
      x = (z.key < x.key ? x.left : x.right)
    end
    z.parent = y
    if y == nil_node
      @root = z
    elsif z.key < y.key
      y.left = z
    else
      y.right = z
    end
    z.left = nil_node
    z.right = nil_node
    insert_fixup(z)
  end

  def insert_fixup(z)
    while z.parent.color == :red
      if z.parent == z.parent.parent.left
        y = z.parent.parent.right
        if y.color == :red
          z.parent.color = :black
          y.color        = :black
          z.parent.parent.color = :red
          z = z.parent.parent
        else
          if z == z.parent.right
            z = z.parent
            left_rotate(z)
          end
          z.parent.color        = :black
          z.parent.parent.color = :red
          right_rotate(z.parent.parent)
        end
      else
        y = z.parent.parent.left
        if y.color == :red
          z.parent.color = :black
          y.color        = :black
          z.parent.parent.color = :red
          z = z.parent.parent
        else
          if z == z.parent.left
            z = z.parent
            right_rotate(z)
          end
          z.parent.color        = :black
          z.parent.parent.color = :red
          left_rotate(z.parent.parent)
        end
      end
    end
    root.color = :black
  end

  def inorder(node = root, res = [])
    return res if node == nil_node
    inorder(node.left, res)
    res << [node.key, node.color]
    inorder(node.right, res)
    res
  end
end

# 3. Segment Tree (soma em intervalo)
class SegmentTree
  def initialize(data)
    @n    = data.size
    @tree = Array.new(2 * @n, 0)
    @n.times { |i| @tree[@n + i] = data[i] }
    (@n-1).downto(1) { |i| @tree[i] = @tree[2*i] + @tree[2*i+1] }
  end

  def update(idx, value)
    i = idx + @n
    @tree[i] = value
    while i > 1
      i /= 2
      @tree[i] = @tree[2*i] + @tree[2*i+1]
    end
  end

  def query(left, right)
    res = 0
    l = left + @n; r = right + @n
    while l < r
      res += @tree[l] if (l & 1).positive?
      l += 1 if (l & 1).positive?
      r -= 1 if (r & 1).positive?
      res += @tree[r] if (r & 1).positive?
      l >>= 1; r >>= 1
    end
    res
  end
end

# 4. Fenwick Tree (BIT)
class FenwickTree
  def initialize(size)
    @n   = size
    @bit = Array.new(@n+1, 0)
  end

  def update(idx, delta)
    while idx <= @n
      @bit[idx] += delta
      idx += idx & -idx
    end
  end

  def prefix_sum(idx)
    s = 0
    while idx > 0
      s += @bit[idx]
      idx -= idx & -idx
    end
    s
  end

  def range_sum(left, right)
    prefix_sum(right) - prefix_sum(left-1)
  end
end

# 5. Trie
class TrieNode
  attr_accessor :children, :is_end
  def initialize
    @children = {}
    @is_end   = false
  end
end

class Trie
  def initialize
    @root = TrieNode.new
  end

  def insert(word)
    node = @root
    word.each_char do |ch|
      node.children[ch] ||= TrieNode.new
      node = node.children[ch]
    end
    node.is_end = true
  end

  def search(word)
    node = @root
    word.each_char do |ch|
      return false unless node.children[ch]
      node = node.children[ch]
    end
    node.is_end
  end

  def starts_with(prefix)
    node = @root
    prefix.each_char do |ch|
      return false unless node.children[ch]
      node = node.children[ch]
    end
    true
  end
end

# 6. Union-Find (Disjoint Set)
class UnionFind
  def initialize(n)
    @parent = (0...n).to_a
    @rank   = Array.new(n, 0)
  end

  def find(x)
    @parent[x] = find(@parent[x]) while @parent[x] != x
    @parent[x]
  end

  def union(x, y)
    rx = find(x); ry = find(y)
    return false if rx == ry
    if @rank[rx] < @rank[ry]
      @parent[rx] = ry
    elsif @rank[ry] < @rank[rx]
      @parent[ry] = rx
    else
      @parent[ry] = rx
      @rank[rx] += 1
    end
    true
  end

  def connected?(x, y)
    find(x) == find(y)
  end
end

# 7. Interval Tree
class IntervalNode
  attr_accessor :low, :high, :max, :left, :right
  def initialize(low, high)
    @low   = low
    @high  = high
    @max   = high
    @left  = nil
    @right = nil
  end
end

def insert_interval(root, low, high)
  return IntervalNode.new(low, high) unless root
  if low < root.low
    root.left  = insert_interval(root.left, low, high)
  else
    root.right = insert_interval(root.right, low, high)
  end
  root.max = [root.max, high].max
  root
end

def overlap?(a_low, a_high, b_low, b_high)
  a_low <= b_high && b_low <= a_high
end

def search_overlap(root, low, high)
  node = root
  while node
    return node if overlap?(node.low, node.high, low, high)
    if node.left && node.left.max >= low
      node = node.left
    else
      node = node.right
    end
  end
  nil
end

# Demonstrações de uso
if __FILE__ == $PROGRAM_NAME
  # AVL
  keys = [10,20,30,40,50,25]
  root_avl = nil
  keys.each { |k| root_avl = avl_insert(root_avl, k) }
  p avl_inorder(root_avl)  # => [10,20,25,30,40,50]

  # Red-Black
  rbt = RedBlackTree.new
  [10,20,30,15,25,5,1].each { |k| rbt.insert(k) }
  p rbt.inorder          # => [[1,:black],[5,:red],...,[30,:black]]

  # Segment Tree
  data = [2,5,1,4,9,3]
  st = SegmentTree.new(data)
  p st.query(1,5)        # => 19
  st.update(3,6)
  p st.query(1,5)        # => 21

  # Fenwick Tree
  ft = FenwickTree.new(data.size)
  data.each_with_index { |v,i| ft.update(i+1, v) }
  p ft.range_sum(2,5)    # => 21

  # Trie
  trie = Trie.new
  %w[carro casa cachorro gato].each { |w| trie.insert(w) }
  p trie.search("casa")      # => true
  p trie.starts_with("ca")    # => true

  # Union-Find
  uf = UnionFind.new(5)
  uf.union(0,1); uf.union(1,2)
  p uf.connected?(0,2)       # => true
  p uf.connected?(3,4)       # => false

  # Interval Tree
  intervals = [[15,20],[10,30],[17,19],[5,20],[12,15],[30,40]]
  root_it = nil
  intervals.each { |l,h| root_it = insert_interval(root_it, l, h) }
  res = search_overlap(root_it, 14,16)
  p [res.low,res.high] if res  # => [15,20]
  p search_overlap(root_it, 21,23) # => nil
end
