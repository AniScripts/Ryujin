import nextcord
from nextcord.ext import commands
import os
import random
from cogs.utils.base import RyujinCog

class EditAudioCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    @nextcord.slash_command(
        name="edit_audio",
        description="Sends a random edit audio!",
    )
    async def edit_audio(self, interaction: nextcord.Interaction, category: str):
        if await self.blacklist_guard(interaction):
            return

        edit_audio_categories = {
            "dragonball": "dragonball",
            "fireforce": "fireforce", 
            "naruto": "naruto",
            "whooshes": "whooshes",
            "random": "random"
        }

        if category not in edit_audio_categories:
            await interaction.send(f"**The category `{category}` was not found! Please use `/edit_audio_categories` to see the categories available.**", ephemeral=True)
            return

        assets = [f for f in os.listdir(f"resources/edit audios/{category}") if f.endswith(".mp3")]
        if not assets:
            await interaction.send(f"No edit audios found in the `{category}` category.", ephemeral=True)
            return

        asset = random.choice(assets)
        file_path = os.path.join(f"resources/edit audios/{category}", asset)
        await interaction.send(file=nextcord.File(file_path), ephemeral=True)
        await self.bot.maybe_send_ad(interaction)

def setup(bot):
    bot.add_cog(EditAudioCog(bot)) 