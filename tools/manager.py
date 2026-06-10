import json
import re
from typing import Dict, Any, Callable, List, Tuple

# Registry tĩnh toàn cục để lưu trữ các tool được khai báo qua decorator @register_tool tại thời điểm import
_DEFAULT_REGISTRY: Dict[str, Dict[str, Any]] = {}


def register_tool(name: str, description: str, parameters: Dict[str, Any]):
    """Decorator để đăng ký một tool mới vào registry mặc định."""
    def decorator(func: Callable):
        _DEFAULT_REGISTRY[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
            "func": func
        }
        return func
    return decorator


class ToolManager:
    def __init__(self, approval_callback: Callable[[str, Dict[str, Any]], bool] = None):
        """Khởi tạo ToolManager.
        
        Args:
            approval_callback: Hàm callback nhận vào (tool_name, args) và trả về True/False
                              để xác nhận quyền thực thi. Nếu None, mặc định sẽ tự động đồng ý.
        """
        self.registry = dict(_DEFAULT_REGISTRY)
        self.approval_callback = approval_callback

    def register(self, name: str, description: str, parameters: Dict[str, Any], func: Callable):
        """Đăng ký thủ công một tool vào instance này."""
        self.registry[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
            "func": func
        }

    def get_tools_prompt(self) -> str:
        """Tạo chuỗi mô tả tất cả các công cụ của instance này để đưa vào system prompt."""
        if not self.registry:
            return "Hiện không có công cụ nào khả dụng."
        
        prompt = "Bạn có quyền truy cập vào các công cụ (tools) sau để giải quyết công việc. Để gọi một công cụ, hãy sử dụng cú pháp chính xác sau:\n"
        prompt += '<tool_call name="TÊN_CÔNG_CỤ">{"THAM_SỐ": "GIÁ_TRỊ"}</tool_call>\n\n'
        prompt += "Lưu ý:\n"
        prompt += "- Bạn PHẢI viết suy nghĩ của mình trong thẻ <thought>...</thought> trước khi gọi tool.\n"
        prompt += "- Mỗi lần phản hồi, bạn chỉ được gọi TỐI ĐA một công cụ. Sau khi công cụ chạy và trả về kết quả, bạn sẽ được cung cấp kết quả đó và tiếp tục suy nghĩ.\n"
        prompt += "- Các tham số của công cụ phải là một chuỗi JSON hợp lệ.\n\n"
        prompt += "Danh sách các công cụ:\n"
        
        for tool_name, tool_info in self.registry.items():
            prompt += f"- **{tool_name}**:\n"
            prompt += f"  Mô tả: {tool_info['description']}\n"
            prompt += f"  Tham số: {json.dumps(tool_info['parameters'], ensure_ascii=False, indent=2)}\n\n"
        
        return prompt

    def parse_tool_calls(self, text: str) -> List[Tuple[str, Dict[str, Any]]]:
        """Tìm tất cả các thẻ <tool_call> trong văn bản phản hồi của model."""
        pattern = r'<tool_call\s+name="([^"]+)"\s*>([\s\S]*?)</tool_call>'
        matches = re.findall(pattern, text)
        
        results = []
        for tool_name, args_str in matches:
            tool_name = tool_name.strip()
            args_str = args_str.strip()
            try:
                args = json.loads(args_str) if args_str else {}
            except json.JSONDecodeError:
                # Cố gắng sửa lỗi JSON nếu model quên đóng/mở dấu ngoặc nhọn
                try:
                    if not args_str.startswith("{"):
                        args_str = "{" + args_str
                    if not args_str.endswith("}"):
                        args_str = args_str + "}"
                    args = json.loads(args_str)
                except:
                    args = {"raw_arguments": args_str}
            results.append((tool_name, args))
        
        return results

    def execute_tool(self, name: str, args: Dict[str, Any]) -> str:
        """Thực thi một công cụ theo tên, sau khi được xác nhận phê duyệt."""
        if name not in self.registry:
            return f"Error: Công cụ '{name}' không tồn tại."
        
        tool_info = self.registry[name]
        func = tool_info["func"]
        
        # Kiểm tra phê duyệt thông qua callback
        if self.approval_callback:
            approved = self.approval_callback(name, args)
            if not approved:
                return "Error: Thao tác bị từ chối bởi Boss."
        
        try:
            # Gọi hàm xử lý công cụ
            result = func(**args)
            # Ép kiểu kết quả về string để phản hồi cho LLM
            if not isinstance(result, str):
                result = str(result)
            return result
        except Exception as e:
            return f"Error: Lỗi khi thực thi công cụ: {str(e)}"

