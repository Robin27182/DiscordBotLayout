from DataClasses.CommandData import CommandData
from DataClasses.EventContext import EventContext


class Hello:
    def __init__(self, command_data: CommandData) -> None:
        return

    async def execute(self, context: EventContext) -> None:
        await context.interaction.response.send_message("Hello!")