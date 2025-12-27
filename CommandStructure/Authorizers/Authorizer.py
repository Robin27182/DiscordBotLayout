from typing import runtime_checkable, Protocol

from DataClasses.EventContext import EventContext

@runtime_checkable
class Authorizer(Protocol):
    def __init__(self, *args, **kwargs): ...
    def get_authorization(self, event_context: EventContext) -> bool: ...

