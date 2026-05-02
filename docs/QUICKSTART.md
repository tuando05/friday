# Quick Start Guide for F.R.I.D.A.Y

For complete setup and development instructions, see [DEVELOPMENT.md](DEVELOPMENT.md).

## TL;DR

```bash
# Setup
git clone <url>
cd friday
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run (in separate terminals)
ollama serve            # Terminal 1
ollama pull phi3:mini   # Terminal 2 (first time only)
python main.py          # Terminal 3
```

Edit `.env` to customize AI_NAME, BOSS_NAME, MODEL_NAME, etc.
