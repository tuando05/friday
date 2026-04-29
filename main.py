from core import config, memory, brain, guard

def main():
    print(f"--- {config.AI_NAME} Mark 1 Modular Online ---")
    
    # Khởi tạo trí nhớ
    chat_history = memory.load_memory()
    
    while True:
        try:
            cmd = input(f"\n{config.BOSS_NAME}: ")
            
            # Lệnh đặc biệt
            if cmd.lower() in ["exit", "nghỉ ngơi đi"]:
                print(f"{config.AI_NAME}: Hệ thống ngoại tuyến. Chào {config.BOSS_NAME}.")
                break
                
            if "xóa trí nhớ" in cmd.lower():
                memory.clear_memory()
                chat_history = []
                print(f"{config.AI_NAME}: Trí nhớ đã được dọn dẹp.")
                continue

            if "kiểm tra file" in cmd.lower():
                files = guard.list_vault_files()
                print(f"{config.AI_NAME}: Các file trong vault: {', '.join(files) if files else 'Trống'}")
                continue

            # Xử lý qua AI
            reply = brain.generate_response(cmd, chat_history)
            
            # Lưu lịch sử
            chat_history.append({'role': 'user', 'content': cmd})
            chat_history.append({'role': 'assistant', 'content': reply})
            memory.save_memory(chat_history)
            
            print(f"{config.AI_NAME}: {reply}")

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()