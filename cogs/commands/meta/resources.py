import discord
from discord.ext import commands
from discord import app_commands
import os
from cogs.utils.base import RyujinCog

class ResourcesCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="resources",
        description="See the editing resources that the bot has.",
    )
    async def resources(self, interaction: discord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        overlays = len([f for f in os.listdir("resources/overlays") if f.endswith(".mp4")])
        edit_audios_categories = len(os.listdir("resources/edit audios"))
        with open("edits.txt", "r") as f:
            edits = len(f.read().strip().split("\n"))
        
        stats = discord.Embed(title="Resources", description=f"**Number of resouces that `Ryujin Editing Bot` has:**\n\n**Overlays:** {overlays}\n**Edit audios categories:** {edit_audios_categories}\n**Edits:** {edits}")
        stats.set_footer(
            text="© Ryujin Bot (2023-2025) | Information System",
            icon_url=self.logo
        )
        stats.set_author(name="Ryujin", icon_url=self.logo)
        
        await self.bot.maybe_send_ad(interaction)
        await interaction.response.send_message(embed=stats, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ResourcesCog(bot)) 