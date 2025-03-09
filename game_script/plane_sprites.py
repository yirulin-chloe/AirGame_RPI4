import random
import pygame
# Define constant: screen
SCREEN_RECT = pygame.Rect(0, 0, 600, 900)
# Define constant: frame frequency
FRAME_PER_SEC = 60
# Define constant: timer for enemy event
CREATE_ENEMY_EVENT = pygame.USEREVENT
# Define constant: timer for hero's bullet event
HERO_FIRE_EVENT = pygame.USEREVENT + 1
# Defind images:
BULLET_IMG = "./resource/images/bullet/10.png"
BACKGROUND_IMG = "./resource/images/bg/bg0.jpg"
ENEMY_IMG = "./resource/images/enemy/enemy2.png"
HERO_IMG = "./resource/images/hero/hero02.png"
HEALTH_IMG = "./resource/images/heart.png"
EXPLODE_IMG = "./resource/images/boom01.png"

class GameSprite(pygame.sprite.Sprite):
    """ plane fight with sprite"""

    def __init__(self, image_name, speed=1):
        super().__init__()
        # define attributions
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self, *args):
        # moving up
        self.rect.y += self.speed

# we will have two pictures for background:top and bottom.
class BackGround(GameSprite):

    def __init__(self, is_alt=False): # if false, background pic is not the topper pic.
        super().__init__(BACKGROUND_IMG)
        if is_alt: # if it is topper picture
            self.rect.y = - self.rect.height

    def update(self):
        # 1. use parent method
        super().update()
        # 2. check if image move out screen, then move it back to top of screen
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    def __init__(self, explosion_group):
        # 1. use parent method, create enemy sprite
        super().__init__(ENEMY_IMG)
        # 2. enemy speed
        self.speed = random.randint(1, 3)
        # 3. enemy initial position
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
        self.explosions_group = explosion_group

    def update(self):
        # 1. use parent method, vertical movement
        super().update()

    # delete sprite to save cache
    def __del__(self):
        # print("enemy died %s" % self.rect)
        # Create an explosion at the enemy's position when deleted
        explosion = Explosion(self.rect.centerx, self.rect.centery-5)
        self.explosions_group.add(explosion)
        pass


class Hero(GameSprite):
    def __init__(self):
        # 1. use parent method, set image & speed
        super().__init__(HERO_IMG)
        self.speed = 0
        # 2. set hero's initial position
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.bottom - 200
        # 3. set bullet sprite & sprite group
        self.bullets = pygame.sprite.Group()

    def update(self):
        # hero moving horizontally: left or right
        self.rect.x += self.speed
        # control hero not moving outside of screen
        if self.rect.left < 0: # also x = left
            self.rect.left = 0
        elif self.rect.right > SCREEN_RECT.right: # also x + width = right
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        print("firing bullet")
        # fire n bullets at once
        n = 1
        for i in range(n):
            # 1. create bullet sprite
            bullet = Bullet()
            # 2. set bullet position: right above, and in middle of  hero
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            # add bullet sprite into sprite group
            self.bullets.add(bullet)

class Health(GameSprite):
    def __init__(self):
        #use parent method, set image & speed
        super().__init__(HEALTH_IMG)
        self.speed = 0
        self.image = pygame.transform.scale(self.image, (40, 30))

    def update(self): 
        pass

    def __del__(self):
        #print("heart is being deleted")
        pass

class Bullet(GameSprite):
    def __init__(self):
        super().__init__(BULLET_IMG, -2) # speed -2: bullet moves up

    def update(self):
        # use parent method, let bullet flying vertically up
        super().update()
        # check if bullet flying out of screen
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        #print("bullet is being deleted")
        pass

class Explosion(GameSprite):
    def __init__(self, x, y):
        super().__init__(EXPLODE_IMG)
        self.rect.center = (x, y)
        self.frame_counter = 10  # time of explosion on screen

    def update(self):
        self.frame_counter -= 1
        if self.frame_counter <= 0:
            self.kill()  # Remove the explosion sprite after a short time
