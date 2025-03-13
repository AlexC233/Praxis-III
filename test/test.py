import numpy as np

# Motor positions (modify based on actual coordinates)
motors = {
    "L1": (-w/2, -h/2),
    "L2": (-w/2, h/2),
    "R1": (w/2, -h/2),
    "R2": (w/2, h/2),
}

# Function to compute motor speeds
def compute_motor_speeds(x0, y0, x, y, t):
    # Compute velocity in x and y directions
    vx = (x - x0) / t  # Constant velocity assumption
    vy = (y - y0) / t

    speeds = {}
    for motor, (mx, my) in motors.items():
        # Initial and final cable lengths
        L0 = np.sqrt((mx - x0)**2 + (my - y0)**2)
        L = np.sqrt((mx - x)**2 + (my - y)**2)

        # Compute speed
        speed = ((mx - x) * vx + (my - y) * vy) / L
        speeds[motor] = speed

    return speeds

# Example usage
speeds = compute_motor_speeds(0, 0, 10, 10, 5)
print(speeds)
