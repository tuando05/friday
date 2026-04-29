import json
import os
from core.config import MEMORY_FILE, MAX_HISTORY


def _ensure_memory_dir():
    if not MEMORY_FILE:
        return
    memory_dir = os.path.dirname(MEMORY_FILE)
    if memory_dir and not os.path.exists(memory_dir):
        os.makedirs(memory_dir, exist_ok=True)

def load_memory():
    if not MEMORY_FILE:
        return []
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_memory(history):
    if not MEMORY_FILE:
        return
    _ensure_memory_dir()
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history[-MAX_HISTORY:], f, ensure_ascii=False, indent=4)

def clear_memory():
    if not MEMORY_FILE:
        return
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)