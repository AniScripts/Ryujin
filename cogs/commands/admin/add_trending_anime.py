import nextcord
from nextcord.ext import commands
import json
from cogs.utils.base import RyujinCog

class AddTrendingAnimeCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="add_trending_anime",
        description="Add a trending anime (Moongetsu only)",
        guild_ids=[1060144274722787328]
    )
    async def add_trending_anime(
        self,
        interaction: nextcord.Interaction,
        name: str = nextcord.SlashOption(description="Anime name")
    ):
        if await self.blacklist_guard(interaction):
            return

        if interaction.user.id != 977190163736322088:
            await interaction.send("This command is only for moongetsu!", ephemeral=True)
            return

        try:
            with open('data/trending.json', 'r') as f:
                data = json.load(f)
            
            new_anime = {
                "name": name
            }
            
            data["Animes"].append(new_anime)
            
            with open('data/trending.json', 'w') as f:
                json.dump(data, f, indent=4)
                
            await self.bot.maybe_send_ad(interaction)
            await interaction.send(f"Added anime **{name}** to trending!", ephemeral=True)
            
        except Exception as e:
            await interaction.send(f"Error adding anime: {str(e)}", ephemeral=True)

def setup(bot):
    bot.add_cog(AddTrendingAnimeCog(bot)) 