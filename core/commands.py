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
                f"{services.config.AI_NAME}: Lệnh hỗ trợ: /bye, /exit, /quit, /help, /clear, /check-files."
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

    return CommandResult(handled=False, should_exit=False, chat_history=chat_history, message=None)
