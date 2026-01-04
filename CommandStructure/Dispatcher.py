from typing import List, Tuple, Callable

from DataClasses.CommandProtocol import Command
from DataClasses.EventContext import EventContext

Authorizer = Callable[[EventContext], bool]

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Dispatcher(metaclass=Singleton):
    def __init__(self) -> None:
        """
        The dispatcher's life goal is to take in commands and authorizers,
        whenever something happens, dispatch is called, and it asks the authorizers if the command should run.
        If the authorizers say yes, run the command.
        """
        self._handlers: List[Tuple[Command, Authorizer]] = []

    def register(self, command: Command, authorizer: Authorizer) -> None:
        self._handlers.append((command, authorizer))

    async def dispatch(self, event_context: EventContext):
        for command, authorizer in self._handlers:
            if authorizer(event_context):
                await command.execute(event_context)