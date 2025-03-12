# import time

# import controller
# import chassis

# controller = controller.Controller()
# chassis = chassis.Chassis()

# while True:
# # main.py
import time
import controller_pio

ctrl = controller_pio.Controller()

while True:
    # Example: move forward once
    ctrl.forward()
    time.sleep(2)
    # Then do something else...
    # ctrl.right()
    # etc.
