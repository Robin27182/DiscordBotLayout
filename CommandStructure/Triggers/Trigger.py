from CommandStructure.Dispatcher import Dispatcher
from DataClasses.EventContext import EventContext


class Trigger:
    def __init__(self):
        """
        Triggers are designed to emit contexts to the Dispatcher.
        The emitting of contexts is just saying "Something happened, here's info about that."
        """
        self.dispatcher = Dispatcher()

    async def emit(self, event_context: EventContext):
        await self.dispatcher.dispatch(event_context)