import sys
import json
from core import commands, services


def format_assistant_message(name, content):
    if content is None:
        return f"{name}:"
    cleaned = content.strip()
    if not cleaned:
        return f"{name}:"
    return f"{name}:\n{cleaned}"


def cli_approval_callback(name, args):
    """Callback để hiển thị và yêu cầu xác nhận gọi công cụ từ Boss qua CLI."""
    print(f"\n[F.R.I.D.A.Y] 🛡️  Đề xuất gọi công cụ: {name}")
    print(f"            Tham số: {json.dumps(args, ensure_ascii=False)}")
    try:
        confirm = input("👉 Boss, bạn có đồng ý thực hiện hành động này không? (y/N): ").strip().lower()
        if confirm in ["y", "yes", "có", "đồng ý"]:
            print("[F.R.I.D.A.Y] ⚙️  Đang thực thi công cụ...")
            return True
        else:
            print("[F.R.I.D.A.Y] 🛑 Quyền thực thi bị từ chối.")
            return False
    except (EOFError, KeyboardInterrupt):
        print("\n[F.R.I.D.A.Y] Thao tác bị hủy bỏ.")
        return False


def main():
    # Khởi tạo services và truyền callback phê duyệt qua CLI
    svc = services.build_services(approval_callback=cli_approval_callback)
    print(f"--- {svc.config.AI_NAME} Mark 1 Modular Online ---")
    
    # Khởi tạo trí nhớ
    chat_history = svc.memory.load_memory()

    while True:
        try:
            cmd = input(f"\n{svc.config.BOSS_NAME}: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break
        
        cmd = cmd.strip()
        if not cmd:
            continue

        # Lệnh đặc biệt
        result = commands.handle_command(cmd, chat_history, svc)
        if result.handled:
            if result.message:
                print(format_assistant_message(svc.config.AI_NAME, result.message))
            chat_history = result.chat_history
            if result.should_exit:
                break
            continue

        # Xử lý qua AI (sẽ tự động quản lý history và gọi các công cụ)
        reply = svc.brain.generate_response(cmd, chat_history)
        print(format_assistant_message(svc.config.AI_NAME, reply))


if __name__ == "__main__":
    main()


