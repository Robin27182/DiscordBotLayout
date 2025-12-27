from typing import Type, TypeVar

from DataClasses.CommandData import CommandData
from DataClasses.CommandProtocol import Command

C = TypeVar("C", bound=Command)
class CommandBuilder:
    def __init__(self, command_to_build: Type[C]):
        self._command: Type[C] = command_to_build
        self._args = None
        self._command_data = None

    def with_args(self, *args) -> "CommandBuilder":
        self._args = args
        return self

    def with_data(self, command_data: CommandData) -> "CommandBuilder":
        self._command_data = command_data
        return self

    def build(self) -> Command:
        return self._command(self._command_data, *self._args)