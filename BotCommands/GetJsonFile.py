from BotCommands.Command import Command
from DataInterpreter.UserConfigInterpreter import UserConfigInterpreter
from UserManager.UserManager import UserManager


class GetJsonFile(Command):
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
        self.userInterpreter = UserConfigInterpreter()

    def get_description(self) -> str:
        return "Get your personalized Json!"

    def execute(self):
        async def executee(interaction):
            await interaction.response.send_message(self.userInterpreter.write(self.user_manager.get_user_from_member(interaction.user).user_config))
        return executee