# voice_clients/python_assistant/voice_assistant.py
import time
import requests
import pyttsx3

# Optional: use VOSK for offline STT; fallback to online Google STT if not configured
try:
    from stt_vosk import recognize_from_microphone
    VOSK_AVAILABLE = True
except Exception:
    VOSK_AVAILABLE = False

TTS = pyttsx3.init()
BACKEND_VOICE_ENDPOINT = "http://localhost:8000/api/voice/transcript"
USER_ID = "local_user"
WAKE_WORD = "hey assistant"

def speak(text: str):
    TTS.say(text)
    TTS.runAndWait()

def main():
    print("Voice assistant starting. Say 'hey assistant' to wake.")
    while True:
        if VOSK_AVAILABLE:
            text = recognize_from_microphone()
        else:
            # simple blocking input fallback for demo
            text = input("Type simulated transcript (or 'quit'): ")
        if not text:
            continue
        text = text.strip()
        if text.lower() in ("quit", "exit"):
            speak("Goodbye")
            break
        if text.lower().startswith(WAKE_WORD):
            command = text[len(WAKE_WORD):].strip() or input("What can I do? ")
            print("Command:", command)
            resp = requests.post(BACKEND_VOICE_ENDPOINT, json={"user_id": USER_ID, "message": command}).json()
            reply = resp.get("response", "Sorry, no response.")
            print("Assistant:", reply)
            speak(reply)
        else:
            # optional always-on mode: send directly
            resp = requests.post(BACKEND_VOICE_ENDPOINT, json={"user_id": USER_ID, "message": text}).json()
            reply = resp.get("response", "")
            print("Assistant:", reply)
            speak(reply)

if __name__ == "__main__":
    main()
