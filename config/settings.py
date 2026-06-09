import os
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL_NAME")
AI_NAME = os.getenv("AI_NAME")
BOSS_NAME = os.getenv("BOSS_NAME")
DATA_DIR = os.path.abspath(os.getenv("DATA_PATH"))
MEMORY_FILE = os.path.join(DATA_DIR, os.getenv("MEMORY_FILE"))
TODO_FILE = os.path.join(DATA_DIR, os.getenv("TODO_FILE", "todo.json"))
MODE_FILE = os.path.join(DATA_DIR, os.getenv("MODE_FILE", "mode.json"))
MAX_HISTORY = int(os.getenv("MAX_HISTORY"))

VOICE_ENABLED = os.getenv("VOICE_ENABLED", "false").lower() == "true"
VOICE_WAKE_WORD = os.getenv("VOICE_WAKE_WORD", "hey_jarvis")
VOICE_SAMPLE_RATE = int(os.getenv("VOICE_SAMPLE_RATE", "16000"))
VOICE_FRAME_MS = int(os.getenv("VOICE_FRAME_MS", "20"))
VOICE_WAKE_THRESHOLD = float(os.getenv("VOICE_WAKE_THRESHOLD", "0.4"))
VOICE_SILENCE_MS = int(os.getenv("VOICE_SILENCE_MS", "800"))
VOICE_MAX_RECORD_MS = int(os.getenv("VOICE_MAX_RECORD_MS", "8000"))
VOICE_VAD_AGGRESSIVENESS = int(os.getenv("VOICE_VAD_AGGRESSIVENESS", "2"))
_voice_device = os.getenv("VOICE_DEVICE")
if _voice_device and _voice_device.strip():
    try:
        VOICE_DEVICE = int(_voice_device)
    except ValueError:
        VOICE_DEVICE = _voice_device
else:
    VOICE_DEVICE = None
VOICE_ASR_MODEL = os.getenv("VOICE_ASR_MODEL")

TTS_ENABLED = os.getenv("TTS_ENABLED", "false").lower() == "true"
TTS_RATE = int(os.getenv("TTS_RATE", "175"))
TTS_VOLUME = float(os.getenv("TTS_VOLUME", "1.0"))
TTS_VOICE_ID = os.getenv("TTS_VOICE_ID")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
