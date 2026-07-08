import discord
from discord.ext import commands
from discord import app_commands
import json
from cogs.utils.base import RyujinCog

class TrendingCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="trending",
        description="See what's trending in AMV Community!"
    )
    async def trending(self, interaction: discord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        try:
            with open('data/trending.json', 'r') as f:
                trending_data = json.load(f)
            
            description = "Here's what's currently trending in the AMV community:\n\n"
            description += "🎵 **Trending Songs in AMVs**\n"
            
            for song in trending_data["Songs"]:
                description += f"» **{song['name']}**\n"
                description += f"Original: [YouTube]({song['link']})\n"
                description += f"Popular Edit: [YouTube]({song['popular-edit']})\n\n"
            
            description += "📺 **Trending Anime**\n"
            for anime in trending_data["Animes"]:
                description += f"» **{anime['name']}**\n"
            
            embed = discord.Embed(
                title="📈 AMV Community Trends",
                description=description,
                color=0x2a2a2a
            )
            
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Social & Community System",
                icon_url=self.logo
            )
            
            embed.set_author(
                name="Ryujin",
                icon_url=self.logo
            )
            await self.bot.maybe_send_ad(interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Error",
                description="Could not fetch trending data. Please try again later.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(TrendingCog(bot)) 