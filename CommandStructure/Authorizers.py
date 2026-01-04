from typing import runtime_checkable, Protocol, Callable, Iterable

from DataClasses.EventContext import EventContext
from DataClasses.EventType import EventType

Authorizer = Callable[[EventContext], bool]
ParamAuthorizer = Callable[[EventContext, ...], bool]
"""
There are two kinds of authorizers. Those with parameters and those without.
Parameterized: Callable[[EventContext, ...], bool]
Non-Parameterized: Callable[[EventContext], bool]

To use parameterized in the code, use partials.
"""


# Non-Parameterized
def accept_all(event_context: EventContext) -> bool:
    return True

def reject_all(event_context: EventContext) -> bool:
    return False # If you need this, you are doing something wrong.


# Parameterized
def on_command_name(event_context: EventContext, command_name: str) -> bool:
    return event_context.interaction.command.name == command_name

def on_event_type(event_context: EventContext, event_type: EventType):
    return event_context.event_type == event_type

def on_id(event_context: EventContext, event_id: int) -> bool:
    return event_context.id == event_id

# Logic operators
def all_of(event_context: EventContext, authorizers: Iterable[Authorizer]) -> bool:
    return all(authorizer(event_context) for authorizer in authorizers)

def is_not(event_context: EventContext, authorizer: Authorizer) -> bool:
    return not authorizer(event_context)

def is_none_of(event_context: EventContext, authorizers: Iterable[Authorizer]) -> bool:
    return not any(authorizer(event_context) for authorizer in authorizers)

def is_any_of(event_context: EventContext, authorizers: Iterable[Authorizer]) -> bool:
    return any(authorizer(event_context) for authorizer in authorizers)