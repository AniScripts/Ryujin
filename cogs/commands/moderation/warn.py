import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.db import add_warning, get_warning_count
from cogs.utils.base import RyujinCog

class WarnCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="warn",
        description="Warn a member for breaking the rules.",
        default_member_permissions=discord.Permissions(manage_messages=True)
    )
    async def warn(
        self,
        interaction: discord.Interaction,
        user: discord.Member ,
        reason: str):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True
            )
            return

        if user.top_role >= interaction.user.top_role:
            await interaction.response.send_message(
                "❌ You can't use this command due to role hierarchy.",
                ephemeral=True
            )
            return

        if user.id == interaction.user.id:
            await interaction.response.send_message(
                "❌ You can't warn yourself.",
                ephemeral=True
            )
            return

        if user.id == self.bot.user.id:
            await interaction.response.send_message(
                "❌ You can't warn the bot.",
                ephemeral=True
            )
            return

        try:
            warning_id = await add_warning(
                self.bot.connection,
                interaction.guild.id,
                user.id,
                interaction.user.id,
                reason
            )

            if warning_id is None:
                await interaction.response.send_message(
                    "❌ Failed to add warning to database.",
                    ephemeral=True
                )
                return

            total_warnings = await get_warning_count(
                self.bot.connection,
                interaction.guild.id,
                user.id
            )

            try:
                dm_embed = discord.Embed(
                    title="⚠️ You have been warned",
                    description=f"You have received a warning in **{interaction.guild.name}**\n\n"
                              f"**Reason:** {reason}\n"
                              f"**Warned by:** {interaction.user.mention} ({interaction.user.name})\n"
                              f"**Warning ID:** #{warning_id}\n"
                              f"**Total Warnings:** {total_warnings}",
                    color=discord.Color.yellow()
                )
                
                dm_embed.set_footer(
                    text="© Ryujin Bot (2023-2025) | Moderation System",
                    icon_url=self.logo
                )
                
                await user.send(embed=dm_embed)
                dm_sent = True
            except:
                dm_sent = False

            embed = discord.Embed(
                title="⚠️ User Warned",
                description=f"**{user.mention}** has been warned.\n\n"
                          f"**User:** {user.mention} ({user.name})\n"
                          f"**Warned by:** {interaction.user.mention} ({interaction.user.name})\n"
                          f"**Reason:** {reason}\n"
                          f"**Warning ID:** #{warning_id}\n"
                          f"**Total Warnings:** {total_warnings}\n"
                          f"**DM Status:** {'✅ DM sent to user' if dm_sent else '❌ Could not send DM (DMs closed)'}",
                color=discord.Color.yellow()
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
                f"❌ An error occurred while warning the user: `{e}`",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(WarnCog(bot)) 