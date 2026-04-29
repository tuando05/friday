import json
import os
from core.config import MEMORY_FILE, MAX_HISTORY

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return []
    return []

def save_memory(history):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history[-MAX_HISTORY:], f, ensure_ascii=False, indent=4)

def clear_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)