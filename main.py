from functools import partial
from typing import List, Tuple

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from pathlib import Path

from BotCommands.Example.LogInChannel import LogInChannel
from BotCommands.Example.FavoriteOption import FavoriteOption
from BotCommands.Example.Hello import Hello
from CommandStructure.Authorizers import Authorizer, on_command_name, accept_all
from CommandStructure.DiscordCommandManager import DiscordCommandManager
from CommandStructure.Dispatcher import Dispatcher
from CommandStructure.Triggers.SlashBinding import SlashBinding
from DataClasses.CommandProtocol import Command
from CommandTools.CommandBuilder import CommandBuilder
from DataClasses.CommandData import CommandData
from DataClasses.BotConfig import BotConfig
from FileManager.DataInterpreter.BotConfigInterpreter import BotConfigInterpreter
from FileManager.DataInterpreter.UserConfigInterpreter import UserConfigInterpreter
from FileManager.FileManager import FileManager
from RoleManagement.RoleGroup import RoleGroup
from UserManager.User import User
from UserManager.UserManager import UserManager

current_dir = Path(__file__).parent.resolve()
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

discord_token: str = os.getenv("DISCORD_TOKEN")
guild_id: int = int(os.getenv("GUILD_ID"))

handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot declaration
bot = commands.Bot(command_prefix='/', intents=intents)
bot_tree = bot.tree

# Will be assigned in on_ready
guild: discord.Guild | None = None
bot_config: BotConfig | None = None
user_manager: UserManager | None = None
discord_command_manager: DiscordCommandManager | None = None

# File managers
user_config_manager = FileManager(UserConfigInterpreter(), base_dir=(current_dir / "DataStorage" / "UserConfig"))
bot_config_manager = FileManager(BotConfigInterpreter(), base_dir=(current_dir / "DataStorage" / "BotConfig"))
command_info: List[Tuple[CommandBuilder, Authorizer]] = [
    (CommandBuilder(FavoriteOption).with_args(["a", "b", "c"]),
     partial(on_command_name, command_name="choose-letter")),

    (CommandBuilder(Hello).with_args(),
     partial(on_command_name, command_name="hello")),

    (CommandBuilder(LogInChannel).with_args(1432914622402269308),
     accept_all)
]
slash_bindings: List[SlashBinding] = [
    SlashBinding("choose-letter", "Choose your favorite letter!"),
    SlashBinding("hello", "Say hello to the bot!"),
    SlashBinding("hello-cycle", "Say hello way too much")
]
@bot.event
async def on_ready():
    """
    Resolves, all Role Group Enums, Creates Bot Config, Creates User Manager,
    Creates & Syncs Users, Initiates Enabled Commands
    """
    global guild
    global user_manager
    global bot_config

    guild = bot.get_guild(guild_id)

    # Resolve all Role Group Enums
    for group in RoleGroup.__subclasses__():
        group.resolve_roles(guild)

    # Create Bot Config
    if await bot_config_manager.exist(str(guild_id), False):
        bot_config = await bot_config_manager.read(str(guild_id))
    else:
        bot_config = BotConfig("Data")
        await bot_config_manager.write(str(guild_id), bot_config, True)


    # Create User Manager
    user_manager = UserManager(guild, user_config_manager)
    # Create & Sync Users
    await user_manager.create_all_users()
    for user in user_manager.user_list:
        await user.sync_roles()

    # Initialize data for commands
    command_data = CommandData(user_manager, guild)
    dispatcher = Dispatcher()
    # Initialize commands
    discord_command_manager = DiscordCommandManager(bot_tree, guild)

    for command_builder, authorizer in command_info:
        command_instance: Command = command_builder.with_data(command_data).build()
        dispatcher.register(command_instance, authorizer)

    for binding in slash_bindings:
        discord_command_manager.register_binding(binding)

    await bot.tree.sync(guild=guild)
    print("Successfully Initialized")

@bot.event
async def on_member_update(member_before: discord.Member, member_after: discord.Member):
    """
    Ensures that when a user changes a role, that it is changed back as needed
    """
    user: User = user_manager.get_user_from_member(member_before)
    await user.sync_roles()


bot.run(discord_token, log_handler=handler, log_level=logging.DEBUG)