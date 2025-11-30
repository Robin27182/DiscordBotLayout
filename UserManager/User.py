import discord

from DataClasses.UserConfig import UserConfig
from FileManager.FileManagerShard import FileManagerShard


class User:
    def __init__(self, member: discord.member, user_config: UserConfig, file_manager_shard: FileManagerShard):
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

    async def update_info(self):
        await self._file_manager_shard.write(self._user_config, False)