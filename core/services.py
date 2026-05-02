from dataclasses import dataclass

from config import settings as config
from core import brain, guard, memory


@dataclass(frozen=True)
class Services:
    config: object
    memory: object
    brain: object
    guard: object


def build_services():
    return Services(config=config, memory=memory, brain=brain, guard=guard)
