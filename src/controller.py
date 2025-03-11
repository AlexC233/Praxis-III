import time
import keyboard

import stepper_motor
import constant

class Controller:
    def __init__(self):
        self.motors = {
            "motor0": stepper_motor.StepperMotor(index = 0, dir_pin = constant.MOTOR0_DIR, step_pin = constant.MOTOR0_STEP),
            "motor1": stepper_motor.StepperMotor(index = 1, dir_pin = constant.MOTOR1_DIR, step_pin = constant.MOTOR1_STEP),
            "motor2": stepper_motor.StepperMotor(index = 2, dir_pin = constant.MOTOR2_DIR, step_pin = constant.MOTOR2_STEP),
            "motor3": stepper_motor.StepperMotor(index = 3, dir_pin = constant.MOTOR3_DIR, step_pin = constant.MOTOR3_STEP),
        }

    def move_motors(self, directions: list[int], steps: list[int], speeds: list[float]):
        for i in range(4):
            self.motors[f"motor{i}"].step(
                direction=directions[i],
                steps=steps[i],
                speed=speeds[i]
            )

    def left(self):
        self.move_motors(
            directions=[constant.LEFT_MOTOR0_DIRECTION, constant.LEFT_MOTOR1_DIRECTION, constant.LEFT_MOTOR2_DIRECTION, constant.LEFT_MOTOR3_DIRECTION],
            steps=[constant.LEFT_MOTOR0_STEPS, constant.LEFT_MOTOR1_STEPS, constant.LEFT_MOTOR2_STEPS, constant.LEFT_MOTOR3_STEPS],
            speeds=[constant.LEFT_MOTOR0_SPEED, constant.LEFT_MOTOR1_SPEED, constant.LEFT_MOTOR2_SPEED, constant.LEFT_MOTOR3_SPEED]
        )
        
    def right(self):
        self.move_motors(
            directions=[constant.RIGHT_MOTOR0_DIRECTION, constant.RIGHT_MOTOR1_DIRECTION, constant.RIGHT_MOTOR2_DIRECTION, constant.RIGHT_MOTOR3_DIRECTION],
            steps=[constant.RIGHT_MOTOR0_STEPS, constant.RIGHT_MOTOR1_STEPS, constant.RIGHT_MOTOR2_STEPS, constant.RIGHT_MOTOR3_STEPS],
            speeds=[constant.RIGHT_MOTOR0_SPEED, constant.RIGHT_MOTOR1_SPEED, constant.RIGHT_MOTOR2_SPEED, constant.RIGHT_MOTOR3_SPEED]
        )
        
    def forward(self):
        self.move_motors(
            directions=[constant.FORWARD_MOTOR0_DIRECTION, constant.FORWARD_MOTOR1_DIRECTION, constant.FORWARD_MOTOR2_DIRECTION, constant.FORWARD_MOTOR3_DIRECTION],
            steps=[constant.FORWARD_MOTOR0_STEPS, constant.FORWARD_MOTOR1_STEPS, constant.FORWARD_MOTOR2_STEPS, constant.FORWARD_MOTOR3_STEPS],
            speeds=[constant.FORWARD_MOTOR0_SPEED, constant.FORWARD_MOTOR1_SPEED, constant.FORWARD_MOTOR2_SPEED, constant.FORWARD_MOTOR3_SPEED]
        )
        
    def backward(self):
        self.move_motors(
            directions=[constant.BACKWARD_MOTOR0_DIRECTION, constant.BACKWARD_MOTOR1_DIRECTION, constant.BACKWARD_MOTOR2_DIRECTION, constant.BACKWARD_MOTOR3_DIRECTION],
            steps=[constant.BACKWARD_MOTOR0_STEPS, constant.BACKWARD_MOTOR1_STEPS, constant.BACKWARD_MOTOR2_STEPS, constant.BACKWARD_MOTOR3_STEPS],
            speeds=[constant.BACKWARD_MOTOR0_SPEED, constant.BACKWARD_MOTOR1_SPEED, constant.BACKWARD_MOTOR2_SPEED, constant.BACKWARD_MOTOR3_SPEED]
        )
        
    def up(self):
        self.move_motors(
            directions=[constant.UP_MOTOR0_DIRECTION, constant.UP_MOTOR1_DIRECTION, constant.UP_MOTOR2_DIRECTION, constant.UP_MOTOR3_DIRECTION],
            steps=[constant.UP_MOTOR0_STEPS, constant.UP_MOTOR1_STEPS, constant.UP_MOTOR2_STEPS, constant.UP_MOTOR3_STEPS],
            speeds=[constant.UP_MOTOR0_SPEED, constant.UP_MOTOR1_SPEED, constant.UP_MOTOR2_SPEED, constant.UP_MOTOR3_SPEED]
        )
    
    def down(self):
        self.move_motors(
            directions=[constant.DOWN_MOTOR0_DIRECTION, constant.DOWN_MOTOR1_DIRECTION, constant.DOWN_MOTOR2_DIRECTION, constant.DOWN_MOTOR3_DIRECTION],
            steps=[constant.DOWN_MOTOR0_STEPS, constant.DOWN_MOTOR1_STEPS, constant.DOWN_MOTOR2_STEPS, constant.DOWN_MOTOR3_STEPS],
            speeds=[constant.DOWN_MOTOR0_SPEED, constant.DOWN_MOTOR1_SPEED, constant.DOWN_MOTOR2_SPEED, constant.DOWN_MOTOR3_SPEED]
        )