import discord
from discord.ext import commands
from discord import app_commands
import os
import random
from cogs.utils.base import RyujinCog

class SfxCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
        self.sfxcategories = {
            "dragonball": "dragonball",
            "fireforce": "fireforce",
            "naruto": "naruto",
            "whooshes": "whooshes",
            "random": "random"
        }


    @app_commands.command(
        name="sfx",
        description="Sends a random SFX!",
    )
    async def sfx(self, interaction: discord.Interaction, category: str):
        if await self.blacklist_guard(interaction):
            return

        if category not in self.sfxcategories:
            await interaction.response.send_message(f"**The category `{category}` was not found! Please use `/sfx_categories` to see the categories available.**")
            return

        assets = [f for f in os.listdir(f"resources/sfx/{category}") if f.endswith(".mp3")]
        asset = random.choice(assets)
        file_path = os.path.join(f"resources/sfx/{category}", asset)
        await self.bot.maybe_send_ad(interaction)
        await interaction.response.send_message(file=discord.File(file_path), ephemeral=True)

async def setup(bot):
    await bot.add_cog(SfxCog(bot)) 