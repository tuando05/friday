import os
from dotenv import load_dotenv

class Settings:
    def __init__(self, dotenv_path=None):
        load_dotenv(dotenv_path)

        self.MODEL = os.getenv("MODEL_NAME", "phi3:mini")
        self.AI_NAME = os.getenv("AI_NAME", "F.R.I.D.A.Y")
        self.BOSS_NAME = os.getenv("BOSS_NAME", "Sir")
        
        data_path = os.getenv("DATA_PATH", "./data")
        self.DATA_DIR = os.path.abspath(data_path)
        
        if not os.path.exists(self.DATA_DIR):
            os.makedirs(self.DATA_DIR, exist_ok=True)

        self.MEMORY_FILE = os.path.join(self.DATA_DIR, os.getenv("MEMORY_FILE", "memory.json"))
        self.TODO_FILE = os.path.join(self.DATA_DIR, os.getenv("TODO_FILE", "todo.json"))
        self.MODE_FILE = os.path.join(self.DATA_DIR, os.getenv("MODE_FILE", "mode.json"))
        
        self.MAX_HISTORY = int(os.getenv("MAX_HISTORY", "10"))

        self.VOICE_ENABLED = os.getenv("VOICE_ENABLED", "false").lower() == "true"
        self.VOICE_WAKE_WORD = os.getenv("VOICE_WAKE_WORD", "hey_jarvis")
        self.VOICE_SAMPLE_RATE = int(os.getenv("VOICE_SAMPLE_RATE", "16000"))
        self.VOICE_FRAME_MS = int(os.getenv("VOICE_FRAME_MS", "20"))
        self.VOICE_WAKE_THRESHOLD = float(os.getenv("VOICE_WAKE_THRESHOLD", "0.4"))
        self.VOICE_SILENCE_MS = int(os.getenv("VOICE_SILENCE_MS", "800"))
        self.VOICE_MAX_RECORD_MS = int(os.getenv("VOICE_MAX_RECORD_MS", "8000"))
        self.VOICE_VAD_AGGRESSIVENESS = int(os.getenv("VOICE_VAD_AGGRESSIVENESS", "2"))
        
        _voice_device = os.getenv("VOICE_DEVICE")
        if _voice_device and _voice_device.strip():
            try:
                self.VOICE_DEVICE = int(_voice_device)
            except ValueError:
                self.VOICE_DEVICE = _voice_device
        else:
            self.VOICE_DEVICE = None
        
        self.VOICE_ASR_MODEL = os.getenv("VOICE_ASR_MODEL")

        self.TTS_ENABLED = os.getenv("TTS_ENABLED", "false").lower() == "true"
        self.TTS_RATE = int(os.getenv("TTS_RATE", "175"))
        self.TTS_VOLUME = float(os.getenv("TTS_VOLUME", "1.0"))
        self.TTS_VOICE_ID = os.getenv("TTS_VOICE_ID")

