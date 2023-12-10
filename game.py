import pygame
import os
import time 
import random
pygame.font.init() # Need for using fonts

# OPENING GAME WINDOW
WIDTH, HEIGHT = 750, 750 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load images
# PLAYERS SPACESHIP
MAIN_SPACE_SHIP = pygame.image.load(os.path.join("ships", "spaceship2.png"))

# Enemy ship
ENEMY_SPACE_SHIP1 = pygame.image.load(os.path.join("ships", "ship1.png"))
ENEMY_SPACE_SHIP2 = pygame.image.load(os.path.join("ships", "ship2.png"))
ENEMY_SPACE_SHIP3 = pygame.image.load(os.path.join("ships", "ship3.png"))

# Laser Bullets
BLUE_LASER = pygame.image.load(os.path.join("bullets", "01.png"))
RED_LASER = pygame.image.load(os.path.join("bullets", "02.png"))
PINK_LASER = pygame.image.load(os.path.join("bullets", "03.png"))
PURPLE_LASER = pygame.image.load(os.path.join("bullets", "04.png"))

# Background 
BG = pygame.transform.scale(pygame.image.load(os.path.join("backgrounds", "desert_background.png")), (WIDTH, HEIGHT))
# class for  all ships behavior
class Ship:
    def __init__(self, x,y, color, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

        ship = Ship(300, 650)


# Main function
def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("monospace", 40)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))
        #draw text
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

main()