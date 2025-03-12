# controller.py

import time
import stepper_motor_pio
import constant

class Controller:
    def __init__(self):
        self.motors = {
            "motor0": stepper_motor_pio.StepperMotorPIO(
                dir_pin_num=constant.MOTOR0_DIR, 
                step_pin_num=constant.MOTOR0_STEP, 
                pio_id=0
            ),
            "motor1": stepper_motor_pio.StepperMotorPIO(
                dir_pin_num=constant.MOTOR1_DIR, 
                step_pin_num=constant.MOTOR1_STEP, 
                pio_id=1
            ),
            "motor2": stepper_motor_pio.StepperMotorPIO(
                dir_pin_num=constant.MOTOR2_DIR, 
                step_pin_num=constant.MOTOR2_STEP, 
                pio_id=2
            ),
            "motor3": stepper_motor_pio.StepperMotorPIO(
                dir_pin_num=constant.MOTOR3_DIR, 
                step_pin_num=constant.MOTOR3_STEP, 
                pio_id=3
            ),
        }

    def move_motors(self, directions: list[int], steps: list[int], speeds: list[float]):
        """
        Adapted version that calls PIO-based move_steps for each motor.
        This still moves them sequentially. If you want them to run
        simultaneously, you'd start each motor's PIO, then wait, then stop.
        """
        for i in range(4):
            frequency = int(1.0 / (speeds[i] * 2))
            # Convert the "speed" you had (seconds of delay) into a frequency
            # This is a naive example. Adjust to match your old speed logic.
            
            self.motors[f"motor{i}"].move_steps(
                steps=steps[i],
                frequency=frequency,
                direction=directions[i]
            )
    
    def forward(self):
        self.move_motors(
            directions=[
                constant.FORWARD_MOTOR0_DIRECTION,
                constant.FORWARD_MOTOR1_DIRECTION,
                constant.FORWARD_MOTOR2_DIRECTION,
                constant.FORWARD_MOTOR3_DIRECTION
            ],
            steps=[
                constant.FORWARD_MOTOR0_STEPS,
                constant.FORWARD_MOTOR1_STEPS,
                constant.FORWARD_MOTOR2_STEPS,
                constant.FORWARD_MOTOR3_STEPS
            ],
            speeds=[
                constant.FORWARD_MOTOR0_SPEED,
                constant.FORWARD_MOTOR1_SPEED,
                constant.FORWARD_MOTOR2_SPEED,
                constant.FORWARD_MOTOR3_SPEED
            ]
        )
    
    # ... and similarly for backward, left, right, etc. ...
