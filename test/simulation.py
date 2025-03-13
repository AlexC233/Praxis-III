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
speed = 1  # Initial box movement speed
speed_step = 0.5  # Speed adjustment step

# Function to compute motor speeds
def compute_motor_speeds(box_x, box_y):
    speeds = {}
    for motor, (mx, my) in motor_positions.items():
        L = np.sqrt((mx - box_x) ** 2 + (my - box_y) ** 2)
        speeds[motor] = L
    return speeds

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
        speed += speed_step
    if keys[pygame.K_DOWN]:  # Decrease speed
        speed = max(0.1, speed - speed_step)  # Minimum speed of 0.1
    
    # Compute motor speeds
    motor_speeds = compute_motor_speeds(box_x, box_y)
    
    # Print motor speeds and current speed
    print("\033[2J\033[H")  # Clear screen
    print(f"Current Speed: {speed:.2f}")
    print("Motor Speeds:")
    for motor, speed in motor_speeds.items():
        print(f"{motor}: {speed:.4f}")
    print("-" * 40)
    
    # Draw motors
    for motor, (mx, my) in motor_positions.items():
        pygame.draw.circle(screen, RED, (mx, my), 10)
        pygame.draw.line(screen, BLACK, (mx, my), (box_x, box_y), 2)
    
    # Draw the box (load)
    pygame.draw.rect(screen, BLUE, (box_x - 10, box_y - 10, 20, 20))
    
    pygame.display.flip()
    pygame.time.delay(50)  # Adjust frame rate

pygame.quit()
