# Árvores e Algoritmos Relacionados em Ruby

# Definição de nó de árvore binária
class TreeNode
  attr_accessor :val, :left, :right
  def initialize(val, left = nil, right = nil)
    @val   = val
    @left  = left
    @right = right
  end
end

# Travessias (pré, in, pós-ordem) e BFS
def preorder(root)
  return [] if root.nil?
  [root.val] + preorder(root.left) + preorder(root.right)
end

def inorder(root)
  return [] if root.nil?
  inorder(root.left) + [root.val] + inorder(root.right)
end

def postorder(root)
  return [] if root.nil?
  postorder(root.left) + postorder(root.right) + [root.val]
end

def bfs(root)
  return [] if root.nil?
  queue = [root]
  result = []
  until queue.empty?
    node = queue.shift
    result << node.val
    queue << node.left  if node.left
    queue << node.right if node.right
  end
  result
end

# Verificar árvore balanceada
def is_balanced(root)
  # retorna -1 se não balanceada, ou altura caso contrário
  height = lambda do |node|
    return 0 if node.nil?
    lh = height.call(node.left)
    return -1 if lh == -1
    rh = height.call(node.right)
    return -1 if rh == -1 || (lh - rh).abs > 1
    [lh, rh].max + 1
  end
  height.call(root) != -1
end

# Menor ancestral comum (LCA)
def lowest_common_ancestor(root, p, q)
  return root if root.nil? || root == p || root == q
  left  = lowest_common_ancestor(root.left,  p, q)
  right = lowest_common_ancestor(root.right, p, q)
  return root if left && right
  left || right
end

# Definição de nó de lista duplamente ligada
class ListNode
  attr_accessor :val, :prev, :next
  def initialize(val, prev_node = nil, next_node = nil)
    @val  = val
    @prev = prev_node
    @next = next_node
  end
end

# Conversão BST → DLL (in-order)
def tree_to_dll(root)
  head = last = nil
  build = lambda do |node|
    next unless node
    build.call(node.left)
    curr = ListNode.new(node.val)
    if last
      last.next = curr
      curr.prev = last
    else
      head = curr
    end
    last = curr
    build.call(node.right)
  end
  build.call(root)
  head
end

# Conversão DLL → BST balanceada
def dll_to_bst(head)
  # conta nós
  cnt = 0
  p = head
  while p
    cnt += 1
    p = p.next
  end
  # referência mutável para o head
  head_ref = head
  build = lambda do |n|
    return nil if n == 0
    # esquerda
    left = build.call(n / 2)
    # raiz
    root = TreeNode.new(head_ref.val)
    head_ref = head_ref.next
    # encaixa subárvore
    root.left  = left
    root.right = build.call(n - n / 2 - 1)
    root
  end
  build.call(cnt)
end

# Hash Tables (Mapas e Sets)

# Two Sum
def two_sum(nums, target)
  seen = {}
  nums.each_with_index do |v, i|
    diff = target - v
    return [seen[diff], i] if seen.key?(diff)
    seen[v] = i
  end
  []
end

# Agrupar anagramas
def group_anagrams(strs)
  buckets = {}
  strs.each do |s|
    key = s.chars.sort.join
    (buckets[key] ||= []) << s
  end
  buckets.values
end

# Maior substring sem caracteres repetidos
def length_of_longest_substring(s)
  last_index = {}
  start = max_len = 0
  s.chars.each_with_index do |ch, i|
    if last_index.key?(ch) && last_index[ch] >= start
      start = last_index[ch] + 1
    end
    last_index[ch] = i
    max_len = [max_len, i - start + 1].max
  end
  max_len
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  # Construindo árvore de exemplo:
  #       10
  #      /  \
  #     5    15
  #    / \     \
  #   3   7     18
  n3  = TreeNode.new(3)
  n7  = TreeNode.new(7)
  n5  = TreeNode.new(5, n3, n7)
  n18 = TreeNode.new(18)
  n15 = TreeNode.new(15, nil, n18)
  root = TreeNode.new(10, n5, n15)

  p preorder(root)  # => [10, 5, 3, 7, 15, 18]
  p inorder(root)   # => [3, 5, 7, 10, 15, 18]
  p postorder(root) # => [3, 7, 5, 18, 15, 10]
  p bfs(root)       # => [10, 5, 15, 3, 7, 18]

  # Balanceamento
  balanced = TreeNode.new(4,
    TreeNode.new(2, TreeNode.new(1), TreeNode.new(3)),
    TreeNode.new(6, TreeNode.new(5), TreeNode.new(7))
  )
  p is_balanced(balanced)  # => true

  unbal = TreeNode.new(1, TreeNode.new(2, TreeNode.new(3)))
  p is_balanced(unbal)     # => false

  # LCA
  lca = lowest_common_ancestor(root, n5, n15)
  p lca.val  # => 10

  # BST ↔ DLL
  head = tree_to_dll(balanced)
  arr = []
  p = head
  arr << p.val while (p = p.next)
  p arr      # => [1,2,3,4,5,6,7]

  new_root = dll_to_bst(head)
  p inorder(new_root)  # => [1,2,3,4,5,6,7]

  # Hash tables
  p two_sum([2,7,11,15], 9)        # => [0,1]
  p group_anagrams(%w[eat tea tan ate nat bat])
    # => [["eat","tea","ate"],["tan","nat"],["bat"]]
  p length_of_longest_substring("pwwkew")  # => 3
end
