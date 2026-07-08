import discord
from discord.ext import commands
import os
import json
import platform
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv
from pytube.innertube import _default_clients

from cogs.utils.db import initialize_database, get_blacklist
from cogs.utils.constants import RYUJIN_LOGO
from cogs.utils.helpers import maybe_send_ad

load_dotenv()

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

os.makedirs("logs", exist_ok=True)
os.makedirs("temp", exist_ok=True)
os.makedirs("data", exist_ok=True)

log_file_name = f"logs/bot_logs_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
logging.basicConfig(filename=log_file_name, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATA_DEFAULTS = {
    "messages.json": {"Info": {"channel_id": "", "message_id": ""}, "Servers": {"channel_id": "", "message_id": ""}},
    "trending.json": {"Animes": [], "Songs": []},
    "afk.json": {},
}

for filename, default in DATA_DEFAULTS.items():
    path = os.path.join("data", filename)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f, indent=4)
        print(f"Created default {path}")

connection = initialize_database()
blacklist = {}
if connection:
    blacklist = get_blacklist(connection)
else:
    print("Warning: Database connection failed. Bot will run without database features.")

TOKEN = os.getenv("RYUJIN_TOKEN", "your_bot_token_here")
WELCOME_LEAVE_CHANNEL = os.getenv("WELCOME_LEAVE_CHANNEL_ID", "0")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="+", intents=intents)

bot.blacklist = blacklist
bot.connection = connection
bot.RYUJIN_LOGO = RYUJIN_LOGO
bot.welcome_leave_channel = WELCOME_LEAVE_CHANNEL
bot.maybe_send_ad = lambda interaction: maybe_send_ad(bot, interaction)


@bot.event
async def on_ready():
    bot.start_time = datetime.now()

    print("\n" + "=" * 100)
    print(f"{'RYUJIN BOT STARTUP':^100}")
    print("=" * 100 + "\n")

    print(f"Connected as {bot.user.name} (ID: {bot.user.id})")
    print(f"Running Python {platform.python_version()} | discord.py {discord.__version__}")
    print(f"OS: {platform.system()} {platform.release()}")
    print("\n" + "=" * 100 + "\n")
    print("Bot startup completed successfully!")


async def setup_hook():
    print("Starting cog loading process...")

    cog_dirs = ["cogs/commands", "cogs/events"]
    for base_dir in cog_dirs:
        for folder in os.listdir(base_dir):
            folder_path = os.path.join(base_dir, folder)
            if os.path.isdir(folder_path):
                print(f"\nProcessing folder: {folder}")
                for file in os.listdir(folder_path):
                    if file.endswith(".py") and not file.startswith("__"):
                        extension_name = f"{base_dir.replace('/', '.')}.{folder}.{file[:-3]}"
                        try:
                            print(f"  Loading: {extension_name}")
                            await bot.load_extension(extension_name)
                            print(f"  Successfully loaded: {extension_name}")
                        except Exception as e:
                            print(f"  Failed to load: {extension_name}")
                            print(f"    Error: {e}")
                            import traceback
                            traceback.print_exc()

    print("Syncing slash commands with Discord...")
    try:
        await bot.tree.sync()
        print("Slash commands synced successfully!")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")


bot.setup_hook = setup_hook
bot.run(TOKEN)
