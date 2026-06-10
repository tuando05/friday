from dataclasses import dataclass

from config import Settings
from core.memory import MemoryManager
from core.guard import SecurityGuard
from core.brain import Brain
from tools import ToolManager
from audio import VoiceManager, Speaker


@dataclass(frozen=True)
class Services:
    config: Settings
    memory: MemoryManager
    guard: SecurityGuard
    tools: ToolManager
    brain: Brain
    voice: VoiceManager
    speaker: Speaker


def build_services(approval_callback=None):
    # 1. Khởi tạo cấu hình từ file .env
    config = Settings()
    
    # 2. Khởi tạo quản lý bộ nhớ
    memory = MemoryManager(
        memory_file=config.MEMORY_FILE,
        todo_file=config.TODO_FILE,
        mode_file=config.MODE_FILE,
        max_history=config.MAX_HISTORY
    )
    
    # 3. Khởi tạo guard bảo vệ file hệ thống
    guard = SecurityGuard(data_dir=config.DATA_DIR)
    
    # 4. Khởi tạo quản lý tool cùng callback phê duyệt
    tools_manager = ToolManager(approval_callback=approval_callback)
    
    # 5. Khởi tạo bộ não AI và các dịch vụ âm thanh
    brain_service = Brain(
        config=config,
        memory_manager=memory,
        tool_manager=tools_manager
    )
    
    voice = VoiceManager(config)
    speaker = Speaker(config)
    
    return Services(
        config=config,
        memory=memory,
        guard=guard,
        tools=tools_manager,
        brain=brain_service,
        voice=voice,
        speaker=speaker
    )

