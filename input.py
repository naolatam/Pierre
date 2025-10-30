import pyaudio
import logging
import aslaNoOutPut
from singleton import singleton


logging.basicConfig(level=logging.INFO)


@singleton
class InputMethod:
    
    KEYBOARD = 'keyboard'
    MICROPHONE = 'microphone'

    def __init__(self, selected_method=None):
        self.__selected_method = selected_method
        self.pAudio = pyaudio.PyAudio()
        self.audioStream = None
        if self.__selected_method == self.MICROPHONE:
            self._initialize_microphone()

    def _initialize_microphone(self):
        logging.info("Initializing microphone...")
        self.audioStream = self.pAudio.open(
            format=pyaudio.paInt16, 
            channels=1, 
            rate=16000,
            input=True, 
            frames_per_buffer=4000,
            output=False
        )
        self.audioStream.start_stream()

    def get_selected_method(self):
        return self.__selected_method
    def set_selected_method(self, method):
        logging.info(f"Setting input method to: {method}")
        if method in [self.KEYBOARD, self.MICROPHONE]:
            self.__selected_method = method
            if method == self.MICROPHONE and self.audioStream is None:
                self._initialize_microphone()
        else:
            raise ValueError("Invalid input method selected.")
    def getAudioStream(self):
        if self.__selected_method == self.MICROPHONE:
            return self.audioStream
        else:
            return None

    def getCommand(self):
        if self.__selected_method == self.KEYBOARD:
            command = input("You: ")
            return command
        else:
            return None

    def closeAudioStream(self):
        if self.audioStream:
            self.audioStream.stop_stream()
            self.audioStream.close()
        self.pAudio.terminate()

    def askForInputMethod(self):
        print("Select input method:")
        print("1. Keyboard")
        print("2. Microphone")
        choice = input("Enter choice (1 or 2): ")
        if choice == '1':
            self.__selected_method = self.KEYBOARD
        elif choice == '2':
            self.__selected_method = self.MICROPHONE
            self._initialize_microphone()
        else:
            print("Invalid choice, defaulting to Keyboard.")
            self.__selected_method = self.KEYBOARD



