# Programação Dinâmica (DP) em Ruby

# 1. Fibonacci (DP / memoização)
def fib(n, memo = {})
  return n if n < 2
  memo[n] ||= fib(n-1, memo) + fib(n-2, memo)
end

# 2. Subsequência comum máxima (LCS)
def lcs(a, b)
  m, n = a.size, b.size
  dp = Array.new(m+1) { Array.new(n+1, 0) }
  (1..m).each do |i|
    (1..n).each do |j|
      if a[i-1] == b[j-1]
        dp[i][j] = dp[i-1][j-1] + 1
      else
        dp[i][j] = [dp[i-1][j], dp[i][j-1]].max
      end
    end
  end
  dp[m][n]
end

# 3a. Knapsack 0/1 – cada item 0 ou 1 vez
def knapsack_01(values, weights, W)
  n = values.size
  dp = Array.new(n+1) { Array.new(W+1, 0) }
  (1..n).each do |i|
    v, w = values[i-1], weights[i-1]
    (0..W).each do |cap|
      dp[i][cap] = dp[i-1][cap]
      if w <= cap
        dp[i][cap] = [dp[i][cap], dp[i-1][cap-w] + v].max
      end
    end
  end
  dp[n][W]
end

# 3b. Knapsack fracionário – frações permitidas
def knapsack_fractional(values, weights, W)
  items = values.zip(weights)
                .sort_by { |v, w| -v.to_f / w }
  total = 0.0
  items.each do |v, w|
    break if W.zero?
    take = [w, W].min
    total += take * (v.to_f / w)
    W -= take
  end
  total
end

# 4. Caminho mínimo em grade (Grid DP)
def min_path_sum(grid)
  m, n = grid.size, grid.first.size
  dp = Array.new(m) { Array.new(n, 0) }
  dp[0][0] = grid[0][0]
  (1...m).each { |i| dp[i][0] = dp[i-1][0] + grid[i][0] }
  (1...n).each { |j| dp[0][j] = dp[0][j-1] + grid[0][j] }
  (1...m).each do |i|
    (1...n).each do |j|
      dp[i][j] = [dp[i-1][j], dp[i][j-1]].min + grid[i][j]
    end
  end
  dp[m-1][n-1]
end

# 5. Edit Distance (Levenshtein)
def edit_distance(a, b)
  m, n = a.size, b.size
  dp = Array.new(m+1) { Array.new(n+1, 0) }
  (0..m).each { |i| dp[i][0] = i }
  (0..n).each { |j| dp[0][j] = j }
  (1..m).each do |i|
    (1..n).each do |j|
      cost = (a[i-1] == b[j-1] ? 0 : 1)
      dp[i][j] = [
        dp[i-1][j] + 1,    # deleção
        dp[i][j-1] + 1,    # inserção
        dp[i-1][j-1] + cost # substituição ou match
      ].min
    end
  end
  dp[m][n]
end

# 6. Palíndromos e corte mínimo (min cut)
def min_cut_palindrome(s)
  n = s.size
  is_pal = Array.new(n) { Array.new(n, false) }
  (n-1).downto(0) do |i|
    (i...n).each do |j|
      if s[i] == s[j] && (j - i < 2 || is_pal[i+1][j-1])
        is_pal[i][j] = true
      end
    end
  end
  dp = Array.new(n+1, 0)
  dp[0] = -1
  (1..n).each do |i|
    dp[i] = i - 1
    (0...i).each do |j|
      dp[i] = [dp[i], dp[j] + 1].min if is_pal[j][i-1]
    end
  end
  dp[n]
end

# 7. DP com Bitmask – Assignment problem (n×n)
def assignment_min_cost(cost)
  n = cost.size
  size = 1 << n
  dp = Array.new(size, Float::INFINITY)
  dp[0] = 0
  (0...size).each do |mask|
    i = mask.to_s(2).count('1')
    next if i >= n
    (0...n).each do |j|
      next if (mask & (1 << j)) != 0
      nxt = mask | (1 << j)
      dp[nxt] = [dp[nxt], dp[mask] + cost[i][j]].min
    end
  end
  dp[size - 1]
end

# 8. DP com Trie – Word Break
class TrieNode
  attr_accessor :children, :is_end
  def initialize
    @children = {}
    @is_end = false
  end
end

def build_trie(words)
  root = TrieNode.new
  words.each do |word|
    node = root
    word.each_char do |ch|
      node.children[ch] ||= TrieNode.new
      node = node.children[ch]
    end
    node.is_end = true
  end
  root
end

def word_break(s, word_dict)
  root = build_trie(word_dict)
  n = s.size
  dp = Array.new(n+1, false)
  dp[0] = true
  (0...n).each do |i|
    next unless dp[i]
    node = root
    (i...n).each do |j|
      ch = s[j]
      break unless node.children[ch]
      node = node.children[ch]
      dp[j+1] = true if node.is_end
    end
  end
  dp[n]
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  puts fib(10)                                                   # => 55
  puts lcs("AGGTAB", "GXTXAYB")                                  # => 4
  puts knapsack_01([60,100,120], [10,20,30], 50)                 # => 220
  puts knapsack_fractional([60,100,120], [10,20,30], 50)         # => 240.0
  puts min_path_sum([[1,3,1],[1,5,1],[4,2,1]])                   # => 7
  puts edit_distance("kitten", "sitting")                        # => 3
  puts min_cut_palindrome("aab")                                 # => 1
  puts assignment_min_cost([[9,2,7,8],[6,4,3,7],[5,8,1,8],[7,6,9,4]]) # => 13
  puts word_break("leetcode", ["leet","code"])                   # => true
  puts word_break("applepenapple", ["apple","pen"])              # => true
  puts word_break("catsandog", ["cats","dog","sand","and","cat"])# => false
end
