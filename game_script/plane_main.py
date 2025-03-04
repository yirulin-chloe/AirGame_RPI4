import random
import pygame
from plane_sprites import *
from gpiozero import Button, LED

class PlaneGame(object):
    def __init__(self):
        print("Game initialization")
        # 1. Build game window -> see pygame02.py for detail
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. Create game clock
        self.clock = pygame.time.Clock()
        # 3. Private method: build sprite, sprite group
        self.__create_sprites()
        # 4. Set up timer: Build enemy: this will execute CREATE_ENEMY_EVENT every 1 sec
        #                  Fire bullet: this will execute HERO_FIRE_EVENT every 0.5 sec
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        #pygame.time.set_timer(HERO_FIRE_EVENT, 500) 

        ## 5. For GPIO buttons control
        self.left_button = Button(2)  # GPIO2
        self.right_button = Button(3)  # GPIO3
        self.shoot_button = Button(17, bounce_time = 0.05) # GPIO17
        self.pause_button = Button(27, bounce_time = 0.1)  # GPIO27

        self.left_button.when_pressed = self.move_left
        self.left_button.when_released = self.stop_movement
        self.right_button.when_pressed = self.move_right
        self.right_button.when_released = self.stop_movement
        self.shoot_button.when_pressed = self.shoot
        self.pause_button.when_pressed = self.toggle_pause
        self.pause_button.when_held = self.exit_game

        self.paused = False  # Track pause state

        # 6. Start LED - indicating if the game has started
        self.start_led= LED(4)

        #7. Indicating game over
        self.is_game_over = False

    # GPIO Button Functions
    def move_left(self):
        #print("GPIO button was pressed: left")
        self.hero.speed = -3

    def move_right(self):
        #print("GPIO button was pressed: right")
        self.hero.speed = 3

    # Stop movement when button is released
    def stop_movement(self):
        #print("Button is released")
        self.hero.speed = 0 

    # Hero shooting bullet
    def shoot(self):
        if not self.paused:
            print("Shoot bullet")
            #self.shoot_sound.play()
            self.hero.fire()

    def toggle_pause(self):
        self.paused = not self.paused
        print("Game Paused" if self.paused else "Game Resumed")

    def exit_game(self):
        print("Long pressed detected - Exiting game...")
        # Just set a flag instead of calling game_over directly
        self.is_game_over = True
        # # Quit the game
        # pygame.quit()
        # exit()

    def __create_sprites(self):
        # create background sprite & sprite group
        bg1 = BackGround()
        bg2 = BackGround(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)

        # create enemy sprite & sprite group
        self.enemy_group = pygame.sprite.Group()

        # create hero sprite & sprite group
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)


    def start_game(self):
        print("Start game")
        self.start_led.on()
        while True:
            # Always allow event handling while paused
            self.__event_handler() 
            # Check the exit flag
            if self.is_game_over:
                PlaneGame.__game_over(self.screen)
                break
            if not self.paused:
                # 1. Set frame frequency
                self.clock.tick(FRAME_PER_SEC)
                # 2. Check collision
                self.__check_collide()
                # 3. Update/draw sprite
                self.__update_sprites()
                # 4. Update display
                pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               PlaneGame.__game_over(self.screen)
            elif event.type == CREATE_ENEMY_EVENT:
                #print("Enemy shows up...")
                # create enemy sprite and add to its group
                enemy = Enemy()
                self.enemy_group.add(enemy)
            ## Hero fire bullet:
            # elif event.type == HERO_FIRE_EVENT:
            #     self.hero.fire()
        ## Hero movement - for keyboard usage.
        # keys_pressed = pygame.key.get_pressed()
        # if keys_pressed[pygame.K_RIGHT]:
        #     self.hero.speed = 3
        # elif keys_pressed[pygame.K_LEFT]:
        #     self.hero.speed = -3
        # else:
        #     self.hero.speed = 0


    def __check_collide(self):
        # 1. Bullet destroy enemy, and both are deleted: True
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        # 2. Enemy destroy hero, enemy is deleted
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)

    def __update_sprites(self):
        # update background
        self.back_group.update()
        self.back_group.draw(self.screen)
        # update enemy
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        # update hero
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        # update bullet
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)


    # This is a static method since we don't need to use 'self'
    @staticmethod
    def __game_over(screen):
        print("Game over")
        gameover_image = pygame.image.load('./resource/images/gameover.png') 
        
        # Display the gameover image
        screen.fill((0, 0, 0))  # Clear the screen with black
        screen.blit(gameover_image, (0, 0))  # Blit the gameover image onto the screen
        pygame.display.update()  # Update the screen to show the image

        pygame.time.wait(2000)  # Wait for 2 seconds to show the gameover image
        # Give Pygame some time to cleanly exit
        time.sleep(1)  # Add a small delay before quitting
        # Quit the game
        pygame.quit()
        exit()


if __name__ == '__main__':
    # create game object
    game = PlaneGame()
    # start game
    game.start_game()
