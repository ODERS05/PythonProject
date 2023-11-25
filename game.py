import pygame
pygame.init()
screen = pygame.display.set_mode ((1000, 500))
WHITE = (255, 255, 255)
running = True

def backround():
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
pygame.quit()