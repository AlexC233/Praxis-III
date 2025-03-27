import pygame
import numpy as np
import math

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Cable-Driven Robot Simulation with Inverse Kinematics")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 128)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Center of the screen for projection
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

# Define motor positions in 3D space (x, y, z)
motor_positions = {
    "C1": [-200, 200, -200],   # Top left front
    "C2": [-200, 200, 200],    # Top left back
    "C3": [200, 200, 200],     # Top right back
    "C4": [200, 200, -200],    # Top right front
}

# Physics constants
GRAVITY = 9.81  # Gravity acceleration (m/s²)
MASS = 1.0      # Mass of the box (kg)
DAMPING = 0.7   # Damping factor (air resistance)
TIME_STEP = 0.05  # Time step for physics simulation (50ms)

# Initial box position, velocity and acceleration
box_x, box_y, box_z = 0, 0, 0
box_vel_x, box_vel_y, box_vel_z = 0, 0, 0
box_acc_x, box_acc_y, box_acc_z = 0, 0, 0

# Cable tension (maximum pulling force per motor)
MAX_TENSION = 50.0  # Maximum tension force (N)
MIN_CABLE_LENGTH = 10.0  # Minimum cable length before it becomes taut
# BASE_TENSION is no longer used in the new IK calculation

# Control parameters
mode = "COMBINED"  # COMBINED mode uses WASD/UP/DOWN with physics
control_force = 20.0  # Force applied when using directional controls
speed = 5.0  # Speed for visualization

# Camera rotation parameters
camera_angle_x = 30  # Initial camera angle in degrees (looking down)
camera_angle_y = 45  # Initial rotation around Y axis
camera_distance = 800

# Debug visualization
show_debug = False
target_position = [0, 0, 0]  # Target position for box (used for visualization)

# Function to compute cable data (length, tension, direction)
def compute_cable_data(box_x, box_y, box_z):
    cable_data = {}
    
    for motor, (mx, my, mz) in motor_positions.items():
        # Vector from box to motor
        dx = mx - box_x
        dy = my - box_y
        dz = mz - box_z
        
        # Calculate current cable length
        length = np.sqrt(dx**2 + dy**2 + dz**2)
        
        # Normalize direction vector (unit vector from box to motor)
        if length > 0:
            dir_x = dx / length
            dir_y = dy / length
            dir_z = dz / length
        else:
            dir_x, dir_y, dir_z = 0, 0, 0
        
        # Initialize tension to zero; it will be set via inverse kinematics
        cable_data[motor] = {
            'length': length,
            'tension': 0,
            'direction': (dir_x, dir_y, dir_z)
        }
    
    return cable_data

# Function to calculate inverse kinematics using a matrix-based least squares approach.
# It computes the cable tensions required to produce the desired force,
# while also compensating for gravity.
def calculate_inverse_kinematics(cable_data, desired_force_x, desired_force_y, desired_force_z):
    # Total force needed: desired motion plus gravity compensation.
    # Gravity is compensated by generating an upward force equal to MASS * GRAVITY.
    F_total = np.array([desired_force_x, desired_force_y + MASS * GRAVITY, desired_force_z])
    
    # Use a fixed motor order to build the system
    motor_order = ["C1", "C2", "C3", "C4"]
    
    # Build the direction matrix D (3 x 4)
    D = np.zeros((3, 4))
    for i, motor in enumerate(motor_order):
        d = cable_data[motor]['direction']
        D[:, i] = d
    
    # Solve for tensions T in the equation D * T = F_total using least squares
    T_solution, residuals, rank, s = np.linalg.lstsq(D, F_total, rcond=None)
    
    # Enforce non-negative tensions and clamp to the maximum tension
    T_solution = np.clip(T_solution, 0, MAX_TENSION)
    
    # Update cable_data with the computed tensions
    for i, motor in enumerate(motor_order):
        cable_data[motor]['tension'] = T_solution[i]
    
    return cable_data

