import os
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL_NAME", "phi3.5")
AI_NAME = os.getenv("AI_NAME", "F.R.I.D.A.Y")
BOSS_NAME = os.getenv("BOSS_NAME", "Boss")
DATA_DIR = os.path.abspath(os.getenv("DATA_PATH", "./data"))
MEMORY_FILE = os.path.join(DATA_DIR, os.getenv("MEMORY_FILE", "memory.json"))
MAX_HISTORY = int(os.getenv("MAX_HISTORY", 10))

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)