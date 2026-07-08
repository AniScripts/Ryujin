import nextcord
from nextcord.ext import commands
import os
from cogs.utils.base import RyujinCog

class ScriptsListCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    @nextcord.slash_command(
        name="scripts_list",
        description="Shows all the available scripts for After Effects"
    )
    async def scripts_list(self, interaction: nextcord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        subfolders = os.listdir("resources/scripts")
        subfolders = [folder.replace("_", " ") for folder in subfolders]
        
        subfolders.sort()
        
        files = "\n".join(f"**{i+1}**. {folder}" for i, folder in enumerate(subfolders))
        embed = nextcord.Embed(title="Scripts List")
        embed.description = files
        embed.add_field(name="How to use the command?", value="\n Example:\nIf you want to download `Flow Script`, you can just use: **/script 1**.")
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Resources System",
            icon_url=self.logo
        )
        await interaction.send(embed=embed, ephemeral=True)
        await self.bot.maybe_send_ad(interaction)

def setup(bot):
    bot.add_cog(ScriptsListCog(bot)) 