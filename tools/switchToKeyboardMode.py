from langchain.tools import tool
from input import InputMethod
import logging
@tool("switch_to_keyboard_mode", return_direct=False)
def switch_to_keyboard_mode() -> str:
    """
    Switch the interaction with IA mode to use keyboard input and output.
    Use this tool when the user says something like:
    - "Use keyboard instead of audio"
    - "Switch to keyboard mode"
    - "Enable keyboard interaction"
    """
    try:
        input_tool = InputMethod()
        input_tool.set_selected_method(input_tool.KEYBOARD)

        return "Keyboard mode activated. I am now listening via the keyboard."
    except Exception as e:
        return f"Error switching to keyboard mode: {e}"

