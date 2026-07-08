import nextcord
from nextcord.ext import commands
import os
import json
from cogs.utils.base import RyujinCog

class ProjectFileCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    @nextcord.slash_command(
        name="project_file",
        description="Sends a project file and a preview link.",
    )
    async def project_file(self, interaction: nextcord.Interaction, project_number: int):
        if await self.blacklist_guard(interaction):
            return

        project_files_dir = "resources/project_files"
        
        with open("data/project_files.json", "r") as json_file:
            project_files = json.load(json_file)
        
        try:
            project_name = project_files.get(str(project_number))
        except KeyError:
            return await interaction.send(f"No project file found with number {project_number}.", ephemeral=True)
        
        project_path = os.path.join(project_files_dir, project_name.replace(" ", "_"))
        
        if os.path.exists(project_path):
            aep_file = None
            preview_link = None
            
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith(".aep"):
                        aep_file = os.path.join(root, file)
                    if file == "preview.txt":
                        with open(os.path.join(root, file), "r") as f:
                            preview_link = f.read().strip()
            
            if aep_file and preview_link:
                await interaction.send(f"{preview_link}", file=nextcord.File(aep_file), ephemeral=True)
                await self.bot.maybe_send_ad(interaction)
            else:
                await interaction.send(f"Project file or preview link not found for {project_name}.", ephemeral=True)
        else:
            await interaction.send(f"The specified project files for {project_name} do not exist.", ephemeral=True)

def setup(bot):
    bot.add_cog(ProjectFileCog(bot)) 