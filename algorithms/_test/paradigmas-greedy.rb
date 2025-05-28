# Greedy Algorithms em Ruby

# 1. Interval Scheduling (máximo de atividades não sobrepostas)
def interval_scheduling(intervals)
  # ordena por tempo de término
  sorted = intervals.sort_by { |start, finish| finish }
  result = []
  last_end = -Float::INFINITY

  sorted.each do |start, finish|
    if start >= last_end
      result << [start, finish]
      last_end = finish
    end
  end

  result
end

# 2. Troco com moedas (mínimo de moedas via DP)
def min_coins(coins, amount)
  inf = amount + 1
  dp = [0] + [inf] * amount

  (1..amount).each do |i|
    coins.each do |c|
      if c <= i && dp[i - c] + 1 < dp[i]
        dp[i] = dp[i - c] + 1
      end
    end
  end

  dp[amount] == inf ? -1 : dp[amount]
end

# 3. Huffman Coding (construção de árvore sem heap)
class Node
  attr_accessor :char, :freq, :left, :right
  def initialize(char = nil, freq = 0, left = nil, right = nil)
    @char, @freq, @left, @right = char, freq, left, right
  end
end

def build_huffman(freqs)
  nodes = freqs.map { |c, f| Node.new(c, f) }
  while nodes.size > 1
    nodes.sort_by!(&:freq)
    a = nodes.shift
    b = nodes.shift
    merged = Node.new(nil, a.freq + b.freq, a, b)
    nodes << merged
  end
  nodes.first
end

def make_codes(root)
  codes = {}
  dfs = lambda do |node, prefix|
    return if node.nil?
    if node.char
      codes[node.char] = prefix.empty? ? "0" : prefix
    else
      dfs.call(node.left,  prefix + "0")
      dfs.call(node.right, prefix + "1")
    end
  end
  dfs.call(root, "")
  codes
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  puts "--- Interval Scheduling ---"
  activities = [
    [1,4], [3,5], [0,6], [5,7], [3,9],
    [5,9], [6,10], [8,11], [8,12], [2,14], [12,16]
  ]
  chosen = interval_scheduling(activities)
  p "Atividades escolhidas: #{chosen}"
  # => Atividades escolhidas: [[1,4], [5,7], [8,11], [12,16]]

  puts "\n--- Troco com Moedas ---"
  coins = [1, 3, 4]
  amount = 6
  p "Min moedas para #{amount}: #{min_coins(coins, amount)}"
  # => Min moedas para 6: 2

  puts "\n--- Huffman Coding ---"
  freq_map = { 'a' => 5, 'b' => 9, 'c' => 12,
               'd' => 13, 'e' => 16, 'f' => 45 }
  root = build_huffman(freq_map)
  codes = make_codes(root)
  puts "Códigos de Huffman:"
  codes.each { |ch, code| puts " #{ch}: #{code}" }
end
