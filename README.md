# 🧠 Pierre – Local AI Assistant

**Pierre** is an advanced voice-activated and keyboard-controlled conversational AI assistant powered by a local LLM (Qwen via Ollama). Inspired by the "Jarvis" project from [LLM Guys](https://github.com/llm-guys), Pierre extends the concept with enhanced features including multilingual support, hot-reloadable tools, conversation history, and intelligent terminal detection.

Pierre listens for a wake word ("Pierre"), processes spoken or typed commands using a local language model with LangChain, and responds via TTS. It supports dynamic tool-calling for various functions like checking time, taking screenshots, web searches, and more.

---

## 🚀 Features

### Core Features
- 🗣 **Voice-Activated** with wake word **"Pierre"**
- ⌨️ **Keyboard Mode** for text-based interactions
- 🧠 **Local LLM** - Runs Qwen 3 via Ollama (no cloud dependency)
- 🌍 **Multilingual** - Responds in the same language you use (French, English, etc.)
- 💬 **Conversation History** - Remembers context across multiple interactions
- 🔊 **Text-to-Speech** responses via `pyttsx3`

### Advanced Features
- 🔧 **Hot-Reload Tools** - Update tools without restarting the application
- 🛠️ **Dynamic Tool Discovery** - Automatically loads all tools from the `tools/` directory
- 🖥️ **Cross-Platform Terminal Detection** - Intelligently detects and uses the best terminal on your system (Linux, macOS, Windows)
- � **Tool-Calling** with LangChain - Extensible architecture for adding new capabilities
- 🔐 **Privacy-First** - Everything runs locally (optional OpenAI API support available)

### Voice Recognition
- 🎤 **VOSK Speech Recognition** - French model (vosk-model-fr-0.22) for accurate voice detection
- 🎯 **Wake Word Detection** - Only activates when you say "Pierre"
- ⏱️ **Conversation Timeout** - Returns to standby after 30 seconds of inactivity

---

## 📁 Project Structure

```
pierre/
├── main.py                      # Main application entry point
├── ai_manager.py                # Manages LLM agent and executor
├── tool_manager.py              # Hot-reload system for tools
├── input.py                     # Input method handler (keyboard/microphone)
├── speechToText.py              # VOSK speech-to-text implementation
├── test.py                      # Text-to-speech functionality
├── singleton.py                 # Singleton pattern decorator
├── requirements.txt             # Python dependencies
│
├── tools/                       # All tool modules
│   ├── time.py                  # Get local time
│   ├── time_city.py             # Get time in specific cities
│   ├── screenshot.py            # Take screenshots
│   ├── OCR.py                   # Extract text from images
│   ├── duckduckgo.py            # Web search
│   ├── matrix.py                # Matrix-style terminal effect
│   ├── arp_scan.py              # Network device scanning
│   ├── yahoo_finance_news.py    # Fetch financial news
│   ├── reload_tools.py          # Hot-reload tool system
│   ├── switchToAudioMode.py     # Switch to voice input
│   └── switchToKeyboardMode.py  # Switch to keyboard input
│
├── utils/                       # Utility modules
│   ├── terminal.py              # Terminal detection and command execution
│   └── detectTerminal.py        # Cross-platform terminal discovery
│
└── models/                      # VOSK language models
    ├── vosk-model-fr-0.22/      # French voice model
    └── vosk-model-small-en-us-0.15/  # English voice model
```

---

## ⚙️ How It Works

### 1. **Startup & Initialization**
   - Loads environment variables from `.env`
   - Initializes the local Ollama LLM (`qwen3`)
   - Dynamically discovers and loads all tools from `tools/` directory
   - Creates LangChain agent with tool-calling capabilities
   - Sets up conversation history management

### 2. **Input Method Selection**
   - **Keyboard Mode**: Direct text input for immediate conversation
   - **Microphone Mode**: Loads VOSK model and opens audio stream for voice interaction

### 3. **Voice Interaction Flow (Microphone Mode)**
   - Continuously listens for wake word **"Pierre"**
   - When detected, enters "conversation mode"
   - Captures spoken command via microphone
   - Processes audio through VOSK speech-to-text
   - Sends command to LLM agent
   - Agent may invoke tools to fulfill the request
   - Responds via text-to-speech
   - Returns to standby after 30 seconds of inactivity

### 4. **Keyboard Interaction Flow**
   - Waits for text input
   - Sends command directly to LLM agent
   - Agent processes and may use tools
   - Displays response in terminal

### 5. **Tool System**
   - Tools are automatically discovered from `tools/` directory
   - Each tool is a LangChain-compatible function
   - Tools can be hot-reloaded without restarting Pierre
   - Agent intelligently selects and chains tools based on user request

---

## 🛠️ Available Tools

Pierre dynamically loads all tools from the `tools/` directory. Current tools include:

### Time & Date
1. **Get Time (`get_time`)** - Returns current time in local timezone
2. **Get Time by City (`get_time_city`)** - Returns time in specific cities (New York, London, Paris, Tokyo, Sydney)

### System & Utilities
3. **Screenshot (`take_screenshot`)** - Captures the screen
4. **OCR (`read_text_from_latest_image`)** - Extracts text from screenshots using Tesseract
5. **ARP Scan (`arp_scan_terminal`)** - Scans network for connected devices
6. **Matrix Mode (`matrix_mode`)** - Displays Matrix-style terminal animation

### Web & Information
7. **DuckDuckGo Search (`duckduckgo_search_tool`)** - Performs web searches
8. **Yahoo Finance News (`yahoo_finance_news`)** - Fetches latest financial news articles

### Mode Switching
9. **Switch to Audio Mode (`switch_to_audio_mode`)** - Enables voice input
10. **Switch to Keyboard Mode (`switch_to_keyboard_mode`)** - Enables text input

### System Management
11. **Reload Tools (`reload_tools`)** - Hot-reload tools without restarting
    - Usage: "Reload all tools" or "Reload the time tool"

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Ollama with `qwen3` model installed
- Microphone (for voice mode)
- Tesseract OCR (for OCR functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pierre
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Ollama and pull the model**
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull qwen3
   ```

4. **Install Tesseract OCR** (optional, for OCR tool)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   
   # macOS
   brew install tesseract
   
   # Windows
   # Download from https://github.com/UB-Mannheim/tesseract/wiki
   ```

5. **Install yfinance** (for Yahoo Finance tool)
   ```bash
   pip install yfinance
   ```

### Running Pierre

```bash
python main.py
```

You'll be prompted to select an input method:
- **1** for Keyboard mode
- **2** for Microphone mode

---

## � Usage Examples

### Voice Commands (Microphone Mode)
```
You: "Pierre"
Pierre: "Oui monsieur?"
You: "Quelle heure est-il ?"
Pierre: "Il est actuellement 14h30 à Paris."

You: "What time is it in New York?"
Pierre: "The current time in New York is 08:30 AM."

You: "Take a screenshot"
Pierre: "Screenshot saved successfully!"

You: "Search for Python tutorials"
Pierre: [Returns search results from DuckDuckGo]

You: "Reload all tools"
Pierre: "✅ Successfully reloaded all tools!"
```

### Text Commands (Keyboard Mode)
```
You: What's the weather in Paris?
Pierre: [Uses DuckDuckGo to search for weather information]

You: Show me news about Tesla
Pierre: [Fetches latest TSLA news from Yahoo Finance]

You: Activate matrix mode
Pierre: [Opens terminal with Matrix animation]
```

---

## 🔧 Advanced Features

### Hot-Reload System

Pierre includes a sophisticated hot-reload system that allows you to modify tools without restarting:

1. **Edit a tool** in the `tools/` directory
2. **Tell Pierre**: "Reload all tools" or "Reload [tool name]"
3. **Use the updated tool** immediately

The ToolManager automatically:
- Discovers all Python files in `tools/`
- Extracts LangChain-compatible tools
- Tracks which tools belong to which modules
- Supports reload by tool name or module name

### Conversation History

Pierre maintains conversation context across multiple interactions:
- Remembers previous questions and answers
- Can reference earlier parts of the conversation
- Uses LangChain's `RunnableWithMessageHistory`

### Multilingual Support

Pierre automatically detects the language you're using and responds accordingly:
- **French**: "Quelle heure est-il ?" → Responds in French
- **English**: "What time is it?" → Responds in English
- Tool descriptions are in English, but the LLM translates context automatically

### Cross-Platform Terminal Detection

The terminal detection utility (`utils/terminal.py`) intelligently finds the best terminal emulator:
- **Linux**: Supports gnome-terminal, konsole, xterm, alacritty, kitty, and more
- **macOS**: Uses AppleScript for Terminal.app
- **Windows**: Uses cmd.exe with appropriate flags

---

## 🏗️ Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────┐
│                         Main.py                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ InputMethod │  │  AIManager   │  │ ToolManager  │    │
│  │             │  │              │  │              │    │
│  │ - Keyboard  │  │ - LLM Agent  │  │ - Discovery  │    │
│  │ - Microphone│  │ - Executor   │  │ - Hot-Reload │    │
│  │ - Audio     │  │ - History    │  │ - Tool Map   │    │
│  └─────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │    LangChain Agent      │
              │                         │
              │  - Tool Selection       │
              │  - Chain Execution      │
              │  - Context Management   │
              └─────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │    Dynamic Tools        │
              │                         │
              │  Auto-loaded from       │
              │  tools/ directory       │
              └─────────────────────────┘
```

### Key Classes

- **`AIManager`**: Manages LLM, agent creation, and tool integration
- **`ToolManager`**: Handles dynamic tool loading and hot-reloading (Singleton)
- **`InputMethod`**: Manages keyboard and microphone input
- **`SpeechToText`**: VOSK-based speech recognition

---

## 🤝 Contributing

Contributions are welcome! To add a new tool:

1. Create a new Python file in `tools/`
2. Use the `@tool` decorator from LangChain
3. Pierre will automatically discover and load it
4. Test with "Reload all tools"

Example tool:
```python
from langchain.tools import tool

@tool("my_tool", return_direct=False)
def my_tool(param: str) -> str:
    """
    Description of what this tool does.
    
    Args:
        param: Description of parameter
    
    Example queries:
    - "Example user command"
    """
    # Your implementation
    return "Result"
```

---

## 📝 Credits

- **Original Concept**: Inspired by "Jarvis" project from [LLM Guys](https://github.com/llm-guy)
- **LLM**: Qwen 3 via Ollama
- **Speech Recognition**: VOSK
- **Framework**: LangChain
- **TTS**: piper

---

## 🐛 Troubleshooting

### Voice recognition not working
- Ensure VOSK models are downloaded in `models/` directory
- Check microphone permissions
- Verify PyAudio is installed correctly

### Tools not loading
- Run `python tool_manager.py` to test tool discovery
- Check for syntax errors in tool files
- Ensure tools have proper `@tool` decorator

### Ollama connection issues
- Verify Ollama is running: `ollama list`
- Check if `qwen3` model is pulled: `ollama pull qwen3`
- Ensure Ollama is accessible at `http://127.0.0.1:11434`

---

## 🔮 Future Enhancements

- [ ] Multi-language voice model support in progress with a new model_manager
- [ ] Plugin system for community tools
- [ ] Web interface
- [ ] Enhanced context awareness

---


