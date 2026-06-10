import unittest
import os
import shutil
import tempfile
from core.guard import SecurityGuard

class TestSecurityGuard(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.guard = SecurityGuard(data_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_is_safe_path(self):
        # Đường dẫn an toàn nằm trong data_dir
        self.assertTrue(self.guard.is_safe_path("file.txt"))
        self.assertTrue(self.guard.is_safe_path("subdir/file.txt"))
        
        # Đường dẫn không an toàn tìm cách thoát ra ngoài data_dir
        self.assertFalse(self.guard.is_safe_path("../outside.txt"))
        self.assertFalse(self.guard.is_safe_path("/absolute/path/outside"))
        self.assertFalse(self.guard.is_safe_path("subdir/../../outside.txt"))

    def test_list_data_files(self):
        # Mặc định danh sách trống
        self.assertEqual(self.guard.list_DATA_files(), [])
        
        # Tạo thử các tệp
        file1 = os.path.join(self.test_dir, "test1.txt")
        file2 = os.path.join(self.test_dir, "test2.json")
        with open(file1, 'w') as f:
            f.write("hello")
        with open(file2, 'w') as f:
            f.write("{}")
            
        files = self.guard.list_DATA_files()
        self.assertEqual(len(files), 2)
        self.assertIn("test1.txt", files)
        self.assertIn("test2.json", files)

if __name__ == '__main__':
    unittest.main()
