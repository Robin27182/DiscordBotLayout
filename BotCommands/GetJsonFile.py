from DataClasses.CommandData import CommandData
from DataClasses.EventContext import EventContext
from DataInterpreter.UserConfigInterpreter import UserConfigInterpreter

class GetJsonFile:
    def __init__(self, command_data: CommandData):
        self.user_manager = command_data.user_manager
        self.userInterpreter = UserConfigInterpreter()

    async def execute(self, context: EventContext) -> None:
        await context.interaction.response.send_message(self.userInterpreter.write(self.user_manager.get_user_from_member(context.interaction.user).user_config))