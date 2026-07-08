import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.base import RyujinCog

class SfxCategoriesCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
        self.sfxcategories = {
            "dragonball": "dragonball",
            "fireforce": "fireforce",
            "naruto": "naruto",
            "whooshes": "whooshes",
            "random": "random"
        }


    @app_commands.command(
        name="sfx_categories",
        description="See the SFX categories.",
    )
    async def sfx_categories(self, interaction: discord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        embed = discord.Embed(title="SFX Categories")
        embed.description = "\n".join(self.sfxcategories)
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Media Tools System",
            icon_url=self.logo
        )
        await self.bot.maybe_send_ad(interaction)
        await interaction.response.send_message("Have some SFX?\n**Please join our discord server!** https://discord.gg/FSjRSaJ4bt", embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(SfxCategoriesCog(bot)) 