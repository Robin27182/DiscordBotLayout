from dataclasses import fields

import discord

from DataClasses.UserConfig import UserConfig
from FileManager.FileManager import FileManager
from FileManager.FileManagerShard import FileManagerShard
from UserManager.User import User


class UserManager:
    def __init__(self, guild: discord.Guild, user_file_manager: FileManager):
        self.guild = guild
        self.file_manager = user_file_manager
        self.user_list = []

    async def create_user(self, member: discord.Member):
        if not isinstance(member, discord.Member):
            raise TypeError(f"member is not of the right type, it is type {type(member)}")

        # Check for existing files
        filename = str(member.id)
        if await self.file_manager.exist(filename, give_error=False):
            user_config = await self.file_manager.read(filename)
        else:
            user_config = UserConfig(**{
                f.name: (member.name if f.name == "username" else None)
                for f in fields(UserConfig)
            })
            await self.file_manager.write(filename, user_config, True)

        shard = FileManagerShard(self.file_manager, filename)
        self.user_list.append(User(member, user_config, shard))
        return None

    async def create_all_users(self):
        for member in self.guild.members:
            await self.create_user(member)

