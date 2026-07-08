import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.db import get_user_warnings, get_warning_count
from datetime import datetime
from cogs.utils.base import RyujinCog

class WarnsCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="warns",
        description="Display all warnings for a member.",
        default_member_permissions=discord.Permissions(manage_messages=True)
    )
    async def warns(
        self,
        interaction: discord.Interaction,
        user: discord.Member 
    ):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True
            )
            return

        try:
            warnings = await get_user_warnings(
                self.bot.connection,
                interaction.guild.id,
                user.id
            )

            total_warnings = await get_warning_count(
                self.bot.connection,
                interaction.guild.id,
                user.id
            )

            if not warnings:
                embed = discord.Embed(
                    title="📋 Warning History",
                    description=f"**User:** {user.mention} ({user.name})\n"
                              f"**Total Warnings:** 0\n"
                              f"**Status:** ✅ Clean record",
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
                return

            warning_list = []
            for warning in warnings:
                warning_id, moderator_id, reason, warn_date = warning
                
                try:
                    moderator = await self.bot.fetch_user(moderator_id)
                    moderator_name = moderator.name
                except:
                    moderator_name = f"Unknown User ({moderator_id})"
                
                if isinstance(warn_date, str):
                    try:
                        warn_date = datetime.fromisoformat(warn_date.replace('Z', '+00:00'))
                    except:
                        warn_date = "Unknown date"
                
                if isinstance(warn_date, datetime):
                    date_str = f"<t:{int(warn_date.timestamp())}:R>"
                else:
                    date_str = str(warn_date)
                
                warning_list.append(f"**#{warning_id}** | {moderator_name} | {date_str}\n└ {reason}")

            if total_warnings == 0:
                status = "✅ Clean record"
            elif total_warnings == 1:
                status = "⚠️ 1 warning"
            elif total_warnings <= 3:
                status = f"⚠️ {total_warnings} warnings"
            else:
                status = f"🚨 {total_warnings} warnings (High risk)"

            warnings_text = "\n\n".join(warning_list[:10])
            if len(warning_list) > 10:
                warnings_text += f"\n\n*... and {len(warning_list) - 10} more warnings*"

            embed = discord.Embed(
                title="📋 Warning History",
                description=f"**User:** {user.mention} ({user.name})\n"
                          f"**Total Warnings:** {total_warnings}\n"
                          f"**Status:** {status}\n\n"
                          f"**Recent Warnings:**\n{warnings_text}",
                color=discord.Color.orange() if total_warnings > 0 else discord.Color.green()
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
                f"❌ An error occurred while fetching warnings: `{e}`",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(WarnsCog(bot)) 