import os
import subprocess
import urllib.request
import urllib.parse
import re
from tools.manager import register_tool

# Xác định thư mục gốc dự án làm root cho các đường dẫn tương đối
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _resolve_path(path: str) -> str:
    """Giải quyết đường dẫn tương đối so với thư mục gốc dự án."""
    if not path:
        return WORKSPACE_ROOT
    if not os.path.isabs(path):
        return os.path.abspath(os.path.join(WORKSPACE_ROOT, path))
    return os.path.abspath(path)


@register_tool(
    name="read_file",
    description="Đọc nội dung của một tệp văn bản từ hệ thống.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Đường dẫn đến tệp cần đọc (tương đối từ gốc dự án hoặc tuyệt đối)."
            }
        },
        "required": ["path"]
    }
)
def read_file(path: str) -> str:
    full_path = _resolve_path(path)
    if not os.path.exists(full_path):
        return f"Error: Tệp '{path}' không tồn tại."
    if os.path.isdir(full_path):
        return f"Error: '{path}' là một thư mục, không thể đọc dưới dạng tệp."
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error: Không thể đọc tệp: {str(e)}"


@register_tool(
    name="write_file",
    description="Tạo hoặc ghi đè nội dung vào một tệp tin.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Đường dẫn tệp cần tạo/ghi (tương đối từ gốc dự án hoặc tuyệt đối)."
            },
            "content": {
                "type": "string",
                "description": "Nội dung ghi vào tệp."
            }
        },
        "required": ["path", "content"]
    }
)
def write_file(path: str, content: str) -> str:
    full_path = _resolve_path(path)
    dir_name = os.path.dirname(full_path)
    try:
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Success: Đã ghi thành công vào tệp '{path}'."
    except Exception as e:
        return f"Error: Không thể ghi tệp: {str(e)}"


@register_tool(
    name="list_dir",
    description="Liệt kê danh sách các tệp và thư mục con trong một thư mục.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Đường dẫn đến thư mục cần liệt kê (tương đối từ gốc dự án hoặc tuyệt đối). Để trống hoặc '.' là thư mục gốc."
            }
        },
        "required": []
    }
)
def list_dir(path: str = ".") -> str:
    full_path = _resolve_path(path)
    if not os.path.exists(full_path):
        return f"Error: Thư mục '{path}' không tồn tại."
    if not os.path.isdir(full_path):
        return f"Error: '{path}' là một tệp tin, không phải thư mục."
    try:
        items = os.listdir(full_path)
        if not items:
            return f"Thư mục '{path}' trống."
        
        output = []
        for item in items:
            item_path = os.path.join(full_path, item)
            prefix = "[DIR] " if os.path.isdir(item_path) else "[FILE]"
            output.append(f"{prefix} {item}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: Không thể liệt kê thư mục: {str(e)}"


@register_tool(
    name="shell_run",
    description="Chạy một lệnh shell hệ thống (CMD/PowerShell) và trả về kết quả.",
    parameters={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Lệnh cần thực thi trên terminal."
            }
        },
        "required": ["command"]
    }
)
def shell_run(command: str) -> str:
    try:
        # Thực thi lệnh và nhận kết quả
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
            cwd=WORKSPACE_ROOT
        )
        out = result.stdout or ""
        err = result.stderr or ""
        
        output = []
        if out.strip():
            output.append(f"STDOUT:\n{out}")
        if err.strip():
            output.append(f"STDERR:\n{err}")
        if not output:
            output.append("Lệnh đã chạy thành công nhưng không có phản hồi đầu ra (STDOUT/STDERR trống).")
            
        return f"Mã thoát (Exit code): {result.returncode}\n" + "\n".join(output)
    except subprocess.TimeoutExpired:
        return "Error: Lệnh bị dừng do hết thời gian thực thi (timeout 30s)."
    except Exception as e:
        return f"Error: Không thể thực thi lệnh: {str(e)}"


@register_tool(
    name="web_search",
    description="Tìm kiếm thông tin trên Internet qua DuckDuckGo và lấy kết quả tóm tắt.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Từ khóa tìm kiếm."
            }
        },
        "required": ["query"]
    }
)
def web_search(query: str) -> str:
    try:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
        # Trích xuất đoạn trích kết quả tìm kiếm bằng regex đơn giản
        snippets = re.findall(r'<a class="result__snippet"[^>]*>([\s\S]*?)</a>', html)
        titles = re.findall(r'<a class="result__url"[^>]*>([\s\S]*?)</a>', html)
        
        results = []
        for i, snippet in enumerate(snippets[:5]):
            clean_snippet = re.sub(r'<[^>]+>', '', snippet).strip()
            clean_title = re.sub(r'<[^>]+>', '', titles[i]).strip() if i < len(titles) else "Không có tiêu đề"
            results.append(f"[{i+1}] Tiêu đề: {clean_title}\n    Nội dung: {clean_snippet}\n")
            
        if not results:
            return "Không tìm thấy kết quả phù hợp trên DuckDuckGo."
        return "\n".join(results)
    except Exception as e:
        return f"Error: Không thể thực hiện tìm kiếm trực tuyến: {str(e)}"
