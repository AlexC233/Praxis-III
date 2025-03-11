import time
import board
import digitalio

import constant

class StepperMotor:
    def __init__(self, index: int, dir_pin: board.Pin, step_pin: board.Pin, steps_per_rev: int = constant.STEPS_PER_REV):
        """
        Initialize the stepper motor with given GPIO pins.
        :param index: Motor index (0-3).
        :param dir_pin: Instance of GPIO pin on the board for the direction pin.
        :param step_pin: Instance of GPIO pin on the board for the step pin.
        :param steps_per_rev: Number of steps per revolution (default 200 for our stepper motors).
        """
        self.index = index
        
        self.dir_pin = digitalio.DigitalInOut(dir_pin)
        self.dir_pin.direction = digitalio.Direction.OUTPUT
        
        self.step_pin = digitalio.DigitalInOut(step_pin)
        self.step_pin.direction = digitalio.Direction.OUTPUT
        
        self.steps_per_rev = steps_per_rev


    def step(self, direction: int = 0, steps: int = 1, speed: float = constant.ONE_REV_PER_MIN):
        """
        Move a specific number of steps.
        :param steps: Number of steps to move.
        :param speed: Delay between steps (lower value = higher speed).
        """
        self.dir_pin.value = direction
        
        for _ in range(abs(steps)):
            self.step_pin.value = True
            time.sleep(speed)
            self.step_pin.value = False
            time.sleep(speed)
    
    def rotate(self, direction: int = 0, revolutions: float = 1, speed: float = constant.ONE_REV_PER_MIN):
        """
        Rotate the motor by a certain number of revolutions.
        :param direction: Direction of rotation.
        :param revolutions: Number of full revolutions to rotate.
        :param speed: Delay between steps.
        """
        self.dir_pin.value = direction
        
        steps = int(revolutions * self.steps_per_rev)
        self.move_steps(direction, steps, speed)
