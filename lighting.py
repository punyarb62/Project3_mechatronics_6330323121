import time

class LightingController:
    def __init__(self, keypad):
        self.keypad = keypad
        self.effects = [self.rainbow_effect, self.night_mode, self.day_mode, self.no_light]
        self.current_effect = 0

    def next_effect(self):
        self.current_effect = (self.current_effect + 1) % len(self.effects)
        self.apply_effect()

    def apply_effect(self):
        # Clear all keys before applying new effect
        for key in self.keypad.keys:
            key.color = (0, 0, 0)
        # Apply the selected effect
        self.effects[self.current_effect]()

    def rainbow_effect(self):
        rainbow_colors = [
            (148, 0, 211),  # Violet
            (75, 0, 130),   # Indigo
            (0, 0, 255),    # Blue
            (0, 255, 0),    # Green
            (255, 255, 0),  # Yellow
            (255, 127, 0),  # Orange
            (255, 0, 0)     # Red
        ]
        num_keys = len(self.keypad.keys)
        for i, key in enumerate(self.keypad.keys):
            key.color = rainbow_colors[i % len(rainbow_colors)]

    def night_mode(self):
        # Set all keys to blue for Night mode
        for key in self.keypad.keys:
            key.color = (0, 0, 255)

    def day_mode(self):
        # Define a simple gradient from red to yellow
        gradient_colors = [
            (255, 0, 0),    # Red
            (255, 69, 0),   # Orange Red
            (255, 140, 0),  # Dark Orange
            (255, 165, 0),  # Orange
            (255, 215, 0),  # Gold
            (255, 255, 0)   # Yellow
        ]
        num_keys = len(self.keypad.keys)
        for i, key in enumerate(self.keypad.keys):
            key.color = gradient_colors[i % len(gradient_colors)]

    def no_light(self):
        # Turn off all keys for No light mode
        for key in self.keypad.keys:
            key.color = (0, 0, 0)
    def no_light(self):
        # Turn off all keys for No light mode
        for key in self.keypad.keys:
            key.color =key.color