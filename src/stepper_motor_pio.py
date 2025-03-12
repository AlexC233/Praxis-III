# stepper_motor_pio.py

import time
from machine import Pin
import rp2
from rp2 import PIO, StateMachine, asm_pio

@asm_pio(sideset_init=PIO.OUT_LOW)
def stepper_pio():
    """
    A simple program that toggles the step pin high/low.
    Each iteration: 1 cycle high, 1 cycle low.
    The frequency we set on the StateMachine determines
    how fast the pin toggles (2 toggles per full cycle).
    """
    wrap_target()
    nop().side(1)  # step pin = HIGH
    nop().side(0)  # step pin = LOW
    wrap()

class StepperMotorPIO:
    def __init__(self, dir_pin_num, step_pin_num, pio_id=0):
        """
        :param dir_pin_num: GPIO pin number for direction
        :param step_pin_num: GPIO pin number for step
        :param pio_id: Which PIO state machine (0 to 3 on RP2040)
        """
        # Direction pin (normal I/O)
        self.dir_pin = Pin(dir_pin_num, Pin.OUT)
        self.dir_pin.value(0)

        # State machine for step signals
        self.sm = StateMachine(
            pio_id,                 # which state machine
            stepper_pio,           # PIO program
            freq=0,                # we’ll set frequency later
            sideset_base=Pin(step_pin_num)  # the "side" pin for toggling
        )
        # By default, the SM is not running until we call active(1)
        self.sm.active(0)

    def set_direction(self, direction: int):
        """Set the direction pin: 0 or 1."""
        self.dir_pin.value(direction)

    def run(self, frequency: int):
        """
        Start toggling the step pin at 'frequency' Hz.
        Because the PIO toggles the pin high then low,
        you'll effectively get frequency/2 full step cycles
        per second. For example, freq=2000 => 1000 steps/sec.
        """
        self.sm.freq(frequency)
        self.sm.active(1)

    def stop(self):
        """Stop toggling the step pin."""
        self.sm.active(0)

    def move_steps(self, steps: int, frequency: int, direction: int):
        """
        Move the motor for a given number of steps by
        running PIO at 'frequency' for enough time to achieve 'steps'.
        NOTE: This is approximate since we’re timing it
        rather than truly counting edges in hardware.
        """
        # Set direction
        self.set_direction(direction)

        # Each full "step" is 2 toggles (HIGH then LOW).
        # The PIO toggles at 'frequency' toggles/second -> 
        #    actual steps/second = frequency / 2
        # So time needed for 'steps' is:
        #    t = steps / (frequency/2) = 2 * steps / frequency
        step_time = (2 * steps) / frequency

        # Run the PIO
        self.run(frequency)
        time.sleep(step_time)
        self.stop()
