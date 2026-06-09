from dataclasses import dataclass

from config import settings as config
from core import brain, guard, memory
from audio import VoiceManager, Speaker


@dataclass(frozen=True)
class Services:
    config: object
    memory: object
    brain: object
    guard: object
    voice: object
    speaker: object


def build_services():
    return Services(
        config=config,
        memory=memory,
        brain=brain,
        guard=guard,
        voice=VoiceManager(config),
        speaker=Speaker(config),
    )
