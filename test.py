"""import json
import vosk
import pyaudio

model = vosk.Model("models/vosk-model-small-en-us-0.15")
rec = vosk.KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                input=True, frames_per_buffer=4000)
stream.start_stream()

print("🎙️ Speak now...")

while True:
    data = stream.read(4000, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        print("You said:", result.get("text", ""))
"""

import pyttsx3
import time
import logging

def speak_text(text: str):
    

