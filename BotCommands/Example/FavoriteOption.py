from typing import List

from DataClasses.CommandData import CommandData
from CommandTools.Container import Container
from DataClasses.EventContext import EventContext
from CommandTools.Querys.ButtonViewQuery import ButtonViewQuery


class FavoriteOption:
    def __init__(self, command_data: CommandData, options: List[str]):
        self.choice_list = options

    async def execute(self, context: EventContext) -> None:
        interaction = context.interaction
        response_container: Container = Container[str]()

        question_options = {c: c for c in self.choice_list}
        query = ButtonViewQuery(question_options, response_container.set_value)

        await interaction.response.send_message("Choose your favorite!", view=query, ephemeral=True)
        await query.wait()
        await interaction.delete_original_response()
        await interaction.followup.send(f"You chose {response_container.value}")