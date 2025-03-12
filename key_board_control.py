import serial
import keyboard
import time

SERIAL_PORT = "/dev/tty.usbmodem101"

BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout = 1)
time.sleep(2)

print("Use WASD to control. Press ESC to stop.")

key_map = {
    "w": "w",
    "s": "s",
    "a": "a",
    "d": "d",
    "q": "q",
    "e": "e",
    "esc": "stop"
}

while True:
    for key, command in key_map.items():
        if keyboard.is_pressed(key):
            ser.write((command + "\n").encode())  # Send command to Pico
            print(f"Sent: {command}")
            time.sleep(0.2)  # Small delay to prevent spamming
