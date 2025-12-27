from dataclasses import dataclass

import discord

from DataClasses import EventType


@dataclass
class EventContext:
    """
    Designed to be added upon, based on needed information.
    All fields past event_type need to default to none, because other instances can be made without that specific context
    """
    event_type: EventType
    id: int | None = None
    interaction: discord.Interaction | None = None