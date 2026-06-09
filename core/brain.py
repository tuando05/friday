import ollama
import datetime
import os
import re
from config.settings import MODEL, AI_NAME, BOSS_NAME, DATA_DIR
from core.memory import save_memory
import tools


def load_system_prompt():
    prompt_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "prompts", "sysPromt.txt")
    )
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt_content = f.read().strip()
    
    # Thay thế các cấu hình
    prompt_content = prompt_content.replace('{AI_NAME}', AI_NAME)
    prompt_content = prompt_content.replace('{BOSS_NAME}', BOSS_NAME)
    prompt_content = prompt_content.replace('{DATA_DIR}', DATA_DIR)
    
    # Nạp mô tả công cụ
    prompt_content = prompt_content.replace('{TOOLS_DESCRIPTION}', tools.get_tools_prompt())
    
    return prompt_content


def clean_final_reply(text: str) -> str:
    """Loại bỏ các thẻ thought và tool_call để trả về câu trả lời sạch cho Boss."""
    text = re.sub(r'<thought>[\s\S]*?</thought>', '', text)
    text = re.sub(r'<thought>[\s\S]*$', '', text)  # Xử lý thẻ chưa đóng
    text = re.sub(r'<tool_call[^>]*>[\s\S]*?</tool_call>', '', text)
    text = re.sub(r'<tool_call[^>]*>[\s\S]*$', '', text)  # Xử lý thẻ chưa đóng
    return text.strip()


def generate_response(user_input, history):
    current_time = datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")
    
    # 1. Thêm câu hỏi của user vào history
    history.append({'role': 'user', 'content': f"Time: {current_time}\n{user_input}"})
    save_memory(history)
    
    max_steps = 5
    step = 0
    
    while step < max_steps:
        system_prompt = load_system_prompt()
        messages = [{'role': 'system', 'content': system_prompt}] + history
        
        try:
            response = ollama.chat(model=MODEL, messages=messages)
            reply_content = response['message']['content']
        except Exception as e:
            err_msg = f"Lỗi kết nối bộ não: {str(e)}"
            print(f"\n[{AI_NAME}] {err_msg}")
            return err_msg

        # 2. Lưu phản hồi của trợ lý vào lịch sử
        history.append({'role': 'assistant', 'content': reply_content})
        save_memory(history)

        # 3. Hiển thị suy nghĩ trung gian nếu có
        thought_match = re.search(r'<thought>([\s\S]*?)</thought>', reply_content)
        if thought_match:
            thought_text = thought_match.group(1).strip()
            if thought_text:
                print(f"\n[{AI_NAME} (Suy nghĩ)]: {thought_text}")

        # 4. Tìm kiếm tool call
        tool_calls = tools.parse_tool_calls(reply_content)
        
        if not tool_calls:
            # Không gọi thêm tool, trả về kết quả cuối cùng
            return clean_final_reply(reply_content)
            
        # 5. Thực thi tool đầu tiên
        tool_name, tool_args = tool_calls[0]
        result = tools.execute_tool(tool_name, tool_args)
        
        # Hiển thị kết quả ngắn gọn cho người dùng trên CLI
        print(f"[{AI_NAME}] 📥 Kết quả công cụ:")
        # Giới hạn hiển thị kết quả nếu quá dài để đỡ trôi CLI
        lines = result.splitlines()
        if len(lines) > 20:
            print("\n".join(lines[:20]))
            print(f"... (còn {len(lines) - 20} dòng nữa) ...")
        else:
            print(result)
        
        # 6. Đưa kết quả vào lịch sử để mô hình đọc ở bước tiếp theo
        history.append({
            'role': 'user',
            'content': f"[Hệ thống] Kết quả thực thi công cụ '{tool_name}': {result}"
        })
        save_memory(history)
        
        step += 1
        
    return f"Tôi đã đạt giới hạn suy nghĩ ({max_steps} bước) cho yêu cầu này."