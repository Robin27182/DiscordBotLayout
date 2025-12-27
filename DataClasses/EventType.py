from enum import Enum, auto

class EventType(Enum):
    """
    Designed to be added upon, based on things that can trigger.
    """
    ON_READY = auto()
    USER_COMMAND = auto()
    SCHEDULED = auto()
