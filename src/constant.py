import board

#
# Pin configuration
#
MOTOR0_DIR_PIN = board.GP0
MOTOR0_STEP_PIN = board.GP1

MOTOR1_DIR_PIN = board.GP2
MOTOR1_STEP_PIN = board.GP3

MOTOR2_DIR_PIN = board.GP4
MOTOR2_STEP_PIN = board.GP5

MOTOR3_DIR_PIN = board.GP14
MOTOR3_STEP_PIN = board.GP15

#
# Stepper Motor Parameters
#
STEPS_PER_REV = 200       # Typical for many stepper motors
DEFAULT_STEP_DELAY = 0.01 # A small delay between steps (adjust as needed)

#
# Directions
#
DIR_CW  = False  # You can rename or invert these if your motor turns in the opposite direction.
DIR_CCW = True

#
# Movement definitions:
# Each "working mode" uses a list of directions and steps for each of the 4 motors.
# This is just an example configuration for demonstration.
# Feel free to customize these so your motors move as desired.
#

# Move forward
FORWARD_DIRECTIONS = [DIR_CW, DIR_CW, DIR_CW, DIR_CW] 
FORWARD_STEPS      = [100, 100, 100, 100]   # all motors take 100 steps
FORWARD_DELAY      = [DEFAULT_STEP_DELAY]*4

# Move backward
BACKWARD_DIRECTIONS = [DIR_CCW, DIR_CCW, DIR_CCW, DIR_CCW]
BACKWARD_STEPS      = [100, 100, 100, 100]
BACKWARD_DELAY      = [DEFAULT_STEP_DELAY]*4

# Move left
LEFT_DIRECTIONS = [DIR_CW, DIR_CCW, DIR_CW, DIR_CCW]
LEFT_STEPS      = [100, 100, 100, 100]
LEFT_DELAY      = [DEFAULT_STEP_DELAY]*4

# Move right
RIGHT_DIRECTIONS = [DIR_CCW, DIR_CW, DIR_CCW, DIR_CW]
RIGHT_STEPS      = [100, 100, 100, 100]
RIGHT_DELAY      = [DEFAULT_STEP_DELAY]*4

# Move up
UP_DIRECTIONS = [DIR_CW, DIR_CW, DIR_CCW, DIR_CCW]
UP_STEPS      = [100, 100, 100, 100]
UP_DELAY      = [DEFAULT_STEP_DELAY]*4

# Move down
DOWN_DIRECTIONS = [DIR_CCW, DIR_CCW, DIR_CW, DIR_CW]
DOWN_STEPS      = [100, 100, 100, 100]
DOWN_DELAY      = [DEFAULT_STEP_DELAY]*4
