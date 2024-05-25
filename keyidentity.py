# keyidentity.py
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode
from commandfunc import open_website, alt_tab, open_cal, poon  # Import utility functions

KEYBOARD_MAP = {
    (0, 0): ("Previous Track", ConsumerControlCode.SCAN_PREVIOUS_TRACK, (255, 255, 0)),
    (1, 0): ("Play/Pause", ConsumerControlCode.PLAY_PAUSE, (0, 255, 0)),
    (2, 0): ("Next Track", ConsumerControlCode.SCAN_NEXT_TRACK, (255, 165, 0)),
    (3, 0): ("Mute Toggle", ConsumerControlCode.MUTE, (255, 0, 0)),
    (0, 1): ("Open YouTube", lambda kbd: open_website(kbd, 'www.youtube.com'), (255, 0, 0)),
    (1, 1): ("Open Netflix", lambda kbd: open_website(kbd, 'www.netflix.com'), (255, 192, 203)),
    (2, 1): ("Open Disneyplus", lambda kbd: open_website(kbd, 'www.disneyplus.com'), (128, 128, 128)),
    (3, 1): ("Volume Up", ConsumerControlCode.VOLUME_INCREMENT, (0, 0, 255)),
    (0, 2): ("Screen Brightness Down", ConsumerControlCode.BRIGHTNESS_DECREMENT, (64, 224, 208)),
    (1, 2): ("calculator", lambda kbd: open_cal(kbd, 'calc.exe'), (0, 255, 255)),
    (2, 2): ("Screen Brightness Up", ConsumerControlCode.BRIGHTNESS_INCREMENT, (255, 215, 0)),
    (3, 2): ("Volume Down", ConsumerControlCode.VOLUME_DECREMENT, (75, 0, 130)),
    (0, 3): ("Lock Computer", (Keycode.GUI, Keycode.L), (128, 0, 128)),
    (1, 3): ("Type my name", lambda kbd: poon(kbd, 'PUNYAPHAT SUKWAN'), (255, 20, 147)),
    (2, 3): ("Enter", (Keycode.ENTER,), (0, 128, 0)),
    (3, 3): ("Cycle Lighting Effects", lambda kbd: lighting_controller.next_effect(), (255, 255, 255)),
}
