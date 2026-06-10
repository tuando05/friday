import unittest
import os
import shutil
import tempfile
from core.memory import MemoryManager

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        # Tạo thư mục tạm để lưu file test
        self.test_dir = tempfile.mkdtemp()
        self.memory_file = os.path.join(self.test_dir, "memory.json")
        self.todo_file = os.path.join(self.test_dir, "todo.json")
        self.mode_file = os.path.join(self.test_dir, "mode.json")
        
        self.memory_manager = MemoryManager(
            memory_file=self.memory_file,
            todo_file=self.todo_file,
            mode_file=self.mode_file,
            max_history=3
        )

    def tearDown(self):
        # Xóa thư mục tạm sau khi test xong
        shutil.rmtree(self.test_dir)

    def test_memory_load_save(self):
        # Mặc định bộ nhớ rỗng
        self.assertEqual(self.memory_manager.load_memory(), [])
        
        # Lưu hội thoại dài hơn max_history (4 item, max là 3)
        history = [
            {'role': 'user', 'content': 'hello'},
            {'role': 'assistant', 'content': 'hi'},
            {'role': 'user', 'content': 'how are you'},
            {'role': 'assistant', 'content': 'fine'}
        ]
        self.memory_manager.save_memory(history)
        
        # Kiểm tra chỉ lưu 3 item cuối cùng
        saved = self.memory_manager.load_memory()
        self.assertEqual(len(saved), 3)
        self.assertEqual(saved[0]['content'], 'hi')
        self.assertEqual(saved[2]['content'], 'fine')

    def test_memory_clear(self):
        history = [{'role': 'user', 'content': 'hello'}]
        self.memory_manager.save_memory(history)
        self.assertTrue(os.path.exists(self.memory_file))
        
        self.memory_manager.clear_memory()
        self.assertEqual(self.memory_manager.load_memory(), [])
        self.assertFalse(os.path.exists(self.memory_file))

    def test_todo_load_save(self):
        self.assertEqual(self.memory_manager.load_todo(), [])
        
        todos = ["Viết unit test", "Chạy thử CLI"]
        self.memory_manager.save_todo(todos)
        
        self.assertEqual(self.memory_manager.load_todo(), todos)

    def test_mode_load_save(self):
        self.assertIsNone(self.memory_manager.load_mode())
        
        self.memory_manager.save_mode("think")
        self.assertEqual(self.memory_manager.load_mode(), "think")

if __name__ == '__main__':
    unittest.main()
