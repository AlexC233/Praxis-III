import board
import math

# All units in CM
#
# Pin configuration for each motor, including index
#
MOTOR_PINS = {
    "motor0": {"INDEX": 0, "DIR_PIN": board.GP0, "STEP_PIN": board.GP1},
    "motor1": {"INDEX": 1, "DIR_PIN": board.GP2, "STEP_PIN": board.GP3},
    "motor2": {"INDEX": 2, "DIR_PIN": board.GP4, "STEP_PIN": board.GP5},
    "motor3": {"INDEX": 3, "DIR_PIN": board.GP14, "STEP_PIN": board.GP15},
}

MOTOR_PINS = {
    "motor0": {"INDEX": 0, "DIR_PIN": board.GP14, "STEP_PIN": board.GP15},
    "motor1": {"INDEX": 1, "DIR_PIN": board.GP4, "STEP_PIN": board.GP5},
    "motor2": {"INDEX": 2, "DIR_PIN": board.GP2, "STEP_PIN": board.GP3},
    "motor3": {"INDEX": 3, "DIR_PIN": board.GP0, "STEP_PIN": board.GP1},
}

MOTOR_ANCHORS = [
            (0.0,  0.0,  0.0),  # Motor0 anchor
            (1.0,  0.0,  0.0),  # Motor1 anchor
            (1.0,  1.0,  0.0),  # Motor2 anchor
            (0.0,  1.0,  0.0),  # Motor3 anchor
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
    "forward": {
        "motor0": "shorten",  
        "motor1": "release",  
        "motor2": "release",  
        "motor3": "shorten",  
    },
    "backward": {
        "motor0": "release",  
        "motor1": "shorten",  
        "motor2": "shorten",  
        "motor3": "release",  
    },
    "left": {
        "motor0": "shorten",  
        "motor1": "shorten",   
        "motor2": "release",  
        "motor3": "release",  
    },
    "right": {
        "motor0": "release",  
        "motor1": "release",   
        "motor2": "shorten",  
        "motor3": "shorten",  
    },
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


