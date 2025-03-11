import time
import keyboard

class Chassis:
    def run(controller):
        if keyboard.is_pressed('w'):
            controller.forward()
        elif keyboard.is_pressed('a'):
            controller.left()
        elif keyboard.is_pressed('s'):
            controller.backward()
        elif keyboard.is_pressed('d'):
            controller.right()
        elif keyboard.is_pressed('ctrl'):  # Left Control
            controller.down()
        elif keyboard.is_pressed('space'):
            controller.up()