class VoiceManager:
    def __init__(self, config):
        self._config = config
        self._active = False

    def set_transcript_queue(self, transcript_queue):
        pass

    def is_active(self):
        return False

    def start(self):
        return False, "Voice listener đã bị đóng gói và tạm khóa."

    def stop(self):
        return True, "Voice listener đã tắt."


class Speaker:
    def __init__(self, config):
        self._config = config
        self._enabled = False

    def say(self, text):
        # Không nói gì cả (chế độ văn bản thuần túy)
        pass

    def stop(self):
        pass
