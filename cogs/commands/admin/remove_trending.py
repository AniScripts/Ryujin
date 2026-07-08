import discord
from discord.ext import commands
from discord import app_commands
import json
from cogs.utils.base import RyujinCog

class RemoveTrendingCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(
        name="remove_trending",
        description="Remove a trending item (Moongetsu only)",
        guild_ids=[1060144274722787328]
    )
    async def remove_trending(
        self,
        interaction: discord.Interaction,
        type: str,
        name: str):
        if interaction.user.id != 977190163736322088:
            await interaction.response.send_message("This command is only for moongetsu!", ephemeral=True)
            return

        try:
            with open('data/trending.json', 'r') as f:
                data = json.load(f)
            
            if type == "song":
                data["Songs"] = [s for s in data["Songs"] if s["name"] != name]
                item_type = "song"
            else:
                data["Animes"] = [a for a in data["Animes"] if a["name"] != name]
                item_type = "anime"
            
            with open('data/trending.json', 'w') as f:
                json.dump(data, f, indent=4)
                
            await interaction.response.send_message(f"Removed {item_type} **{name}** from trending!", ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(f"Error removing item: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(RemoveTrendingCog(bot)) 