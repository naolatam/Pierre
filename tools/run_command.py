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
def run_command(commands: str, open_terminal: bool = False) -> str:
    """
    Runs commands and captures output. Only opens a terminal window for interactive applications.
    
    Args:
        commands: Commands to run. Can be:
                 - A single command: "ls -la"
                 - Multiple commands on separate lines (each will be executed after the previous)
        open_terminal: Set to True ONLY when launching interactive applications or GUI programs.
                      Default: False (capture output)

    !IMPORTANT - DEFAULT BEHAVIOR:
    By default, this tool CAPTURES OUTPUT and returns it to you.
    This is what you want 99% of the time for:
    - File operations: ls, pwd, find, cat, grep, etc.
    - System info: uname, df, ps, top, etc.
    - Installing packages: pip install, apt install, npm install, etc.
    - Running scripts: python script.py, bash script.sh, etc.
    - Checking status: git status, docker ps, systemctl status, etc.
    
    ONLY set open_terminal=True for:
    - Interactive applications: vim, nano, htop, etc.
    - GUI applications: code, firefox, chrome, etc.
    - Long-running servers when user wants to monitor: python manage.py runserver
    - User explicitly asks to "open terminal" or "show in terminal"
    
    Example workflows:
    ✅ CORRECT - Capture output (default):
    - "Check if file exists" → run_command("test -f file.txt && echo EXISTS")
    - "Install package" → run_command("pip install requests")
    - "Get current directory" → run_command("pwd")
    - "List files" → run_command("ls -la")
    - "Run Python script" → run_command("python script.py")
    
    ❌ WRONG - Don't open terminal for these:
    - "Run ls" → Don't use open_terminal=True
    - "Install numpy" → Don't use open_terminal=True
    - "Execute script.py" → Don't use open_terminal=True
    
    ✅ CORRECT - Open terminal:
    - "Open vim to edit file" → run_command("vim file.txt", open_terminal=True)
    - "Launch VSCode" → run_command("code .", open_terminal=True)
    - "Start server in terminal" → run_command("python server.py", open_terminal=True)
    - User says "open terminal and run X" → use open_terminal=True
    
    Output format when capturing:
    - Returns stdout, stderr, and exit code
    - Perfect for checking results, debugging, or chaining commands
    
    Output format when opening terminal:
    - Opens new terminal window
    - User can see interactive output
    - Output is NOT returned to you
    """
    try:
        # Clean up the command string
        command_input = commands.strip()
        
        if not command_input:
            return "Error: No command provided."

        logger.info(f"Running command(s): {command_input} (open_terminal={open_terminal})")

        if not open_terminal:
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
                       f"The terminal window is now open. You can interact with it there.\n" \
                       f"Note: Output is not captured when opening a terminal window."
            else:
                return "❌ Failed to launch terminal. Make sure a terminal emulator is installed on your system."
            
    except Exception as e:
        error_msg = f"Failed to run command: {str(e)}"
        logger.error(error_msg)
        import traceback
        traceback.print_exc()
        return error_msg
    
