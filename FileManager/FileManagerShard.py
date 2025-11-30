from typing import Final, Type

from FileManager.FileFormatABC import FileFormatABC
from FileManager.FileManager import FileManager


class FileManagerShard:
    def __init__(self, file_manager: FileManager, file_name: str):
        self.file_manager: Final = file_manager
        self.file_name: Final = file_name

    async def read(self) -> Type[FileFormatABC]:
        return await self.file_manager.read(self.file_name)

    async def write(self, formatted: Type[FileFormatABC], create_if_none = False) -> None:
        await self.file_manager.write(self.file_name, formatted, create_if_none)