# Function to update box physics
def update_box_physics(cable_data):
    global box_x, box_y, box_z, box_vel_x, box_vel_y, box_vel_z, box_acc_x, box_acc_y, box_acc_z
    
    # Reset acceleration
    box_acc_x, box_acc_y, box_acc_z = 0, 0, 0
    
    # Apply cable tensions
    for motor, data in cable_data.items():
        tension = data['tension']
        dir_x, dir_y, dir_z = data['direction']
        
        # Force = tension * direction
        force_x = tension * dir_x
        force_y = tension * dir_y
        force_z = tension * dir_z
        
        # Acceleration = force / mass
        box_acc_x += force_x / MASS
        box_acc_y += force_y / MASS
        box_acc_z += force_z / MASS
    
    # Apply gravity (negative y-direction)
    box_acc_y -= GRAVITY
    
    # Update velocity with acceleration
    box_vel_x += box_acc_x * TIME_STEP
    box_vel_y += box_acc_y * TIME_STEP
    box_vel_z += box_acc_z * TIME_STEP
    
    # Apply damping (air resistance)
    box_vel_x *= (1 - DAMPING * TIME_STEP)
    box_vel_y *= (1 - DAMPING * TIME_STEP)
    box_vel_z *= (1 - DAMPING * TIME_STEP)
    
    # Update position
    box_x += box_vel_x * TIME_STEP
    box_y += box_vel_y * TIME_STEP
    box_z += box_vel_z * TIME_STEP
    
    # Constrain box position
    constrain_box_position()

# Function to constrain box position within motor boundaries
def constrain_box_position():
    global box_x, box_y, box_z, box_vel_x, box_vel_y, box_vel_z
    
    # Find the boundaries defined by the motors
    min_x = min(motor_positions[m][0] for m in motor_positions)
    max_x = max(motor_positions[m][0] for m in motor_positions)
    min_y = min(motor_positions[m][1] for m in motor_positions) - 400  # Allow falling below motors
    max_y = max(motor_positions[m][1] for m in motor_positions)
    min_z = min(motor_positions[m][2] for m in motor_positions)
    max_z = max(motor_positions[m][2] for m in motor_positions)
    
    # Add a small buffer to keep the box fully visible within the boundaries
    buffer = 20
    
    # Constrain the box position
    if box_x < min_x + buffer:
        box_x = min_x + buffer
        box_vel_x = -box_vel_x * 0.5  # Bounce with energy loss
    elif box_x > max_x - buffer:
        box_x = max_x - buffer
        box_vel_x = -box_vel_x * 0.5  # Bounce with energy loss
        
    # Allow falling below but not going above
    if box_y > max_y - buffer:
        box_y = max_y - buffer
        box_vel_y = -box_vel_y * 0.5  # Bounce with energy loss
    
    if box_z < min_z + buffer:
        box_z = min_z + buffer
        box_vel_z = -box_vel_z * 0.5  # Bounce with energy loss
    elif box_z > max_z - buffer:
        box_z = max_z - buffer
        box_vel_z = -box_vel_z * 0.5  # Bounce with energy loss

# Function to project 3D coordinates to 2D screen
def project_3d_to_2d(x, y, z):
    # Rotate around Y axis
    angle_y_rad = math.radians(camera_angle_y)
    rotated_x = x * math.cos(angle_y_rad) - z * math.sin(angle_y_rad)
    rotated_z = x * math.sin(angle_y_rad) + z * math.cos(angle_y_rad)
    
    # Rotate around X axis
    angle_x_rad = math.radians(camera_angle_x)
    rotated_y = y * math.cos(angle_x_rad) - rotated_z * math.sin(angle_x_rad)
    rotated_z = y * math.sin(angle_x_rad) + rotated_z * math.cos(angle_x_rad)
    
    # Apply perspective (simple division by z distance)
    scale_factor = 1
    perspective_scale = scale_factor * camera_distance / (camera_distance + rotated_z + 400)
    
    # Project to 2D screen coordinates
    screen_x = CENTER_X + rotated_x * perspective_scale
    screen_y = CENTER_Y + rotated_y * perspective_scale
    
    return int(screen_x), int(screen_y), perspective_scale

