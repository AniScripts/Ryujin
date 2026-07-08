import discord
from discord.ext import commands
from discord import app_commands
import os
from cogs.utils.base import RyujinCog

class ExtensionsListCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(
        name="extensions_list",
        description="Shows all the available extensions for After Effects"
    )
    async def extensions_list(self, interaction: discord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        subfolders = os.listdir("resources/extensions")
        subfolders = [folder.replace("_", " ") for folder in subfolders]
        subfolders.sort()
        files = "\n".join(f"**{i+1}**. {folder}" for i, folder in enumerate(subfolders))
        embed = discord.Embed(title="Extensions List")
        embed.description = files
        embed.add_field(name="How to use the command?", value="\n Example:\nIf you want to download `Flow Script`, you can just use: **/extension 1**.")
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Resources System",
            icon_url=self.logo
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.bot.maybe_send_ad(interaction)

async def setup(bot):
    await bot.add_cog(ExtensionsListCog(bot)) 