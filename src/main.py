import time
import supervisor  # for checking serial input in CircuitPython
from command_processor import CommandProcessor

processor = CommandProcessor()

print("Stepper controller initialized.")
print("Commands:")
print("  w = forward")
print("  s = backward")
print("  a = left")
print("  d = right")
print("  u = up")
print("  n = down")
print("  r = reverse last command")
print("Send one or multiple characters above, then press ENTER.")

while True:
    # Only check input if there's something available
    if supervisor.runtime.serial_bytes_available:
        user_input = input().strip().lower()
        
        if user_input == 'r':
            print("Reversing last command...")
            processor.reverse_last_command()
        else:
            print(f"Processing command: {user_input}")
            processor.execute_command(user_input)
    
    # Wait a short time before checking again
    time.sleep(0.1)