# Function to draw a line between two 3D points
def draw_line_3d(screen, start_3d, end_3d, color, width=2):
    start_x, start_y, _ = project_3d_to_2d(*start_3d)
    end_x, end_y, _ = project_3d_to_2d(*end_3d)
    pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), width)

# Function to draw a cable with tension visualization
def draw_cable(screen, start_3d, end_3d, tension, max_tension):
    start_x, start_y, _ = project_3d_to_2d(*start_3d)
    end_x, end_y, _ = project_3d_to_2d(*end_3d)
    
    # Determine color based on tension (from green to red)
    tension_ratio = min(1.0, tension / max_tension)
    r = int(255 * tension_ratio)
    g = int(255 * (1 - tension_ratio))
    b = 0
    cable_color = (r, g, b)
    
    # Width based on tension (1-4 pixels)
    width = max(1, int(1 + tension_ratio * 3))
    
    # Draw the cable
    pygame.draw.line(screen, cable_color, (start_x, start_y), (end_x, end_y), width)

# Function to draw a 3D cube at the given position
def draw_cube_3d(screen, position, size, color):
    x, y, z = position
    
    # Define the vertices of the cube in 3D space
    vertices = [
        [x - size, y - size, z - size],  # 0
        [x + size, y - size, z - size],  # 1
        [x + size, y + size, z - size],  # 2
        [x - size, y + size, z - size],  # 3
        [x - size, y - size, z + size],  # 4
        [x + size, y - size, z + size],  # 5
        [x + size, y + size, z + size],  # 6
        [x - size, y + size, z + size]   # 7
    ]
    
    # Define the edges of the cube
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    
    # Project vertices to 2D space
    projected_vertices = [project_3d_to_2d(*vertex) for vertex in vertices]
    
    # Draw edges
    for edge in edges:
        start, end = edge
        pygame.draw.line(
            screen, 
            color, 
            (projected_vertices[start][0], projected_vertices[start][1]),
            (projected_vertices[end][0], projected_vertices[end][1]),
            2
        )

# Draw axes for reference
def draw_axes(screen):
    # Origin point
    origin = [0, 0, 0]
    
    # Endpoints of axes
    x_axis_end = [100, 0, 0]
    y_axis_end = [0, 100, 0]
    z_axis_end = [0, 0, 100]
    
    # Draw the axes
    draw_line_3d(screen, origin, x_axis_end, RED)     # X-axis in red
    draw_line_3d(screen, origin, y_axis_end, GREEN)   # Y-axis in green
    draw_line_3d(screen, origin, z_axis_end, BLUE)    # Z-axis in blue
    
    # Project the label positions
    x_label_pos = project_3d_to_2d(110, 0, 0)
    y_label_pos = project_3d_to_2d(0, 110, 0)
    z_label_pos = project_3d_to_2d(0, 0, 110)
    
    # Create font for labels
    font = pygame.font.SysFont('Arial', 16)
    
    # Create label surfaces
    x_label = font.render("X", True, RED)
    y_label = font.render("Y", True, GREEN)
    z_label = font.render("Z", True, BLUE)
    
    # Draw labels
    screen.blit(x_label, (x_label_pos[0], x_label_pos[1]))
    screen.blit(y_label, (y_label_pos[0], y_label_pos[1]))
    screen.blit(z_label, (z_label_pos[0], z_label_pos[1]))

# Game loop
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 16)
last_mouse_pos = None

# Initialize cable data
cable_data = compute_cable_data(box_x, box_y, box_z)

