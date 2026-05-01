# F.R.I.D.A.Y - AI Personal Assistant

## Overview
F.R.I.D.A.Y is a modular AI assistant built with Python that provides an interactive conversational experience. The system uses local AI models (via Ollama) to generate responses while maintaining conversation history and memory.

## Features
- 🤖 **Local AI Integration** - Uses Ollama for running language models locally
- 💾 **Persistent Memory** - Automatically saves and loads conversation history
- 🔒 **File Management** - Vault system for secure file handling
- 🎯 **Modular Architecture** - Clean separation of concerns with configurable components
- 📝 **Vietnamese Support** - Full Vietnamese language support in UI and prompts

## Project Structure
```
friday/
├── main.py              # Entry point for the application
├── README.md            # Project documentation
├── .env                 # Environment variables
├── config/              # Configuration files
├── core/                # Core modules
│   ├── __init__.py
│   ├── brain.py         # AI response generation
│   ├── config.py        # Configuration management
│   ├── guard.py         # File vault management
│   ├── memory.py        # Conversation memory handling
│   └── sysPromt.txt     # System prompt template
├── data/                # Data storage directory
├── skill/               # Additional skills/abilities
└── venv/                # Python virtual environment
```

## Requirements
- Python 3.8+
- Ollama (for running local LLMs)
- Dependencies listed in requirements.txt

## Installation

### Prerequisites
- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Ollama** - [Download Ollama](https://ollama.ai/)
- **Git** - For cloning the repository

### Step-by-Step Installation

#### 1. Clone the repository

**Linux/Mac:**
```bash
git clone <repository-url>
cd friday
```

**Windows (Command Prompt or PowerShell):**
```cmd
git clone <repository-url>
cd friday
```

#### 2. Create and activate virtual environment

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

> ⚠️ **Note for Windows PowerShell:** If you get an execution policy error, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

#### 3. Install dependencies

**Linux/Mac/Windows (same for all):**
```bash
pip install -r requirements.txt
```

#### 4. Configure environment

- Copy `.env.example` to `.env` (if available):
  - **Linux/Mac:** `cp .env.example .env`
  - **Windows:** `copy .env.example .env`
- Update configuration values as needed in `.env`

### Setting up Ollama

1. **Install Ollama**
   - Download from [ollama.ai](https://ollama.ai/)
   - Follow the installation instructions for your OS

2. **Start Ollama**
   - **Linux/Mac:** Run `ollama serve` in a terminal
   - **Windows:** Ollama typically runs as a background service after installation

3. **Pull a model** (e.g., mistral):
   ```bash
   ollama pull mistral
   ```

### Troubleshooting Installation

**Python not found on Windows:**
- Make sure Python is installed and added to PATH
- Try `python --version` or `py --version`

**Virtual environment activation fails on Windows:**
- Check that PowerShell execution policy allows script execution
- Use Command Prompt instead: `venv\Scripts\activate`

**Ollama connection error:**
- Ensure Ollama service is running on your system
- Check that Ollama is listening on `http://localhost:11434` (default)

## Usage

### Starting the application

**Activate virtual environment first:**

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

Then run the application:

**All platforms:**
```bash
python main.py
```

### Interactive Commands

Once the application is running, you can use these commands:

| Command | Purpose |
|---------|---------|
| `exit` | Exit the application |
| `nghỉ ngơi đi` | Exit the application (Vietnamese) |
| `xóa trí nhớ` | Clear conversation memory |
| `kiểm tra file` | List files in the vault |

### Example Session

```
--- F.R.I.D.A.Y Mark 1 Modular Online ---

Your Name: Hello F.R.I.D.A.Y
F.R.I.D.A.Y: Hello! How can I assist you today?

Your Name: What's the current time?
F.R.I.D.A.Y: The current time is 14:30 - 29/04/2026

Your Name: xóa trí nhớ
F.R.I.D.A.Y: Trí nhớ đã được dọn dẹp.

Your Name: exit
F.R.I.D.A.Y: Hệ thống ngoại tuyến. Chào Your Name.
```

### Deactivate Virtual Environment

When you're done, deactivate the virtual environment:

**All platforms:**
```bash
deactivate
```

## Configuration

Key configuration variables (in `core/config.py`):
- `AI_NAME` - Name of the AI assistant
- `BOSS_NAME` - Name of the user
- `MODEL` - Ollama model to use (default: "mistral")
- `DATA_DIR` - Working directory for the AI

## Core Modules

### brain.py
Handles AI response generation using Ollama. Processes user input with conversation history and system prompts.

### memory.py
Manages conversation history persistence, loading and saving chat records.

### guard.py
Manages file vault operations for secure file handling.

### config.py
Centralized configuration management for the application.

## Dependencies
- `ollama` - Local language model interface
- Other dependencies in `requirements.txt`

## Notes
- Ensure Ollama is installed and running before starting the application
- The system maintains conversation context for more natural interactions
- All conversations are saved to persistent storage for continuity

## Future Enhancements
- Additional skills and abilities
- Web interface
- Multi-user support
- Advanced memory management

## License
MIT License - See LICENSE file for details

## Contact
For questions, issues, or suggestions, please open an issue in the repository.

## Changelog
See [CHANGELOG.md](CHANGELOG.md) for version history and updates.
