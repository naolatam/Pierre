import logging
import time
from dotenv import load_dotenv

# Importing main classes
from input import InputMethod
from speechToText import SpeechToText, SpeechToTextBadInputError, SpeechToTextError
from ai_manager import AIManager
from tts import speak_text

load_dotenv()

TRIGGER_WORD = "pierre"
CONVERSATION_TIMEOUT = 30  # seconds of inactivity before exiting conversation mode

logging.basicConfig(level=logging.DEBUG)  # logging

# api_key = os.getenv("OPENAI_API_KEY") removed because it's not needed for ollama
# org_id = os.getenv("OPENAI_ORG_ID") removed because it's not needed for ollama

inputTool = InputMethod()
stream = inputTool.getAudioStream() 


# Initialize LLM
ai_manager = AIManager()

conversation_mode = False
last_interaction_time = None
# Main interaction loop
def write():
    while True:
        if inputTool.get_selected_method() == inputTool.MICROPHONE:
            promptUsingAudio()
        elif inputTool.get_selected_method() == inputTool.KEYBOARD:
            promptUsingKeyboard()
def promptUsingAudio():
    global conversation_mode, last_interaction_time

    try:
        if not conversation_mode:
            if SpeechToText().waitForWakeWord(TRIGGER_WORD):
                logging.info(f"🗣 Triggered by wake word: {TRIGGER_WORD}")
                conversation_mode = True
                speak_text("Oui monsieur?")
                last_interaction_time = time.time()
        else:
            logging.info("🎤 Listening for next command...")
            audio = inputTool.getAudioStream().read(32000, exception_on_overflow=False)
            logging.info("🔊 Processing audio...")
            command = SpeechToText().getText(audio)
            if not command:
                logging.info("⚠️ No command detected, continuing...")
                return
            logging.info(f"📥 Command: {command}")
            logging.info("🤖 Sending command to agent...")
            response = ai_manager.get_executor().invoke({"input": command})
            content = response["output"]
            logging.info(f"✅ Agent responded: {content}")
            print("Pierre:", content)
            speak_text(content)
            last_interaction_time = time.time()
            if time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                logging.info("⌛ Timeout: Returning to wake word mode.")
                conversation_mode = False

    except Exception as e:
        logging.critical(f"❌ Critical error in main loop: {e}")

def promptUsingKeyboard():
    try:
        command = inputTool.getCommand()
        logging.info(f"📥 Command: {command}")
        logging.info("🤖 Sending command to agent...")
        response = ai_manager.get_executor().invoke({"input": command})
        content = response["output"]
        logging.info(f"✅ Agent responded: {content}")
        print("Pierre:", content)
    except Exception as e:
        logging.critical(f"❌ Critical error in main loop: {e}")



if __name__ == "__main__":
    inputTool.askForInputMethod()
    if inputTool.get_selected_method() == inputTool.MICROPHONE:
        stt = SpeechToText()
        try:
            stt.loadModel()
        except SpeechToTextBadInputError as e:
            logging.critical(f"❌ {e}")
            exit(1)
    write()


