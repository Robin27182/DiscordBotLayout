from dataclasses import dataclass

from FileManager.FileFormatABC import FileFormatABC


@dataclass
class BotConfig(FileFormatABC):
    data: str