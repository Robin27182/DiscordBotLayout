from typing import List, Coroutine, Callable

import discord
from discord import app_commands, Guild
from discord.ext.commands import Bot

from CommandStructure.Triggers import SlashBinding
from CommandStructure.Triggers.SlashBinding import SlashBinding
from DataClasses.EventContext import EventContext
from DataClasses.EventType import EventType


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DiscordCommandManager:
    def __init__(self, bot_tree: Bot.tree, guild: Guild):
        self.tree = bot_tree
        self.guild = guild
        self.current_bindings: List[SlashBinding] = []

    def register_binding(self, binding: SlashBinding):
        self.current_bindings.append(binding)
        async def callback(interaction: discord.Interaction):
            context = EventContext(event_type=EventType.USER_COMMAND,
                                       interaction=interaction,
                                       )
            await binding.emit(context)

        callback: Callable[[discord.Interaction], Coroutine] = callback
        execute = app_commands.guilds(self.guild)(callback)

        self.tree.command(
            name=binding.get_name(),
            description=binding.get_description()
        )(execute)

    def remove_binding(self, binding: SlashBinding):
        for current_binding in self.current_bindings:
            if current_binding == binding:
                self.current_bindings.remove(current_binding)
                return

    def update_tree(self):
        self.tree.sync(guild=guild)