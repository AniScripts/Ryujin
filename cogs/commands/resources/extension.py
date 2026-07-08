import discord
from discord.ext import commands
from discord import app_commands
import os
import json
from cogs.utils.base import RyujinCog

class ExtensionCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(
        name="extension",
        description="Sends an extension for After Effects.",
    )
    async def extension(self, interaction: discord.Interaction, extension_number: int):
        if await self.blacklist_guard(interaction):
            return

        extension_files_dir = "resources/extensions"
        
        with open("data/extensions.json", "r") as json_file:
            extension_files = json.load(json_file)
        
        try:
            extension_name = extension_files.get(str(extension_number))
        except KeyError:
            return await interaction.response.send_message(f"No extension found with number {extension_number}.", ephemeral=True)

        extension_path = os.path.join(extension_files_dir, extension_name.replace(" ", "_"))

        if os.path.exists(extension_path):
            extension_file = None
            preview_link = None
            
            for root, dirs, files in os.walk(extension_path):
                for file in files:
                    if file.endswith((".zip", ".rar", ".jsx")):
                        extension_file = os.path.join(root, file)
                    if file == "preview.txt":
                        with open(os.path.join(root, file), "r") as f:
                            preview_link = f.read().strip()

            if extension_file and preview_link:
                await interaction.response.send_message(f"{preview_link}", file=discord.File(extension_file), ephemeral=True)
                await self.bot.maybe_send_ad(interaction)
            else:
                await interaction.response.send_message(f"Extension file or preview link not found for {extension_name}.", ephemeral=True)
        else:
            await interaction.response.send_message(f"The specified extension file for {extension_name} does not exist.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ExtensionCog(bot)) 