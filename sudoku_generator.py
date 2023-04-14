import math, random
import pygame


"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""


class SudokuGenerator:
    '''
	create a sudoku board - initialize class variables and set up the 2D board
	This should initialize:
	self.row_length		- the length of each row
	self.removed_cells	- the total number of cells to be removed
	self.board			- a 2D list of ints to represent the board
	self.box_length		- the square root of row_length

	Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

	Return:
	None
    '''

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for x in range(row_length)] for y in range(row_length)]
        self.box_length = int(math.sqrt(row_length))

    '''
	Returns a 2D python list of numbers which represents the board

	Parameters: None
	Return: list[list]
    '''

    def get_board(self):
        return self.board

    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''

    def print_board(self):
        for row in range(self.row_length):
            print(self.board[row])

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row
	
	Return: boolean
    '''

    def valid_in_row(self, row, num):
        for col in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column
	
	Return: boolean
    '''

    def valid_in_col(self, col, num):
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''

    def valid_in_box(self, row_start, col_start, num):
        for row in range(row_start, row_start + self.box_length):
            for col in range(col_start, col_start + self.box_length):
                if self.board[row][col] == num:
                    return False
        return True

    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''

    def is_valid(self, row, col, num):
        row_validity = self.valid_in_row(row, num)
        col_validity = self.valid_in_col(col, num)
        if 0 <= row <= 2:
            row_start = 0
        elif 3 <= row <= 5:
            row_start = 3
        elif 6 <= row <= 8:
            row_start = 6
        if 0 <= row <= 2:
            col_start = 0
        elif 3 <= row <= 5:
            col_start = 3
        elif 6 <= row <= 8:
            col_start = 6
        box_validity = self.valid_in_box(row_start, col_start, num)
        return row_validity and col_validity  and box_validity

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''

    def fill_box(self, row_start, col_start):
        for i in range(0, 3):
            for j in range(0, 3):
                while True:  # loop until fill the valid number
                    ran_num = random.randint(1, 9)
                    if self.is_valid(row_start, col_start, ran_num):
                        self.board[row_start + i][col_start + j] = ran_num
                        return

    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''

    def fill_diagonal(self):
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled
	
	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(3, 0)

    '''
        Removes the appropriate number of cells from the board
        This is done by setting some values to 0
        Should be called after the entire solution has been constructed
        i.e. after fill_values has been called
        
        NOTE: Be careful not to 'remove' the same cell multiple times
        i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''

    def remove_cells(self):
        removed = 0
        while removed < self.removed_cells:
            ran_row = random.randint(0, 8)  # random row
            ran_col = random.randint(0, 8)  # random column
            if self.board[ran_row][ran_col] != 0:
                self.board[ran_row][ran_col] = 0
                removed += 1


'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    answer_board = board
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board, answer_board


def main():
    pygame.init()

    width = 800
    height = 800
    CELL_SIZE = 70
    GRID_WIDTH = CELL_SIZE * 9
    GRID_HEIGHT = CELL_SIZE * 9
    GRID_TOP_LEFT = (85, 123)

    board, solution_board, working_board = [0], [0], None

    screen = pygame.display.set_mode([width, height])
    pygame.display.set_caption("Sudoku") #game title
    main_menu = False
    font = pygame.font.Font('freesansbold.ttf', 24) #set font

    run = True
    while run:
        if main_menu:
            screen.fill('light blue')

            #display board
            for i in range(10):
                if i % 3 == 0:
                    thickness = 4
                else:
                    thickness = 1

                # Draw horizontal line
                pygame.draw.line(screen, "black", (GRID_TOP_LEFT[0], GRID_TOP_LEFT[1] + i * CELL_SIZE), 
                                                    (GRID_TOP_LEFT[0] + GRID_WIDTH, GRID_TOP_LEFT[1] + i * CELL_SIZE), thickness)

                # Draw vertical line
                pygame.draw.line(screen, "black", (GRID_TOP_LEFT[0] + i * CELL_SIZE, GRID_TOP_LEFT[1]), 
                                                    (GRID_TOP_LEFT[0] + i * CELL_SIZE, GRID_TOP_LEFT[1] + GRID_HEIGHT), thickness)

            #bring to main menu
            restart = pygame.draw.rect(screen, 'orange', [80, 30, 180, 60], 0, 5)  # [x,y, width, height]
            text_restart = font.render('Restart', True, 'white')
            screen.blit(text_restart, [125, 50])

            #quit program
            exit = pygame.draw.rect(screen, 'orange', [310, 30, 180, 60], 0, 5)  # [x,y, width, height]
            text_exit = font.render('Exit', True, 'white')
            screen.blit(text_exit, [375, 50])

            #resets board
            reset = pygame.draw.rect(screen, 'orange', [540, 30, 180, 60], 0, 5)  # [x,y, width, height]
            text_reset = font.render('Reset', True, 'white')
            screen.blit(text_reset, [600, 50])

            if exit.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                pygame.quit()

            if restart.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                main_menu = False

            if reset.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                board = working_board

        else:
            pygame.draw.rect(screen, 'dark blue', [0, 0, 800, 800])
            mode_msg = font.render('Select a Game Mode', True, 'white')
            welcome_msg = font.render('Welcome to Sudoku!', True, 'white')
            screen.blit(welcome_msg, [275, 250])
            screen.blit(mode_msg, [275, 550])

            easy = pygame.draw.rect(screen, 'orange', [80, 630, 180, 60], 0, 5)  # [x,y, width, height]
            text_easy = font.render('Easy', True, 'white')
            screen.blit(text_easy, [140, 650])

            medium = pygame.draw.rect(screen, 'orange', [310, 630, 180, 60], 0, 5)
            text_med = font.render('Medium', True, 'white')
            screen.blit(text_med, [355, 650])

            hard = pygame.draw.rect(screen, 'orange', [540, 630, 180, 60], 0, 5)
            text_hard = font.render('Hard', True, 'white')
            screen.blit(text_hard, [600, 650])

            level = None  # initialize the level variable

            if easy.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                main_menu = True
                level = 30

            if medium.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                main_menu = True
                level = 40

            if hard.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                main_menu = True
                level = 50

            if level is not None:
                # Generate a Sudoku solution and retrieve the board with cells removed and the solution board
                board, solution_board = generate_sudoku(9, level)
                working_board = board

                for row in range(len(board)):
                    for col in range(len(board)):
                        if board[row][col] != 0:
                            text = font.render(str(board[row][col]), True, 'black')
                            text_rect = text.get_rect(center=(col * 50 + 80, row * 50 + 105))
                            screen.blit(text, text_rect)

        if working_board == solution_board:
            pygame.draw.rect(screen, 'dark blue', [0, 0, 800, 800])
            game_over = pygame.draw.rect(screen, 'orange', [270, 310, 270, 60], 0, 5)
            game_over_text = font.render('You Win! Go Again?', True, 'black')
            screen.blit(game_over_text, [290, 330])
            if game_over.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                main()
                pygame.quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.flip() #put display on screen

    pygame.quit()

main()