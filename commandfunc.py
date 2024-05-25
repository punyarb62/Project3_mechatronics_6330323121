# commandfunc.py
from adafruit_hid.keycode import Keycode
import time

def type_string(kbd, string):
    for char in string:
        shift = False
        if char.isupper() or char in '~!@#$%^&*()_+{}|:"<>?':
            shift = True

        special_keys = {
            ' ': Keycode.SPACE,
            '.': Keycode.PERIOD,
            ',': Keycode.COMMA,
            '/': Keycode.FORWARD_SLASH,
            '\\': Keycode.BACKSLASH,
            '-': Keycode.MINUS,
            '=': Keycode.EQUALS,
            '`': Keycode.GRAVE_ACCENT,
            '[': Keycode.LEFT_BRACKET,
            ']': Keycode.RIGHT_BRACKET,
            ';': Keycode.SEMICOLON,
            "'": Keycode.QUOTE,
        }

        keycode = special_keys.get(char, None)
        if not keycode:
            if 'a' <= char <= 'z':
                keycode = Keycode.A + (ord(char) - ord('a'))
            elif 'A' <= char <= 'Z':
                keycode = Keycode.A + (ord(char.lower()) - ord('a'))
                shift = True
            elif '0' <= char <= '9':
                keycode = Keycode.ZERO + (ord(char) - ord('0'))
        
        if keycode:
            if shift:
                kbd.send(Keycode.SHIFT, keycode)
            else:
                kbd.send(keycode)
        else:
            print(f"Unsupported character: {char}")

def open_website(kbd, url):
    kbd.release_all()
    kbd.send(Keycode.GUI, Keycode.R)  # Windows + R to open Run dialog
    time.sleep(0.5)
    type_string(kbd, f'chrome {url}')
    time.sleep(0.1)
    kbd.send(Keycode.ENTER)
    kbd.release_all()

def open_cal(kbd, cal):
    kbd.release_all()
    kbd.send(Keycode.GUI, Keycode.R)  # Windows + R to open Run dialog
    time.sleep(0.5)
    type_string(kbd, cal)
    time.sleep(0.1)
    kbd.send(Keycode.ENTER)
    kbd.release_all()

def alt_tab(kbd):
    kbd.press(Keycode.ALT, Keycode.TAB)
    time.sleep(0.1)  # Adjust timing as needed for the Alt+Tab window to appear
    kbd.release_all()

def poon(kbd, name):
    kbd.release_all()
    time.sleep(0.1)
    type_string(kbd, name)
    time.sleep(0.1)
    kbd.release_all()
