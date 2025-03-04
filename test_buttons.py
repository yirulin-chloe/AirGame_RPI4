from gpiozero import Button
from signal import pause

# Define buttons
left_button = Button(2, pull_up=True)  # GPIO 2
right_button = Button(3, pull_up=True) # GPIO 3

def move_left():
    print("Left button pressed")  # Replace with movement logic

def move_right():
    print("Right button pressed")  # Replace with movement logic

# Attach event listeners
left_button.when_pressed = move_left
right_button.when_pressed = move_right

print("Waiting for button presses...")
pause()  # Keep the script running
