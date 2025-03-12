import time
import digitalio

class StepperMotor:
    """
    Encapsulates a single stepper motor, including direction and step pins,
    plus a method to run a specified number of steps at a given speed.
    """
    def __init__(self, dir_pin, step_pin, steps_per_rev, initial_dir=False):
        self.dir_pin = digitalio.DigitalInOut(dir_pin)
        self.dir_pin.direction = digitalio.Direction.OUTPUT
        self.dir_pin.value = initial_dir

        self.step_pin = digitalio.DigitalInOut(step_pin)
        self.step_pin.direction = digitalio.Direction.OUTPUT
        self.step_pin.value = False

        self.steps_per_rev = steps_per_rev

    def step(
        self,
        direction: bool,
        steps: int,
        delay: float
    ):
        """
        Rotate the motor by `steps` steps in the given `direction`,
        pausing `delay` seconds between each step. 
        """
        self.dir_pin.value = direction

        for _ in range(steps):
            # Step pin high
            self.step_pin.value = True
            time.sleep(delay)

            # Step pin low
            self.step_pin.value = False
            time.sleep(delay)
