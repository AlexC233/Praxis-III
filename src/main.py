import time
import board
import digitalio

# Define pins
DIR_PIN = digitalio.DigitalInOut(board.GP8)
STEP_PIN = digitalio.DigitalInOut(board.GP9)

# Set pins as outputs
DIR_PIN.direction = digitalio.Direction.OUTPUT
STEP_PIN.direction = digitalio.Direction.OUTPUT

def step_motor(steps, direction, delay=0.001):
    """Move stepper motor a given number of steps in a direction."""
    DIR_PIN.value = direction  # Set direction (1 = CW, 0 = CCW)

    for _ in range(steps):
        STEP_PIN.value = True
        time.sleep(delay)  # Step pulse width
        STEP_PIN.value = False
        time.sleep(delay)

while True:
    step_motor(200, True)  # Move forward 1 revolution
    time.sleep(1)
    step_motor(200, False)  # Move backward 1 revolution
    time.sleep(1)