while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle mouse drag for camera rotation
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                last_mouse_pos = pygame.mouse.get_pos()
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                last_mouse_pos = None
        
        elif event.type == pygame.MOUSEMOTION:
            if last_mouse_pos is not None:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - last_mouse_pos[0]
                dy = mouse_y - last_mouse_pos[1]
                
                camera_angle_y += dx * 0.5
                camera_angle_x += dy * 0.5
                
                # Constrain camera angles
                camera_angle_x = max(-90, min(90, camera_angle_x))
                
                last_mouse_pos = (mouse_x, mouse_y)
        
        # Toggle debug visualization
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                show_debug = not show_debug
    
    # Get keys pressed
    keys = pygame.key.get_pressed()
    
    # Calculate desired force vector based on key presses
    desired_force_x = 0
    desired_force_y = 0
    desired_force_z = 0
    
    # Convert WASD/UP/DOWN to desired force
    if keys[pygame.K_a]:  # Move left (negative X)
        desired_force_x = -control_force
        target_position[0] = box_x - speed  # For visualization
    if keys[pygame.K_d]:  # Move right (positive X)
        desired_force_x = control_force
        target_position[0] = box_x + speed  # For visualization
    if keys[pygame.K_UP]:  # Move up (positive Y)
        desired_force_y = control_force
        target_position[1] = box_y + speed  # For visualization
    if keys[pygame.K_DOWN]:  # Move down (negative Y)
        desired_force_y = -control_force
        target_position[1] = box_y - speed  # For visualization
    if keys[pygame.K_w]:  # Move forward (positive Z)
        desired_force_z = control_force
        target_position[2] = box_z + speed  # For visualization
    if keys[pygame.K_s]:  # Move backward (negative Z)
        desired_force_z = -control_force
        target_position[2] = box_z - speed  # For visualization
        
    # If no keys are pressed, update target to current position
    if not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_UP] or 
            keys[pygame.K_DOWN] or keys[pygame.K_w] or keys[pygame.K_s]):
        target_position = [box_x, box_y, box_z]
    
    # Reset view
    if keys[pygame.K_r]:
        camera_angle_x = 30
        camera_angle_y = 45
    
    # Compute cable data based on current box position
    cable_data = compute_cable_data(box_x, box_y, box_z)
    
    # Apply inverse kinematics to calculate tensions
    cable_data = calculate_inverse_kinematics(cable_data, desired_force_x, desired_force_y, desired_force_z)
    
    # Update box physics with the calculated tensions
    update_box_physics(cable_data)
    
    # Draw workspace boundaries
    min_x = min(motor_positions[m][0] for m in motor_positions)
    max_x = max(motor_positions[m][0] for m in motor_positions)
    min_y = min(motor_positions[m][1] for m in motor_positions)
    max_y = max(motor_positions[m][1] for m in motor_positions)
    min_z = min(motor_positions[m][2] for m in motor_positions)
    max_z = max(motor_positions[m][2] for m in motor_positions)
    
    # Define the vertices of the workspace
    workspace_vertices = [
        [min_x, min_y, min_z],  # 0
        [max_x, min_y, min_z],  # 1
        [max_x, min_y, max_z],  # 2
        [min_x, min_y, max_z],  # 3
        [min_x, max_y, min_z],  # 4
        [max_x, max_y, min_z],  # 5
        [max_x, max_y, max_z],  # 6
        [min_x, max_y, max_z]   # 7
    ]
    
    # Define the edges of the workspace
    workspace_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    
    # Draw workspace edges
    for edge in workspace_edges:
        start, end = edge
        draw_line_3d(screen, workspace_vertices[start], workspace_vertices[end], GRAY)
    
    # Draw ground
    ground_y = min_y - 50  # Below the workspace
    ground_vertices = [
        [min_x - 100, ground_y, min_z - 100],
        [max_x + 100, ground_y, min_z - 100],
        [max_x + 100, ground_y, max_z + 100],
        [min_x - 100, ground_y, max_z + 100]
    ]
    
    ground_edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    
    # Draw ground edges
    for edge in ground_edges:
        start, end = edge
        draw_line_3d(screen, ground_vertices[start], ground_vertices[end], (100, 100, 100))
    
    # Draw ground grid
    grid_step = 50
    for x in range(min_x - 100, max_x + 101, grid_step):
        draw_line_3d(screen, [x, ground_y, min_z - 100], [x, ground_y, max_z + 100], (200, 200, 200))
    
    for z in range(min_z - 100, max_z + 101, grid_step):
        draw_line_3d(screen, [min_x - 100, ground_y, z], [max_x + 100, ground_y, z], (200, 200, 200))
    
    # Draw the coordinate axes for reference
    draw_axes(screen)
    
    # Draw motors and cables
    for motor, position in motor_positions.items():
        # Draw motor as a red sphere (approximated as a circle in 2D projection)
        motor_x, motor_y, scale = project_3d_to_2d(*position)
        radius = int(10 * scale)  # Scale the radius based on perspective
        pygame.draw.circle(screen, RED, (motor_x, motor_y), max(1, radius))
        
        # Draw cable from motor to box with tension visualization
        box_position = [box_x, box_y, box_z]
        tension = cable_data[motor]['tension']
        draw_cable(screen, position, box_position, tension, MAX_TENSION)
        
        # Draw motor label
        motor_label = font.render(motor, True, BLACK)
        screen.blit(motor_label, (motor_x + radius, motor_y))
    
    # Draw the box (load) as a blue cube
    draw_cube_3d(screen, [box_x, box_y, box_z], 15, BLUE)
    
    # Draw velocity vector
    vel_scale = 5.0  # Scale for better visualization
    vel_end = [
        box_x + box_vel_x * vel_scale,
        box_y + box_vel_y * vel_scale,
        box_z + box_vel_z * vel_scale
    ]
    draw_line_3d(screen, [box_x, box_y, box_z], vel_end, YELLOW, 3)
    
    # Draw target position (if debug is enabled)
    if show_debug:
        draw_cube_3d(screen, target_position, 5, PURPLE)
        
        # Draw force vectors for debugging
        force_scale = 3.0
        for motor, data in cable_data.items():
            motor_pos = motor_positions[motor]
            tension = data['tension']
            dx, dy, dz = data['direction']
            
            # Calculate force vector endpoint
            force_end = [
                box_x - dx * tension * force_scale,
                box_y - dy * tension * force_scale,
                box_z - dz * tension * force_scale
            ]
            
            # Draw force vector
            draw_line_3d(screen, [box_x, box_y, box_z], force_end, (255, 0, 255), 2)
    
    # Draw screen information
    info_lines = [
        "COMBINED MODE (Physics + WASD Controls)",
        f"Box Position: ({box_x:.1f}, {box_y:.1f}, {box_z:.1f})",
        f"Box Velocity: ({box_vel_x:.1f}, {box_vel_y:.1f}, {box_vel_z:.1f})",
        f"Controls: WASD = XZ movement, UP/DOWN = Y movement",
        f"Press D to {('hide' if show_debug else 'show')} debug visualization",
        f"Camera: Mouse drag to rotate, R to reset view"
    ]
    
    y_offset = 10
    for line in info_lines:
        info_text = font.render(line, True, BLACK)
        screen.blit(info_text, (10, y_offset))
        y_offset += 20
    
    # Print cable info to console
    print("\033[2J\033[H")  # Clear screen
    print(f"3D Cable-Driven Robot Simulation with Inverse Kinematics")
    print(f"Box Position: ({box_x:.1f}, {box_y:.1f}, {box_z:.1f})")
    print(f"Box Velocity: ({box_vel_x:.1f}, {box_vel_y:.1f}, {box_vel_z:.1f})")
    print("-" * 50)
    print("Cable Data:")
    print(f"{'Motor':<5} {'Length (units)':<15} {'Tension (N)':<15}")
    print("-" * 50)
    for motor, data in cable_data.items():
        length = data['length']
        tension = data['tension']
        print(f"{motor:<5} {length:<15.2f} {tension:<15.2f}")
    
    print("-" * 50)
    print("Controls: WASD = XZ movement, UP/DOWN = Y movement")
    
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
