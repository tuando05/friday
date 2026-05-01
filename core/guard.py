import os
from config.settings import DATA_DIR

def is_safe_path(path):
    full_path = os.path.realpath(os.path.join(DATA_DIR, path))
    return full_path.startswith(os.path.realpath(DATA_DIR))

def list_DATA_files():
    files = os.listdir(DATA_DIR)
    return files if files else []