import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import shutil
from config import Settings
from core.memory import MemoryManager
from core.brain import Brain
from tools import ToolManager

class TestBrain(unittest.TestCase):
    def setUp(self):
        # Tạo thư mục và tệp tạm
        self.test_dir = tempfile.mkdtemp()
        self.prompt_file = os.path.join(self.test_dir, "sysPromt.txt")
        with open(self.prompt_file, 'w', encoding='utf-8') as f:
            # Viết prompt mẫu
            f.write("System Prompt {AI_NAME} {BOSS_NAME} {DATA_DIR} {TOOLS_DESCRIPTION}")
            
        # Mock Config
        self.config = MagicMock()
        self.config.MODEL = "mock-model"
        self.config.AI_NAME = "Jarvis"
        self.config.BOSS_NAME = "Boss"
        self.config.DATA_DIR = self.test_dir
        
        # Mock MemoryManager
        self.memory_manager = MagicMock(spec=MemoryManager)
        self.memory_manager.load_memory.return_value = []
        
        # Mock ToolManager
        self.tool_manager = MagicMock(spec=ToolManager)
        self.tool_manager.get_tools_prompt.return_value = "Tool prompt"
        self.tool_manager.parse_tool_calls.side_effect = [
            [("mock_tool", {"param": 123})],  # Bước 1: Gọi tool
            []                              # Bước 2: Không gọi tool nữa
        ]
        self.tool_manager.execute_tool.return_value = "Tool response: success"
        
        # Khởi tạo Brain
        self.brain = Brain(
            config=self.config,
            memory_manager=self.memory_manager,
            tool_manager=self.tool_manager,
            prompt_path=self.prompt_file
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_system_prompt(self):
        prompt = self.brain.load_system_prompt()
        self.assertIn("Jarvis", prompt)
        self.assertIn("Boss", prompt)
        self.assertIn("Tool prompt", prompt)

    @patch('core.brain.ollama.chat')
    def test_generate_response_loop(self, mock_ollama_chat):
        # Thiết lập phản hồi giả lập của ollama.chat cho từng bước
        response_step1 = {
            'message': {
                'content': '<thought>Tôi cần chạy công cụ</thought>\n<tool_call name="mock_tool">{"param": 123}</tool_call>'
            }
        }
        response_step2 = {
            'message': {
                'content': 'Tôi đã chạy xong công cụ. Kết quả đây.'
            }
        }
        mock_ollama_chat.side_effect = [response_step1, response_step2]
        
        history = []
        reply = self.brain.generate_response("chạy thử công cụ giúp tôi", history)
        
        # Kiểm tra phản hồi cuối cùng đã được làm sạch thẻ suy nghĩ và tool_call
        self.assertEqual(reply, "Tôi đã chạy xong công cụ. Kết quả đây.")
        
        # Kiểm tra ToolManager được gọi chạy chính xác
        self.tool_manager.execute_tool.assert_called_once_with("mock_tool", {"param": 123})
        
        # Kiểm tra MemoryManager được gọi ghi nhiều lần xuyên suốt chu trình suy nghĩ
        # Bước 1: user hỏi, Bước 1 (phản hồi LLM 1), Bước 1 (kết quả tool), Bước 2 (phản hồi LLM 2)
        # Số lượt ghi tối thiểu là 3 (user input, assistant response 1, tool output/assistant response 2)
        self.assertTrue(self.memory_manager.save_memory.call_count >= 3)

if __name__ == '__main__':
    unittest.main()
