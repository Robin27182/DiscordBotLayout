import discord
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from pathlib import Path

from BotCommands.GetJsonFile import GetJsonFile
from BotCommands.Hello import Hello
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
guild = None
user_manager: UserManager = None
bot_config = None

# File managers
user_config_manager = FileManager(UserConfigInterpreter(), base_dir=(current_dir / "DataStorage" / "UserConfig"))
bot_config_manager = FileManager(BotConfigInterpreter(), base_dir=(current_dir / "DataStorage" / "BotConfig"))

# Commands that are enabled
enabled_commands = [GetJsonFile,
                    Hello]

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

    # Init Commands
    GetJsonFile(user_manager)

    # Initiate Enabled Commands
    for command in enabled_commands:
        execute = (app_commands.guilds(guild)(command.execute(command())))
        bot_tree.command(name=command.__name__.lower(), description=command.get_description(command()))(execute)

    await bot.tree.sync(guild=guild)

@bot.event
async def on_member_update(member_before: discord.Member, member_after: discord.Member):
    """
    Ensures that when a user changes a role, that it is changed back as needed
    """
    user: User = user_manager.get_user_from_member(member_before)
    await user.sync_roles()


bot.run(discord_token, log_handler=handler, log_level=logging.DEBUG)