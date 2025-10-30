# tools/time_tool.py

from langchain.tools import tool
from datetime import datetime
import time

@tool("get_time", return_direct=False)
def get_time( ) -> str:
    """Returns the local time
    """
    try:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time} in local timezone."
    except Exception as e:
        return f"Error: {e}"
