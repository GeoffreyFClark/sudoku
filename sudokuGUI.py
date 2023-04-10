
import pygame

pygame.init()

width = 800
height = 800

screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Sudoku") #game title
main_menu = False
font = pygame.font.Font('freesansbold.ttf', 24) #set font

def draw_game(): #display main menu
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

    if restart.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        menu = False
    else:
        menu = True
    return menu

def make_menu(): #display game
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

    menu = False

    if easy.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        menu = True

    if medium.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        menu = True

    if hard.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        menu = True

    return menu

run = True
while run:
    screen.fill('light blue')

    if main_menu:
        main_menu = draw_game()
    else:
        main_menu = make_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip() #put display on screen

pygame.quit()


