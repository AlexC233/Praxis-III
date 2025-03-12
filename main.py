import time
import controller
import sys
import select
import board
import busio 

controller = controller.Controller()
uart = busio.UART(board.GP0, board.GP1, baudrate = 115200)

def read_serial_command():
    if sys.stdin in select.select([sys.stdin],[],[],0)[0]:
        return sys.stdin.readline().strip()
    return None

print("Pico is ready. Waiting for commands...")

while True:
    command = read_serial_command()

    if command:
        print(f"Received command: {command}")  # Debug print

    if command == "w":
        controller.forward()  # Move forward
    elif command == "s":
        controller.backward()  # Move backward
    elif command == "a":
        controller.left()  # Move left
    elif command == "d":
        controller.right()  # Move right
    elif command == "q":
        controller.up()  # Move up
    elif command == "e":
        controller.down()  # Move down
    elif command == "stop":
        print("Stopping motors")
