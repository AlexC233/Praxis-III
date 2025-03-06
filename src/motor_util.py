import time
import board
import digitalio
from adafruit_motor import stepper

class StepperMotor:
    def __init__(self, dir_pin, step_pin):
        """
        Initialize the stepper motor with given GPIO pins.
        :param 
        dir_pin: The GPIO pin on the board for the direction pin.
        step_pin: The GPIO pin on the board for the step pin.
        """
        self.dir_pin = digitalio.DigitalInOut(dir_pin)
        self.dir_pin.direction = digitalio.Direction.OUTPUT
        
        self.step_pin = digitalio.DigitalInOut(step_pin)
        self.step_pin.direction = digitalio.Direction.OUTPUT

    
    def step(self, steps, direction=stepper.FORWARD, style=stepper.SINGLE, delay=0.01):
        """Move the stepper motor a given number of steps in a direction and style."""
        for _ in range(steps):
            self.motor.onestep(direction=direction, style=style)
            time.sleep(delay)
    
    def forward(self, steps, style=stepper.SINGLE, delay=0.01):
        """Move the stepper forward."""
        self.step(steps, direction=stepper.FORWARD, style=style, delay=delay)

    def backward(self, steps, style=stepper.SINGLE, delay=0.01):
        """Move the stepper backward."""
        self.step(steps, direction=stepper.BACKWARD, style=style, delay=delay)
    
    def lock(self):
        """Lock the stepper motor (holds position)."""
        self.motor.onestep()  # Holding position by stepping in place

    def release(self):
        """Release the motor (disable holding torque)."""
        self.motor.release()

