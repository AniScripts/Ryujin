import nextcord
from nextcord.ext import commands
import os
import json
from cogs.utils.base import RyujinCog

class ScriptCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    @nextcord.slash_command(
        name="script",
        description="Sends a script for After Effects.",
    )
    async def script(self, interaction: nextcord.Interaction, script_number: int):
        if await self.blacklist_guard(interaction):
            return

        script_files_dir = "resources/scripts"
        
        with open("data/scripts.json", "r") as json_file:
            script_files = json.load(json_file)
        
        try:
            script_name = script_files.get(str(script_number))
        except KeyError:
            return await interaction.send(f"No script found with number {script_number}.", ephemeral=True)

        script_path = os.path.join(script_files_dir, script_name.replace(" ", "_"))

        if os.path.exists(script_path):
            script_file = None
            preview_link = None
            
            for root, dirs, files in os.walk(script_path):
                for file in files:
                    if file.endswith(("jsx", ".jsxbin", "zip", "rar")):
                        script_file = os.path.join(root, file)
                    if file == "preview.txt":
                        with open(os.path.join(root, file), "r") as f:
                            preview_link = f.read().strip()

            if script_file and preview_link:
                await interaction.send(f"{preview_link}", file=nextcord.File(script_file), ephemeral=True)
                await self.bot.maybe_send_ad(interaction)
            else:
                await interaction.send(f"Script file or preview link not found for {script_name}.", ephemeral=True)
        else:
            await interaction.send(f"The specified script file for {script_name} does not exist.", ephemeral=True)

def setup(bot):
    bot.add_cog(ScriptCog(bot)) 