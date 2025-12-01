from abc import ABC, ABCMeta


class SingletonMeta(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # Create and store the instance
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Command(ABC, metaclass=SingletonMeta):
    def get_description(self) -> str:
        ...

    def execute(self):
        return self._execute
