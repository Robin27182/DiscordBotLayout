from discord import Guild

from DataClasses.CommandData import CommandData
from DataClasses.EventContext import EventContext


class LogInChannel:
    def __init__(self, command_data: CommandData, channel_id: int) -> None:
        self.guild = command_data.guild
        self.channel_id = channel_id

    async def execute(self, context: EventContext) -> None:
        channel = self.guild.get_channel(self.channel_id)
        if channel is None:
            if self.guild is None:
                raise TypeError("guild is NONE")
            raise ValueError("Channel could not be found")
        await self.guild.get_channel(self.channel_id).send(str(context))