from abc import ABCMeta, ABC

import discord

from RoleManagement.RoleWrapper import RoleWrapper


class RoleMeta(ABCMeta):
    """Allows MarchingRole to be iterable"""
    def __iter__(cls):
        for attr in cls._roles:
            yield getattr(cls, attr)

class RoleGroup(ABC, metaclass=RoleMeta):
    """
    This is an abstract class. DO NOT MAKE AN INSTANCE OF THIS
    The metaclass just allows inheriting instances to be iterable.
    All inheriting classes are expected to have _roles, and the class variables associated
    _roles follows the format "Name in class": "Name that discord can find"
    """

    @classmethod
    def resolve_roles(cls, guild: discord.Guild) -> None:
        for attr_name, role_name in cls._roles.items():
            role = discord.utils.get(guild.roles, name=role_name)
            if role is None:
                raise ValueError(f"Role '{role_name}' not found in guild.")
            wrapped = RoleWrapper(cls, role, role_name)
            setattr(cls, attr_name, wrapped)
        cls._role_lookup = {getattr(cls, attr).name.lower(): getattr(cls, attr) for attr in cls._roles}

    @classmethod
    def get_role_by_name(cls, name: str, give_error=True) -> RoleWrapper | None:
        if cls._role_lookup is None:
            raise RuntimeError(f"{cls.__name__} roles not resolved yet")
        if name not in cls._role_lookup:
            if give_error:
                raise RuntimeError(f"Role {name} is not and available role in {cls.__name__}")
            return None
        return cls._role_lookup.get(name)

    @classmethod
    def get_name_by_role(cls, role: RoleWrapper, give_error=True) -> RoleWrapper | None:
        if cls._role_lookup is None:
            raise RuntimeError(f"{cls.__name__} roles not resolved yet")
        if role.name not in cls._role_lookup.__reversed__():
            if give_error:
                raise RuntimeError(f"Role {role.name} is not and available role in {cls.__name__}")
            return None
        return cls._role_lookup.__reversed__().get(role.name)