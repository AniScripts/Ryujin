import nextcord
from nextcord.ext import commands
import os
from cogs.utils.base import RyujinCog

class ProjectsListCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    @nextcord.slash_command(
        name="projects_list",
        description="Shows all the available project files"
    )
    async def projects_list(self, interaction: nextcord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        subfolders = os.listdir("resources/project_files")
        subfolders = [folder.replace("_", " ") for folder in subfolders]
        
        subfolders.sort()
        
        files = "\n".join(f"**{i+1}**. {folder}" for i, folder in enumerate(subfolders))
        embed = nextcord.Embed(title="Project Files List")
        embed.description = files
        embed.add_field(name="How to use the command?", value="\n Example:\nIf you want `AMV Flow edit (Chophurr)`, you can just use: **/project_file 1**.")
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Resources System",
            icon_url=self.logo
        )
        await interaction.send("Have some Project Files?\n**Please join our discord server!** https://discord.gg/FSjRSaJ4bt", embed=embed, ephemeral=True)
        await self.bot.maybe_send_ad(interaction)

def setup(bot):
    bot.add_cog(ProjectsListCog(bot)) 