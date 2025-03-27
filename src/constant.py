import board
import math

# All units in CM
#
INITIAL_POSITION = (3.0, 3.0, 36.0)  # Initial position of the robot in CM
# Pin configuration for each motor, including index
#
# MOTOR_PINS = {
#     "motor0": {"INDEX": 0, "DIR_PIN": board.GP0, "STEP_PIN": board.GP1},
#     "motor1": {"INDEX": 1, "DIR_PIN": board.GP2, "STEP_PIN": board.GP3},
#     "motor2": {"INDEX": 2, "DIR_PIN": board.GP4, "STEP_PIN": board.GP5},
#     "motor3": {"INDEX": 3, "DIR_PIN": board.GP14, "STEP_PIN": board.GP15},
# }

MOTOR_PINS = {
    "motor0": {"INDEX": 0, "DIR_PIN": board.GP14, "STEP_PIN": board.GP15},
    "motor1": {"INDEX": 1, "DIR_PIN": board.GP4, "STEP_PIN": board.GP5},
    "motor2": {"INDEX": 2, "DIR_PIN": board.GP2, "STEP_PIN": board.GP3},
    "motor3": {"INDEX": 3, "DIR_PIN": board.GP0, "STEP_PIN": board.GP1},
}

# Assuming diamond edge length of 46 cm
DIAMOND_SIZE = 46.0
CENTER_HEIGHT = 36.0

MOTOR_ANCHORS = [
    (DIAMOND_SIZE/2,  0.0,         CENTER_HEIGHT),  # North motor
    (DIAMOND_SIZE,    DIAMOND_SIZE/2, CENTER_HEIGHT),  # East motor
    (DIAMOND_SIZE/2,  DIAMOND_SIZE, CENTER_HEIGHT),  # South motor
    (0.0,          DIAMOND_SIZE/2, CENTER_HEIGHT),  # West motor
]

#
# Stepper Motor Parameters
#
STEPS_PER_REV = 200       # Nemo 17
DEFAULT_STEP_DELAY = 0.01 # Time (in seconds) between steps.

#
# Direction constants, top down view facing the shaft
#
DIR_CW  = False  # Clockwise
DIR_CCW = True   # Counterclockwise


#
# Spool Parameters
SPOOL_DIAMETER = 5.0
SPOOL_CIRCUMFERENCE = math.pi * SPOOL_DIAMETER



MOTOR_SHORTEN_RELEASE = {
    "motor0": {"shorten": DIR_CW,  "release": DIR_CCW},
    "motor1": {"shorten": DIR_CW,  "release": DIR_CCW },
    "motor2": {"shorten": DIR_CCW, "release": DIR_CW},
    "motor3": {"shorten": DIR_CCW, "release": DIR_CW },
}
MODE_ACTIONS = {
    "forward": {  # North (w key)
        "motor0": "shorten",  # North motor (primary)
        "motor1": "release",  # East motor
        "motor2": "release",  # South motor
        "motor3": "release",  # West motor
    },
    "backward": {  # South (s key)
        "motor0": "release",  # North motor
        "motor1": "release",  # East motor
        "motor2": "shorten",  # South motor (primary)
        "motor3": "release",  # West motor
    },
    "left": {  # West (a key)
        "motor0": "release",  # North motor
        "motor1": "release",  # East motor
        "motor2": "release",  # South motor
        "motor3": "shorten",  # West motor (primary)
    },
    "right": {  # East (d key)
        "motor0": "release",  # North motor
        "motor1": "shorten",  # East motor (primary)
        "motor2": "release",  # South motor
        "motor3": "release",  # West motor
    },
    # Up/Down commands control Z-axis movement
    "up": {
        "motor0": "shorten",  
        "motor1": "shorten",   
        "motor2": "shorten",   
        "motor3": "shorten",  
    },
    "down": {
        "motor0": "release",  
        "motor1": "release",  
        "motor2": "release",  
        "motor3": "release",  
    },
}


def build_move_dict(mode_name: str):
    """
    Given a mode_name (e.g. "forward"), build the final dictionary like:
    {
      "motor0": {"direction": DIR_CW or DIR_CCW, "delay": DEFAULT_STEP_DELAY},
      "motor1": {...},
      ...
    }
    """
    move_dict = {}
    for motor, action in MODE_ACTIONS[mode_name].items():
        move_dict[motor] = {
            "direction": MOTOR_SHORTEN_RELEASE[motor][action],
            "delay": DEFAULT_STEP_DELAY
        }
    return move_dict


MOVE_FORWARD  = build_move_dict("forward")
MOVE_BACKWARD = build_move_dict("backward")
MOVE_LEFT     = build_move_dict("left")
MOVE_RIGHT    = build_move_dict("right")
MOVE_UP       = build_move_dict("up")
MOVE_DOWN     = build_move_dict("down")


