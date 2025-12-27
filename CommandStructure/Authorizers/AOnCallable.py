from typing import Callable

from DataClasses.EventContext import EventContext


class AOnCallable:
    def __init__(self, boolean_supplier: Callable[[], bool]):
        self.supplier = boolean_supplier

    def get_authorization(self, event_context: EventContext) -> bool:
        return self.supplier()
