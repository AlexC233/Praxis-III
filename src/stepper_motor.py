import time
import board
import digitalio

class StepperMotor:

    def __init__(self, index: int, dir_pin: board.Pin, step_pin: board.Pin, steps_per_rev: int, initial_dir: bool=False):
        """
        params:
        index: int, index of the motor, starting from 0
        dir_pin: instance of board.Pin, direction pin
        step_pin: instance of board.Pin, steps pin
        steps_per_rev: int, steps per revolation, specific to motor type
        initial_direction: bool, initial direction for initialization of the motor
        Encapsulates a single stepper motor.
    """
        self.index = index

        self.dir_pin = digitalio.DigitalInOut(dir_pin)
        self.dir_pin.direction = digitalio.Direction.OUTPUT
        self.dir_pin.value = initial_dir  # default direction

        self.step_pin = digitalio.DigitalInOut(step_pin)
        self.step_pin.direction = digitalio.Direction.OUTPUT
        self.step_pin.value = False

        self.steps_per_rev = steps_per_rev

    def single_step(self, direction: bool, delay: float):
        """
        params:
        direction: bool, direction of rotation
        delay: float, half delay for speed control
        Perform a single step in the specified direction, with the specified delay.
        """
        self.dir_pin.value = direction

        self.step_pin.value = True
        time.sleep(delay)

        self.step_pin.value = False
        time.sleep(delay)

    def step(self, direction: bool, steps: int, delay: float):
        """
        params:
        direction: bool, direction of rotation
        steps: int, number of steps
        delay: float, half delay for speed control
        Rotate the motor by `steps` steps in the given `direction`,
        pausing 2 times `delay` seconds between each step.
        """
        self.dir_pin.value = direction

        for _ in range(steps):
            self.step_pin.value = True
            time.sleep(delay)
            self.step_pin.value = False
            time.sleep(delay)
