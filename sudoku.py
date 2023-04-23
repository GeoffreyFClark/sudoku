import sudoku_generator as sg
import pygame
import copy

def main():
    pygame.init()

    # Initialization
    board, solution_board, starting_board = [1], [2], [3]  
    sketch_board = [[0 for x in range(9)] for y in range(9)]
    main_menu, game_screen = True, False
    selected_row, selected_col = 0, 0
    gator_img = pygame.image.load('UF_GATOR.jpg')

    width, height, cell_size = 800, 800, 70
    grid_width, grid_height = cell_size * 9, cell_size * 9
    grid_top_left = (85, 123)

    font = pygame.font.Font('freesansbold.ttf', 24) #set font, font size
    welcome_font = pygame.font.Font('freesansbold.ttf', 70)
    screen = pygame.display.set_mode([width, height])
    pygame.display.set_caption("Sudoku") #game title
    event = pygame.event.poll()

    # Main game loop
    run = True
    while run:

        # Displays main menu
        if main_menu:
            screen.blit(gator_img, [0, 0])
            empty_cells = None
            selected_row, selected_col = 0, 0

            welcome_msg = welcome_font.render('Welcome to Sudoku!', True, 'orange')
            screen.blit(welcome_msg, [50, 70])

            mode_msg = font.render('Select a Game Mode', True, 'orange')
            screen.blit(mode_msg, [275, 640])

            # Easy Button
            easy = pygame.draw.rect(screen, 'orange', [80, 681, 180, 60], 0, 5)  # [x,y, width, height]
            text_easy = font.render('Easy', True, 'dark blue')
            screen.blit(text_easy, [140, 699])
            if easy.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                game_screen, main_menu = True, False
                empty_cells = 30
                board, solution_board, starting_board = sg.generate_sudoku_better(9, empty_cells)

            # Medium Button
            medium = pygame.draw.rect(screen, 'orange', [310, 681, 180, 60], 0, 5)
            text_med = font.render('Medium', True, 'dark blue')
            screen.blit(text_med, [355, 699])
            if medium.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                game_screen, main_menu = True, False
                empty_cells = 40
                board, solution_board, starting_board = sg.generate_sudoku_better(9, empty_cells)

            # Hard Button
            hard = pygame.draw.rect(screen, 'orange', [540, 681, 180, 60], 0, 5)
            text_hard = font.render('Hard', True, 'dark blue')
            screen.blit(text_hard, [600, 699])
            if hard.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                game_screen, main_menu = True, False
                empty_cells = 50
                board, solution_board, starting_board = sg.generate_sudoku_better(9, empty_cells)

        # Main sudoku game screen
        elif game_screen:
            screen.fill('dark blue')

            # Display boardlines
            for i in range(10):  
                if i % 3 == 0:
                    thickness = 10
                else:
                    thickness = 5

                # Horizontal
                pygame.draw.line(screen, "orange", (grid_top_left[0] - 4, grid_top_left[1] + i * cell_size), 
                                 (grid_top_left[0] + 5 + grid_width, grid_top_left[1] + i * cell_size), thickness)  
                
                # Vertical
                pygame.draw.line(screen, "orange", (grid_top_left[0] + i * cell_size, grid_top_left[1]), 
                                 (grid_top_left[0] + i * cell_size, grid_top_left[1] + grid_height), thickness)  
                
            # Display board numbers
            for row in range(len(board)): 
                for col in range(len(board)):
                    if board[row][col] != 0:
                        text = font.render(str(board[row][col]), True, 'orange')
                        text_rect = text.get_rect(center=((col * cell_size) + (cell_size // 2) + grid_top_left[0], 
                                                          (row * cell_size) + (cell_size // 2) + grid_top_left[1]))
                        screen.blit(text, text_rect)
                    if sketch_board[row][col] != 0:
                        text = font.render(str(sketch_board[row][col]), True, 'gray')
                        text_rect = text.get_rect(center=((col * cell_size) + 18 + grid_top_left[0], 
                                                          (row * cell_size) + 23 + grid_top_left[1]))
                        screen.blit(text, text_rect)

            # Highlight cell
            rect = pygame.Rect(grid_top_left[0] + selected_col * cell_size, grid_top_left[1] + selected_row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, 'red', rect, 11)

            # Restart Button
            restart = pygame.draw.rect(screen, 'orange', [80, 30, 180, 60], 0, 5)  # [x,y, width, height]
            text_restart = font.render('Restart', True, 'dark blue')
            screen.blit(text_restart, [125, 50])
            if restart.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                game_screen, main_menu = False, True
                empty_cells = None
                sketch_board = [[0 for x in range(9)] for y in range(9)]

            # Exit Button
            exit = pygame.draw.rect(screen, 'orange', [310, 30, 180, 60], 0, 5)  # [x,y, width, height]
            text_exit = font.render('Exit', True, 'dark blue')
            screen.blit(text_exit, [375, 50])
            if exit.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                pygame.quit()

            # Reset Button
            reset = pygame.draw.rect(screen, 'orange', [540, 30, 180, 60], 0, 5)  # [x,y, width, height]
            text_reset = font.render('Reset', True, 'dark blue')
            screen.blit(text_reset, [600, 50])
            if reset.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                board = copy.deepcopy(starting_board)
                sketch_board = [[0 for x in range(9)] for y in range(9)]

        # Main event handler
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            # Select cell
            if event.type == pygame.MOUSEBUTTONDOWN:  
                mouse_pos = pygame.mouse.get_pos()
                row = (mouse_pos[1] - grid_top_left[1]) // cell_size
                col = (mouse_pos[0] - grid_top_left[0]) // cell_size
                if 0 <= row < 9 and 0 <= col < 9:
                    selected_row, selected_col = row, col

            # Input sketched number into cell
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if board[selected_row - i][selected_col] == 0:
                        sketch_board[selected_row][selected_col] = int(1)
                if event.key == pygame.K_2:
                    if board[selected_row - i][selected_col] == 0:
                        sketch_board[selected_row][selected_col] = int(2)                        
                if event.key == pygame.K_3:
                    if board[selected_row - i][selected_col] == 0:
                        sketch_board[selected_row][selected_col] = int(3)                    
                if event.key == pygame.K_4:
                    if board[selected_row - i][selected_col] == 0:
                        sketch_board[selected_row][selected_col] = int(4)                        
                if event.key == pygame.K_5:
                    if board[selected_row - i][selected_col] == 0:
                        sketch_board[selected_row][selected_col] = int(5)
                if event.key == pygame.K_6:
                    if board[selected_row - i][selected_col] == 0:
                        sketch_board[selected_row][selected_col] = int(6)
                if event.key == pygame.K_7:
                    if board[selected_row - i][selected_col] == 0:
                        sketch_board[selected_row][selected_col] = int(7)
                if event.key == pygame.K_8:
                    if board[selected_row - i][selected_col] == 0:
                        sketch_board[selected_row][selected_col] = int(8)
                if event.key == pygame.K_9:
                    if board[selected_row - i][selected_col] == 0:
                        sketch_board[selected_row][selected_col] = int(9)
                if event.key == pygame.K_BACKSPACE:
                    if board[selected_row - i][selected_col] == 0:
                        sketch_board[selected_row][selected_col] = 0

                # Move selected cell using arrow keys
                if event.key == pygame.K_UP:
                    if selected_row >= 1:
                        selected_row -= 1
                if event.key == pygame.K_DOWN:
                    if selected_row <= 7:
                        selected_row += 1
                if event.key == pygame.K_LEFT:
                    if selected_col >= 1:
                        selected_col -= 1
                if event.key == pygame.K_RIGHT:
                    if selected_col <= 7:
                        selected_col += 1

                # Input sketched number, locking it in
                elif event.key == pygame.K_RETURN and sketch_board[selected_row][selected_col] != 0:
                    board[selected_row][selected_col] = sketch_board[selected_row][selected_col]
                    sketch_board[selected_row][selected_col] = 0

                    # After inputting a number, check if Victory/Loss and load Game Over screen if board full
                    if all(0 not in row for row in board):

                        # Victory Screen
                        if board == solution_board:  
                            screen.blit(gator_img, [0, 0])
                            game_screen, main_menu = False, False

                            game_over_go_again = pygame.draw.rect(screen, 'orange', [260, 70, 270, 60], 0, 5)
                            game_over_go_again_text = font.render('You Win! Go Again?', True, 'dark blue')
                            screen.blit(game_over_go_again_text, [280, 90])
                            pygame.display.flip() 

                            game_over_quit = pygame.draw.rect(screen, 'orange', [335, 660, 120, 60], 0, 5)
                            game_over_quit_text = font.render('Quit', True, 'dark blue')
                            screen.blit(game_over_quit_text, [365, 680])

                        # Loss Screen
                        if board != solution_board:  
                            screen.blit(gator_img, [0, 0])
                            game_screen, main_menu = False, False

                            game_over_go_again = pygame.draw.rect(screen, 'orange', [257, 70, 280, 60], 0, 5)
                            game_over_go_again_text = font.render('You Lose! Go Again?', True, 'dark blue')
                            screen.blit(game_over_go_again_text, [277, 90])
                            pygame.display.flip() 

                            game_over_quit = pygame.draw.rect(screen, 'orange', [337, 660, 120, 60], 0, 5)
                            game_over_quit_text = font.render('Quit', True, 'dark blue')
                            screen.blit(game_over_quit_text, [368, 680])

            # Provide functionality to gameover screen buttons
            if main_menu == False and game_screen == False:

                # Quit Button
                if game_over_quit.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:  
                    pygame.quit()

                # Go again button
                if game_over_go_again.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:  
                    game_screen, main_menu = False, True                    
                    empty_cells = None
                    sketch_board = [[0 for x in range(9)] for y in range(9)]

        # Display on screen
        pygame.display.flip()  
    
if __name__ == "__main__":
    main()
