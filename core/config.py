import os
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL_NAME")
AI_NAME = os.getenv("AI_NAME")
BOSS_NAME = os.getenv("BOSS_NAME")
DATA_DIR = os.path.abspath(os.getenv("DATA_PATH"))
MEMORY_FILE = os.path.join(DATA_DIR, os.getenv("MEMORY_FILE"))
MAX_HISTORY = int(os.getenv("MAX_HISTORY"))

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)