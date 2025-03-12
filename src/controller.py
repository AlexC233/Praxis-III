import constant
from stepper_motor import StepperMotor

class Controller:
    """
    Coordinates the four motors so that they run together.
    Each 'move_*' method sends directions/steps/speeds to all motors at once.
    """

    def __init__(self):
        # Create four StepperMotor objects
        self.motors = [
            StepperMotor(
                constant.MOTOR0_DIR_PIN,
                constant.MOTOR0_STEP_PIN,
                constant.STEPS_PER_REV
            ),
            StepperMotor(
                constant.MOTOR1_DIR_PIN,
                constant.MOTOR1_STEP_PIN,
                constant.STEPS_PER_REV
            ),
            StepperMotor(
                constant.MOTOR2_DIR_PIN,
                constant.MOTOR2_STEP_PIN,
                constant.STEPS_PER_REV
            ),
            StepperMotor(
                constant.MOTOR3_DIR_PIN,
                constant.MOTOR3_STEP_PIN,
                constant.STEPS_PER_REV
            ),
        ]

    def move_motors(self, directions, steps, delays):
        """
        Moves all four motors simultaneously (as close to 'at the same time' as Python can manage).
        For each step, we do a single step on all motors that need steps.
        """
        max_steps = max(steps)
        motor_positions = [0, 0, 0, 0]  # track how many steps each motor has completed

        # We'll do a loop up to `max_steps` times, stepping each motor if it still has steps left.
        for _ in range(max_steps):
            for i, motor in enumerate(self.motors):
                if motor_positions[i] < steps[i]:
                    motor.dir_pin.value = directions[i]
                    # Step once
                    motor.step_pin.value = True
            # short delay for the rising edge
            # Choose the smallest delay among the motors that are stepping
            # so they roughly can step in unison
            active_delays = []
            for i in range(4):
                if motor_positions[i] < steps[i]:
                    active_delays.append(delays[i])
            if len(active_delays) > 0:
                step_delay = min(active_delays)
            else:
                step_delay = 0.0

            # Half-step delay
            import time
            time.sleep(step_delay)

            # Drive all pins low
            for i, motor in enumerate(self.motors):
                if motor_positions[i] < steps[i]:
                    motor.step_pin.value = False
                    motor_positions[i] += 1

            # Another half-step delay
            time.sleep(step_delay)

    def forward(self):
        self.move_motors(
            constant.FORWARD_DIRECTIONS,
            constant.FORWARD_STEPS,
            constant.FORWARD_DELAY
        )

    def backward(self):
        self.move_motors(
            constant.BACKWARD_DIRECTIONS,
            constant.BACKWARD_STEPS,
            constant.BACKWARD_DELAY
        )

    def left(self):
        self.move_motors(
            constant.LEFT_DIRECTIONS,
            constant.LEFT_STEPS,
            constant.LEFT_DELAY
        )

    def right(self):
        self.move_motors(
            constant.RIGHT_DIRECTIONS,
            constant.RIGHT_STEPS,
            constant.RIGHT_DELAY
        )

    def up(self):
        self.move_motors(
            constant.UP_DIRECTIONS,
            constant.UP_STEPS,
            constant.UP_DELAY
        )

    def down(self):
        self.move_motors(
            constant.DOWN_DIRECTIONS,
            constant.DOWN_STEPS,
            constant.DOWN_DELAY
        )
