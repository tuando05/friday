from dataclasses import dataclass


@dataclass
class CommandResult:
    handled: bool
    should_exit: bool
    chat_history: list
    message: str | None


def _format_section(title, lines=None):
    if not lines:
        return title
    bullet_lines = "\n".join(f"- {line}" for line in lines)
    return f"{title}\n{bullet_lines}"


def handle_command(raw_cmd, chat_history, services):
    cmd = raw_cmd.lower().strip()

    if cmd in ["/bye", "/exit", "/quit", "nghỉ ngơi đi"]:
        return CommandResult(
            handled=True,
            should_exit=True,
            chat_history=chat_history,
            message=_format_section(
                "Tam biet",
                [
                    "He thong ngoai tuyen.",
                    f"Chao {services.config.BOSS_NAME}.",
                ],
            ),
        )

    if cmd == "/help":
        return CommandResult(
            handled=True,
            should_exit=False,
            chat_history=chat_history,
            message=_format_section(
                "Huong dan lenh dac biet",
                [
                    "/help: Tom tat cac lenh va cach dung.",
                    "/bye | /exit | /quit: Thoat phien lam viec.",
                    "/clear: Xoa lich su hoi thoai da luu.",
                    "/check-files: Liet ke file trong vault.",
                    "/search <tu_khoa>: Dieu huong tim thong tin tren mang.",
                    "/status: Trang thai he thong.",
                    "/mode <ten>: Xem/doi che do. Vi du: /mode think.",
                    "/todo [list|add <noi_dung>]: Quan ly danh sach viec can lam.",
                ],
            ),
        )

    if cmd == "/clear" or cmd.startswith("/clear "):
        services.memory.clear_memory()
        return CommandResult(
            handled=True,
            should_exit=False,
            chat_history=[],
            message=_format_section(
                "Tri nho",
                [
                    "Da don dep tri nho.",
                    "Lich su da duoc reset.",
                ],
            ),
        )

    if "/check-files" in cmd:
        files = services.guard.list_DATA_files()
        vault_line = ", ".join(files) if files else "Trong"
        return CommandResult(
            handled=True,
            should_exit=False,
            chat_history=chat_history,
            message=_format_section(
                "File vault",
                [
                    f"Danh sach: {vault_line}.",
                    f"Thu muc: {services.config.DATA_DIR}.",
                ],
            ),
        )

    if cmd.startswith("/search"):
        query = raw_cmd.strip()[len("/search"):].strip()
        if not query:
            return CommandResult(
                handled=True,
                should_exit=False,
                chat_history=chat_history,
                message=_format_section(
                    "Tim kiem",
                    [
                        "Vui long nhap tu khoa de tim kiem.",
                        "Vi du: /search cong nghe AI moi nhat.",
                    ],
                ),
            )
        return CommandResult(
            handled=True,
            should_exit=False,
            chat_history=chat_history,
            message=_format_section(
                "Tim kiem",
                [
                    f"Da nhan tu khoa: {query}.",
                    "Chuc nang dieu huong web se duoc cap nhat sau.",
                ],
            ),
        )

    if cmd == "/status":
        mode_name = services.memory.load_mode() or "default"
        todo_items = services.memory.load_todo()
        return CommandResult(
            handled=True,
            should_exit=False,
            chat_history=chat_history,
            message=_format_section(
                "Trang thai he thong",
                [
                    f"Boss: {services.config.BOSS_NAME}.",
                    f"Mode: {mode_name}.",
                    f"Lich su: {len(chat_history)} muc.",
                    f"TODO: {len(todo_items)} muc.",
                    f"Data: {services.config.DATA_DIR}.",
                ],
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
                message=_format_section(
                    "Che do",
                    [
                        f"Mode hien tai: {current_mode}.",
                        "Cach dung: /mode <ten_che_do>.",
                    ],
                ),
            )
        mode_name = parts[1].strip()
        if not mode_name:
            return CommandResult(
                handled=True,
                should_exit=False,
                chat_history=chat_history,
                message=_format_section(
                    "Che do",
                    [
                        "Vui long nhap ten che do.",
                        "Vi du: /mode think.",
                    ],
                ),
            )
        services.memory.save_mode(mode_name)
        return CommandResult(
            handled=True,
            should_exit=False,
            chat_history=chat_history,
            message=_format_section(
                "Che do",
                [f"Da chuyen sang che do {mode_name}."],
            ),
        )

    if cmd.startswith("/todo"):
        parts = raw_cmd.strip().split(maxsplit=2)
        todo_items = services.memory.load_todo()
        if len(parts) == 1 or (len(parts) == 2 and parts[1].lower() == "list"):
            if not todo_items:
                message = _format_section("Danh sach TODO", ["Chua co muc nao."])
            else:
                lines = [f"{idx + 1}. {item}" for idx, item in enumerate(todo_items)]
                message = _format_section("Danh sach TODO", lines)
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
                message=_format_section(
                    "TODO",
                    [
                        "Vui long nhap noi dung TODO.",
                        "Vi du: /todo add mua sua.",
                    ],
                ),
            )

        todo_items.append(todo_text)
        services.memory.save_todo(todo_items)
        return CommandResult(
            handled=True,
            should_exit=False,
            chat_history=chat_history,
            message=_format_section(
                "TODO",
                [
                    "Da them TODO.",
                    f"Tong cong: {len(todo_items)} muc.",
                ],
            ),
        )

    return CommandResult(handled=False, should_exit=False, chat_history=chat_history, message=None)
