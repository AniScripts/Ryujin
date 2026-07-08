import nextcord
from nextcord.ext import commands
import os
import random
from cogs.utils.base import RyujinCog

class OverlayCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="overlay",
        description="Sends a random overlay!",
    )
    async def overlay(self, interaction: nextcord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        assets = [f for f in os.listdir("resources/overlays") if f.endswith(".mp4")]
        if not assets:
            await interaction.send("No overlays found.", ephemeral=True)
            return

        asset = random.choice(assets)
        file_path = os.path.join("resources/overlays", asset)
        
        button_view = AnotherButton()
        await self.bot.maybe_send_ad(interaction)
        await interaction.send(file=nextcord.File(file_path), view=button_view, ephemeral=True)

class AnotherButton(nextcord.ui.View):
    def __init__(self):
        super().__init__()
    @nextcord.ui.button(label="Another One 👀", style=nextcord.ButtonStyle.gray)
    async def create_ronde(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        global current_overlay
        assets = [f for f in os.listdir("resources/overlays") if f.endswith(".mp4")]
        new_overlay = random.choice(assets)
        while new_overlay == current_overlay:
            new_overlay = random.choice(assets)
        current_overlay = new_overlay
        file_path = os.path.join("resources/overlays", current_overlay)
        await interaction.response.edit_message(file=nextcord.File(file_path))

def setup(bot):
    bot.add_cog(OverlayCog(bot))
