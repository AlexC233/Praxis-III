
import RPi.GPIO as GPIO
import keyboard
import time

# Define motor step and direction pins
motors = [
    {'step': 17, 'dir': 18},  # Motor 1
    {'step': 22, 'dir': 23},  # Motor 2
    {'step': 24, 'dir': 25},  # Motor 3
    {'step': 5, 'dir': 6}     # Motor 4
]

# GPIO setup
GPIO.setmode(GPIO.BCM)
for motor in motors:
    GPIO.setup(motor['step'], GPIO.OUT)
    GPIO.setup(motor['dir'], GPIO.OUT)

def move_motor(motor_index, direction):
    GPIO.output(motors[motor_index]['dir'], direction)
    for _ in range(10):  # Adjust step count as needed
        GPIO.output(motors[motor_index]['step'], GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(motors[motor_index]['step'], GPIO.LOW)
        time.sleep(0.001)

print("Stepper motor control started. Press ESC to exit.")

try:
    while True:
        if keyboard.is_pressed('w'):
            move_motor(0, GPIO.HIGH)  # Motor 1 forward
        elif keyboard.is_pressed('s'):
            move_motor(0, GPIO.LOW)   # Motor 1 backward
        
        if keyboard.is_pressed('a'):
            move_motor(1, GPIO.HIGH)  # Motor 2 forward
        elif keyboard.is_pressed('d'):
            move_motor(1, GPIO.LOW)   # Motor 2 backward
        
        if keyboard.is_pressed('up'):
            move_motor(2, GPIO.HIGH)  # Motor 3 forward
        elif keyboard.is_pressed('down'):
            move_motor(2, GPIO.LOW)   # Motor 3 backward
        
        if keyboard.is_pressed('left'):
            move_motor(3, GPIO.HIGH)  # Motor 4 forward
        elif keyboard.is_pressed('right'):
            move_motor(3, GPIO.LOW)   # Motor 4 backward
        
        if keyboard.is_pressed('esc'):
            break
        
        time.sleep(0.1)

finally:
    GPIO.cleanup()
    print("Stepper motor control stopped.")
