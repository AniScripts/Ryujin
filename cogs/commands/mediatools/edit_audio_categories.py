import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.base import RyujinCog

class EditAudioCategoriesCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(
        name="edit_audio_categories",
        description="See the edit audio categories.",
    )
    async def edit_audio_categories(self, interaction: discord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        edit_audio_categories = ["dragonball", "fireforce", "naruto", "whooshes", "random"]
        categories_list = "\n".join(edit_audio_categories)
        
        embed = discord.Embed(title="Edit Audio Categories")
        embed.description = categories_list
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Resources System",
            icon_url=self.logo
        )
        await interaction.response.send_message("Have some Edit Audios?\n**Please join our discord server!** https://discord.gg/FSjRSaJ4bt", embed=embed, ephemeral=True)
        await self.bot.maybe_send_ad(interaction)

async def setup(bot):
    await bot.add_cog(EditAudioCategoriesCog(bot)) 