from langchain.tools import tool
import subprocess
import platform
import sys
import os
from utils.terminal import run_command_in_terminal


@tool("arp_scan_terminal", return_direct=True)
def arp_scan_terminal() -> str:
    """
    Runs 'arp -a' in a new Terminal window on macOS, Windows, or Linux.
    Example queries:
    - "Show me the ARP table"
    - "Run arp scan"
    - "Find all devices on my network"
    """
    system = platform.system()

    if system == "Darwin":
        # macOS - use AppleScript
        apple_script = '''
        tell application "Terminal"
            activate
            do script "arp -a"
        end tell
        '''
        subprocess.Popen(["osascript", "-e", apple_script])
        return "Absolutely sir! All devices on your network are now been listed in your Terminal, what else can I help with?."
    
    elif system == "Windows":
        # Windows - use cmd or PowerShell
        try:
            subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", "arp -a"])
            return "Absolutely sir! All devices on your network are now been listed in your Terminal, what else can I help with?."
        except Exception as e:
            return f"⚠️ Failed to open terminal on Windows: {e}"
    
    elif system == "Linux":
        # Linux - use detectTerminal utility
        success = run_command_in_terminal("arp -a")
        if success:
            return "Absolutely sir! All devices on your network are now been listed in your Terminal, what else can I help with?."
        else:
            return "⚠️ Failed to open terminal on Linux. Make sure you have a terminal emulator installed."
    
    else:
        return f"⚠️ arp scan in terminal not implemented for {system}."
