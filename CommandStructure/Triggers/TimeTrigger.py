import datetime

from DataClasses.EventContext import EventContext
from CommandStructure.Scheduler import Scheduler
from CommandStructure.Triggers.Trigger import Trigger


class TimeTrigger(Trigger):
    def __init__(self):
        """
        TimeTrigger is a trigger that emits a context at a specified time.
        This is passed onto APScheduler to do its magic.
        """
        super().__init__()

    def schedule(self, time: datetime, context: EventContext):
        async def run_emit():
            await self.emit(context)
        Scheduler().schedule(time, run_emit)