import discord
from cogs.utils.base import RyujinCog
from cogs.utils.helpers import GenerateHashtagsModal


class GenerateTagsCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="generatetags",
        description="Generate hashtags for anime/character"
    )
    async def generatetags(self, interaction: discord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        modal = GenerateHashtagsModal(self.bot)
        await interaction.response.send_modal(modal)
        await self.bot.maybe_send_ad(interaction)


async def setup(bot):
    await bot.add_cog(GenerateTagsCog(bot))
