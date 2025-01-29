import pygame
import pygame_textinput

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("FRUIT SLICER BY FLAPPOU")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)
background = pygame.image.load("assets/background.jpg")

font = pygame.font.Font(None, 74)
text_font = pygame.font.Font(None, 36)

play_button = font.render('Play', True, (255, 255, 255))
leaderboard_button = font.render('Leaderboard', True, (255, 255, 255))
exit_button = font.render('Exit', True, (255, 255, 255))

play_rect = play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
leaderboard_rect = leaderboard_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
exit_rect = exit_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

running = True
clock = pygame.time.Clock()

def get_username():
    textinput = pygame_textinput.TextInputVisualizer()
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            textinput.update([event])
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                input_active = False

        SCREEN.blit(background, (0, 0))
        
        # Draw "Enter your name"
        instruction_text = text_font.render("Enter your name", True, (255, 255, 255))
        SCREEN.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 - 80))

        # Draw input box
        input_box_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 20, 300, 40)
        pygame.draw.rect(SCREEN, (255, 255, 255), input_box_rect, border_radius=10)

        # Render text input inside the box
        SCREEN.blit(textinput.surface, (input_box_rect.x + 10, input_box_rect.y + 5))

        pygame.display.update()
        clock.tick(FPS)

    return textinput.value

def save_to_leaderboard(username):
    with open("leaderboard.txt", "a") as file:
        file.write(username + "\n")

def display_leaderboard():
    SCREEN.blit(background, (0, 0))
    try:
        with open("leaderboard.txt", "r") as file:
            lines = file.readlines()
            y_offset = 100
            for line in lines:
                leaderboard_text = text_font.render(line.strip(), True, (255, 255, 255))
                SCREEN.blit(leaderboard_text, (WIDTH // 2 - leaderboard_text.get_width() // 2, y_offset))
                y_offset += 40
    except FileNotFoundError:
        error_text = text_font.render("No leaderboard data found.", True, (255, 255, 255))
        SCREEN.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, HEIGHT // 2))
    
    # Draw "ESC to back" in the top right corner
    esc_text = text_font.render("ESC to back", True, (255, 255, 255))
    SCREEN.blit(esc_text, (WIDTH - esc_text.get_width() - 10, 10))
    
    pygame.display.update()

showing_leaderboard = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                print("Play button clicked")
                username = get_username()
                save_to_leaderboard(username)
            elif leaderboard_rect.collidepoint(event.pos):
                print("Leaderboard button clicked")
                showing_leaderboard = True
            elif exit_rect.collidepoint(event.pos):
                print("Exit button clicked")
                running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if showing_leaderboard:
                    showing_leaderboard = False

    if showing_leaderboard:
        display_leaderboard()
    else:
        SCREEN.blit(background, (0, 0))
        SCREEN.blit(play_button, play_rect)
        SCREEN.blit(leaderboard_button, leaderboard_rect)
        SCREEN.blit(exit_button, exit_rect)
        pygame.display.update()

    clock.tick(FPS)

pygame.quit()
