# Recursão e Backtracking em Ruby

# 1. Sudoku Solver (backtracking)
def solve_sudoku(board)
  find_empty = lambda {
    (0...9).each do |i|
      (0...9).each { |j| return [i, j] if board[i][j].zero? }
    end
    nil
  }

  valid = lambda do |i, j, v|
    # linha e coluna
    (0...9).each do |k|
      return false if board[i][k] == v || board[k][j] == v
    end
    # sub-grade 3x3
    bi, bj = (i / 3) * 3, (j / 3) * 3
    (bi...(bi+3)).each do |r|
      (bj...(bj+3)).each do |c|
        return false if board[r][c] == v
      end
    end
    true
  end

  empty = find_empty.call
  return true unless empty  # sem vazios, resolvido
  i, j = empty

  (1..9).each do |v|
    if valid.call(i, j, v)
      board[i][j] = v
      return true if solve_sudoku(board)
      board[i][j] = 0
    end
  end

  false
end

# 2. N-Queens (backtracking)
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
      next if cols.include?(c) || diag1.include?(r - c) || diag2.include?(r + c)
      cols.add(c); diag1.add(r - c); diag2.add(r + c)
      board[r][c] = 'Q'
      backtrack.call(r + 1)
      board[r][c] = '.'
      cols.delete(c); diag1.delete(r - c); diag2.delete(r + c)
    end
  end

  backtrack.call(0)
  solutions
end

# 3. Geração de Permutações (backtracking)
def permutations(nums)
  res = []
  perm = []
  used = Array.new(nums.size, false)

  dfs = lambda do
    if perm.size == nums.size
      res << perm.dup
      return
    end
    nums.each_with_index do |v, i|
      next if used[i]
      used[i] = true
      perm << v
      dfs.call
      perm.pop
      used[i] = false
    end
  end

  dfs.call
  res
end

# 4. Combinações (backtracking)
def combinations(nums, k)
  res = []
  combo = []

  dfs = lambda do |start|
    if combo.size == k
      res << combo.dup
      return
    end
    (start...nums.size).each do |i|
      combo << nums[i]
      dfs.call(i + 1)
      combo.pop
    end
  end

  dfs.call(0)
  res
end

# Exemplos de uso
if __FILE__ == $PROGRAM_NAME
  require 'set'

  puts "--- Sudoku Solver ---"
  puzzle = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
  ]
  if solve_sudoku(puzzle)
    puzzle.each { |row| p row }
  else
    puts "Sem solução"
  end

  puts "\n--- N-Queens (n=4) ---"
  solve_n_queens(4).each do |sol|
    sol.each { |row| puts row }
    puts
  end

  puts "\n--- Permutações de [1,2,3] ---"
  p permutations([1,2,3])

  puts "\n--- Combinações de [1,2,3,4], k=2 ---"
  p combinations([1,2,3,4], 2)
end
