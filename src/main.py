import time
import supervisor  # for checking serial input in CircuitPython
from controller import Controller

controller = Controller()

print("Stepper controller initialized.")
print("Commands:")
print("  w = forward")
print("  s = backward")
print("  a = left")
print("  d = right")
print("  u = up")
print("  n = down")
print("Send one of the characters above, then press ENTER.")

while True:
    # Only check input if there's something available
    if supervisor.runtime.serial_bytes_available:
        user_input = input().strip().lower()

        if user_input == 'w':
            print("Forward...")
            controller.forward()

        elif user_input == 's':
            print("Backward...")
            controller.backward()

        elif user_input == 'a':
            print("Left...")
            controller.left()

        elif user_input == 'd':
            print("Right...")
            controller.right()

        elif user_input == 'u':
            print("Up...")
            controller.up()

        elif user_input == 'n':
            print("Down...")
            controller.down()

        else:
            print("Unrecognized command:", user_input)

    # Wait 1 second before checking again
    time.sleep(1)
    