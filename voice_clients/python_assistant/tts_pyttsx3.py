# voice_clients/python_assistant/tts_pyttsx3.py
import pyttsx3
_engine = pyttsx3.init()
def speak(text: str):
    _engine.say(text)
    _engine.runAndWait()
