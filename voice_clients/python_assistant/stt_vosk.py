# voice_clients/python_assistant/stt_vosk.py
# Requires: pip install vosk sounddevice
def recognize_from_microphone():
    try:
        from vosk import Model, KaldiRecognizer
        import sounddevice as sd
        import json
    except Exception:
        raise RuntimeError("VOSK or sounddevice not installed")

    model = Model("voice_clients/python_assistant/vosk-model-small")  # download and place model
    rec = KaldiRecognizer(model, 16000)
    print("Listening (VOSK)... press Ctrl+C to stop")
    def callback(indata, frames, time, status):
        if rec.AcceptWaveform(indata):
            res = json.loads(rec.Result())
            if res.get("text"):
                print("Heard:", res["text"])
                raise KeyboardInterrupt  # stop after first phrase for demo
    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
            sd.sleep(10000)
    except KeyboardInterrupt:
        final = json.loads(rec.FinalResult())
        return final.get("text", "")
    return ""
