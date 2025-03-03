from gpiozero import Button, LED, OutputDevice
import time
import pygame

# Initialize Pygame mixer
pygame.mixer.init()

# Track last state of left button
# to ensure one action per pressed
prev_left_button_state = False
prev_right_button_state = False

# Left/Right Buttons: 
left_button = Button(2)
right_button = Button(3)

# Indicate game started
game_led = LED(4) 

# # Control sound
# speaker = OutputDevice(12)

# # Sound effects
# background_music = pygame.mixer.Sound('gameBackground.mp3')
# shoot_sound = pygame.mixer.Sound('shoot.mp3')
# crash_sound = pygame.mixer.Sound('explode.mp3')

## Set volumn levels
#background_music.set_volume(0.5)
# shoot_sound.set_volume(0.8)
# crash_sound.set_volume(0.5)

# Play background music continuously
def play_background_music():
    #pygame.mixer.Channel(0).play(background_music, loops=-1)  # Loop forever
    pygame.mixer.music.load("gameBackground.wav")
    pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # Play in a loop
    time.sleep(10)

# Play shooting sound effect on a separate channel
def play_shoot_sound():
    pygame.mixer.Channel(1).play(shoot_sound)  # Uses a different channel

# Play crash sound effect and activate speaker
def play_crash_sound():
    pygame.mixer.Channel(2).play(crash_sound)  # Uses a different channel

    # Activate the speaker (turn on the transistor)
    speaker.on()
    
    # Wait for the crash sound to finish playing
    time.sleep(crash_sound.get_length())
    
    # Deactivate the speaker after the sound finishes
    speaker.off()

# Example: Simulating the game events
def simulate_game_events():
    print("Starting the game...")
    play_background_music()  # Start background music

    time.sleep(2)  # Simulate delay

    print("Plane Shoots!")
    play_shoot_sound()  # Play shooting sound while background music plays

    time.sleep(3)  # Simulate delay

    print("The plane has crashed!")
    play_crash_sound()  # Play crash sound while background music plays

# # Run the simulation
# simulate_game_events()

# # Play background music
# speaker.on()
# play_background_music()

while True:
    # Indicating game start
    game_led.on()

    left = left_button.is_pressed
    if left and not prev_left_button_state:
        print("Plane moves left!")

    right = right_button.is_pressed
    if right and not prev_right_button_state:
        print("Plane moves right!")

    # Update prev button state
    prev_left_button_state = left
    prev_right_button_state = right
    
