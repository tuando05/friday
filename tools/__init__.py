# Tự động nạp các công cụ hệ thống để kích hoạt @register_tool
from tools import system
from tools.manager import get_tools_prompt, parse_tool_calls, execute_tool, _REGISTRY

__all__ = ["get_tools_prompt", "parse_tool_calls", "execute_tool"]
