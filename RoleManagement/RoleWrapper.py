import discord


class RoleWrapper:
    """
    Simple wrapper class for the discord.Role object
    TO WORK WITH DISCORD API, CALL .raw
    """
    def __init__(self, category, role: discord.Role, name: str) -> None:
        self._role = role
        self.name = name
        self.category = category

    def __getattr__(self, attr):
        return getattr(self._role, attr)

    def __str__(self):
        return str(self._role)

    @property
    def raw(self):
        return self._role
