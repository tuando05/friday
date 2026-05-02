import json
import os
from config.settings import MEMORY_FILE, MAX_HISTORY, TODO_FILE, MODE_FILE


def _ensure_dir(file_path):
    if not file_path:
        return
    target_dir = os.path.dirname(file_path)
    if target_dir and not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)


def _read_json(file_path, default_value):
    if not file_path:
        return default_value
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default_value
    return default_value


def _write_json(file_path, data):
    if not file_path:
        return
    _ensure_dir(file_path)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_memory():
    return _read_json(MEMORY_FILE, [])

def save_memory(history):
    _write_json(MEMORY_FILE, history[-MAX_HISTORY:])

def clear_memory():
    if not MEMORY_FILE:
        return
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)


def load_todo():
    return _read_json(TODO_FILE, [])


def save_todo(todo_items):
    _write_json(TODO_FILE, todo_items)


def load_mode():
    data = _read_json(MODE_FILE, {})
    if isinstance(data, dict):
        return data.get("mode")
    if isinstance(data, str):
        return data
    return None


def save_mode(mode_name):
    _write_json(MODE_FILE, {"mode": mode_name})