import pygame
import random

pygame.init()

W, H = 1200, 800
FPS = 60

screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
clock = pygame.time.Clock()
bg = (0, 0, 0)
pygame.display.set_caption("Ackanoid")


# Game states
MAIN_MENU = 0
GAME_RUNNING = 1
PAUSE_MENU = 2
SETTINGS_MENU = 3

# Current game state
game_state = MAIN_MENU
pygame.display.set_caption("Ackanoid")

# Paddle
paddleW = 150
paddleH = 25
paddleSpeed = 20
paddle = pygame.Rect(W // 2 - paddleW // 2, H - paddleH - 30, paddleW, paddleH)

# Ball
ballRadius = 20
ballSpeed = 6
ball_rect = int(ballRadius * 2 ** 0.5)
ball = pygame.Rect(random.randrange(ball_rect, W - ball_rect), H // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# Game score
game_score = 0
game_score_fonts = pygame.font.SysFont('comicsansms', 40)
game_score_text = game_score_fonts.render(f'Your game score is: {game_score}', True, (0, 0, 0))
game_score_rect = game_score_text.get_rect()
game_score_rect.center = (210, 20)

# Block settings
class Block:
    def __init__(self, x, y, width, height, breakable=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.breakable = breakable

block_list = [Block(10 + 120 * i, 50 + 70 * j, 100, 50, random.choice([True, False])) for i in range(10) for j in range(4)]
color_list = [(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)) for _ in range(10 * 4)]

# Game over Screen
losefont = pygame.font.SysFont('comicsansms', 40)
losetext = losefont.render('Game Over', True, (255, 255, 255))
losetextRect = losetext.get_rect()
losetextRect.center = (W // 2, H // 2)

# Win Screen
winfont = pygame.font.SysFont('comicsansms', 40)
wintext = losefont.render('You win yay', True, (0, 0, 0))
wintextRect = wintext.get_rect()
wintextRect.center = (W // 2, H // 2)

# Settings
settings_font = pygame.font.SysFont('comicsansms', 30)
settings_text = settings_font.render('Settings Menu', True, (255, 255, 255))
settings_rect = settings_text.get_rect(center=(W//2, H//2))
settings_options = [
    {'label': 'Ball Speed', 'value': ballSpeed},
    {'label': 'Paddle Width', 'value': paddleW},
]

# Main menu options
main_menu_font = pygame.font.SysFont('comicsansms', 50)
main_menu_options = ['Start Game', 'Settings', 'Quit']
main_menu_texts = [main_menu_font.render(option, True, (255, 255, 255)) for option in main_menu_options]
main_menu_rects = [text.get_rect(center=(W//2, 200 + i*100)) for i, text in enumerate(main_menu_texts)]

# Pause menu options
pause_menu_font = pygame.font.SysFont('comicsansms', 50)
pause_menu_options = ['Resume', 'Settings', 'Main Menu', 'Quit']
pause_menu_texts = [pause_menu_font.render(option, True, (255, 255, 255)) for option in pause_menu_options]
pause_menu_rects = [text.get_rect(center=(W//2, 200 + i*100)) for i, text in enumerate(pause_menu_texts)]

# Function to handle events in the settings menu
def handle_settings_events():
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = MAIN_MENU
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = PAUSE_MENU
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for i, rect in enumerate(settings_rects):
                    if rect.collidepoint(event.pos):
                        if i == len(settings_options):
                            game_state = PAUSE_MENU
                        else:
                            change_setting(i)

# Function to change settings
def change_setting(index):
    global ballSpeed, paddleW
    option = settings_options[index]
    if option['label'] == 'Ball Speed':
        ballSpeed += 1
    elif option['label'] == 'Paddle Width':
        paddleW = max(50, paddleW - 10)

# Function to handle events in the main menu
def handle_main_menu_events():
    global game_state, selected_option
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = MAIN_MENU
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if selected_option == 0:  # Start Game
                    game_state = GAME_RUNNING
                elif selected_option == 1:  # Settings
                    game_state = SETTINGS_MENU
                elif selected_option == 2:  # Quit
                    pygame.quit()  # Quit pygame
                    quit()         # Quit Python program
            elif event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(main_menu_options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(main_menu_options)

# Function to handle events in the pause menu
def handle_pause_menu_events():
    global game_state, selected_option
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = MAIN_MENU
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if selected_option == 0:  # Resume
                    game_state = GAME_RUNNING
                elif selected_option == 1:  # Settings
                    game_state = SETTINGS_MENU
                elif selected_option == 2:  # Main Menu
                    game_state = MAIN_MENU
                elif selected_option == 3:  # Quit
                    pygame.quit()  # Quit pygame
                    quit()         # Quit Python program
            elif event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(pause_menu_options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(pause_menu_options)

# Main game loop
selected_option = 0
while True:
    if game_state == MAIN_MENU:
        handle_main_menu_events()
        screen.fill(bg)
        for i, text in enumerate(main_menu_texts):
            screen.blit(text, main_menu_rects[i])
        # Highlight the selected option
        pygame.draw.rect(screen, (255, 0, 0), main_menu_rects[selected_option], 3)
        pygame.display.flip()
    elif game_state == GAME_RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit pygame
                quit()         # Quit Python program
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = PAUSE_MENU
        screen.fill(bg)
        # Game Logic
        for block, color in zip(block_list, color_list):
            pygame.draw.rect(screen, color, block.rect)
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), paddle)
        pygame.draw.circle(screen, pygame.Color(255, 0, 0), ball.center, ballRadius)
        # Ball movement
        ball.x += ballSpeed * dx
        ball.y += ballSpeed * dy
        # Collision handling, scoring, etc.
        pygame.display.flip()
        clock.tick(FPS)
    elif game_state == PAUSE_MENU:
        handle_pause_menu_events()
        screen.fill(bg)
        for i, text in enumerate(pause_menu_texts):
            screen.blit(text, pause_menu_rects[i])
        # Highlight the selected option
        pygame.draw.rect(screen, (255, 0, 0), pause_menu_rects[selected_option], 3)
        pygame.display.flip()
    elif game_state == SETTINGS_MENU:
        handle_settings_events()
        screen.fill(bg)
        screen.blit(settings_text, settings_rect)
        settings_rects = [settings_font.render(f"{option['label']}: {option['value']}", True, (255, 255, 255)).get_rect(center=(W//2, H//2 + 50 * i)) for i, option in enumerate(settings_options)]
        for i, rect in enumerate(settings_rects):
            screen.blit(settings_font.render(f"{settings_options[i]['label']}: {settings_options[i]['value']}", True, (255, 255, 255)), rect)
        pygame.display.flip()
