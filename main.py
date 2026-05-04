from core import commands, services


def format_assistant_message(name, content):
    if content is None:
        return f"{name}:"
    cleaned = content.strip()
    if not cleaned:
        return f"{name}:"
    return f"{name}:\n{cleaned}"

def main():
    svc = services.build_services()
    print(f"--- {svc.config.AI_NAME} Mark 1 Modular Online ---")
    
    # Khởi tạo trí nhớ
    chat_history = svc.memory.load_memory()
    
    while True:
        try:
            cmd = input(f"\n{svc.config.BOSS_NAME}: ")

            # Lệnh đặc biệt
            result = commands.handle_command(cmd, chat_history, svc)
            if result.handled:
                if result.message:
                    print(format_assistant_message(svc.config.AI_NAME, result.message))
                chat_history = result.chat_history
                if result.should_exit:
                    break
                continue

            # Xử lý qua AI
            reply = svc.brain.generate_response(cmd, chat_history)
            
            # Lưu lịch sử
            chat_history.append({'role': 'user', 'content': cmd})
            chat_history.append({'role': 'assistant', 'content': reply})
            svc.memory.save_memory(chat_history)

            print(format_assistant_message(svc.config.AI_NAME, reply))

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()