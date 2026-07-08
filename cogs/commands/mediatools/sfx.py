import nextcord
from nextcord.ext import commands
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


    @nextcord.slash_command(
        name="sfx",
        description="Sends a random SFX!",
    )
    async def sfx(self, interaction: nextcord.Interaction, category: str):
        if await self.blacklist_guard(interaction):
            return

        if category not in self.sfxcategories:
            await interaction.send(f"**The category `{category}` was not found! Please use `/sfx_categories` to see the categories available.**")
            return

        assets = [f for f in os.listdir(f"resources/sfx/{category}") if f.endswith(".mp3")]
        asset = random.choice(assets)
        file_path = os.path.join(f"resources/sfx/{category}", asset)
        await self.bot.maybe_send_ad(interaction)
        await interaction.send(file=nextcord.File(file_path), ephemeral=True)

def setup(bot):
    bot.add_cog(SfxCog(bot)) 