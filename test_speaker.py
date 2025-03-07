import pygame
import time

# Initialize the Pygame mixer
pygame.mixer.init()

# Load the MP3 file (change the path to your file

pygame.mixer.music.load('bg.mp3')  # Replace with the actual file path
shoot_sound = pygame.mixer.Sound("shoot.mp3")
#pygame.mixer.music.load('explode.wav')
#pygame.mixer.music.load('gameBackground.wav')


# Play the MP3 file
pygame.mixer.music.play()

# Wait until the music finishes playinsg
while pygame.mixer.music.get_busy():
    time.sleep(1)

print("Audio playback finished.")
