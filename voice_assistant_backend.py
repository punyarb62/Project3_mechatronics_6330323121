import speech_recognition as sr
import pyttsx3
import datetime
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import paho.mqtt.client as mqtt
import openai
import pyautogui

# Environment and API setup
openai_api_key = 'xxx'
class SpeechManager:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()

    def record_audio(self):
        """Record audio from the microphone and return as audio data."""
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        return audio

    def audio_to_text(self, audio):
        """Convert audio data to text."""
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

    def text_to_speech(self, text):
        """Convert text to speech."""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client("PythonGesturePublisher")
        self.client.username_pw_set("onaguuni", "xy5BTcTTk63B")
        self.client.connect("hairdresser.cloudmqtt.com", 18486)

    def publish(self, topic, message):
        """Publish a message to a MQTT topic."""
        self.client.publish(topic, message)

class SpotifyController:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id='xxxx',
            client_secret='xxx',
            redirect_uri='http://localhost:8888/callback',
            scope='user-modify-playback-state,user-read-playback-state,user-read-currently-playing'
        ))

    def play_pause(self):
        """Toggle play or pause on Spotify."""
        playback = self.sp.current_playback()
        if playback and playback['is_playing']:
            self.sp.pause_playback()
        else:
            self.sp.start_playback()

    def play_song(self, song_name):
        """Search for a song and play it."""
        results = self.sp.search(song_name, limit=1, type='track')
        track_uri = results['tracks']['items'][0]['uri']
        self.sp.start_playback(uris=[track_uri])

    def search_song(self, song_name):
        """Search for a song and return the top results."""
        results = self.sp.search(song_name, limit=5, type='track')
        songs = [track['name'] for track in results['tracks']['items']]
        return ", ".join(songs)

    def set_volume(self, volume_level):
        """Set the Spotify volume."""
        self.sp.volume(volume_level)

class OpenAIChat:
    def __init__(self, api_key):
        self.api_key = api_key

    def chat(self, message):
        """Query OpenAI's ChatGPT model with text."""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            max_tokens=150,
            api_key=self.api_key
        )
        return response.choices[0].message.content

class Assistant:
    def __init__(self, language='en-US'):
        self.language = language
        self.speech_manager = SpeechManager()
        self.mqtt_client = MQTTClient()
        self.spotify_controller = SpotifyController()
        self.chat_model = OpenAIChat(openai_api_key)

    def get_time(self):
        """Return the current time."""
        now = datetime.datetime.now()
        return now.strftime("%H:%M")

    def get_date(self):
        """Return today's date and day."""
        today = datetime.datetime.now()
        return today.strftime("%Y-%m-%d, %A")

    def handle_command(self, text):
        """Process and respond to voice commands."""
        text_lower = text.lower()
        if "what time is it" in text_lower:
            return self.get_time()
        elif "what's today's date" in text_lower:
            return self.get_date()
        elif "turn on the light" in text_lower:
            self.mqtt_client.publish("home/light", "ON")
            return "Turning on the light."
        elif "turn off the light" in text_lower:
            self.mqtt_client.publish("home/light", "OFF")
            return "Turning off the light."
        elif "play spotify" in text_lower or "pause spotify" in text_lower:
            self.spotify_controller.play_pause()
            return "Toggled play/pause on Spotify."
        elif "play song " in text_lower:
            song_name = text_lower.split("play song ")[1]
            self.spotify_controller.play_song(song_name)
            return f"Playing {song_name}"
        elif "search song " in text_lower:
            song_name = text_lower.split("search song ")[1]
            songs = self.spotify_controller.search_song(song_name)
            return f"Top songs: {songs}"
        elif "set volume to " in text_lower:
            volume_level = int(text_lower.split("set volume to ")[1])
            self.spotify_controller.set_volume(volume_level)
            return f"Volume set to {volume_level}%"
        elif "typing " in text_lower:
            typing_text = text_lower.split("typing ", 1)[1]
            pyautogui.write(typing_text,interval=0.1)
            return f"Typing: {typing_text}"
        else:
            return self.chat_model.chat(text)

if __name__ == "__main__":
    assistant = Assistant()
    while True:
        audio_data = assistant.speech_manager.record_audio()
        text = assistant.speech_manager.audio_to_text(audio_data)
        if text:
            response = assistant.handle_command(text)
            assistant.speech_manager.text_to_speech(response)
