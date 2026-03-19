"""
Utility script to demonstrate programmatic access to keyboard and mouse using `pynput`.
Note: This requires a GUI environment (e.g., a real monitor or Xvfb) to function.
"""

import threading
import time

from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import (
    Key,
)
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

# Initialize controllers
keyboard = KeyboardController()
mouse = MouseController()


def simulate_typing(text):
    """Simulates typing the given text."""
    print(f"Typing: {text}")
    for char in text:
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(0.05)


def simulate_mouse_movement_and_click():
    """Simulates moving the mouse and clicking."""
    print("Moving mouse...")
    # Read pointer position
    print(f"Current pointer position: {mouse.position}")

    # Set pointer position (this just demonstrates movement, be careful when using in real automation)
    # mouse.position = (100, 200)

    # Move pointer relative to current position
    mouse.move(50, -50)

    print("Clicking right button...")
    mouse.press(Button.right)
    mouse.release(Button.right)

    # Double click
    print("Double clicking left button...")
    mouse.click(Button.left, 2)


def on_press(key):
    """Callback for when a key is pressed."""
    try:
        print(f"Key {key.char} pressed")
    except AttributeError:
        print(f"Special key {key} pressed")


def on_release(key):
    """Callback for when a key is released."""
    print(f"Key {key} released")
    if key == Key.esc:
        # Stop listener
        print("Escape pressed. Exiting listener.")
        return False


def start_keyboard_listener():
    """Starts listening to keyboard events in the background."""
    print("Starting keyboard listener... (Press ESC to stop)")
    with KeyboardListener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    print("Keyboard and Mouse Automation Utils")
    print("-----------------------------------")
    print("Note: In a headless server (VPS) environment without X11/GUI, ")
    print("this script may crash or fail to execute.\n")

    # Example usage (Uncomment to test if you have a GUI)

    # 1. Type something
    # simulate_typing("Hello from GenX!")

    # 2. Move mouse and click
    # simulate_mouse_movement_and_click()

    # 3. Start listener (blocks execution)
    # start_keyboard_listener()

    print("Utils are ready to be used. See commented examples in the script.")
