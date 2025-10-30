from langchain.tools import tool
import utils.terminal as terminal
from input import InputMethod
from speechToText import SpeechToText
@tool("switch_to_audio_mode", return_direct=False)
def switch_to_audio_mode() -> str:
    """
    Switch the interaction with IA mode to use audio input and output.
    Use this tool when the user says something like:
    - "Use microphone instead of keyboard"
    - "Switch to audio mode"
    - "Enable audio interaction"
    """
    try:
        input_tool = InputMethod()
        input_tool.set_selected_method(input_tool.MICROPHONE)
        if(not SpeechToText().isLoaded()):
            SpeechToText().loadModel()

        return "Audio mode activated. I am now listening via the microphone."
    except Exception as e:
        return f"Error switching to audio mode: {e}"
    
