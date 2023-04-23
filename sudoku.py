import sudoku_generator as sg
import pygame
from pygame.time import Clock
import copy

def main():
    pygame.init()

    # Initialize boards and variables
    board, solution_board, starting_board = [1], [2], [3]  
    sketch_board = [[0 for x in range(9)] for y in range(9)]
    selected_row = None
    selected_col = None
    game_screen = False
    main_menu = True
    run = True

    clock = Clock()
    clock.tick(20)

    width = 800
    height = 800
    CELL_SIZE = 70
    GRID_WIDTH = CELL_SIZE * 9
    GRID_HEIGHT = CELL_SIZE * 9
    GRID_TOP_LEFT = (85, 123)

    font = pygame.font.Font('freesansbold.ttf', 24) #set font, font size
    screen = pygame.display.set_mode([width, height])
    pygame.display.set_caption("Sudoku") #game title
    event = pygame.event.poll()
    
    while run:
        if game_screen:
            screen.fill('light blue')

            # Display boardlines
            for i in range(10):
                if i % 3 == 0:
                    thickness = 4
                else:
                    thickness = 1
                pygame.draw.line(screen, "black", (GRID_TOP_LEFT[0], GRID_TOP_LEFT[1] + i * CELL_SIZE), 
                                                    (GRID_TOP_LEFT[0] + GRID_WIDTH, GRID_TOP_LEFT[1] + i * CELL_SIZE), thickness)  # Draw horizontal line
                pygame.draw.line(screen, "black", (GRID_TOP_LEFT[0] + i * CELL_SIZE, GRID_TOP_LEFT[1]), 
                                                    (GRID_TOP_LEFT[0] + i * CELL_SIZE, GRID_TOP_LEFT[1] + GRID_HEIGHT), thickness)  # Draw vertical line

            #  Display backend board numbers in PyGame GUI
            for row in range(len(board)): 
                for col in range(len(board)):
                    if board[row][col] != 0:
                        text = font.render(str(board[row][col]), True, 'black')
                        text_rect = text.get_rect(center=((col * CELL_SIZE) + (CELL_SIZE // 2) + GRID_TOP_LEFT[0], 
                                (row * CELL_SIZE) + (CELL_SIZE // 2) + GRID_TOP_LEFT[1]))
                        screen.blit(text, text_rect)
                    if sketch_board[row][col] != 0:
                        text = font.render(str(sketch_board[row][col]), True, 'dark gray')
                        text_rect = text.get_rect(center=((col * CELL_SIZE) + (14) + GRID_TOP_LEFT[0], 
                                (row * CELL_SIZE) + (15) + GRID_TOP_LEFT[1]))
                        screen.blit(text, text_rect)

            # Bring to main menu
            restart = pygame.draw.rect(screen, 'orange', [80, 30, 180, 60], 0, 5)  # [x,y, width, height]
            text_restart = font.render('Restart', True, 'white')
            screen.blit(text_restart, [125, 50])
            if restart.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                game_screen = False
                main_menu = True
                selected_row, selected_col = None, None
                level = None
                sketch_board = [[0 for x in range(9)] for y in range(9)]

            # Quit program
            exit = pygame.draw.rect(screen, 'orange', [310, 30, 180, 60], 0, 5)  # [x,y, width, height]
            text_exit = font.render('Exit', True, 'white')
            screen.blit(text_exit, [375, 50])
            if exit.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                pygame.quit()

            # Resets board
            reset = pygame.draw.rect(screen, 'orange', [540, 30, 180, 60], 0, 5)  # [x,y, width, height]
            text_reset = font.render('Reset', True, 'white')
            screen.blit(text_reset, [600, 50])
            if reset.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                board = copy.deepcopy(starting_board)
                sketch_board = [[0 for x in range(9)] for y in range(9)]

            # Select cell
            if event.type == pygame.MOUSEBUTTONDOWN:  
                mouse_pos = pygame.mouse.get_pos()
                row = (mouse_pos[1] - GRID_TOP_LEFT[1]) // CELL_SIZE
                col = (mouse_pos[0] - GRID_TOP_LEFT[0]) // CELL_SIZE
                if 0 <= row < 9 and 0 <= col < 9 and board[row][col] == 0:
                    selected_row = row
                    selected_col = col

            # Highlight cell
            if selected_row is not None and selected_col is not None:  
                rect = pygame.Rect(GRID_TOP_LEFT[0] + selected_col * CELL_SIZE, GRID_TOP_LEFT[1] + selected_row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, 'red', rect, 3)

        # Displays main menu
        elif main_menu:
            pygame.draw.rect(screen, 'dark blue', [0, 0, 800, 800])
            mode_msg = font.render('Select a Game Mode', True, 'white')
            welcome_msg = font.render('Welcome to Sudoku!', True, 'white')
            screen.blit(welcome_msg, [275, 250])
            screen.blit(mode_msg, [275, 550])

            level = None

            # Easy Button
            easy = pygame.draw.rect(screen, 'orange', [80, 630, 180, 60], 0, 5)  # [x,y, width, height]
            text_easy = font.render('Easy', True, 'white')
            screen.blit(text_easy, [140, 650])
            if easy.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                game_screen = True
                main_menu = False
                level = 30
                board, solution_board, starting_board = sg.generate_sudoku_better(9, level)
                print(solution_board) # For debugging purposes

            # Medium Button
            medium = pygame.draw.rect(screen, 'orange', [310, 630, 180, 60], 0, 5)
            text_med = font.render('Medium', True, 'white')
            screen.blit(text_med, [355, 650])
            if medium.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                game_screen = True
                main_menu = False
                level = 40
                board, solution_board, starting_board = sg.generate_sudoku_better(9, level)

            # Hard Button
            hard = pygame.draw.rect(screen, 'orange', [540, 630, 180, 60], 0, 5)
            text_hard = font.render('Hard', True, 'white')
            screen.blit(text_hard, [600, 650])
            if hard.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                game_screen = True
                main_menu = False
                level = 50
                board, solution_board, starting_board = sg.generate_sudoku_better(9, level)

        # Main event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if selected_row is not None and selected_col is not None:
                    if event.type == pygame.QUIT:
                        run = False
                    if event.key == pygame.K_1:
                        sketch_board[selected_row][selected_col] = int(1)
                    if event.key == pygame.K_2:
                        sketch_board[selected_row][selected_col] = int(2)                        
                    if event.key == pygame.K_3:
                        sketch_board[selected_row][selected_col] = int(3)                    
                    if event.key == pygame.K_4:
                        sketch_board[selected_row][selected_col] = int(4)                        
                    if event.key == pygame.K_5:
                        sketch_board[selected_row][selected_col] = int(5)
                    if event.key == pygame.K_6:
                        sketch_board[selected_row][selected_col] = int(6)
                    if event.key == pygame.K_7:
                        sketch_board[selected_row][selected_col] = int(7)
                    if event.key == pygame.K_8:
                        sketch_board[selected_row][selected_col] = int(8)
                    if event.key == pygame.K_9:
                        sketch_board[selected_row][selected_col] = int(9)
                    if event.key == pygame.K_BACKSPACE:
                        sketch_board[selected_row][selected_col] = 0
                    if event.key == pygame.K_UP:
                        for i in range(1, selected_row + 1):
                            if board[selected_row - i][selected_col] == 0:
                                selected_row -= i
                                break
                    if event.key == pygame.K_DOWN:
                        for i in range(1, 9 - selected_row):
                            if board[selected_row + i][selected_col] == 0:
                                selected_row += i
                                break
                    if event.key == pygame.K_LEFT:
                        for i in range(1, selected_col + 1):
                            if board[selected_row][selected_col - i] == 0:
                                selected_col -= i
                                break
                    if event.key == pygame.K_RIGHT:
                        for i in range(1, 9 - selected_col):
                            if board[selected_row][selected_col + i] == 0:
                                selected_col += i
                                break
                    elif event.key == pygame.K_RETURN:
                        board[selected_row][selected_col] = sketch_board[selected_row][selected_col]
                        sketch_board[selected_row][selected_col] = 0

                        # Check if Victory/Loss and load Game Over screen once board full
                        if all(0 not in row for row in board):

                            # Victory Screen
                            if board == solution_board:
                                pygame.draw.rect(screen, 'dark blue', [0, 0, 800, 800])
                                game_screen = False
                                main_menu = False

                                game_over_go_again = pygame.draw.rect(screen, 'orange', [270, 290, 270, 60], 0, 5)
                                game_over_go_again_text = font.render('You Win! Go Again?', True, 'black')
                                screen.blit(game_over_go_again_text, [290, 310])
                                pygame.display.flip() 

                                game_over_quit = pygame.draw.rect(screen, 'orange', [345, 360, 120, 60], 0, 5)
                                game_over_quit_text = font.render('Quit', True, 'black')
                                screen.blit(game_over_quit_text, [375, 380])

                            # Loss Screen
                            if board != solution_board:
                                pygame.draw.rect(screen, 'dark blue', [0, 0, 800, 800])
                                game_screen = False
                                main_menu = False

                                game_over_go_again = pygame.draw.rect(screen, 'orange', [265, 290, 280, 60], 0, 5)
                                game_over_go_again_text = font.render('You Lose! Go Again?', True, 'black')
                                screen.blit(game_over_go_again_text, [286, 310])
                                pygame.display.flip() 

                                game_over_quit = pygame.draw.rect(screen, 'orange', [345, 360, 120, 60], 0, 5)
                                game_over_quit_text = font.render('Quit', True, 'black')
                                screen.blit(game_over_quit_text, [376, 380])

            # Provide functionality to gameover screen buttons
            if main_menu == False and game_screen == False:
                # Quit Button
                if game_over_quit.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    pygame.quit()

                # Go again button
                if game_over_go_again.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    game_screen = False
                    main_menu = True
                    selected_row, selected_col = None, None
                    level = None
                    sketch_board = [[0 for x in range(9)] for y in range(9)]
                    pygame.display.flip()
                    break

        # Display on screen
        pygame.display.flip() 

    pygame.quit()
    
if __name__ == "__main__":
    main()
