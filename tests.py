from sudoku_generator import *

def test_silly():
  assert 4 == 4

def test_remove_cells():
  board = generate_sudoku(9, 30)
  # Check if 30 cells are removed
  count = 0
  for i in range(9):
    for j in range(9):
      if(board[i][j] == 0):
        count += 1

  assert count == 30, f'Failed: Should have removed 30 cells; instead removed {count} cells.'

def check_box(board, row, col):
  # looping from row to row+2 for i
  # looping from col to col+2 for j
  seen = [False] * 10
  seen[0] = True

  for i in range(3):
    for j in range(3):
      current = board[row + i][col + j]
      if seen[current]:
        return False
      seen[current] = True

  return True
  
def test_fill_diagonals():
  sudoku = SudokuGenerator(9, 30)
  sudoku.fill_diagonal()

  for i in range(0, sudoku.row_length, sudoku.box_length):
    assert check_box(sudoku.get_board(),i,i), "Failed: Diagonals not filled properly"
    
def test_valid_in_row():
  sudoku = SudokuGenerator(9, 30)
  sudoku.fill_values()
  sudoku.remove_cells()
  board = sudoku.get_board()

  def row_unused(board, row, num):
    for col in range(sudoku.row_length):
      if board[row][col] == num:
        return False
    return True

  for i in range(9):
    for j in range(1,10):  
      temp = row_unused(board, i, j)
      temp2 = sudoku.unused_in_row(i, j)
      assert temp == temp2, "Failed: valid_in_row implemented incorrectly"
 
def test_valid_in_col():
  sudoku = SudokuGenerator(9, 30)
  sudoku.fill_values()
  sudoku.remove_cells()
  board = sudoku.get_board()

  def col_unused(board, col, num):
    for row in range(sudoku.row_length):
      if board[row][col] == num:
        return False
    return True


  for i in range(9):
    for j in range(1,10):  
      temp = col_unused(board, i, j)
      temp2 = sudoku.unused_in_col(i, j)
      assert temp == temp2, 'Failed: valid_in_col implemented incorrectly'

def test_is_valid():
  sudoku = SudokuGenerator(9, 30)
  sudoku.fill_values()
  sudoku.remove_cells()
  board = sudoku.get_board()

  # All of these functions are the solutions functions
  def col_unused(board, col, num):
    for row in range(sudoku.row_length):
      if board[row][col] == num:
        return False
    return True

  def row_unused(board, row, num):
    for col in range(sudoku.row_length):
      if board[row][col] == num:
        return False
    return True

  def unused_inbox(sudoku, row_start, col_start, num):
    for i in range(sudoku.box_length):
      for j in range(sudoku.box_length):
        if sudoku.board[row_start + i][col_start + j] == num:
          return False
    return True

  def check_safe(sudoku, row, col, num):
    return row_unused(board, row, num) and col_unused(board, col, num) and unused_inbox(sudoku, row - row % sudoku.box_length, col - col % sudoku.box_length, num)


  for i in range(9):
    for j in range(9): 
      for k in range(1,10):
        temp = check_safe(sudoku, i, j, k)
        temp2 = sudoku.check_if_safe(i, j, k)
        # Compare the solution with the student's code
        assert temp == temp2, 'Failed: is_valid implemented incorrectly'

def test_valid_board():
  def valid(bo, num, pos):
    # check row
    for i in range(len(bo[0])):
      if bo[pos[0]][i] == num and pos[1] != i:
        return False
    # check column
    for i in range(len(bo)):
      if bo[i][pos[1]] == num and pos[0] != i:
        return False
    # check box
    box_x = pos[0] // 3
    box_y = pos[1] // 3
    for i in range(box_x * 3, box_x * 3 + 3):
      for j in range(box_y * 3, box_y * 3 + 3):
        if bo[i][j] == num and (i, j) != pos:
          return False
    return True
  
  def find_empty(board):
    for i in range(len(board)):
      for j in range(len(board[0])):
        if board[i][j] == 0:
          return (i, j)
    return None
        
  def solve(board):
    find = find_empty(board)
    if not find:
      return True
    else:
      row, col = find
    for i in range(1, 10):
      if valid(board, i, (row, col)):
        board[row][col] = i
        if solve(board):
          return True
        board[row][col] = 0
    return False
  
  board = generate_sudoku(9, 30)
    
  assert solve(board), 'Failed: The board you create with generate_sudoku is an invalid sudoku board.'
