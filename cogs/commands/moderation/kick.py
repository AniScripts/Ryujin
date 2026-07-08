import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.base import RyujinCog

class KickCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="kick",
        description="Kick a member from the server.",
        default_member_permissions=discord.Permissions(kick_members=True)
    )
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member ,
        reason: str):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.kick_members:
            return await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)

        if member == interaction.user:
            return await interaction.response.send_message("❌ You can't kick yourself.", ephemeral=True)

        if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            return await interaction.response.send_message("❌ You can't kick someone with equal or higher role than yours.", ephemeral=True)

        try:
            try:
                dm_embed = discord.Embed(
                    title="You have been kicked",
                    description=f"You have been kicked from **{interaction.guild.name}**.\nReason: {reason}",
                    color=discord.Color.red()
                )
                dm_embed.set_footer(
                    text="© Ryujin Bot (2023-2025) | Moderation System",
                    icon_url=self.logo
                )
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                pass

            await member.kick(reason=reason)

            embed = discord.Embed(
                title="👢 Member Kicked",
                description=f"**{member.mention}** has been kicked.\nReason: {reason}",
                color=discord.Color.red()
            )
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Moderation System",
                icon_url=self.logo
            )
            await self.bot.maybe_send_ad(interaction)
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to kick user: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(KickCog(bot))
