import discord
from discord.ext import commands
from discord import app_commands
import os
import random
from cogs.utils.base import RyujinCog

class OverlayCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="overlay",
        description="Sends a random overlay!",
    )
    async def overlay(self, interaction: discord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        assets = [f for f in os.listdir("resources/overlays") if f.endswith(".mp4")]
        if not assets:
            await interaction.response.send_message("No overlays found.", ephemeral=True)
            return

        asset = random.choice(assets)
        file_path = os.path.join("resources/overlays", asset)
        
        button_view = AnotherButton()
        await self.bot.maybe_send_ad(interaction)
        await interaction.response.send_message(file=discord.File(file_path), view=button_view, ephemeral=True)

class AnotherButton(discord.ui.View):
    def __init__(self):
        super().__init__()
    @discord.ui.button(label="Another One 👀", style=discord.ButtonStyle.gray)
    async def create_ronde(self, button: discord.ui.Button, interaction: discord.Interaction):
        global current_overlay
        assets = [f for f in os.listdir("resources/overlays") if f.endswith(".mp4")]
        new_overlay = random.choice(assets)
        while new_overlay == current_overlay:
            new_overlay = random.choice(assets)
        current_overlay = new_overlay
        file_path = os.path.join("resources/overlays", current_overlay)
        await interaction.response.edit_message(file=discord.File(file_path))

async def setup(bot):
    await bot.add_cog(OverlayCog(bot))
