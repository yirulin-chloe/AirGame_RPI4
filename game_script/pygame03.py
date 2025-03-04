# Create game screen, background, hero
import pygame
from plane_sprites import *
# initialize game
pygame.init()
# Create game screen: 600 x 900
screen = pygame.display.set_mode((600, 900))

# Create background: load image -> blit graph pic -> update window
bg = pygame.image.load("./resource/images/bg/bg0.jpg")
screen.blit(bg, (0, 0)) # graph's location in screen

# Create hero
hero = pygame.image.load("./resource/images/hero/hero02.png")
screen.blit(hero, (250, 500))

# Update window after setting up bg and hero
pygame.display.update()

# Create clock
clock = pygame.time.Clock()

# 1. Define rect to record plane initial position & its size
hero_rect = pygame.Rect(250, 500, 120, 100)

# create enemy sprite
enemy = GameSprite("./resource/images/enemy/enemy2.png")
enemy2 = GameSprite("./resource/images/enemy/enemy3.png", speed=2)
# create enemy sprite group
enemy_group = pygame.sprite.Group(enemy, enemy2)

# Game start (start looping)
# while loop: so that the window can stay open
while True:
    # frequency of frame
    # clock.tick(40) means that for every second at most 40 frames should pass.
    clock.tick(60)

    # capture event: capture user input
    for event in pygame.event.get():
        # check if user want to quit game
        if event.type == pygame.QUIT:
            print("Exit game...")
            pygame.quit() # exit module
            exit() # stop executing program

    # 2. edit plane position
    hero_rect.y -= 1
    # if plane flies off top of the screen
    if hero_rect.y <= -hero_rect.height:
        hero_rect.y = 900
    # 3. blit graph pic
    screen.blit(bg, (0, 0))
    screen.blit(hero, hero_rect)

    # for sprite
    # update all sprite position
    enemy_group.update()
    # draw all sprite on screen
    enemy_group.draw(screen)

    # 4. update
    pygame.display.update()

# close game
pygame.quit()

"""
pygame.display.set_mode(resolution = (0.0), flags = 0, depth = 0)
used to create, manage game window
    - resolution: size of window <- we only need to specify this
    - flag: whether the screen is full
    - depth: color digit
"""
