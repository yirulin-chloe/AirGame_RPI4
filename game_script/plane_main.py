import random
import pygame
from plane_sprites import *
from gpiozero import Button, LED
import time

# Initial hero's health rate
INIT_HEART = 3

class PlaneGame(object):
    def __init__(self):
        print("Game initialization")
        # 1. Build game window -> see pygame02.py for detail
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. Create game clock
        self.clock = pygame.time.Clock()
        # 3.0. Hero health
        self.health = INIT_HEART  # Start health rate
        # 3.1 Private method: build sprite, sprite group
        self.__create_sprites()
        # 4. Set up timer: Build enemy: this will execute CREATE_ENEMY_EVENT every 1 sec
        #                  Fire bullet: this will execute HERO_FIRE_EVENT every 0.5 sec
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        #pygame.time.set_timer(HERO_FIRE_EVENT, 500) 

        ## 5. For GPIO buttons control
        self.left_button = Button(2)  # GPIO2
        self.right_button = Button(3)  # GPIO3
        self.shoot_button = Button(17)
        self.pause_button = Button(27, bounce_time = 0.1)  

        self.left_button.when_pressed = self.move_left
        self.left_button.when_released = self.stop_movement
        self.right_button.when_pressed = self.move_right
        self.right_button.when_released = self.stop_movement
        self.shoot_button.when_pressed = self.shoot
        # Pause/Resume & Exit logic
        self.pause_start_time = 0
        self.pause_button.when_pressed = self.start_press_timer
        self.pause_button.when_released = self.evaluate_press_duration

        # 6. Start LED - indicating if the game has started
        self.start_led= LED(4)

        #7. Indicating tags
        self.is_game_over = False
        self.paused = False  # Track pause state
        self.exit = False    # Track if user wants exit game
        self.lose = False    # Track if user has lost

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
        if self.paused:
            print("Game Paused")
            pygame.time.set_timer(CREATE_ENEMY_EVENT, 0)  # Stop enemy spawning
        else:
            print("Game Resumed")
            pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)  # Resume enemy spawning

    def start_press_timer(self):
        self.pause_start_time = time.time()

    def evaluate_press_duration(self):
        press_duration = time.time() - self.pause_start_time
        if press_duration < 1:  # Short press (<1 sec) for pause/resume
            self.toggle_pause()
        else:  # Long press (≥1 sec) for exit
            self.exit_game()

    def exit_game(self):
        print("Long pressed detected - Exiting game...")
        # Just set a flag
        self.exit = True

    def lose_game(self):
        print("Losing game...")
        # Just set a flag 
        self.is_game_over = True

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

        # Health tracking
        self.health_group = pygame.sprite.Group()
        for i in range(3):  # Create hearts based on health count
            heart = Health()
            heart.rect.x = SCREEN_RECT.right - (i + 1) * (heart.rect.width + 10)  # Positioning hearts
            heart.rect.y = 20  # Position near top
            self.health_group.add(heart)

    def start_game(self):
        print("Start game")
        self.start_led.on()
        while True:
            # Always allow event handling while paused
            self.__event_handler() 
            # Check game over flag (if user lose)
            if self.is_game_over:
                self.__game_over()
                break
            # Check exiting game 
            if self.exit:
                self.__exit_game(self.screen)
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
            else:
                self.__pause(self.screen)

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               self.__game_over()
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
        if enemies:
            self.health -= 1  # Lose 1 health when hit by enemy
            print(f"Enemy hit Hero! Lose Health")
                # Remove one heart from health display

            if self.health_group:
                last_heart = self.health_group.sprites()[-1]  # Get last heart
                last_heart.kill()  # Remove it from the group

        # Enemy passes hero (bottom of screen)
        for enemy in self.enemy_group:
            if enemy.rect.y >= SCREEN_RECT.height:
                self.health -= 1  # Lose 1 health
                enemy.kill()  # Remove enemy
                print(f"Enemy passed! Lose Health")

                if self.health_group:
                    last_heart = self.health_group.sprites()[-1]  # Get last heart
                    last_heart.kill()  # Remove it from the group

        # 4. Check if hero is out of health
        if self.health <= 0:
            self.lose_game()

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
        # update health 
        self.health_group.update()
        self.health_group.draw(self.screen)


    # This is a static method since we don't need to use 'self'
    #@staticmethod
    def __game_over(self):
        print("Game over")
        gameover_image = pygame.image.load('./resource/images/gameover.png') 
        # Resize the image to the desired dimensions
        gameover_image = pygame.transform.scale(gameover_image, (500, 400))
        # Initial position (above the screen)
        x = 50  # Centered horizontally
        y = -300  # Start above the screen

        while y < 150:  # Move down until it reaches its final position
            self.screen.fill((0, 0, 0))  # Clear screen
            self.screen.blit(gameover_image, (x, y))  # Draw image at new position
            pygame.display.update()  # Refresh screen
            
            y += 10  # Move downward in steps (increase speed by adjusting this)
            self.clock.tick(30)  # Control animation speed (30 FPS)

        pygame.time.wait(2000)  # Hold for 2 seconds before quitting
        pygame.quit()
        exit()

    @staticmethod
    def __pause(screen):
        print("Pausing game")
        pause_image = pygame.image.load('./resource/images/Pause.png') 
        # Resize the image to the desired dimensions
        pause_image = pygame.transform.scale(pause_image, (500, 400))
        
        # Display the gameover image
        screen.blit(pause_image, (30, 250))  # Blit the image onto the screen
        pygame.display.update()  # Update the screen to show the image

        pygame.time.wait(2000)  # Wait for 2 seconds to show the image
        # Give Pygame some time to cleanly exit
        time.sleep(1)  # Add a small delay before quitting

    @staticmethod
    def __exit_game(screen):
        print("Exiting game")
        exit_image = pygame.image.load('./resource/images/Exit.png') 
        # Resize the image to the desired dimensions
        exit_image = pygame.transform.scale(exit_image, (500, 400))
        
        # Display the image
        screen.blit(exit_image, (30, 250))  # Blit the image onto the screen
        pygame.display.update()  # Update the screen to show the image

        pygame.time.wait(2000)  # Wait for 2 seconds to show the image
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
