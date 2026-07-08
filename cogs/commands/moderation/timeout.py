import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from datetime import timedelta
from cogs.utils.base import RyujinCog

class TimeoutCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="timeout",
        description="Timeout a user for a specific duration and reason.",
        default_member_permissions=nextcord.Permissions(moderate_members=True)
    )
    async def timeout(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = SlashOption(description="User to timeout"),
        duration: int = SlashOption(description="Duration in minutes"),
        reason: str = SlashOption(description="Reason for the timeout")
    ):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.moderate_members:
            return await interaction.send("❌ You don't have permission to use this command.", ephemeral=True)

        if user.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            return await interaction.send("❌ You can't timeout someone with equal or higher role than yours.", ephemeral=True)

        try:
            await user.timeout(timedelta(minutes=duration), reason=reason)

            embed = nextcord.Embed(
                title="⏱️ User Timed Out",
                description=f"**{user.mention}** has been timed out for **{duration}** minutes.\nReason: {reason}",
                color=nextcord.Color.red()
            )
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Moderation System",
                icon_url=self.logo
            )
            await self.bot.maybe_send_ad(interaction)
            await interaction.send(embed=embed)

        except Exception as e:
            await interaction.send(f"❌ Error: {e}", ephemeral=True)
    @nextcord.slash_command(
        name="remove_timeout",
        description="Remove timeout from a user.",
        default_member_permissions=nextcord.Permissions(moderate_members=True)
    )
    async def remove_timeout(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = SlashOption(description="User to remove timeout")
    ):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.moderate_members:
            return await interaction.send("❌ You don't have permission to use this command.", ephemeral=True)

        try:
            await user.timeout(None)

            embed = nextcord.Embed(
                title="✅ Timeout Removed",
                description=f"Timeout has been removed for {user.mention}.",
                color=nextcord.Color.green()
            )
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Moderation System",
                icon_url=self.logo
            )
            await self.bot.maybe_send_ad(interaction)
            await interaction.send(embed=embed)

        except Exception as e:
            await interaction.send(f"❌ Error: {e}", ephemeral=True)

def setup(bot):
    bot.add_cog(TimeoutCog(bot))
