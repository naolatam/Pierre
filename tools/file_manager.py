from langchain.tools import tool

@tool("read_file", return_direct=False)
def read_file(filename: str) -> str:
    """
    Reads and returns the contents of a specified file.
    Args:
        filename: The path to the file to read.
    
    !IMPORTANT: Path Validation & Error Recovery Strategy
    
    1. PATH VALIDATION:
       - Use get_os tool first to detect operating system
       - Validate path format matches OS:
         * Linux/macOS: /path/to/file or ~/path/to/file
         * Windows: C:\\path\\to\\file or C:/path/to/file
       - If no path provided (just filename), use run_command with "pwd" to get current directory
    
    2. ERROR RECOVERY (if read_file fails):
       Step 1: Use run_command to check if file exists
               - Linux/macOS: run_command("test -f /path/to/file && echo 'EXISTS' || echo 'NOT_FOUND'")
               - Windows: run_command("if exist C:\\path\\file (echo EXISTS) else (echo NOT_FOUND)")
       
       Step 2: If file not found, try to locate it
               - Linux/macOS: run_command("find . -name 'filename' -type f")
               - Windows: run_command("dir /s /b filename")
       
       Step 3: If relative path was provided, resolve absolute path
               - Use run_command with "pwd" to get current directory
               - Construct full path: current_dir + "/" + filename
               - Retry read_file with absolute path
       
       Step 4: If file still not found, list directory contents
               - run_command("ls -la /parent/directory") on Linux/macOS
               - run_command("dir /a /b C:\\parent\\directory") on Windows
               - Help user identify correct filename (case sensitivity, extensions)
    
    3. COMMON ERROR PATTERNS:
       - "No such file or directory" → File doesn't exist, run find/locate
       - "Permission denied" → Use run_command("ls -l filepath") to check permissions
       - "Is a directory" → User provided directory instead of file
       - Encoding errors → Try different encodings or check if file is binary

    Example queries:
    - "Read the contents of /path/to/file.txt"
    - "Open and display the file /etc/hosts"
    - "Show me what's inside C:\\Users\\Name\\document.docx"
    - "Read config.json" (no path provided)

    Agent workflow:
    1. Get OS using get_os tool
    2. Validate path format matches OS
    3. If no directory in path, use run_command("pwd") to get current directory
    4. Call read_file with validated/constructed path
    5. If error occurs:
       a. Use run_command to verify file exists
       b. Try to locate file if not found
       c. Resolve relative paths to absolute
       d. List directory contents to help user
       e. Retry with corrected path
    """

    try:
        with open(filename, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"
