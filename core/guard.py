import os

class SecurityGuard:
    def __init__(self, data_dir: str):
        self.data_dir = os.path.realpath(data_dir)

    def is_safe_path(self, path: str) -> bool:
        full_path = os.path.realpath(os.path.join(self.data_dir, path))
        return full_path.startswith(self.data_dir)

    def list_DATA_files(self) -> list:
        if not os.path.exists(self.data_dir):
            return []
        try:
            files = os.listdir(self.data_dir)
            return files if files else []
        except:
            return []