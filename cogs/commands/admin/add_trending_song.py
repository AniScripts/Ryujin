import discord
from discord.ext import commands
from discord import app_commands
import json
from cogs.utils.base import RyujinCog

class AddTrendingSongCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(
        name="add_trending_song",
        description="Add a trending song (Moongetsu only)",
        guild_ids=[1060144274722787328]
    )
    async def add_trending_song(
        self,
        interaction: discord.Interaction,
        name: str,
        link: str,
        popular_edit: str):
        if interaction.user.id != 977190163736322088:
            await interaction.response.send_message("This command is only for moongetsu!", ephemeral=True)
            return

        try:
            with open('data/trending.json', 'r') as f:
                data = json.load(f)
            
            new_song = {
                "name": name,
                "link": link,
                "popular-edit": popular_edit
            }
            
            data["Songs"].append(new_song)
            
            with open('data/trending.json', 'w') as f:
                json.dump(data, f, indent=4)
                
            await interaction.response.send_message(f"Added song **{name}** to trending!", ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(f"Error adding song: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AddTrendingSongCog(bot)) 