import ollama
import datetime
from core.config import MODEL, AI_NAME, BOSS_NAME, DATA_DIR

def generate_response(user_input, history):
    system_prompt = {
        'role': 'system', 
        'content': f"Bạn là {AI_NAME}, trợ lý AI của {BOSS_NAME}. Trả lời ngắn gọn, chuyên nghiệp. Bạn chỉ làm việc trong {DATA_DIR}."
    }
    
    current_time = datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")
    messages = [system_prompt] + history + [{'role': 'user', 'content': f"Time: {current_time}\n{user_input}"}]
    
    try:
        response = ollama.chat(model=MODEL, messages=messages)
        return response['message']['content']
    except Exception as e:
        return f"Lỗi kết nối bộ não: {str(e)}"