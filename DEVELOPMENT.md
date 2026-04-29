# Development Guide for F.R.I.D.A.Y

## Project Structure

```
friday/
├── main.py                 # Main entry point
├── README.md               # Full documentation
├── QUICKSTART.md           # Quick setup guide  
├── DEVELOPMENT.md          # This file
├── requirements.txt        # Python dependencies
├── .env                    # Configuration (local, not committed)
├── .env.example            # Configuration template
├── .env.documentation      # Environment variable docs
├── .gitignore              # Git ignore rules
├── core/                   # Core application modules
│   ├── __init__.py
│   ├── brain.py            # AI response generation
│   ├── config.py           # Configuration loading
│   ├── guard.py            # File management
│   ├── memory.py           # Conversation memory
│   └── sysPromt.txt        # System prompt template
├── config/                 # Configuration files (for future use)
│   └── __init__.py
├── skill/                  # Custom skills/abilities (for future use)
│   └── __init__.py
├── data/                   # Data storage (created at runtime, git-ignored)
│   └── memory.json         # Conversation history
└── venv/                   # Virtual environment (git-ignored)
```

## Setting Up Development Environment

### 1. Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd friday

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy .env example to .env
cp .env.example .env
```

### 2. Start Ollama
```bash
# In another terminal
ollama serve

# In another terminal, pull a model if not already installed
ollama pull phi3:mini
```

### 3. Run the Application
```bash
# Make sure venv is activated
python main.py
```

## Code Architecture

### Core Modules

#### config.py
- Loads environment variables from `.env`
- Provides centralized configuration access
- Ensures DATA_DIR exists

**Key exports:**
- `MODEL`, `AI_NAME`, `BOSS_NAME`, `DATA_DIR`
- `MEMORY_FILE`, `MAX_HISTORY`

#### brain.py
- Handles communication with Ollama
- Generates AI responses based on user input
- Maintains system prompt context

**Key function:**
- `generate_response(user_input, history)` - Returns AI response

#### memory.py
- Saves/loads conversation history
- Manages JSON-based persistent memory
- Limits history size based on `MAX_HISTORY`

**Key functions:**
- `load_memory()` - Load saved conversations
- `save_memory(history)` - Save current conversation
- `clear_memory()` - Clear all history

#### guard.py
- Manages file operations in DATA_DIR
- Ensures files stay within sandbox
- Lists available files

**Key functions:**
- `is_safe_path(path)` - Check if path is safe
- `list_DATA_files()` - List files in DATA_DIR

### Main Application Flow

```
main.py
├── Load config from .env
├── Initialize memory
└── Loop:
    ├── Read user input
    ├── Check for special commands (exit, clear memory, etc)
    ├── Send to brain.generate_response()
    ├── Save response to memory
    └── Display response
```

## Adding Features

### Adding a New Skill

1. Create a file in `skill/` directory:
```python
# skill/my_skill.py
def my_skill_function(param):
    """Description of what this skill does"""
    return result
```

2. Import and use in main.py:
```python
from skill.my_skill import my_skill_function

# In the command processing section
if "my_command" in cmd.lower():
    result = my_skill_function(cmd)
    print(result)
```

### Adding a New Configuration Value

1. Add to `.env.example`:
```
NEW_VAR=value
```

2. Add to `.env` (your local copy)

3. Load in `core/config.py`:
```python
NEW_VAR = os.getenv("NEW_VAR", "default_value")
```

4. Use throughout the app:
```python
from core.config import NEW_VAR
```

### Modifying the System Prompt

Edit `core/sysPromt.txt` to customize the AI's behavior and personality.

## Testing

Currently, there are no automated tests. To manually test:

1. Run the application
2. Test various inputs
3. Verify memory is saved correctly
4. Test special commands

Future improvements could include:
- Unit tests for each module
- Integration tests for bot responses
- Memory persistence tests

## Debugging

### Enable verbose output (optional modification)

Add debug prints in key functions:
```python
# In brain.py
def generate_response(user_input, history):
    print(f"DEBUG: Input = {user_input}")
    print(f"DEBUG: History size = {len(history)}")
    # ... rest of function
```

### Check logs and files

```bash
# View memory file
cat data/memory.json | python -m json.tool

# Check config values
python -c "from core import config; print(config.__dict__)"
```

## Common Issues and Solutions

### Model not responding
- Check Ollama is running: `ollama serve`
- Check model is installed: `ollama list`
- Check OLLAMA_HOST in .env

### Memory not saving
- Check data/ directory exists and is writable
- Check DATA_PATH in .env is correct
- Check file permissions

### Dependencies not found
- Reinstall: `pip install -r requirements.txt`
- Check venv is activated
- Try: `pip install --upgrade pip`

## Code Standards

- Use clear, descriptive variable names
- Add docstrings to functions
- Comment complex logic
- Use type hints where possible
- Keep functions focused and small
- Handle exceptions gracefully

## Git Workflow

1. Create a branch for your feature: `git checkout -b feature/my-feature`
2. Make changes and test thoroughly
3. Commit with clear messages: `git commit -m "Add feature X"`
4. Push to repository: `git push origin feature/my-feature`
5. Create a pull request

### Files to NOT commit
- `.env` (use `.env.example` template)
- `venv/` (virtual environment)
- `data/` (user data and memory)
- `__pycache__/` (Python cache)
- `.vscode/` settings (local editor config)

## Performance Optimization

### Tips
- Use `phi3:mini` for faster responses
- Reduce `MAX_HISTORY` for faster processing
- Cache frequently accessed data if needed
- Profile code if it becomes slow

## Future Development Ideas

- [ ] Web interface (Flask/FastAPI)
- [ ] Multi-user support
- [ ] Database instead of JSON
- [ ] Advanced caching
- [ ] Custom skill plugins
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Admin dashboard
- [ ] API interface
- [ ] Unit tests

## Questions or Issues?

1. Check documentation in README.md
2. Check .env.documentation for config issues
3. Review code comments in relevant modules
4. Test with different configurations

---

**Happy developing!** 🚀
