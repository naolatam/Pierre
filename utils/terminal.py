import logging
import shutil
import os
import subprocess
from typing import Optional, List, Dict


def detect_default_terminal() -> Optional[str]:
    """
    Detect the default terminal on the system.
    
    Returns:
        str: The name of the default terminal binary, or None if none found.
    """
    # Check environment variable
    default_terminal = os.environ.get('TERMINAL')
    if default_terminal and shutil.which(default_terminal):
        return default_terminal
    
    # Check using update-alternatives (Debian/Ubuntu)
    try:
        result = subprocess.run(
            ['update-alternatives', '--query', 'x-terminal-emulator'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Value:'):
                    terminal_path = line.split(':', 1)[1].strip()
                    return os.path.basename(terminal_path)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Check XDG default
    try:
        result = subprocess.run(
            ['xdg-settings', 'get', 'default-terminal-emulator'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0 and result.stdout.strip():
            terminal = result.stdout.strip().replace('.desktop', '')
            if shutil.which(terminal):
                return terminal
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Fallback to first available terminal
    return detect_available_terminal()


def detect_available_terminal() -> Optional[str]:
    """
    Detect which terminal binary is available on the system.
    
    Returns:
        str: The name of the first available terminal binary, or None if none found.
    """
    terminals = [
        'gnome-terminal',
        'tilix',
        'xterm',
        'kitty',
        'konsole',
        'xfce4-terminal',
        'terminator',
        'alacritty',
        'mate-terminal',
        'lxterminal',
        'rxvt',
        'urxvt',
        'st',
    ]
    
    for terminal in terminals:
        if shutil.which(terminal):
            return terminal
    
    return None


def detect_all_available_terminals() -> List[str]:
    """
    Detect all available terminal binaries on the system.
    
    Returns:
        List[str]: A list of all available terminal binaries.
    """
    terminals = [
        'gnome-terminal',
        'konsole',
        'xfce4-terminal',
        'xterm',
        'terminator',
        'alacritty',
        'kitty',
        'tilix',
        'mate-terminal',
        'lxterminal',
        'rxvt',
        'urxvt',
        'st',
    ]
    
    available = []
    for terminal in terminals:
        if shutil.which(terminal):
            available.append(terminal)
    
    return available


def get_terminal_command_template(terminal: str) -> Optional[List[str]]:
    """
    Get the command template for running a command in a specific terminal.
    
    Args:
        terminal: The name of the terminal binary.
    
    Returns:
        List[str]: The command template with '{command}' placeholder, or None if unsupported.
    """
    templates: Dict[str, List[str]] = {
        'gnome-terminal': ['gnome-terminal', '--', 'bash', '-c', '{command}'],
        'kitty': ['kitty', 'bash', '-c', '{command}'],
        'konsole': ['konsole', '-e', 'bash', '-c', '{command}'],
        'xfce4-terminal': ['xfce4-terminal', '-e', 'bash -c "{command}"'],
        'xterm': ['xterm', '-e', 'bash -c "{command}"'],
        'terminator': ['terminator', '-e', 'bash -c "{command}"'],
        'alacritty': ['alacritty', '-e', 'bash', '-c', '{command}'],
        'tilix': ['tilix', '-e', 'bash -c "{command}"'],
        'mate-terminal': ['mate-terminal', '-e', 'bash -c "{command}"'],
        'lxterminal': ['lxterminal', '-e', 'bash -c "{command}"'],
        'rxvt': ['rxvt', '-e', 'bash', '-c', '{command}'],
        'urxvt': ['urxvt', '-e', 'bash', '-c', '{command}'],
        'st': ['st', '-e', 'bash', '-c', '{command}'],
    }
    
    return templates.get(terminal)


def run_command_in_terminal(command: str, terminal: Optional[str] = None, capture_output: bool = False) -> bool:
    """
    Run a command in a new terminal window.
    
    Args:
        command: The command to run.
        terminal: The terminal to use. If None, uses the default terminal.
        capture_output: If True, capture stdout/stderr (only works for background processes)
    
    Returns:
        bool or subprocess.Popen: True if launched successfully, False otherwise.
                                   If capture_output=True, returns the Popen object.
    """
    if terminal is None:
        terminal = detect_default_terminal()
    
    if not terminal:
        print("Error: No terminal found on the system")
        return False
    
    template = get_terminal_command_template(terminal)
    if not template:
        print(f"Error: Terminal '{terminal}' is not supported")
        return False
    
    # Build the command by replacing {command} placeholder
    terminal_cmd = []
    for part in template:
        terminal_cmd.append(part.replace('{command}', command))
    
    try:
        if capture_output:
            # Capture output - useful for background processes
            result = subprocess.Popen(
                terminal_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logging.info(f"Launched command in terminal '{terminal}' with output capture: {command}")
            return result
        else:
            # Normal terminal launch without output capture
            result = subprocess.Popen(terminal_cmd)
            logging.info(f"Launched command in terminal '{terminal}': {command}")
            return result
    except Exception as e:
        print(f"Error launching terminal: {e}")
        logging.error(f"Error launching terminal: {e}")
        return False


def get_process_output(process: subprocess.Popen, timeout: Optional[int] = None) -> Dict[str, str]:
    """
    Get the output from a running process.
    
    Args:
        process: The Popen process object
        timeout: Maximum time to wait for process completion (in seconds)
    
    Returns:
        Dict with 'stdout', 'stderr', and 'returncode' keys
    """
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return {
            'stdout': stdout if stdout else '',
            'stderr': stderr if stderr else '',
            'returncode': process.returncode
        }
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        return {
            'stdout': stdout if stdout else '',
            'stderr': stderr if stderr else '',
            'returncode': -1,
            'error': 'Process timed out'
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': str(e),
            'returncode': -1,
            'error': str(e)
        }


if __name__ == "__main__":
    # Test the functions
    print("=== Terminal Detection ===")
    
    default = detect_default_terminal()
    if default:
        print(f"Default terminal: {default}")
    else:
        print("No default terminal found")
    
    first_available = detect_available_terminal()
    if first_available:
        print(f"First available terminal: {first_available}")
    else:
        print("No terminal found")
    
    all_terminals = detect_all_available_terminals()
    if all_terminals:
        print(f"All available terminals: {', '.join(all_terminals)}")
    else:
        print("No terminals found")
    
    # Test running a command
    print("\n=== Testing Command Execution ===")
    print("Running 'echo Hello from terminal!' in default terminal...")
    success = run_command_in_terminal("echo 'Hello from terminal!' && sleep 2")
    if success:
        print("Command launched successfully")
    else:
        print("Failed to launch command")
