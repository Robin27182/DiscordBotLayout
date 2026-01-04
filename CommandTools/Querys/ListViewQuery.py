import discord
from typing import Callable, TypeVar, Awaitable, Dict

T = TypeVar("T")


class ListViewQuery(discord.ui.View):
    def __init__(self,
        options: Dict[str, T],
        result_consumer: Callable[[T], None | Awaitable[None]],
        timeout: float = 20,
    ) -> None:
        """
        A View that presents a select menu for the user to pick from.

        :param options: A dictionary mapping option labels to return values.
        :param result_consumer: Function called with the selected value.
        :param timeout: How long to wait for a response before timing out.
        """
        super().__init__(timeout=timeout)
        self._consumer = result_consumer
        self._options = options
        self.add_item(self._Select(options))

    class _Select(discord.ui.Select):
        def __init__(self, options: Dict[str, T]):
            select_options = [
                discord.SelectOption(label=label, value=label)
                for label in options.keys()
            ]
            super().__init__(placeholder="Choose an option...", options=select_options)
            self._options = options

        async def callback(self, interaction: discord.Interaction):
            selected_label = self.values[0]
            value = self._options[selected_label]
            await interaction.response.defer()

            result = self.view._consumer(value)
            if result is not None:
                await result
            self.view.stop()