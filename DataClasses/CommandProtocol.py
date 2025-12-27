from typing import runtime_checkable, Protocol, Any

from DataClasses.CommandData import CommandData
from DataClasses.EventContext import EventContext


@runtime_checkable
class Command(Protocol):
    def __init__(self, command_data: CommandData, *args: Any): ...
    async def execute(self, context: EventContext) -> None: ...