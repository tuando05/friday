import ollama
import datetime
import fileinput
import os
from core.config import MODEL, AI_NAME, BOSS_NAME, DATA_DIR

def load_system_prompt():
    prompt_file = os.path.join(os.path.dirname(__file__), 'sysPromt.txt')
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt_content = f.read().strip()
    
    # Replace placeholders with actual config values
    prompt_content = prompt_content.replace('{AI_NAME}', AI_NAME)
    prompt_content = prompt_content.replace('{BOSS_NAME}', BOSS_NAME)
    prompt_content = prompt_content.replace('{DATA_DIR}', DATA_DIR)
    
    return prompt_content

def generate_response(user_input, history):
    current_time = datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")
    system_prompt = load_system_prompt()
    messages = [{'role': 'system', 'content': system_prompt}] + history + [{'role': 'user', 'content': f"Time: {current_time}\n{user_input}"}]
    
    try:
        response = ollama.chat(model=MODEL, messages=messages)
        return response['message']['content']
    except Exception as e:
        return f"Lỗi kết nối bộ não: {str(e)}"