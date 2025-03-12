import time
import constant
from stepper_motor import StepperMotor

class Controller:

    def __init__(self):
        """
        Coordinates the four motors so they can run simultaneously.
        """
        # Create one StepperMotor object per named motor
        # motors = {'motor0': StepperMotor,}
        self.motors = {}
        for motor_name, pins in constant.MOTOR_PINS.items():
            self.motors[motor_name] = StepperMotor(
                index=pins["INDEX"],
                dir_pin=pins["DIR_PIN"],
                step_pin=pins["STEP_PIN"],
                steps_per_rev=constant.STEPS_PER_REV
            )

    def move_motors(self, movement_dict):
        """
        params:
        movement_dict: dict
            {
              "motor0": {"direction": bool, "steps": int, "delay": float},
              "motor1": {"direction": bool, "steps": int, "delay": float},
              ...
            }
        Drives the four motor approximately at the same time.
        """
        # Determine the maximum steps among all motors
        max_steps = max(movement_dict[m]["steps"] for m in movement_dict)

        # Track how many steps each motor has completed
        steps_completed = {m: 0 for m in self.motors}

        for _ in range(max_steps):
            # First half of the step: set step pins high for each motor that still needs steps
            for motor_name, motor_obj in self.motors.items():
                needed_steps = movement_dict[motor_name]["steps"]
                direction    = movement_dict[motor_name]["direction"]
                if steps_completed[motor_name] < needed_steps:
                    # Set the direction for this motor
                    motor_obj.dir_pin.value = direction
                    # Step pin high
                    motor_obj.step_pin.value = True

            # Determine half-step delay: the minimum of the active motors' delays
            active_delays = []
            for motor_name in self.motors:
                if steps_completed[motor_name] < movement_dict[motor_name]["steps"]:
                    active_delays.append(movement_dict[motor_name]["delay"])
            if len(active_delays) > 0:
                half_step_delay = min(active_delays)
            else:
                half_step_delay = 0

            time.sleep(half_step_delay)

            # Second half of the step: set step pins low and increment step counters
            for motor_name, motor_obj in self.motors.items():
                if steps_completed[motor_name] < movement_dict[motor_name]["steps"]:
                    motor_obj.step_pin.value = False
                    steps_completed[motor_name] += 1

            time.sleep(half_step_delay)

    #
    # Six working modes, each referencing one of the dictionaries in constant.py
    #
    def forward(self):
        self.move_motors(constant.MOVE_FORWARD)

    def backward(self):
        self.move_motors(constant.MOVE_BACKWARD)

    def left(self):
        self.move_motors(constant.MOVE_LEFT)

    def right(self):
        self.move_motors(constant.MOVE_RIGHT)

    def up(self):
        self.move_motors(constant.MOVE_UP)

    def down(self):
        self.move_motors(constant.MOVE_DOWN)
