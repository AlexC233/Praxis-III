import board
import digitalio
import time

# Configure the GPIO pins connected to buttons as digital inputs
w = digitalio.DigitalInOut(board.GP16)
w.direction = digitalio.Direction.INPUT
w.pull = digitalio.Pull.UP  # Enable internal pull-up resistor

a = digitalio.DigitalInOut(board.GP17)
a.direction = digitalio.Direction.INPUT
a.pull = digitalio.Pull.UP

s = digitalio.DigitalInOut(board.GP18)
s.direction = digitalio.Direction.INPUT
s.pull = digitalio.Pull.UP

d = digitalio.DigitalInOut(board.GP19)
d.direction = digitalio.Direction.INPUT
d.pull = digitalio.Pull.UP

# Variables to track previous button states for proper debouncing
prev_w_state = True
prev_a_state = True
prev_s_state = True
prev_d_state = True

debounce_time = 0.05  # 50 milliseconds is usually sufficient

# Loop so the code runs continuously
while True:
     # Check each button and detect transitions from HIGH (not pressed) to LOW (pressed)
     if w.value == False and prev_w_state == True:
          print("w pressed")

     if a.value == False and prev_a_state == True:
          print("a pressed")

     if s.value == False and prev_s_state == True:
          print("s pressed")

     if d.value == False and prev_d_state == True:
          print("d pressed")

     # Update previous states
     prev_w_state = w.value
     prev_a_state = a.value
     prev_s_state = s.value
     prev_d_state = d.value

     time.sleep(debounce_time)