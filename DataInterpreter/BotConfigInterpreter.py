import json
from dataclasses import is_dataclass, asdict

from DataClasses.BotConfig import BotConfig
from FileManager.FileInterpreterABC import FileInterpreterABC


class BotConfigInterpreter(FileInterpreterABC):
    @property
    def extension(self) -> str:
        return ".json"

    def write(self, formatted: BotConfig) -> str:
        # Convert dataclass → dict (fallback to __dict__)
        if is_dataclass(formatted):
            data = asdict(formatted)
        else:
            data = formatted.__dict__

        return json.dumps(data, indent=4)

    def read(self, file_contents: str) -> BotConfig:
        data = json.loads(file_contents)

        # Reconstruct using unpacking
        return BotConfig(**data)

