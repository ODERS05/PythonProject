import pygame
import os
import time 
import random
pygame.font.init() #  fonts library
pygame.mixer.init() # sound effects library

# OPENING GAME WINDOW
WIDTH, HEIGHT = 750, 750 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load
# PLAYERS SPACESHIP
MAIN_SPACE_SHIP = pygame.image.load(os.path.join("ships", "spaceship2.png"))

# Enemy player
ENEMY_SPACE_SHIP1 = pygame.image.load(os.path.join("ships", "ship3.png"))
ENEMY_SPACE_SHIP2 = pygame.image.load(os.path.join("ships", "ship4.png"))
ENEMY_SPACE_SHIP3 = pygame.image.load(os.path.join("ships", "ship5.png"))

# Laser Bullets
BLUE_LASER = pygame.image.load(os.path.join("bullets", "01.png"))
RED_LASER = pygame.image.load(os.path.join("bullets", "02.png"))
PINK_LASER = pygame.image.load(os.path.join("bullets", "03.png"))
PURPLE_LASER = pygame.image.load(os.path.join("bullets", "04.png"))

# Background 
BG = pygame.transform.scale(pygame.image.load(os.path.join("backgrounds", "river_background.png")), (WIDTH, HEIGHT))

# SOUNDS
GAME_SOUND = pygame.mixer.Sound(os.path.join("sounds", "spaceship_shooter.mp3"))
LASER_SOUND = pygame.mixer.Sound(os.path.join("sounds", "blaster.mp3"))

#class for laser behavior
class Laser:
    def __init__(self, x, y, img): #initialize class 
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window): # draw lasers
        window.blit(self.img, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

# class for  all ships behavior
class Ship:
    COOLDOWN = 15 # This is a class attribute, indicating the cooldown duration in frames.
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown() # This method is called to update the cooldown counter
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT): # if hits window border
                self.lasers.remove(laser) 
            elif laser.collision(obj): # if hits object
                obj.health -= 10
                self.lasers.remove(laser) 

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter >= 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - self.get_width() + 10, self.y - self.get_height(), self.laser_img)
            self.lasers.append(laser) 
            pygame.mixer.Channel(0).play(LASER_SOUND, maxtime = 600)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = MAIN_SPACE_SHIP
        self.laser_img = PURPLE_LASER
        self.mask = pygame.mask.from_surface(self.ship_img) # tells us if we hit ships pixels or not
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT): # if hits window border
                self.lasers.remove(laser) 
            else:
                for obj in objs: # removes an enemy if it was hit
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))
class Enemy(Ship):
    ENEMY_SHIP_MAP = {
                "Enemy1":(ENEMY_SPACE_SHIP1, BLUE_LASER),
                "Enemy2":(ENEMY_SPACE_SHIP2, PINK_LASER),
                "Enemy3":(ENEMY_SPACE_SHIP3, RED_LASER)
                } 

    def __init__(self, x, y, enemy_ship, health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.ENEMY_SHIP_MAP[enemy_ship]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y + 50, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# Main function
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("monospace", 40)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 3

    player = Player(300, 630)

    lost = False
    lost_count = 0
    
    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # Display text
        lives_label = main_font.render(f"Lives:{lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level:{level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)
        if lost:
            lost_label = lost_font.render("You lost!!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window() 
        
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost: 
            if lost_count > FPS * 3: # lost will appear message for 3 seconds
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 3 # enemies number
            for i in range(wave_length): # spawn enemies
                enemy = Enemy(random.randrange(0, WIDTH-100), random.randrange(-1000, -100), random.choice(["Enemy1", "Enemy2", "Enemy3"])) # range of enemy spawning
                enemies.append(enemy)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed() # Dictionary of all keys
        if (keys[pygame.K_a]  or keys[pygame.K_LEFT]) and player.x - player_vel > 0: # left
            player.x -= player_vel
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y - player_vel > 0: # up
            player.y -= player_vel
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel   
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel  
        if keys[pygame.K_SPACE]:
            player.shoot()
        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 30) == 1: # number of enemy shoots
                enemy.shoot()
            
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)  
                    
        player.move_lasers(-laser_vel, enemies)
    

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 40)
    title_font_small = pygame.font.SysFont("comicsans", 30)
    run = True
    sound_volume = 0.05
    GAME_SOUND.set_volume(sound_volume)
    while run:
        GAME_SOUND.play(loops = -1)
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 300))
        title_label3 = title_font_small.render("Press the WASD or arrow keys to move", 1, (255,255,255))
        WIN.blit(title_label3, (WIDTH/2 - title_label3.get_width()/2, 400))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()