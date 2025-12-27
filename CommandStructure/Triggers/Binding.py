from CommandStructure.Triggers.Trigger import Trigger


class SlashBinding(Trigger):
    def __init__(self, name, description):
        """
        Bindings are specifically for emitting via direct human input
        :param name: The name Discord sees when trying to use a command.
        :param description: The description Discord sees when trying to use a command.
        """
        super().__init__()
        self.name = name
        self.description = description

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description