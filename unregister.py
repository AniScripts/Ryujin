import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands
from pytube.innertube import _default_clients

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

TOKEN = os.getenv("RYUJIN_TOKEN")
if not TOKEN:
    print("ERROR: RYUJIN_TOKEN not set in .env")
    sys.exit(1)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="+", intents=intents)


async def main():
    async with bot:
        print("Clearing all global commands...")
        data = await bot.http.bulk_upsert_global_commands(bot.application_id, [])
        print(f"Done. All commands removed.")
        await bot.close()

asyncio.run(main())
