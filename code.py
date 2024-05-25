# main.py
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
from rgbkeypad import RGBKeypad
from lighting import LightingController  # Ensure lighting.py is in the same directory
from keyidentity import KEYBOARD_MAP  # Ensure keyidentity.py is in the same directory
from commandfunc import open_website, alt_tab, open_cal, poon  # Ensure commandfunc.py is correctly defined

# Initialize the keypad, keyboard, and consumer control
keypad = RGBKeypad()
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# Initialize the lighting controller with the keypad
lighting_controller = LightingController(keypad)

def execute_key_action(action, code):
    """Executes the action associated with a key press."""
    if callable(code):  # If the code is a function, call it
        code(kbd)
    elif isinstance(code, tuple):  # If the code is a tuple, it's a key combination
        kbd.send(*code)
    else:  # Otherwise, send the code as a consumer control code
        cc.send(code)

while True:
    for key in keypad.keys:
        if key.is_pressed():
            original_color = key.color
            key.color = (255, 255, 255)
            # Retrieve the action and parameters for the pressed key
            key_action = KEYBOARD_MAP.get((key.x, key.y), None)
            if key_action:
                action, code, original_color = key_action

                if action == "Cycle Lighting Effects":
                    lighting_controller.next_effect()
                else:
                    execute_key_action(action, code)

            while key.is_pressed():
                pass  # Wait for the key to be released
            key.color = original_color
