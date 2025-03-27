import time
import math
import constant
from stepper_motor import StepperMotor

class Controller:
    def __init__(self):
        """
        Coordinates the four motors and tracks the current (x, y, z) position.
        """
        self.motors = {}
        for motor_name, pins in constant.MOTOR_PINS.items():
            self.motors[motor_name] = StepperMotor(
                index=pins["INDEX"],
                dir_pin=pins["DIR_PIN"],
                step_pin=pins["STEP_PIN"],
                steps_per_rev=constant.STEPS_PER_REV
            )

        # You can change this if you have a known home or start position 
        self.current_position = constant.INITIAL_POSITION

        # Example anchor points for each motor's cable origin.
        self.anchors = constant.MOTOR_ANCHORS

    def move_motors(self, movement_dict):
        """
        Drives the motors in parallel.
        movement_dict example:
            {
              "motor0": {"direction": bool, "steps": int, "delay": float},
              ...
            }
        """
        max_steps = max(movement_dict[m]["steps"] for m in movement_dict)
        steps_completed = {m: 0 for m in self.motors}

        for _ in range(max_steps):
            # First half-step
            for motor_name, motor_obj in self.motors.items():
                needed_steps = movement_dict[motor_name]["steps"]
                direction    = movement_dict[motor_name]["direction"]
                if steps_completed[motor_name] < needed_steps:
                    motor_obj.dir_pin.value = direction
                    motor_obj.step_pin.value = True

            # Determine the minimum half-step delay among active motors
            active_delays = []
            for motor_name in self.motors:
                if steps_completed[motor_name] < movement_dict[motor_name]["steps"]:
                    active_delays.append(movement_dict[motor_name]["delay"])
            half_step_delay = min(active_delays) if active_delays else 0
            time.sleep(half_step_delay)

            # Second half-step
            for motor_name, motor_obj in self.motors.items():
                if steps_completed[motor_name] < movement_dict[motor_name]["steps"]:
                    motor_obj.step_pin.value = False
                    steps_completed[motor_name] += 1

            time.sleep(half_step_delay)

    def update_current_position(self, new_position):
        """
        Record the new (x, y, z) after a move completes.
        """
        self.current_position = new_position

    def calculate_length(self, anchor, end_effector_pos):
        """
        Euclidean distance from an anchor point to the end effector.
        """
        ax, ay, az = anchor
        ex, ey, ez = end_effector_pos
        return math.sqrt((ex - ax)**2 + (ey - ay)**2 + (ez - az)**2)

    def length_to_steps(self, length_diff):
        """
        Convert a difference in cable length to how many motor steps are needed.
        You must adjust spool_diameter for your spool geometry.
        """

        revs = length_diff / constant.SPOOL_CIRCUMFERENCE
        return int(abs(revs * constant.STEPS_PER_REV))

    def generate_movement_dict_from_mode(self, new_position, mode_dict):
        """
        For each motor in mode_dict, read the direction from mode_dict,
        compute how many steps we need (based on the difference in cable length),
        and keep the same delay from mode_dict.
        """
        movement_dict = {}
        for i, motor_name in enumerate(sorted(self.motors.keys())):
            anchor = self.anchors[i]

            # Get the direction and delay directly from the mode_dict:
            direction = mode_dict[motor_name]["direction"]
            delay     = mode_dict[motor_name]["delay"]

            # Figure out how many steps needed:
            current_len = self.calculate_length(anchor, self.current_position)
            target_len  = self.calculate_length(anchor, new_position)
            length_diff = abs(target_len - current_len)   # ignore sign

            steps = self.length_to_steps(length_diff)

            movement_dict[motor_name] = {
                "direction": direction,
                "steps": steps,
                "delay": delay
            }

        return movement_dict
    
    # ------------------------------------------------------------
    #    The coordinate system
    #      -x = forward, +x = backward,
    #      -y = left,    +y = right,
    #      -z = down,    +z = up.
    # ------------------------------------------------------------


    # def forward(self, distance=5.0):
    #     """
    #     Moves the end effector "distance" forward (-X),
    #     but uses the directions from constant.MOVE_FORWARD.
    #     """
    #     x, y, z = self.current_position
    #     new_pos = (x - distance, y, z)

    #     # Build a movement dict that uses constant.MOVE_FORWARD
    #     movement_dict = self.generate_movement_dict_from_mode(new_pos, constant.MOVE_FORWARD)

    #     self.move_motors(movement_dict)
    #     self.update_current_position(new_pos)

    # def backward(self, distance=5.0):
    #     x, y, z = self.current_position
    #     new_pos = (x + distance, y, z)

    #     movement_dict = self.generate_movement_dict_from_mode(new_pos, constant.MOVE_BACKWARD)

    #     self.move_motors(movement_dict)
    #     self.update_current_position(new_pos)

    # def left(self, distance=5.0):
    #     x, y, z = self.current_position
    #     new_pos = (x, y - distance, z)

    #     movement_dict = self.generate_movement_dict_from_mode(new_pos, constant.MOVE_LEFT)

    #     self.move_motors(movement_dict)
    #     self.update_current_position(new_pos)

    # def right(self, distance=5.0):
    #     x, y, z = self.current_position
    #     new_pos = (x, y + distance, z)

    #     movement_dict = self.generate_movement_dict_from_mode(new_pos, constant.MOVE_RIGHT)

    #     self.move_motors(movement_dict)
    #     self.update_current_position(new_pos)

    # def up(self, distance=5.0):
    #     x, y, z = self.current_position
    #     new_pos = (x, y, z + distance)

    #     movement_dict = self.generate_movement_dict_from_mode(new_pos, constant.MOVE_UP)

    #     self.move_motors(movement_dict)
    #     self.update_current_position(new_pos)

    # def down(self, distance=5.0):
    #     x, y, z = self.current_position
    #     new_pos = (x, y, z - distance)

    #     movement_dict = self.generate_movement_dict_from_mode(new_pos, constant.MOVE_DOWN)

    #     self.move_motors(movement_dict)
    #     self.update_current_position(new_pos)

    # def test_move_anywhere(self, x, y, z):
    #     """
    #     Move directly to (x, y, z), using the MOTOR_SHORTEN_RELEASE dictionary
    #     in constant.py to decide which direction (CW or CCW) means spool-in or spool-out.
    #     """
    #     new_position = (x, y, z)
    #     movement_dict = {}

    #     for i, motor_name in enumerate(sorted(self.motors.keys())):
    #         anchor = self.anchors[i]
    #         current_len = self.calculate_length(anchor, self.current_position)
    #         target_len  = self.calculate_length(anchor, new_position)
    #         diff = target_len - current_len

    #         # If diff > 0 => spool out => "release"; if diff < 0 => spool in => "shorten"
    #         if diff > 0:
    #             direction = constant.MOTOR_SHORTEN_RELEASE[motor_name]["release"]
    #         else:
    #             direction = constant.MOTOR_SHORTEN_RELEASE[motor_name]["shorten"]

    #         steps = self.length_to_steps(abs(diff))

    #         movement_dict[motor_name] = {
    #             "direction": direction,
    #             "steps": steps,
    #             "delay": constant.DEFAULT_STEP_DELAY
    #         }

    #     self.move_motors(movement_dict)
    #     self.update_current_position(new_position)

    def forward(self, distance=5.0):
        x, y, z = self.current_position
        new_pos = (x - distance, y, z)

        movement_dict = self.generate_movement_dict_from_mode(new_pos, constant.MOVE_FORWARD)
        self.move_motors(movement_dict)
        self.update_current_position(new_pos)

        # Print how many steps each motor took
        for motor_name, move_info in movement_dict.items():
            direction_str = "CCW" if move_info["direction"] else "CW"
            print(f"Motor {motor_name} => {move_info['steps']} steps (direction: {direction_str})")

        # Print the updated position
        print(f"Current position after forward: {self.current_position}\n")


    def backward(self, distance=5.0):
        x, y, z = self.current_position
        new_pos = (x + distance, y, z)

        movement_dict = self.generate_movement_dict_from_mode(new_pos, constant.MOVE_BACKWARD)
        self.move_motors(movement_dict)
        self.update_current_position(new_pos)

        for motor_name, move_info in movement_dict.items():
            direction_str = "CCW" if move_info["direction"] else "CW"
            print(f"Motor {motor_name} => {move_info['steps']} steps (direction: {direction_str})")

        print(f"Current position after backward: {self.current_position}\n")


    def left(self, distance=5.0):
        x, y, z = self.current_position
        new_pos = (x, y - distance, z)

        movement_dict = self.generate_movement_dict_from_mode(new_pos, constant.MOVE_LEFT)
        self.move_motors(movement_dict)
        self.update_current_position(new_pos)

        for motor_name, move_info in movement_dict.items():
            direction_str = "CCW" if move_info["direction"] else "CW"
            print(f"Motor {motor_name} => {move_info['steps']} steps (direction: {direction_str})")

        print(f"Current position after left: {self.current_position}\n")


    def right(self, distance=5.0):
        x, y, z = self.current_position
        new_pos = (x, y + distance, z)

        movement_dict = self.generate_movement_dict_from_mode(new_pos, constant.MOVE_RIGHT)
        self.move_motors(movement_dict)
        self.update_current_position(new_pos)

        for motor_name, move_info in movement_dict.items():
            direction_str = "CCW" if move_info["direction"] else "CW"
            print(f"Motor {motor_name} => {move_info['steps']} steps (direction: {direction_str})")

        print(f"Current position after right: {self.current_position}\n")


    def up(self, distance=5.0):
        x, y, z = self.current_position
        new_pos = (x, y, z + distance)

        movement_dict = self.generate_movement_dict_from_mode(new_pos, constant.MOVE_UP)
        self.move_motors(movement_dict)
        self.update_current_position(new_pos)

        for motor_name, move_info in movement_dict.items():
            direction_str = "CCW" if move_info["direction"] else "CW"
            print(f"Motor {motor_name} => {move_info['steps']} steps (direction: {direction_str})")

        print(f"Current position after up: {self.current_position}\n")


    def down(self, distance=5.0):
        x, y, z = self.current_position
        new_pos = (x, y, z - distance)

        movement_dict = self.generate_movement_dict_from_mode(new_pos, constant.MOVE_DOWN)
        self.move_motors(movement_dict)
        self.update_current_position(new_pos)

        for motor_name, move_info in movement_dict.items():
            direction_str = "CCW" if move_info["direction"] else "CW"
            print(f"Motor {motor_name} => {move_info['steps']} steps (direction: {direction_str})")

        print(f"Current position after down: {self.current_position}\n")

    def calculate_motor_powers(self, direction_x, direction_y):
        """
        Convert Cartesian coordinate movement to motor power distribution
        
        Args:
            direction_x: float (-1.0 to 1.0) - horizontal movement
            direction_y: float (-1.0 to 1.0) - vertical movement
        
        Returns:
            Dictionary containing power values for each motor (0.0 to 1.0)
        """
        # Normalize vector
        magnitude = math.sqrt(direction_x**2 + direction_y**2)
        if magnitude > 0:
            direction_x /= magnitude
            direction_y /= magnitude

        # Calculate power for each motor
        motor_powers = {
            "motor0": max(0, direction_y),      # North motor
            "motor1": max(0, direction_x),      # East motor
            "motor2": max(0, -direction_y),     # South motor
            "motor3": max(0, -direction_x),     # West motor
        }
        
        return motor_powers

    def move_with_vector(self, direction_x, direction_y, distance=5.0):
        """
        Move the robot according to vector direction
        
        Args:
            direction_x: float - X component of movement vector
            direction_y: float - Y component of movement vector
            distance: float - Movement distance in cm
        """
        motor_powers = self.calculate_motor_powers(direction_x, direction_y)
        
        # Generate movement dictionary
        movement_dict = {}
        for motor_name, power in motor_powers.items():
            steps = int(power * self.length_to_steps(distance))
            movement_dict[motor_name] = {
                "direction": constant.MOTOR_SHORTEN_RELEASE[motor_name]["shorten"],
                "steps": steps,
                "delay": constant.DEFAULT_STEP_DELAY
            }
        
        self.move_motors(movement_dict)

