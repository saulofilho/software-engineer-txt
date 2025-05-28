# Algoritmos em Strings em Ruby

# 1. KMP (Knuth-Morris-Pratt)
def compute_lps(pat)
  n = pat.length
  lps = Array.new(n, 0)
  length = 0
  i = 1
  while i < n
    if pat[i] == pat[length]
      length += 1
      lps[i] = length
      i += 1
    else
      if length > 0
        length = lps[length - 1]
      else
        lps[i] = 0
        i += 1
      end
    end
  end
  lps
end

def kmp_search(txt, pat)
  lps = compute_lps(pat)
  res = []
  i = j = 0
  while i < txt.length
    if txt[i] == pat[j]
      i += 1
      j += 1
      if j == pat.length
        res << (i - j)
        j = lps[j - 1]
      end
    else
      if j > 0
        j = lps[j - 1]
      else
        i += 1
      end
    end
  end
  res
end

# 2. Rabin–Karp
def rabin_karp_search(txt, pat, base = 256, mod = 101)
  n, m = txt.length, pat.length
  return [] if m > n
  h_pat = h_txt = 0
  power = 1
  (m - 1).times { power = (power * base) % mod }
  m.times do |i|
    h_pat = (h_pat * base + pat[i].ord) % mod
    h_txt = (h_txt * base + txt[i].ord) % mod
  end
  res = []
  (0..n - m).each do |i|
    if h_pat == h_txt && txt[i, m] == pat
      res << i
    end
    if i < n - m
      h_txt = (h_txt - txt[i].ord * power) % mod
      h_txt = (h_txt * base + txt[i + m].ord) % mod
      h_txt += mod if h_txt < 0
    end
  end
  res
end

# 3. Z-Algorithm
def z_array(s)
  n = s.length
  z = Array.new(n, 0)
  z[0] = n
  l = r = 0
  (1...n).each do |i|
    if i <= r
      z[i] = [r - i + 1, z[i - l]].min
    end
    while i + z[i] < n && s[z[i]] == s[i + z[i]]
      z[i] += 1
    end
    if i + z[i] - 1 > r
      l, r = i, i + z[i] - 1
    end
  end
  z
end

# 4. Aho–Corasick
class AhoNode
  attr_accessor :next, :fail, :out
  def initialize
    @next = {}
    @fail = nil
    @out  = []
  end
end

class AhoCorasick
  def initialize(patterns)
    @root = AhoNode.new
    # build trie
    patterns.each_with_index do |pat, idx|
      node = @root
      pat.each_char { |ch| node = (node.next[ch] ||= AhoNode.new) }
      node.out << idx
    end
    # build fail links
    queue = []
    @root.next.values.each { |child| child.fail = @root; queue << child }
    until queue.empty?
      curr = queue.shift
      curr.next.each do |ch, nxt|
        queue << nxt
        f = curr.fail
        while f && !f.next.key?(ch)
          f = f.fail
        end
        nxt.fail = f && f.next[ch] ? f.next[ch] : @root
        nxt.out.concat(nxt.fail.out)
      end
    end
  end

  # returns list of [pattern_idx, end_position]
  def search(text, patterns)
    res = []
    node = @root
    text.each_char.with_index do |ch, i|
      while node && !node.next.key?(ch)
        node = node.fail
      end
      node = node&.next[ch] || @root
      node.out.each { |pat_idx| res << [pat_idx, i] }
    end
    res
  end
end

# 5. Suffix Array + LCP
def build_suffix_array(s)
  (0...s.length).sort_by { |i| s[i..-1] }
end

def build_lcp_array(s, sa)
  n = s.length
  lcp = Array.new(n, 0)
  (1...n).each do |i|
    a, b = sa[i-1], sa[i]
    length = 0
    while a + length < n && b + length < n && s[a+length] == s[b+length]
      length += 1
    end
    lcp[i] = length
  end
  lcp
end

# 6. Trie com compressão (Radix Tree)
class CompressedTrieNode
  attr_accessor :children, :is_end
  def initialize
    @children = {}  # edge_label => node
    @is_end   = false
  end
end

class CompressedTrie
  def initialize
    @root = CompressedTrieNode.new
  end

  def insert(word)
    node = @root
    while !word.empty?
      matched = false
      node.children.each do |label, child|
        # find common prefix
        common = ''
        label.chars.zip(word.chars).each do |x, y|
          break unless x == y
          common << x
        end
        next if common.empty?
        matched = true
        if common == label
          word = word[common.length..-1]
          node = child
        else
          # split edge
          suffix_label = label[common.length..-1]
          new_node = CompressedTrieNode.new
          new_node.children[suffix_label] = child
          new_node.is_end = false
          node.children.delete(label)
          node.children[common] = new_node
          word = word[common.length..-1]
          if word.empty?
            new_node.is_end = true
          else
            leaf = CompressedTrieNode.new
            leaf.is_end = true
            new_node.children[word] = leaf
          end
          return
        end
        break
      end
      unless matched
        leaf = CompressedTrieNode.new
        leaf.is_end = true
        node.children[word] = leaf
        return
      end
    end
    node.is_end = true
  end

  def search(word)
    node = @root
    until word.empty?
      found = false
      node.children.each do |label, child|
        if word.start_with?(label)
          word = word[label.length..-1]
          node = child
          found = true
          break
        end
      end
      return false unless found
    end
    node.is_end
  end
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  # KMP
  text = "ABABDABACDABABCABAB"
  pat  = "ABABCABAB"
  p kmp_search(text, pat)             # => [10]

  # Rabin–Karp
  p rabin_karp_search("hello hello", "lo h")  # => [3]

  # Z-Array
  p z_array("aabcaabxaaaz")           # => [12,1,0,0,3,1,0,0,2,1,0,0]

  # Aho–Corasick
  patterns = ["he", "she", "his", "hers"]
  ac = AhoCorasick.new(patterns)
  hits = ac.search("ahishers", patterns)
  p hits.map { |idx, pos| [patterns[idx], pos] }
  # => [["his",2],["he",3],["she",4],["hers",7]]

  # Suffix Array + LCP
  text2 = "banana"
  sa = build_suffix_array(text2)
  lcp = build_lcp_array(text2, sa)
  p sa    # => [5,3,1,0,4,2]
  p lcp   # => [0,1,3,0,0,2]

  # Compressed Trie
  trie = CompressedTrie.new
  %w[test team teal].each { |w| trie.insert(w) }
  p trie.search("team")  # => true
  p trie.search("tea")   # => false
end
