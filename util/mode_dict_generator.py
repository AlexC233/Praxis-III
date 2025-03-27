#
# Direction constants, top down view facing the shaft
#
DIR_CW  = False  # Clockwise
DIR_CCW = True   # Counterclockwise

DEFAULT_STEP_DELAY = 0.01

#
# For each movement mode, define the direction and delay for every motor.
#
MOVE_FORWARD0 = {
    "motor0": {"direction": DIR_CW,   "delay": DEFAULT_STEP_DELAY},
    "motor1": {"direction": DIR_CCW,  "delay": DEFAULT_STEP_DELAY},
    "motor2": {"direction": DIR_CW,   "delay": DEFAULT_STEP_DELAY},
    "motor3": {"direction": DIR_CCW,  "delay": DEFAULT_STEP_DELAY},
}

MOVE_BACKWARD0 = {
    "motor0": {"direction": DIR_CCW,  "delay": DEFAULT_STEP_DELAY},
    "motor1": {"direction": DIR_CW,   "delay": DEFAULT_STEP_DELAY},
    "motor2": {"direction": DIR_CCW,  "delay": DEFAULT_STEP_DELAY},
    "motor3": {"direction": DIR_CW,   "delay": DEFAULT_STEP_DELAY},
}

MOVE_LEFT0 = {
    "motor0": {"direction": DIR_CW,   "delay": DEFAULT_STEP_DELAY},
    "motor1": {"direction": DIR_CW,   "delay": DEFAULT_STEP_DELAY},
    "motor2": {"direction": DIR_CW,   "delay": DEFAULT_STEP_DELAY},
    "motor3": {"direction": DIR_CW,   "delay": DEFAULT_STEP_DELAY},
}

MOVE_RIGHT0 = {
    "motor0": {"direction": DIR_CCW,   "delay": DEFAULT_STEP_DELAY},
    "motor1": {"direction": DIR_CCW,   "delay": DEFAULT_STEP_DELAY},
    "motor2": {"direction": DIR_CCW,   "delay": DEFAULT_STEP_DELAY},
    "motor3": {"direction": DIR_CCW,   "delay": DEFAULT_STEP_DELAY},
}

MOVE_UP0 = {
    "motor0": {"direction": DIR_CW,    "delay": DEFAULT_STEP_DELAY},
    "motor1": {"direction": DIR_CW,    "delay": DEFAULT_STEP_DELAY},
    "motor2": {"direction": DIR_CCW,   "delay": DEFAULT_STEP_DELAY},
    "motor3": {"direction": DIR_CCW,   "delay": DEFAULT_STEP_DELAY},
}

MOVE_DOWN0 = {
    "motor0": {"direction": DIR_CCW,   "delay": DEFAULT_STEP_DELAY},
    "motor1": {"direction": DIR_CCW,   "delay": DEFAULT_STEP_DELAY},
    "motor2": {"direction": DIR_CW,    "delay": DEFAULT_STEP_DELAY},
    "motor3": {"direction": DIR_CW,    "delay": DEFAULT_STEP_DELAY},
}

# MOVE_TEST = {
#     "motor0": {"direction": DIR_CCW,   "delay": DEFAULT_STEP_DELAY},
#     "motor1": {"direction": DIR_CCW,   "delay": DEFAULT_STEP_DELAY},
#     "motor2": {"direction": DIR_CW,    "delay": DEFAULT_STEP_DELAY},
#     "motor3": {"direction": DIR_CW,    "delay": DEFAULT_STEP_DELAY},

# }


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

# print and compare the generated dictionaries with the original ones  
# in an organized way using loops and in format
for mode in MODE_ACTIONS.keys():
    print(f"{mode}:")
    print(f"Original: {build_move_dict(mode)}")
    print(f"Generated: {globals()[f'MOVE_{mode.upper()}']}")
    print()
    # output true if the generated dictionary is equal to the original one
    print(f"Equal: {build_move_dict(mode) == globals()[f'MOVE_{mode.upper()}']}")
