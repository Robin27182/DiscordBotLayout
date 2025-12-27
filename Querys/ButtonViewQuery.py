from functools import partial
from typing import Callable, TypeVar, Awaitable

import discord

T = TypeVar("T")
class ButtonViewQuery(discord.ui.View):
    def __init__(
        self,
        options: dict[str, T],
        result_consumer: Callable[[T], None | Awaitable[None]],
        timeout: float = 20,
    ) -> None:
        """
        A View that presents buttons for the user to choose from.

        :param options: A dictionary mapping button labels to return values.
        :param result_consumer: Function called with the chosen value.
        :param timeout: How long to wait for a response before timing out.
        """
        super().__init__(timeout=timeout)
        self._consumer = result_consumer

        for label, value in options.items():
            button = discord.ui.Button(label=label, style=discord.ButtonStyle.gray)
            button.callback = partial(self._handle_selection, value=value)
            self.add_item(button)

    async def _handle_selection(self, interaction: discord.Interaction, value: T) -> None:
        await interaction.response.defer()
        self.stop()

        result = self._consumer(value)
        if result is not None:
            await result
