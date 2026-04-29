# Quick Start Guide for F.R.I.D.A.Y

## Quick Setup (Linux/Mac)
```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start Ollama (in another terminal)
ollama serve

# 4. Pull model (if not already installed)
ollama pull phi3:mini

# 5. Run the application
python main.py
```

## Quick Setup (Windows)
```cmd
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start Ollama
# Ollama should be running as a service (or run: ollama serve)

# 4. Pull model (if not already installed)
ollama pull phi3:mini

# 5. Run the application
python main.py
```

## Configuration
- Copy `.env.example` to `.env`
- Edit `.env` with your preferences:
  - Change `AI_NAME` to your preferred assistant name
  - Change `BOSS_NAME` to your name
  - Change `MODEL_NAME` to use different Ollama model
  - Update `OLLAMA_HOST` if not using localhost

## Available Models
Popular Ollama models you can use:
- `phi3:mini` - Lightweight, fast (default)
- `mistral` - Good balance of speed and quality
- `llama2` - Powerful but slower
- `neural-chat` - Optimized for conversations
- `orca-mini` - Good for reasoning

To use a different model:
```bash
ollama pull mistral
# Then update MODEL_NAME=mistral in .env
```

## Troubleshooting

**"Ollama not found" error:**
- Start Ollama service: `ollama serve`
- Check OLLAMA_HOST in .env is correct

**"Model not found" error:**
- Pull the model: `ollama pull phi3:mini`
- Check MODEL_NAME in .env matches pulled model

**Permission error on Linux:**
- Run with Python: `python3 main.py`
- Check the script has correct permissions

## Need Help?
See README.md for full documentation
