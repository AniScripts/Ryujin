import discord
from discord.ext import commands

from cogs.utils.constants import RYUJIN_LOGO


class RyujinCog(commands.Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def logo(self):
        return RYUJIN_LOGO

    def is_blacklisted(self, user_id):
        if hasattr(self.bot, 'blacklist') and user_id in self.bot.blacklist:
            return True, self.bot.blacklist[user_id]
        return False, None

    def blacklist_embed(self, reason):
        embed = discord.Embed(
            title="You are blacklisted!",
            description=f"**You can't use Ryujin's commands anymore because you have been blacklisted for `{reason}`.**",
            color=discord.Color.red(),
        )
        embed.set_footer(text="(c) Ryujin Bot (2023-2025) | Blacklist System", icon_url=RYUJIN_LOGO)
        embed.set_author(name="Ryujin", icon_url=RYUJIN_LOGO)
        return embed

    async def blacklist_guard(self, interaction):
        blocked, reason = self.is_blacklisted(interaction.user.id)
        if blocked:
            await interaction.response.send_message(embed=self.blacklist_embed(reason), ephemeral=True)
            return True
        return False
