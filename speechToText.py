import logging
import time
import vosk
from singleton import singleton
from input import InputMethod
from model_manager import ModelManager as Model
import json

@singleton
class SpeechToText:
    def __init__(self, model_path='models/vosk/vosk-model-fr-0.22'):
        self.input_method = InputMethod()
        self.__model_path = Model().get_model_vosk()
        self.__loaded = False
        self.model = None
        self.rec = None

    def loadModel(self):
        if self.__loaded:
            return
        if not self.input_method.getAudioStream():
            raise SpeechToTextBadInputError("Audio stream not initialized. Please select microphone as input method.")
        self.model = vosk.Model(self.__model_path)
        self.rec = vosk.KaldiRecognizer(self.model, 16000)
        self.__loaded = True
        logging.info("✅ Speech-to-Text model loaded successfully.")

    def getRecognizer(self):
        return self.rec
    
    def isLoaded(self):
        return self.__loaded
    
    def getText(self, audio_data: bytes) -> str:
        if not self.__loaded:
            raise SpeechToTextError("Model not loaded. Call loadModel() before getText().")
        if self.rec.AcceptWaveform(audio_data):
            result = self.rec.Result()
            text = json.loads(result).get("text", "")
            return text
        else:
            return ""

    def waitForWakeWord(self, wake_word: str, timeout: float = 10) -> bool:
        logging.info("🎤 Listening for wake word...")
        if not self.__loaded:
            raise SpeechToTextError("Model not loaded. Call loadModel() before waitForWakeWord().")
        startTime = time.time()
        while True:
            if time.time() - startTime > timeout:
                return False
            audio_data = self.input_method.getAudioStream().read(16000, exception_on_overflow=False)
            text = self.getText(audio_data)
            if wake_word.lower() in text.lower():
                return True

    

class SpeechToTextError(Exception):
    pass

class SpeechToTextBadInputError(SpeechToTextError):
    pass