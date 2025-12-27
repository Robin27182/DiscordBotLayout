from DataClasses.EventContext import EventContext
from DataClasses.EventType import EventType


class AOnCommandName:
    def __init__(self, command_name: str):
        """
        Authorizer that returns True if the command is a UserCommand with the name given.
        :param command_name: the name given
        """
        self.command_name = command_name

    def get_authorization(self, context: EventContext) -> bool:
        return (
                context.interaction.command.name is not None
                and context.event_type == EventType.USER_COMMAND
                and context.interaction.command.name == self.command_name
        )
