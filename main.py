import asyncio

import discord
from discord import Member
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from pathlib import Path

from DataClasses.BotConfig import BotConfig
from DataInterpreter.BotConfigInterpreter import BotConfigInterpreter
from DataInterpreter.UserConfigInterpreter import UserConfigInterpreter
from FileManager.FileInterpreterABC import FileInterpreterABC
from FileManager.FileManager import FileManager
from UserManager.UserManager import UserManager

current_dir = Path(__file__).parent.resolve()
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

discord_token: str = os.getenv("DISCORD_TOKEN")
guild_id: int = int(os.getenv("GUILD_ID"))

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Will be assigned on_ready
guild = None
user_manager = None
bot_config = None

user_config_manager = FileManager(UserConfigInterpreter(), base_dir=(current_dir / "DataStorage" / "UserConfig"))
bot_config_manager = FileManager(BotConfigInterpreter(), base_dir=(current_dir / "DataStorage" / "BotConfig"))

@bot.event
async def on_ready():
    global guild
    global user_manager
    global bot_config

    guild = bot.get_guild(guild_id)


    if await bot_config_manager.exist(str(guild_id), False):
        bot_config = await bot_config_manager.read(str(guild_id))
    else:
        bot_config = BotConfig("Data")
        await bot_config_manager.write(str(guild_id), bot_config, True)

    user_manager = UserManager(guild, user_config_manager)
    await user_manager.create_all_users()
    print(bot_config.data)


bot.run(discord_token, log_handler=handler, log_level=logging.DEBUG)