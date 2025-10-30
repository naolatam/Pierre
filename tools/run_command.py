from langchain.tools import tool
import subprocess
import platform
import tempfile
import sys
import os
import shutil
import logging

# Add parent directory to path for import
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils import terminal

logger = logging.getLogger(__name__)


@tool("run_command", return_direct=False)
def run_command(commands: str) -> str:
    """
    Opens a new terminal window and runs commands interactively.
    
    Args:
        commands: Commands to run. Can be:
                 - A single command: "ls -la"
                 - Multiple commands on separate lines (each will be executed after the previous)
                 - Commands that need shell restart (like conda init) will open an interactive shell
    
    This tool is smart about command execution:
    - For sequential commands, it creates a script that runs them one by one
    - The terminal stays open for you to continue working

    Example queries:
    - "Run ls -la"
    - "Run npm install"
    - "Open terminal and run conda activate myenv"
    - "Run python script.py"
    - "Execute: cd /tmp\nls\npwd" (multiple commands)
    
    Special handling for:
    - Interactive shells: Keeps terminal open after commands
    - All sensitive command are forbidden. But no list was defined, so you should estimate if they can harm the system.
    """
    try:
        # Clean up the command string
        command_input = commands.strip()
        
        if not command_input:
            return "Error: No command provided."
        
        logger.info(f"Running command(s) in terminal: {command_input}")
        
        # Split commands by newlines or semicolons to handle multiple commands
        command_lines = []
        for line in command_input.replace(';', '\n').split('\n'):
            line = line.strip()
            if line:
                command_lines.append(line)
        
        # Build the command script
        if len(command_lines) == 1:
            # Single command - run directly
            final_command = command_lines[0]
        else:
            # Multiple commands - create a script
            script_lines = []
            script_lines.append("#!/bin/bash")
            script_lines.append("set -e")  # Exit on error
            
            # Add each command
            for cmd in command_lines:
                script_lines.append(f"echo '▶ Running: {cmd}'")
                script_lines.append(cmd)
            
            # Keep terminal open
            script_lines.append("echo ''")
            script_lines.append("echo '✅ All commands completed.'")
            script_lines.append("echo 'Press any key to close or continue working...'")
            script_lines.append("exec bash")
            
            # Create a temporary script file
            script_content = '\n'.join(script_lines)
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
                f.write(script_content)
                script_path = f.name
            
            # Make it executable
            os.chmod(script_path, 0o755)
            
            final_command = f"bash {script_path}"
        
        # Run the command in a new terminal window
        result = terminal.run_command_in_terminal(final_command)
        
        if result:
            command_preview = command_input[:100] + "..." if len(command_input) > 100 else command_input
            return f"✅ Successfully launched terminal with command(s):\n{command_preview}\n\nThe terminal window is now open. You can continue working there."
        else:
            return "❌ Failed to launch terminal. Make sure a terminal emulator is installed on your system."
            
    except Exception as e:
        error_msg = f"Failed to run command: {str(e)}"
        logger.error(error_msg)
        import traceback
        traceback.print_exc()
        return error_msg
    
