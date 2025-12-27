from dataclasses import dataclass

import discord

from UserManager import UserManager


@dataclass(frozen=True)
class CommandData:
    """
    This class is needed because some data is declared on runtime, and Commands thus need to be defined on runtime
    """
    user_manager: UserManager
    guild: discord.Guild