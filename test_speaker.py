import pygame
import time

# Initialize the Pygame mixer
pygame.mixer.init()

# Load the MP3 file (change the path to your file)
pygame.mixer.music.load('gameBackground.wav')  # Replace with the actual file path

# Play the MP3 file
pygame.mixer.music.play()

# Wait until the music finishes playing
while pygame.mixer.music.get_busy():
    time.sleep(1)

print("Audio playback finished.")
