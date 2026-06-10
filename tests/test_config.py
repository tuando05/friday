import unittest
import os
import tempfile
from config import Settings

class TestSettings(unittest.TestCase):
    def test_settings_default_values(self):
        # Thiết lập môi trường tạm để tránh ảnh hưởng bởi file .env thực tế
        old_env = dict(os.environ)
        os.environ.clear()
        try:
            # Chạy Settings với môi trường trống
            settings = Settings(dotenv_path="/nonexistent_file")
            self.assertEqual(settings.MODEL, "phi3:mini")
            self.assertEqual(settings.AI_NAME, "F.R.I.D.A.Y")
            self.assertEqual(settings.BOSS_NAME, "Sir")
            self.assertEqual(settings.MAX_HISTORY, 10)
        finally:
            os.environ.update(old_env)

    def test_settings_custom_values(self):
        # Tạo tệp env tạm
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.env') as f:
            f.write("MODEL_NAME=test-model\n")
            f.write("AI_NAME=Jarvis\n")
            f.write("BOSS_NAME=Tony\n")
            f.write("MAX_HISTORY=5\n")
            f.write("DATA_PATH=./test_data_dir\n")
            env_file = f.name
        
        try:
            settings = Settings(dotenv_path=env_file)
            self.assertEqual(settings.MODEL, "test-model")
            self.assertEqual(settings.AI_NAME, "Jarvis")
            self.assertEqual(settings.BOSS_NAME, "Tony")
            self.assertEqual(settings.MAX_HISTORY, 5)
            self.assertTrue(settings.DATA_DIR.endswith("test_data_dir"))
        finally:
            if os.path.exists(env_file):
                os.remove(env_file)
            # Dọn dẹp thư mục test_data_dir nếu được tạo ra
            test_dir = os.path.abspath("./test_data_dir")
            if os.path.exists(test_dir):
                import shutil
                shutil.rmtree(test_dir, ignore_errors=True)

if __name__ == '__main__':
    unittest.main()
