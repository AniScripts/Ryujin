import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from cogs.utils.base import RyujinCog

class SoftbanCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    def parse_duration(self, duration_str):
        """Parse duration string (e.g., '1d', '2h', '30m') and return timedelta"""
        if not duration_str:
            return None
        
        duration_str = duration_str.lower()
        if duration_str == "permanent" or duration_str == "perm":
            return None
        
        try:
            if duration_str.endswith('d'):
                days = int(duration_str[:-1])
                return timedelta(days=days)
            elif duration_str.endswith('h'):
                hours = int(duration_str[:-1])
                return timedelta(hours=hours)
            elif duration_str.endswith('m'):
                minutes = int(duration_str[:-1])
                return timedelta(minutes=minutes)
            elif duration_str.endswith('s'):
                seconds = int(duration_str[:-1])
                return timedelta(seconds=seconds)
            else:
                hours = int(duration_str)
                return timedelta(hours=hours)
        except ValueError:
            return None
    @app_commands.command(
        name="softban",
        default_member_permissions=discord.Permissions(ban_members=True)
    )
    async def softban(
        self,
        interaction: discord.Interaction,
        user: discord.Member ,
        duration: str,
        reason: str):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True
            )
            return

        if not interaction.guild.me.guild_permissions.ban_members:
            await interaction.response.send_message(
                "❌ I don't have permission to use this command.",
                ephemeral=True
            )
            return

        if user.top_role >= interaction.user.top_role:
            await interaction.response.send_message(
                "❌ You can't use this command due to role hierarchy.",
                ephemeral=True
            )
            return

        if user.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                "❌ I can't use this command due to role hierarchy.",
                ephemeral=True
            )
            return

        duration_delta = self.parse_duration(duration) if duration else None
        is_permanent = duration_delta is None
        
        softban_reason = reason or "No reason provided"
        if duration and not is_permanent:
            softban_reason += f" (Duration: {duration})"

        try:
            try:
                dm_embed = discord.Embed(
                    title="🧹 You have been softbanned",
                    description=f"You have been softbanned from **{interaction.guild.name}**\n\n"
                              f"**What is a softban?**\nA softban removes all your messages from the server and kicks you, but you can rejoin immediately.\n\n"
                              f"**Reason:** {softban_reason}\n"
                              f"**Softbanned by:** {interaction.user.mention} ({interaction.user.name})\n"
                              f"**Duration:** {'Permanent' if is_permanent else duration}",
                    color=discord.Color.orange()
                )
                
                dm_embed.set_footer(
                    text="© Ryujin Bot (2023-2025) | Moderation System",
                    icon_url=self.logo
                )
                
                await user.send(embed=dm_embed)
                dm_sent = True
            except:
                dm_sent = False

            ban_reason = f"SOFTBAN - {interaction.user.name}: {softban_reason}"
            await user.ban(reason=ban_reason)
            
            await interaction.guild.unban(user, reason=f"SOFTBAN COMPLETE - {interaction.user.name}: {softban_reason}")
            
            description = f"**{user.mention}** has been softbanned from the server.\nAll their messages have been deleted and they have been kicked.\n\n"
            description += f"**User:** {user.mention} ({user.name})\n"
            description += f"**Softbanned by:** {interaction.user.mention} ({interaction.user.name})\n"
            description += f"**Reason:** {softban_reason}\n"
            description += f"**Duration:** {'Permanent' if is_permanent else duration}\n"
            
            if not is_permanent and duration_delta:
                description += f"**Expires:** <t:{int((datetime.now() + duration_delta).timestamp())}:R>\n"
            
            description += f"**Message Deletion:** ✅ Last 7 days of messages deleted\n"
            description += f"**User Status:** ✅ User can rejoin immediately\n"
            description += f"**DM Status:** {'✅ DM sent to user' if dm_sent else '❌ Could not send DM (DMs closed)'}"
            
            embed = discord.Embed(
                title="🧹 User Softbanned",
                description=description,
                color=discord.Color.orange()
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
            await interaction.response.send_message(embed=embed)

        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I don't have permission to softban this user.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ An error occurred while softbanning the user: `{e}`",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(SoftbanCog(bot)) 