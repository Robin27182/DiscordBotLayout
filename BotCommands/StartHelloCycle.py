import datetime
from datetime import timedelta

from DataClasses.CommandData import CommandData
from DataClasses.EventType import EventType
from DataClasses.EventContext import EventContext
from CommandStructure.Triggers.TimeTrigger import TimeTrigger


class StartHelloCycle:
    def __init__(self, command_data: CommandData) -> None:
        return

    async def execute(self, context: EventContext) -> None:
        if context.id is None:
            await context.interaction.response.send_message("Hello!")
            new_context = EventContext(EventType.SCHEDULED, interaction=context.interaction, id=1, )
        else:
            new_context = context
            await context.interaction.followup.send("Hello!")
        TimeTrigger().schedule(datetime.datetime.now() + timedelta(seconds=3.5), new_context)
