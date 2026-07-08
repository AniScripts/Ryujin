import nextcord
from nextcord.ext import commands
from cogs.utils.db import remove_warning, get_user_warnings, get_warning_count
from cogs.utils.base import RyujinCog

class RemoveWarnCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="remove_warn",
        description="Remove a specific warning from a member.",
        default_member_permissions=nextcord.Permissions(manage_messages=True)
    )
    async def remove_warn(
        self,
        interaction: nextcord.Interaction,
        warn_number: int = nextcord.SlashOption(
            name="warn_number",
            description="The warning ID number to remove",
            required=True
        ),
        user: nextcord.Member = nextcord.SlashOption(
            name="user",
            description="The user to remove the warning from",
            required=True
        ),
        reason: str = nextcord.SlashOption(
            name="reason",
            description="Reason for removing the warning",
            required=False
        )
    ):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.manage_messages:
            await interaction.send(
                "❌ You don't have permission to remove warnings.",
                ephemeral=True
            )
            return

        if user.top_role >= interaction.user.top_role:
            await interaction.send(
                "❌ You can't remove warnings from this user due to role hierarchy.",
                ephemeral=True
            )
            return

        if warn_number <= 0:
            await interaction.send(
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
                await interaction.send(
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
                await interaction.send(
                    "❌ Failed to remove warning from database.",
                    ephemeral=True
                )
                return

            total_warnings = await get_warning_count(
                self.bot.connection,
                interaction.guild.id,
                user.id
            )

            embed = nextcord.Embed(
                title="✅ Warning Removed",
                description=f"Warning #{warn_number} has been removed from **{user.mention}**.\n\n"
                          f"**User:** {user.mention} ({user.name})\n"
                          f"**Removed by:** {interaction.user.mention} ({interaction.user.name})\n"
                          f"**Reason:** {remove_reason}\n"
                          f"**Remaining Warnings:** {total_warnings}",
                color=nextcord.Color.green()
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
            await interaction.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.send(
                f"❌ An error occurred while removing the warning: `{e}`",
                ephemeral=True
            )

def setup(bot):
    bot.add_cog(RemoveWarnCog(bot)) 