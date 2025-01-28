import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Crop Pirate")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)
background = pygame.image.load("assets/background.jpg")

running = True

while True :

    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
            pygame.quit()

    SCREEN.blit(background, (0,0))
    pygame.display.update()