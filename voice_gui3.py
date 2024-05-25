import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import threading
from voice_assistant_backend import Assistant

class AssistantGUI:
    def __init__(self, assistant):
        self.assistant = assistant
        self.window = tk.Tk()
        self.window.title("Assistant")
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", True)
        self.window.attributes('-alpha', 0.9)

        # Load and resize images using Pillow
        idle_image_path = r"C:\Users\asus\python 3.10\ratchatin_mechatronics\bot.png"
        listening_image_path = r"C:\Users\asus\python 3.10\ratchatin_mechatronics\bot (2).png"
        speaking_image_path = r"C:\Users\asus\python 3.10\ratchatin_mechatronics\bot (1).png"
        
        self.idle_image = ImageTk.PhotoImage(Image.open(idle_image_path).resize((300, 300), Image.LANCZOS))
        self.listening_image = ImageTk.PhotoImage(Image.open(listening_image_path).resize((300, 300), Image.LANCZOS))
        self.speaking_image = ImageTk.PhotoImage(Image.open(speaking_image_path).resize((300, 300), Image.LANCZOS))

        self.image_label = tk.Label(self.window, image=self.idle_image, bd=0)
        self.image_label.pack()

        # Button to close the application
        self.close_button = tk.Button(self.window, text="X", command=self.close_window, bg="red", fg="white", bd=0, font=("Helvetica", 8))
        self.close_button.place(x=282, y=2)  # Adjusted for the new image size

        # Bind the click event to activate the assistant
        self.image_label.bind("<Button-1>", self.activate_assistant)

        self.position_window()

    def position_window(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 300  # New width
        window_height = 300  # New height

        x_coordinate = screen_width - window_width - 10
        y_coordinate = screen_height - window_height - 40

        self.window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    def activate_assistant(self, event):
        """Handle interaction when the robot image is clicked."""
        def listen_and_respond():
            self.image_label.config(image=self.listening_image)
            audio_data = self.assistant.speech_manager.record_audio()
            text = self.assistant.speech_manager.audio_to_text(audio_data)
            if text:
                self.image_label.config(image=self.speaking_image)
                response = self.assistant.handle_command(text)
                self.assistant.speech_manager.text_to_speech(response)
                print(f"You said: {text}\nAssistant said: {response}")
                self.image_label.config(image=self.idle_image)
            else:
                print("Sorry, I didn't catch that.")
                self.image_label.config(image=self.idle_image)
        threading.Thread(target=listen_and_respond).start()

    def close_window(self):
        self.window.destroy()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    assistant = Assistant(language='en-US')  # Ensure this matches your backend implementation
    gui = AssistantGUI(assistant)
    gui.run()
