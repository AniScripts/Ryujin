import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands
from pytube.innertube import _default_clients

from cogs.utils.db import initialize_database, get_blacklist
from cogs.utils.constants import RYUJIN_LOGO
from cogs.utils.helpers import maybe_send_ad

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

TOKEN = os.getenv("RYUJIN_TOKEN")
if not TOKEN:
    print("ERROR: RYUJIN_TOKEN not set in .env")
    sys.exit(1)

connection = initialize_database()
blacklist = get_blacklist(connection) if connection else {}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="+", intents=intents)
bot.blacklist = blacklist
bot.connection = connection
bot.RYUJIN_LOGO = RYUJIN_LOGO
bot.welcome_leave_channel = os.getenv("WELCOME_LEAVE_CHANNEL_ID", "0")
bot.maybe_send_ad = lambda i: maybe_send_ad(bot, i)


async def load_cogs():
    cog_dirs = ["cogs/commands", "cogs/events"]
    for base_dir in cog_dirs:
        for folder in os.listdir(base_dir):
            folder_path = os.path.join(base_dir, folder)
            if os.path.isdir(folder_path):
                for file in os.listdir(folder_path):
                    if file.endswith(".py") and not file.startswith("__"):
                        ext = f"{base_dir.replace(os.sep, '.')}.{folder}.{file[:-3]}"
                        await bot.load_extension(ext)
                        print(f"  Loaded: {ext}")


async def main():
    await load_cogs()

    print(f"\nSyncing {len(bot.tree.get_commands())} commands globally...")
    synced = await bot.tree.sync()
    print(f"Done. {len(synced)} commands registered globally.")

    await bot.close()


asyncio.run(main())
