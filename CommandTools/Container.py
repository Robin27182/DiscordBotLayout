from typing import TypeVar, Generic

T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self):
        self.value: T = None

    def set_value(self, val: T):
        self.value = val