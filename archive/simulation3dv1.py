import pygame
import numpy as np
import math

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Cable-Driven Robot Simulation (Pygame Only)")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 128)

# Center of the screen for projection
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

# Define motor positions in 3D space (x, y, z)
motor_positions = {
    "C1": [-200, -200, -200],  # Corner 1
    "C2": [-200, -200, 200],   # Corner 2
    "C3": [200, -200, 200],    # Corner 3
    "C4": [200, -200, -200],   # Corner 4
}

# Initial box position (center of the workspace)
box_x, box_y, box_z = 0, 0, 0
speed = 5.0  # Initial box movement speed
speed_step = 0.5  # Speed adjustment step
MAX_SPEED = 500  # Maximum allowed speed

# Camera rotation parameters
camera_angle_x = 30  # Initial camera angle in degrees (looking down)
camera_angle_y = 45  # Initial rotation around Y axis
camera_distance = 800

# Store previous cable lengths for velocity calculation
prev_cable_lengths = {motor: 0 for motor in motor_positions}
time_step = 0.05  # 50ms in seconds

# Function to compute motor speeds and velocities
def compute_motor_data(box_x, box_y, box_z):
    global prev_cable_lengths
    
    cable_lengths = {}
    velocities = {}
    
    for motor, (mx, my, mz) in motor_positions.items():
        # Calculate current cable length
        current_length = np.sqrt((mx - box_x) ** 2 + (my - box_y) ** 2 + (mz - box_z) ** 2)
        cable_lengths[motor] = current_length
        
        # Calculate velocity (rate of change of cable length)
        if prev_cable_lengths[motor] == 0:  # First iteration
            velocities[motor] = 0
        else:
            # Positive velocity = cable extending, negative = retracting
            velocities[motor] = (current_length - prev_cable_lengths[motor]) / time_step
        
        # Update previous length for next iteration
        prev_cable_lengths[motor] = current_length
        
    return cable_lengths, velocities

# Function to constrain box position within motor boundaries
def constrain_box_position():
    global box_x, box_y, box_z
    
    # Find the boundaries defined by the motors
    min_x = min(motor_positions[m][0] for m in motor_positions)
    max_x = max(motor_positions[m][0] for m in motor_positions)
    min_y = min(motor_positions[m][1] for m in motor_positions)
    max_y = max(motor_positions[m][1] for m in motor_positions)
    min_z = min(motor_positions[m][2] for m in motor_positions)
    max_z = max(motor_positions[m][2] for m in motor_positions)
    
    # Add a small buffer to keep the box fully visible within the boundaries
    buffer = 20
    
    # Constrain the box position
    box_x = max(min_x + buffer, min(max_x - buffer, box_x))
    box_y = max(min_y + buffer, min(max_y - buffer, box_y))
    box_z = max(min_z + buffer, min(max_z - buffer, box_z))

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
def draw_line_3d(screen, start_3d, end_3d, color):
    start_x, start_y, _ = project_3d_to_2d(*start_3d)
    end_x, end_y, _ = project_3d_to_2d(*end_3d)
    pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 2)

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
    
    # Get keys pressed
    keys = pygame.key.get_pressed()
    
    # Box movement in 3D space
    if keys[pygame.K_w]:  # Move forward (positive Z)
        box_z += speed
    if keys[pygame.K_s]:  # Move backward (negative Z)
        box_z -= speed
    if keys[pygame.K_a]:  # Move left (negative X)
        box_x -= speed
    if keys[pygame.K_d]:  # Move right (positive X)
        box_x += speed
    if keys[pygame.K_UP]:  # Move up (positive Y) - as requested
        box_y += speed
    if keys[pygame.K_DOWN]:  # Move down (negative Y) - as requested
        box_y -= speed
    
    # Speed adjustment
    if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:  # Increase speed
        speed = min(MAX_SPEED, speed + speed_step)
    if keys[pygame.K_MINUS]:  # Decrease speed
        speed = max(0.1, speed - speed_step)
    
    # Reset view
    if keys[pygame.K_r]:
        camera_angle_x = 30
        camera_angle_y = 45
    
    # Constrain box position
    constrain_box_position()
    
    # Compute motor data
    cable_lengths, velocities = compute_motor_data(box_x, box_y, box_z)
    
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
        [max_x, max_y, min_z],  # 2
        [min_x, max_y, min_z],  # 3
        [min_x, min_y, max_z],  # 4
        [max_x, min_y, max_z],  # 5
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
    
    # Draw the coordinate axes for reference
    draw_axes(screen)
    
    # Draw motors and cables
    for motor, position in motor_positions.items():
        # Draw motor as a red sphere (approximated as a circle in 2D projection)
        motor_x, motor_y, scale = project_3d_to_2d(*position)
        radius = int(10 * scale)  # Scale the radius based on perspective
        pygame.draw.circle(screen, RED, (motor_x, motor_y), max(1, radius))
        
        # Draw cable from motor to box
        box_position = [box_x, box_y, box_z]
        draw_line_3d(screen, position, box_position, BLACK)
        
        # Draw motor label
        motor_label = font.render(motor, True, BLACK)
        screen.blit(motor_label, (motor_x + radius, motor_y))
    
    # Draw the box (load) as a blue cube
    draw_cube_3d(screen, [box_x, box_y, box_z], 15, BLUE)
    
    # Draw screen information
    info_lines = [
        f"Box Position: ({box_x:.1f}, {box_y:.1f}, {box_z:.1f})",
        f"Movement Speed: {speed:.2f}",
        f"Camera Angles: X={camera_angle_x:.1f}°, Y={camera_angle_y:.1f}°",
        "Controls:",
        "WASD: Move in XZ plane",
        "UP/DOWN: Move in Y dimension",
        "Mouse drag: Rotate camera",
        "R: Reset view",
        "+/-: Adjust speed"
    ]
    
    y_offset = 10
    for line in info_lines:
        info_text = font.render(line, True, BLACK)
        screen.blit(info_text, (10, y_offset))
        y_offset += 20
    
    # Print cable info to console
    print("\033[2J\033[H")  # Clear screen
    print(f"3D Cable-Driven Robot Simulation")
    print(f"Box Position: ({box_x:.1f}, {box_y:.1f}, {box_z:.1f})")
    print(f"Movement Speed: {speed:.2f} (Max: {MAX_SPEED})")
    print("-" * 50)
    print("Cable Lengths vs Motor Velocities:")
    print(f"{'Motor':<5} {'Length (units)':<15} {'Velocity (units/s)':<15}")
    print("-" * 50)
    for motor in motor_positions:
        length = cable_lengths[motor]
        velocity = velocities[motor]
        # Highlight if motor is actively retracting or extending
        if abs(velocity) > 0.1:
            direction = "extending" if velocity > 0 else "retracting"
            print(f"{motor:<5} {length:<15.2f} {velocity:<15.2f} ({direction})")
        else:
            print(f"{motor:<5} {length:<15.2f} {velocity:<15.2f}")
    
    pygame.display.flip()
    clock.tick(20)

pygame.quit()