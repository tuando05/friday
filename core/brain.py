import ollama
import datetime
import os
import re

class Brain:
    def __init__(self, config, memory_manager, tool_manager, prompt_path: str = None):
        """Khởi tạo bộ não AI với các thành phần cần thiết được truyền từ ngoài vào.
        
        Args:
            config: Đối tượng cài đặt Settings
            memory_manager: Đối tượng MemoryManager để đọc ghi bộ nhớ
            tool_manager: Đối tượng ToolManager để gọi các công cụ
            prompt_path: Đường dẫn tệp prompt hệ thống, nếu None sẽ tự tìm từ thư mục core
        """
        self.config = config
        self.memory_manager = memory_manager
        self.tool_manager = tool_manager
        
        if prompt_path:
            self.prompt_path = prompt_path
        else:
            self.prompt_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "prompts", "sysPromt.txt")
            )

    def load_system_prompt(self) -> str:
        with open(self.prompt_path, 'r', encoding='utf-8') as f:
            prompt_content = f.read().strip()
        
        # Thay thế các cấu hình từ đối tượng config
        prompt_content = prompt_content.replace('{AI_NAME}', self.config.AI_NAME)
        prompt_content = prompt_content.replace('{BOSS_NAME}', self.config.BOSS_NAME)
        prompt_content = prompt_content.replace('{DATA_DIR}', self.config.DATA_DIR)
        
        # Nạp mô tả công cụ của instance tool_manager
        prompt_content = prompt_content.replace('{TOOLS_DESCRIPTION}', self.tool_manager.get_tools_prompt())
        
        return prompt_content

    def clean_final_reply(self, text: str) -> str:
        """Loại bỏ các thẻ thought và tool_call để trả về câu trả lời sạch cho Boss."""
        text = re.sub(r'<thought>[\s\S]*?</thought>', '', text)
        text = re.sub(r'<thought>[\s\S]*$', '', text)  # Xử lý thẻ chưa đóng
        text = re.sub(r'<tool_call[^>]*>[\s\S]*?</tool_call>', '', text)
        text = re.sub(r'<tool_call[^>]*>[\s\S]*$', '', text)  # Xử lý thẻ chưa đóng
        return text.strip()

    def generate_response(self, user_input, history):
        current_time = datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")
        
        # 1. Thêm câu hỏi của user vào history
        history.append({'role': 'user', 'content': f"Time: {current_time}\n{user_input}"})
        self.memory_manager.save_memory(history)
        
        max_steps = 5
        step = 0
        
        while step < max_steps:
            system_prompt = self.load_system_prompt()
            messages = [{'role': 'system', 'content': system_prompt}] + history
            
            try:
                response = ollama.chat(model=self.config.MODEL, messages=messages)
                reply_content = response['message']['content']
            except Exception as e:
                err_msg = f"Lỗi kết nối bộ não: {str(e)}"
                print(f"\n[{self.config.AI_NAME}] {err_msg}")
                return err_msg

            # 2. Lưu phản hồi của trợ lý vào lịch sử
            history.append({'role': 'assistant', 'content': reply_content})
            self.memory_manager.save_memory(history)

            # 3. Hiển thị suy nghĩ trung gian nếu có
            thought_match = re.search(r'<thought>([\s\S]*?)</thought>', reply_content)
            if thought_match:
                thought_text = thought_match.group(1).strip()
                if thought_text:
                    print(f"\n[{self.config.AI_NAME} (Suy nghĩ)]: {thought_text}")

            # 4. Tìm kiếm tool call
            tool_calls = self.tool_manager.parse_tool_calls(reply_content)
            
            if not tool_calls:
                # Không gọi thêm tool, trả về kết quả cuối cùng
                return self.clean_final_reply(reply_content)
                
            # 5. Thực thi tool đầu tiên
            tool_name, tool_args = tool_calls[0]
            result = self.tool_manager.execute_tool(tool_name, tool_args)
            
            # Hiển thị kết quả ngắn gọn cho người dùng trên CLI
            print(f"[{self.config.AI_NAME}] 📥 Kết quả công cụ:")
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
            self.memory_manager.save_memory(history)
            
            step += 1
            
        return f"Tôi đã đạt giới hạn suy nghĩ ({max_steps} bước) cho yêu cầu này."
