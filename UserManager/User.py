from typing import List

import discord

from DataClasses.UserConfig import UserConfig
from FileManager.FileManagerShard import FileManagerShard
from RoleManagement.RoleGroup import RoleGroup
from RoleManagement.RoleWrapper import RoleWrapper


class User:
    def __init__(self, member: discord.Member, user_config: UserConfig, file_manager_shard: FileManagerShard):
        if not isinstance(member, discord.Member):
            raise TypeError(f"Member is of the wrong type. It is type {type(member)}.")

        if not isinstance(user_config, UserConfig):
            raise TypeError(f"User data is of the wrong type. It is type {type(user_config)}.")

        if not isinstance(file_manager_shard, FileManagerShard):
            raise TypeError(f"File manager shard is of the wrong type. It is type {type(file_manager_shard)}.")

        # We do not want to be reassigning any of these
        self._member = member
        self._user_config = user_config
        self._file_manager_shard = file_manager_shard

    @property
    def member(self):
        return self._member

    @property
    def id(self):
        return self._member.id

    @property
    def user_config(self):
        return self._user_config

    async def add_roles(self, role: RoleWrapper | List[RoleWrapper]):
        if not isinstance(role, list):
            roles_to_add = [role]
        else:
            roles_to_add = role

        await self._member.add_roles(*(r.raw for r in roles_to_add))
        self._user_config.roles.extend(roles_to_add)

    async def remove_roles(self, role: RoleWrapper | List[RoleWrapper]):
        if not isinstance(role, list):
            roles_to_remove = [role]
        else:
            roles_to_remove = role
        await self._member.remove_roles(*(r.raw for r in roles_to_remove))
        for r in roles_to_remove:
            self._user_config.roles.remove(r)

    async def sync_roles(self):
        desired_roles: List[RoleWrapper] = self._user_config.roles
        if desired_roles is None:
            desired_roles = []
        desired_raw_roles = set(r.raw for r in desired_roles)

        all_group_roles = set()
        for cls in RoleGroup.__subclasses__():
            for role_wrapper in cls._role_lookup.values():
                all_group_roles.add(role_wrapper.raw)

        current_group_roles = set(member_role for member_role in self._member.roles if member_role in all_group_roles)

        to_add = desired_raw_roles - current_group_roles
        to_remove = current_group_roles - desired_raw_roles

        if to_add:
            await self._member.add_roles(*to_add)
        if to_remove:
            await self._member.remove_roles(*to_remove)

    async def update_info(self):
        await self._file_manager_shard.write(self._user_config, False)