from langchain.tools import tool
import logging
import sys
import os


@tool("exit_pierre", return_direct=False)
def exit_pierre() -> str:
    """
    Exits the AI application.

    Example queries:
    - "Exit Pierre"
    - "Shut down the AI"
    - "Terminate the program"
    """
    logging.info("🔴 Exiting Pierre...")
    sys.exit(0)