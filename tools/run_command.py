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
def run_command(commands: str, capture_output: bool = False) -> str:
    """
    Runs commands either in a terminal window or captures output directly.
    
    Args:
        commands: Commands to run. Can be:
                 - A single command: "ls -la"
                 - Multiple commands on separate lines (each will be executed after the previous)
        capture_output: If True, runs in background and captures output (no terminal window).
                       If False, opens a new terminal window (output not captured).

    When capture_output=True:
    - Commands run in the background
    - Output (stdout/stderr) is captured and returned
    - No terminal window opens
    
    When capture_output=False (default):
    - Opens a new terminal window
    - You can see and interact with the terminal
    - Output is NOT captured
    

    Example queries:
    - "Run ls -la" - Opens terminal
    - "Run ls -la and capture output" - Runs in background, returns output
    - "Execute python script.py" - Opens terminal
    - "Get output of: pwd" - Captures and returns output
    
    Note: You cannot both open a terminal window AND capture output at the same time.
    """
    try:
        # Clean up the command string
        command_input = commands.strip()
        
        if not command_input:
            return "Error: No command provided."
        
        logger.info(f"Running command(s): {command_input} (capture_output={capture_output})")
        
        if capture_output:
            # Run command directly and capture output (no terminal window)
            try:
                result = subprocess.run(
                    command_input,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                output = f"✅ Command executed successfully\n"
                output += f"Command: {command_input}\n\n"
                
                if result.stdout:
                    output += f"--- STDOUT ---\n{result.stdout}\n"
                if result.stderr:
                    output += f"--- STDERR ---\n{result.stderr}\n"
                    
                output += f"--- EXIT CODE ---\n{result.returncode}\n"
                
                return output
                
            except subprocess.TimeoutExpired:
                return f"⏱️ Command timed out after 30 seconds: {command_input}"
            except Exception as e:
                return f"❌ Failed to execute command: {str(e)}"
        
        else:
            # Open terminal window (output not captured)
            # Split commands by newlines or semicolons to handle multiple commands
            command_lines = []
            for line in command_input.replace(';', '\n').split('\n'):
                line = line.strip()
                if line:
                    command_lines.append(line)
            
            # Build the command script
            if len(command_lines) == 1:
                # Single command - run directly with exec bash to keep terminal open
                final_command = f"{command_lines[0]} ; exec bash"
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
                script_lines.append("echo 'Press Enter to close or continue working...'")
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
            result = terminal.run_command_in_terminal(final_command, capture_output=False)
            
            if result:
                command_preview = command_input[:100] + "..." if len(command_input) > 100 else command_input
                return f"✅ Successfully launched terminal with command(s):\n{command_preview}\n\n" \
                       f"The terminal window is now open. You can see the output there.\n" \
                       f"Note: To capture output, ask me to 'capture output' or 'get output of command'."
            else:
                return "❌ Failed to launch terminal. Make sure a terminal emulator is installed on your system."
            
    except Exception as e:
        error_msg = f"Failed to run command: {str(e)}"
        logger.error(error_msg)
        import traceback
        traceback.print_exc()
        return error_msg
    
