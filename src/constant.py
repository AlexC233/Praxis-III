import board

#
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

#
# Stepper Motor Parameters
#
STEPS_PER_REV = 200       # Nemo 17
DEFAULT_STEP_DELAY = 0.01 # Time (in seconds) between steps. Adjust as needed.

#
# Direction constants, top down view facing the shaft
#
DIR_CW  = False  # Clockwise
DIR_CCW = True   # Counterclockwise


# get_steps(motor, movement_mode, current_position):

#
# For each movement mode, define the direction, number of steps,
# and delay for every motor. Adjust these to suit your robot.
#
MOVE_FORWARD = {
    "motor0": {"direction": DIR_CW,  "steps": 10, "delay": DEFAULT_STEP_DELAY},
    "motor1": {"direction": DIR_CCW,  "steps": 10, "delay": DEFAULT_STEP_DELAY},
    "motor2": {"direction": DIR_CW,  "steps": 10, "delay": DEFAULT_STEP_DELAY},
    "motor3": {"direction": DIR_CCW,  "steps": 10, "delay": DEFAULT_STEP_DELAY},
}

MOVE_BACKWARD = {
    "motor0": {"direction": DIR_CCW, "steps": 10, "delay": DEFAULT_STEP_DELAY},
    "motor1": {"direction": DIR_CW, "steps": 10, "delay": DEFAULT_STEP_DELAY},
    "motor2": {"direction": DIR_CCW, "steps": 10, "delay": DEFAULT_STEP_DELAY},
    "motor3": {"direction": DIR_CW, "steps": 10, "delay": DEFAULT_STEP_DELAY},
}

MOVE_LEFT = {
    "motor0": {"direction": DIR_CW,  "steps": 10, "delay": DEFAULT_STEP_DELAY},
    "motor1": {"direction": DIR_CW, "steps": 10, "delay": DEFAULT_STEP_DELAY},
    "motor2": {"direction": DIR_CW,  "steps": 10, "delay": DEFAULT_STEP_DELAY},
    "motor3": {"direction": DIR_CW, "steps": 10, "delay": DEFAULT_STEP_DELAY},
}

MOVE_RIGHT = {
    "motor0": {"direction": DIR_CCW, "steps": 10, "delay": DEFAULT_STEP_DELAY},
    "motor1": {"direction": DIR_CCW,  "steps": 10, "delay": DEFAULT_STEP_DELAY},
    "motor2": {"direction": DIR_CCW, "steps": 10, "delay": DEFAULT_STEP_DELAY},
    "motor3": {"direction": DIR_CCW,  "steps": 10, "delay": DEFAULT_STEP_DELAY},
}

MOVE_UP = {
    "motor0": {"direction": DIR_CW,  "steps": 5, "delay": DEFAULT_STEP_DELAY},
    "motor1": {"direction": DIR_CW,  "steps": 5, "delay": DEFAULT_STEP_DELAY},
    "motor2": {"direction": DIR_CCW, "steps": 5, "delay": DEFAULT_STEP_DELAY},
    "motor3": {"direction": DIR_CCW, "steps": 5, "delay": DEFAULT_STEP_DELAY},
}

MOVE_DOWN = {
    "motor0": {"direction": DIR_CCW, "steps": 5, "delay": DEFAULT_STEP_DELAY},
    "motor1": {"direction": DIR_CCW, "steps": 5, "delay": DEFAULT_STEP_DELAY},
    "motor2": {"direction": DIR_CW,  "steps": 5, "delay": DEFAULT_STEP_DELAY},
    "motor3": {"direction": DIR_CW,  "steps": 5, "delay": DEFAULT_STEP_DELAY},
}

MOVE_TEST = {
    "motor0": {"direction": DIR_CCW, "steps": 5, "delay": DEFAULT_STEP_DELAY},
    "motor1": {"direction": DIR_CCW, "steps": 5, "delay": DEFAULT_STEP_DELAY},
    "motor2": {"direction": DIR_CW,  "steps": 5, "delay": DEFAULT_STEP_DELAY},
    "motor3": {"direction": DIR_CW,  "steps": 5, "delay": DEFAULT_STEP_DELAY},

}
