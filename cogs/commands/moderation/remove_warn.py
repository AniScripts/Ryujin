import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.db import remove_warning, get_user_warnings, get_warning_count
from cogs.utils.base import RyujinCog

class RemoveWarnCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="remove_warn",
        description="Remove a specific warning from a member.",
        default_member_permissions=discord.Permissions(manage_messages=True)
    )
    async def remove_warn(
        self,
        interaction: discord.Interaction,
        warn_number: int,
        user: discord.Member ,
        reason: str):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "❌ You don't have permission to remove warnings.",
                ephemeral=True
            )
            return

        if user.top_role >= interaction.user.top_role:
            await interaction.response.send_message(
                "❌ You can't remove warnings from this user due to role hierarchy.",
                ephemeral=True
            )
            return

        if warn_number <= 0:
            await interaction.response.send_message(
                "❌ Warning number must be a positive integer.",
                ephemeral=True
            )
            return

        try:
            user_warnings = await get_user_warnings(
                self.bot.connection,
                interaction.guild.id,
                user.id
            )

            warning_exists = any(warning[0] == warn_number for warning in user_warnings)
            
            if not warning_exists:
                await interaction.response.send_message(
                    f"❌ Warning #{warn_number} not found for {user.mention}.",
                    ephemeral=True
                )
                return

            remove_reason = reason or "No reason provided"

            success = await remove_warning(
                self.bot.connection,
                warn_number,
                interaction.guild.id,
                remove_reason
            )

            if not success:
                await interaction.response.send_message(
                    "❌ Failed to remove warning from database.",
                    ephemeral=True
                )
                return

            total_warnings = await get_warning_count(
                self.bot.connection,
                interaction.guild.id,
                user.id
            )

            embed = discord.Embed(
                title="✅ Warning Removed",
                description=f"Warning #{warn_number} has been removed from **{user.mention}**.\n\n"
                          f"**User:** {user.mention} ({user.name})\n"
                          f"**Removed by:** {interaction.user.mention} ({interaction.user.name})\n"
                          f"**Reason:** {remove_reason}\n"
                          f"**Remaining Warnings:** {total_warnings}",
                color=discord.Color.green()
            )
            
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Moderation System",
                icon_url=self.logo
            )
            
            embed.set_author(
                name="Ryujin",
                icon_url=self.logo
            )

            await self.bot.maybe_send_ad(interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(
                f"❌ An error occurred while removing the warning: `{e}`",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(RemoveWarnCog(bot)) 