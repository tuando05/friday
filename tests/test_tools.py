import unittest
from tools import ToolManager, register_tool

# Đăng ký một tool mẫu tại thời điểm import để kiểm tra xem registry mặc định có hoạt động không
@register_tool(
    name="dummy_calculator",
    description="Tính tổng hai số.",
    parameters={
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["a", "b"]
    }
)
def dummy_calculator(a, b):
    return f"Sum: {a + b}"


class TestToolManager(unittest.TestCase):
    def setUp(self):
        # Tạo ToolManager mặc định (sẽ tự động sao chép dummy_calculator)
        self.tool_manager = ToolManager()

    def test_default_tool_copied(self):
        # Đảm bảo dummy_calculator đã được nạp
        self.assertIn("dummy_calculator", self.tool_manager.registry)
        
    def test_manual_registration(self):
        def greet(name):
            return f"Hello, {name}!"
            
        self.tool_manager.register(
            name="greet_boss",
            description="Chào Boss.",
            parameters={"type": "object", "properties": {"name": {"type": "string"}}},
            func=greet
        )
        self.assertIn("greet_boss", self.tool_manager.registry)
        self.assertEqual(self.tool_manager.execute_tool("greet_boss", {"name": "Sir"}), "Hello, Sir!")

    def test_get_tools_prompt(self):
        prompt = self.tool_manager.get_tools_prompt()
        self.assertIn("dummy_calculator", prompt)
        self.assertIn("Tính tổng hai số.", prompt)
        self.assertIn("dummy_calculator", prompt)

    def test_parse_tool_calls(self):
        # Trường hợp chuẩn
        text = 'Tôi sẽ tính tổng.\n<thought>Cần tính 5 + 3</thought>\n<tool_call name="dummy_calculator">{"a": 5, "b": 3}</tool_call>'
        calls = self.tool_manager.parse_tool_calls(text)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0], "dummy_calculator")
        self.assertEqual(calls[0][1], {"a": 5, "b": 3})

        # Trường hợp thiếu ngoặc JSON (sẽ cố sửa lỗi)
        text_malformed = '<tool_call name="dummy_calculator">"a": 5, "b": 3</tool_call>'
        calls = self.tool_manager.parse_tool_calls(text_malformed)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0], "dummy_calculator")
        self.assertEqual(calls[0][1], {"a": 5, "b": 3})

    def test_execute_tool_with_auto_approve(self):
        # Mặc định approval_callback=None sẽ tự động duyệt chạy
        result = self.tool_manager.execute_tool("dummy_calculator", {"a": 10, "b": 20})
        self.assertEqual(result, "Sum: 30")

    def test_execute_tool_with_custom_approval(self):
        # Giả lập người dùng đồng ý
        approved_calls = []
        def yes_callback(name, args):
            approved_calls.append((name, args))
            return True
            
        mgr_yes = ToolManager(approval_callback=yes_callback)
        res_yes = mgr_yes.execute_tool("dummy_calculator", {"a": 1, "b": 2})
        self.assertEqual(res_yes, "Sum: 3")
        self.assertEqual(approved_calls, [("dummy_calculator", {"a": 1, "b": 2})])

        # Giả lập người dùng từ chối
        rejected_calls = []
        def no_callback(name, args):
            rejected_calls.append((name, args))
            return False
            
        mgr_no = ToolManager(approval_callback=no_callback)
        res_no = mgr_no.execute_tool("dummy_calculator", {"a": 1, "b": 2})
        self.assertTrue(res_no.startswith("Error:"))
        self.assertIn("từ chối", res_no)
        self.assertEqual(rejected_calls, [("dummy_calculator", {"a": 1, "b": 2})])

if __name__ == '__main__':
    unittest.main()
