import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
from cogs.utils.base import RyujinCog

class TimeoutCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="timeout",
        description="Timeout a user for a specific duration and reason.",
        default_member_permissions=discord.Permissions(moderate_members=True)
    )
    async def timeout(
        self,
        interaction: discord.Interaction,
        user: discord.Member ,
        duration: int,
        reason: str):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.moderate_members:
            return await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)

        if user.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            return await interaction.response.send_message("❌ You can't timeout someone with equal or higher role than yours.", ephemeral=True)

        try:
            await user.timeout(timedelta(minutes=duration), reason=reason)

            embed = discord.Embed(
                title="⏱️ User Timed Out",
                description=f"**{user.mention}** has been timed out for **{duration}** minutes.\nReason: {reason}",
                color=discord.Color.red()
            )
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Moderation System",
                icon_url=self.logo
            )
            await self.bot.maybe_send_ad(interaction)
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)
    @app_commands.command(
        name="remove_timeout",
        description="Remove timeout from a user.",
        default_member_permissions=discord.Permissions(moderate_members=True)
    )
    async def remove_timeout(
        self,
        interaction: discord.Interaction,
        user: discord.Member 
    ):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.moderate_members:
            return await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)

        try:
            await user.timeout(None)

            embed = discord.Embed(
                title="✅ Timeout Removed",
                description=f"Timeout has been removed for {user.mention}.",
                color=discord.Color.green()
            )
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Moderation System",
                icon_url=self.logo
            )
            await self.bot.maybe_send_ad(interaction)
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TimeoutCog(bot))
