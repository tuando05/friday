import json
import os

class MemoryManager:
    def __init__(self, memory_file: str, todo_file: str, mode_file: str, max_history: int):
        self.memory_file = memory_file
        self.todo_file = todo_file
        self.mode_file = mode_file
        self.max_history = max_history

    def _ensure_dir(self, file_path):
        if not file_path:
            return
        target_dir = os.path.dirname(file_path)
        if target_dir and not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

    def _read_json(self, file_path, default_value):
        if not file_path:
            return default_value
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default_value
        return default_value

    def _write_json(self, file_path, data):
        if not file_path:
            return
        self._ensure_dir(file_path)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except:
            pass

    def load_memory(self):
        return self._read_json(self.memory_file, [])

    def save_memory(self, history):
        self._write_json(self.memory_file, history[-self.max_history:])

    def clear_memory(self):
        if not self.memory_file:
            return
        if os.path.exists(self.memory_file):
            try:
                os.remove(self.memory_file)
            except:
                pass

    def load_todo(self):
        return self._read_json(self.todo_file, [])

    def save_todo(self, todo_items):
        self._write_json(self.todo_file, todo_items)

    def load_mode(self):
        data = self._read_json(self.mode_file, {})
        if isinstance(data, dict):
            return data.get("mode")
        if isinstance(data, str):
            return data
        return None

    def save_mode(self, mode_name):
        self._write_json(self.mode_file, {"mode": mode_name})