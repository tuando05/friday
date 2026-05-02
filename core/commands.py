from dataclasses import dataclass


@dataclass
class CommandResult:
    handled: bool
    should_exit: bool
    chat_history: list
    message: str | None


def handle_command(raw_cmd, chat_history, services):
    cmd = raw_cmd.lower().strip()

    if cmd in ["/bye", "/exit", "/quit", "/clear", "nghỉ ngơi đi"]:
        return CommandResult(
            handled=True,
            should_exit=True,
            chat_history=chat_history,
            message=f"{services.config.AI_NAME}: Hệ thống ngoại tuyến. Chào {services.config.BOSS_NAME}.",
        )

    if cmd == "/help":
        return CommandResult(
            handled=True,
            should_exit=False,
            chat_history=chat_history,
            message=(
                f"{services.config.AI_NAME}: Lệnh hỗ trợ: /bye, /exit, /quit, /help, /clear, /check-files, /status, /mode, /todo."
            ),
        )

    if "/clear" in cmd:
        services.memory.clear_memory()
        return CommandResult(
            handled=True,
            should_exit=False,
            chat_history=[],
            message=f"{services.config.AI_NAME}: Trí nhớ đã được dọn dẹp.",
        )

    if "/check-files" in cmd:
        files = services.guard.list_DATA_files()
        return CommandResult(
            handled=True,
            should_exit=False,
            chat_history=chat_history,
            message=(
                f"{services.config.AI_NAME}: Các file trong vault: {', '.join(files) if files else 'Trống'}"
            ),
        )

    if cmd == "/status":
        mode_name = services.memory.load_mode() or "default"
        todo_items = services.memory.load_todo()
        return CommandResult(
            handled=True,
            should_exit=False,
            chat_history=chat_history,
            message=(
                f"{services.config.AI_NAME}: Trang thai he thong | Boss: {services.config.BOSS_NAME} | "
                f"Mode: {mode_name} | Lich su: {len(chat_history)} | TODO: {len(todo_items)} | "
                f"Data: {services.config.DATA_DIR}"
            ),
        )

    if cmd.startswith("/mode"):
        parts = raw_cmd.strip().split(maxsplit=1)
        if len(parts) == 1:
            current_mode = services.memory.load_mode() or "default"
            return CommandResult(
                handled=True,
                should_exit=False,
                chat_history=chat_history,
                message=(
                    f"{services.config.AI_NAME}: Mode hien tai: {current_mode}. "
                    f"Dung: /mode <ten_che_do>"
                ),
            )
        mode_name = parts[1].strip()
        if not mode_name:
            return CommandResult(
                handled=True,
                should_exit=False,
                chat_history=chat_history,
                message=(
                    f"{services.config.AI_NAME}: Vui long nhap ten che do. Vi du: /mode think"
                ),
            )
        services.memory.save_mode(mode_name)
        return CommandResult(
            handled=True,
            should_exit=False,
            chat_history=chat_history,
            message=f"{services.config.AI_NAME}: Da chuyen sang che do {mode_name}.",
        )

    if cmd.startswith("/todo"):
        parts = raw_cmd.strip().split(maxsplit=2)
        todo_items = services.memory.load_todo()
        if len(parts) == 1 or (len(parts) == 2 and parts[1].lower() == "list"):
            if not todo_items:
                message = f"{services.config.AI_NAME}: TODO trong."
            else:
                lines = [f"{idx + 1}. {item}" for idx, item in enumerate(todo_items)]
                message = f"{services.config.AI_NAME}: TODO\n" + "\n".join(lines)
            return CommandResult(
                handled=True,
                should_exit=False,
                chat_history=chat_history,
                message=message,
            )

        if len(parts) >= 2 and parts[1].lower() == "add":
            todo_text = parts[2].strip() if len(parts) == 3 else ""
        else:
            todo_text = raw_cmd.strip()[len("/todo"):].strip()

        if not todo_text:
            return CommandResult(
                handled=True,
                should_exit=False,
                chat_history=chat_history,
                message=f"{services.config.AI_NAME}: Vui long nhap noi dung TODO. Vi du: /todo add mua sua",
            )

        todo_items.append(todo_text)
        services.memory.save_todo(todo_items)
        return CommandResult(
            handled=True,
            should_exit=False,
            chat_history=chat_history,
            message=f"{services.config.AI_NAME}: Da them TODO. Tong cong: {len(todo_items)}",
        )

    return CommandResult(handled=False, should_exit=False, chat_history=chat_history, message=None)
