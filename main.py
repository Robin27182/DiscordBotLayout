from typing import List, Callable, Coroutine, Tuple, Any

import discord
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from pathlib import Path

from BotCommands.GetJsonFile import GetJsonFile
from CommandStructure.Authorizers.AOnCommandName import AOnCommandName
from CommandStructure.Authorizers.AOnId import AOnId
from CommandStructure.Authorizers.AOr import AOr
from CommandStructure.Authorizers.Authorizer import Authorizer
from CommandStructure.Dispatcher import Dispatcher
from DataClasses.CommandProtocol import Command
from DataClasses.EventContext import EventContext
from DataClasses.EventType import EventType
from CommandStructure.Triggers.Binding import SlashBinding
from CommandTools.CommandBuilder import CommandBuilder
from DataClasses.CommandData import CommandData
from BotCommands.FavoriteOption import FavoriteOption
from BotCommands.Hello import Hello
from BotCommands.StartHelloCycle import StartHelloCycle
from DataClasses.BotConfig import BotConfig
from DataInterpreter.BotConfigInterpreter import BotConfigInterpreter
from DataInterpreter.UserConfigInterpreter import UserConfigInterpreter
from FileManager.FileManager import FileManager
from RoleManagement.RoleGroup import RoleGroup
from UserManager.User import User
from UserManager.UserManager import UserManager

current_dir = Path(__file__).parent.resolve()
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

discord_token: str = os.getenv("DISCORD_TOKEN")
guild_id: int = int(os.getenv("GUILD_ID"))

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot declaration
bot = commands.Bot(command_prefix='/', intents=intents)
bot_tree = bot.tree

# Will be assigned in on_ready
guild: discord.Guild | None = None
user_manager: UserManager | None = None
bot_config: BotConfig | None = None

# File managers
user_config_manager = FileManager(UserConfigInterpreter(), base_dir=(current_dir / "DataStorage" / "UserConfig"))
bot_config_manager = FileManager(BotConfigInterpreter(), base_dir=(current_dir / "DataStorage" / "BotConfig"))

# Commands that are enabled (| Any is added to shut up the warnings)
command_info: List[Tuple[CommandBuilder, Authorizer | Any, SlashBinding]] = [
    (CommandBuilder(FavoriteOption).with_args(["a", "b", "c"]),
     AOnCommandName("choose-letter"),
     SlashBinding("choose-letter", "Choose your favorite letter!")),

    (CommandBuilder(Hello).with_args(),
     AOnCommandName("hello"),
     SlashBinding("hello", "Say hello to the bot!")),

    (CommandBuilder(GetJsonFile).with_args(),
     AOnCommandName("get-json-file"),
     SlashBinding("get-json-file", "Get your personalized Json file!")),

    (CommandBuilder(StartHelloCycle).with_args(),
     AOr(AOnCommandName("hello-cycle"), AOnId(1)),
     SlashBinding("hello-cycle", "Say hello way too much"))
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
    for command_builder, authorizer, binding in command_info:
        # Create instance
        command_instance: Command = command_builder.with_data(command_data).build()
        dispatcher.register(command_instance, authorizer)
        # Discord gets really, really picky about what kind of object you give it, this is the best way to do that.
        # Takes the instance, so that the function changes with each loop, turns the function's async method into an async function.
        async def callback(interaction: discord.Interaction):
            context = EventContext(event_type=EventType.USER_COMMAND,
                                       interaction=interaction,
                                       )
            await binding.emit(context)

        callback: Callable[[discord.Interaction], Coroutine] = callback
        execute = app_commands.guilds(guild)(callback)

        bot_tree.command(
            name=binding.get_name(),
            description=binding.get_description()
        )(execute)

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