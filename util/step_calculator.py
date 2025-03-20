import math

# Unit : cm
# Define constants for motor positions
MOTOR_POSITIONS = {
    "motor0": (0, 0, 30),
    "motor1": (50, 0, 30),
    "motor2": (50, 50, 30),
    "motor3": (0, 50, 30)
}

# Define initial position of the load
INITIAL_POSITION = (0, 0, 0)

# Conversion factor (e.g., steps per mm)
C = 0.1  # Adjust this based on your motor specs

# Define movement modes
MOVEMENT_MODES = {
    "forward": (-1, 0, 0),  # -x direction
    "backward": (1, 0, 0),  # +x direction
    "left": (0, -1, 0),  # -y direction
    "right": (0, 1, 0),  # +y direction
    "up": (0, 0, 1),  # +z direction
    "down": (0, 0, -1)  # -z direction
}

def get_current_length(motor_pos, load_pos):
    """Calculate the initial cable length from motor to load position."""
    mx, my, mz = motor_pos
    x, y, z = load_pos
    return math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2)

def get_target_length(motor_pos, load_pos, delta_x, delta_y, delta_z):
    """Calculate the target cable length from motor to new load position."""
    mx, my, mz = motor_pos
    x, y, z = load_pos
    return math.sqrt((x + delta_x - mx) ** 2 + (y + delta_y - my) ** 2 + (z + delta_z - mz) ** 2)

def get_difference(current_length, target_length):
    """Calculate the difference in length for a motor."""
    return target_length - current_length

def get_steps(delta_length, conversion_factor):
    """Convert length difference into step count."""
    return round(delta_length / conversion_factor)

# Compute steps for each movement mode
for mode, (dx, dy, dz) in MOVEMENT_MODES.items():
    print(f"Mode: {mode}")
    step_counts = {}
    for motor, motor_pos in MOTOR_POSITIONS.items():
        current_length = get_current_length(motor_pos, INITIAL_POSITION)
        target_length = get_target_length(motor_pos, INITIAL_POSITION, dx, dy, dz)
        delta_length = get_difference(current_length, target_length)
        step_counts[motor] = get_steps(delta_length, C)
    
    # Print step results for the mode
    for motor, step_count in step_counts.items():
        print(f"  {motor}: {step_count} steps")
    print()
