from DataClasses.UserConfig import UserConfig
from FileManager.FileInterpreterABC import FileInterpreterABC


import json
from dataclasses import asdict, is_dataclass


class UserConfigInterpreter(FileInterpreterABC):
    @property
    def extension(self) -> str:
        return ".json"

    def write(self, formatted: UserConfig) -> str:
        # Convert dataclass → dict (fallback to __dict__)
        if is_dataclass(formatted):
            data = asdict(formatted)
        else:
            data = formatted.__dict__

        return json.dumps(data, indent=4)

    def read(self, file_contents: str) -> UserConfig:
        data = json.loads(file_contents)

        # Reconstruct using unpacking
        return UserConfig(**data)