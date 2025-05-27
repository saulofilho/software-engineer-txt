# Recursão e Backtracking
# # Sudoku Solver
# 1. Sudoku Solver (backtracking)

def solve_sudoku(board):
    """
    board: lista 9x9 de inteiros, 0 = vazio.
    Modifica board in-place para solução.
    """
    def find_empty():
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def valid(i, j, val):
        # verifica linha e coluna
        for k in range(9):
            if board[i][k] == val or board[k][j] == val:
                return False
        # verifica sub-grade 3x3
        bi, bj = (i//3)*3, (j//3)*3
        for r in range(bi, bi+3):
            for c in range(bj, bj+3):
                if board[r][c] == val:
                    return False
        return True

    empty = find_empty()
    if not empty:
        return True  # sem vazios: resolvido
    i, j = empty
    for val in range(1, 10):
        if valid(i, j, val):
            board[i][j] = val
            if solve_sudoku(board):
                return True
            board[i][j] = 0
    return False

if __name__ == "__main__":
    puzzle = [
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
    if solve_sudoku(puzzle):
        for row in puzzle:
            print(row)
    else:
        print("Sem solução")


# # N-Rainhas
# 2. N-Queens (backtracking)

def solve_n_queens(n):
    """
    Retorna lista de soluções; cada solução é lista de strings onde 'Q' marca rainha.
    """
    cols = set()
    diag1 = set()  # r - c
    diag2 = set()  # r + c
    board = [['.' for _ in range(n)] for _ in range(n)]
    solutions = []

    def backtrack(r):
        if r == n:
            solutions.append([''.join(row) for row in board])
            return
        for c in range(n):
            if c in cols or (r-c) in diag1 or (r+c) in diag2:
                continue
            cols.add(c); diag1.add(r-c); diag2.add(r+c)
            board[r][c] = 'Q'
            backtrack(r+1)
            board[r][c] = '.'
            cols.remove(c); diag1.remove(r-c); diag2.remove(r+c)

    backtrack(0)
    return solutions

if __name__ == "__main__":
    sols = solve_n_queens(4)
    for sol in sols:
        for row in sol:
            print(row)
        print()


# # Geração de Permutações e Combinações
# 3. Permutações e Combinações (backtracking)

def permutations(nums):
    """
    Retorna todas as permutações de nums.
    """
    res = []
    used = [False]*len(nums)
    perm = []

    def dfs():
        if len(perm) == len(nums):
            res.append(perm[:])
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                perm.append(nums[i])
                dfs()
                perm.pop()
                used[i] = False

    dfs()
    return res

def combinations(nums, k):
    """
    Retorna todas as combinações de k elementos de nums.
    """
    res = []
    combo = []

    def dfs(start):
        if len(combo) == k:
            res.append(combo[:])
            return
        for i in range(start, len(nums)):
            combo.append(nums[i])
            dfs(i+1)
            combo.pop()

    dfs(0)
    return res

if __name__ == "__main__":
    print("Permutações de [1,2,3]:", permutations([1,2,3]))
    print("Combinações de  [1,2,3,4], k=2:", combinations([1,2,3,4], 2))
