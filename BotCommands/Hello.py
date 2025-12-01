from discord.app_commands import commands

from BotCommands.Command import Command


class Hello(Command):
    def get_description(self) -> str:
        return "Say hello in a marvelous fashion!"

    def execute(self):
        async def executee(interaction):
            await interaction.response.send_message("Hello!")
        return executee