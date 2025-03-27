import pygame
import numpy as np

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cable-Driven Robot Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define motor positions (can be changed with WASD keys)
motor_positions = {
    "L1": [100, 100],
    "L2": [100, 500],
    "R1": [500, 100],
    "R2": [500, 500]
}

# Initial box position
box_x, box_y = 300, 300
speed = 5  # Initial box movement speed
speed_step = 0.5  # Speed adjustment step
MAX_SPEED = 500  # Maximum allowed speed

# Store previous cable lengths for velocity calculation
prev_cable_lengths = {motor: 0 for motor in motor_positions}
time_step = 0.05  # 50ms in seconds

# Function to compute motor speeds and velocities
def compute_motor_data(box_x, box_y):
    global prev_cable_lengths
    
    cable_lengths = {}
    velocities = {}
    
    for motor, (mx, my) in motor_positions.items():
        # Calculate current cable length
        current_length = np.sqrt((mx - box_x) ** 2 + (my - box_y) ** 2)
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

# Function to constrain box within motor boundaries
def constrain_box_position():
    global box_x, box_y
    
    # Find the boundaries defined by the motors
    min_x = min(motor_positions[m][0] for m in motor_positions)
    max_x = max(motor_positions[m][0] for m in motor_positions)
    min_y = min(motor_positions[m][1] for m in motor_positions)
    max_y = max(motor_positions[m][1] for m in motor_positions)
    
    # Add a small buffer (5 pixels) to keep the box fully visible within the boundaries
    buffer = 10
    
    # Constrain the box position
    box_x = max(min_x + buffer, min(max_x - buffer, box_x))
    box_y = max(min_y + buffer, min(max_y - buffer, box_y))

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get keys pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:  # Move up
        box_y -= speed
    if keys[pygame.K_s]:  # Move down
        box_y += speed
    if keys[pygame.K_a]:  # Move left
        box_x -= speed
    if keys[pygame.K_d]:  # Move right
        box_x += speed
    if keys[pygame.K_UP]:  # Increase speed
        speed = min(MAX_SPEED, speed + speed_step)  # Limit to maximum speed
    if keys[pygame.K_DOWN]:  # Decrease speed
        speed = max(0.1, speed - speed_step)  # Minimum speed of 0.1
    
    # Constrain box position to stay within motor boundaries
    constrain_box_position()
    
    # Compute motor data (cable lengths and velocities)
    cable_lengths, velocities = compute_motor_data(box_x, box_y)
    
    # Print motor data and current speed
    print("\033[2J\033[H")  # Clear screen
    print(f"Box Position: ({box_x:.1f}, {box_y:.1f})")
    print(f"Movement Speed: {speed:.2f} (Max: {MAX_SPEED})")
    print("-" * 40)
    print("Cable Lengths vs Motor Velocities:")
    print(f"{'Motor':<5} {'Length (px)':<15} {'Velocity (px/s)':<15}")
    print("-" * 40)
    for motor in motor_positions:
        length = cable_lengths[motor]
        velocity = velocities[motor]
        # Highlight if motor is actively retracting or extending
        if abs(velocity) > 0.1:
            direction = "extending" if velocity > 0 else "retracting"
            print(f"{motor:<5} {length:<15.2f} {velocity:<15.2f} ({direction})")
        else:
            print(f"{motor:<5} {length:<15.2f} {velocity:<15.2f}")
    print("-" * 40)
    
    # Draw motors
    for motor, (mx, my) in motor_positions.items():
        pygame.draw.circle(screen, RED, (mx, my), 10)
        pygame.draw.line(screen, BLACK, (mx, my), (box_x, box_y), 2)
    
    # Draw the box (load)
    pygame.draw.rect(screen, BLUE, (box_x - 10, box_y - 10, 20, 20))
    
    # Draw the boundary box
    min_x = min(motor_positions[m][0] for m in motor_positions)
    max_x = max(motor_positions[m][0] for m in motor_positions)
    min_y = min(motor_positions[m][1] for m in motor_positions)
    max_y = max(motor_positions[m][1] for m in motor_positions)
    box_width = max_x - min_x
    box_height = max_y - min_y
    
    # Draw the rectangle
    pygame.draw.rect(screen, (200, 200, 200), (min_x, min_y, box_width, box_height), 1)
    
    # Initialize font
    if not hasattr(pygame, 'font_initialized'):
        pygame.font.init()
        pygame.font_initialized = True
    font = pygame.font.SysFont('Arial', 16)
    
    # Create width label
    width_text = f"Width: {box_width}px"
    width_surface = font.render(width_text, True, BLACK)
    screen.blit(width_surface, (min_x + box_width/2 - width_surface.get_width()/2, max_y + 5))
    
    # Create height label
    height_text = f"Height: {box_height}px"
    height_surface = font.render(height_text, True, BLACK)
    # Rotate the text for the height label
    height_surface = pygame.transform.rotate(height_surface, 90)
    screen.blit(height_surface, (max_x + 5, min_y + box_height/2 - height_surface.get_height()/2))
    
    pygame.display.flip()
    pygame.time.delay(50)  # Adjust frame rate

pygame.quit()