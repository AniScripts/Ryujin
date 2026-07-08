import discord
from discord.ext import commands
from discord import app_commands
import platform
import psutil
from datetime import datetime
from cogs.utils.base import RyujinCog

class BotStatsCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="bot_stats",
        description="Display detailed statistics about the bot.",
    )
    async def bot_stats(self, interaction: discord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        total_servers = len(self.bot.guilds)
        total_members = sum(len(guild.members) for guild in self.bot.guilds)
        current_time = datetime.now()
        uptime = current_time - self.bot.start_time
        latency_ms = round(self.bot.latency * 1000, 2)
        
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"

        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 / 1024

        description = (
            f"🌐 **Servers:** {total_servers:,}\n"
            f"👥 **Total Members:** {total_members:,}\n"
            f"⏰ **Uptime:** {uptime_str}\n"
            f"📶 **Latency:** {latency_ms}ms\n"
            f"💾 **Memory Usage:** {memory_usage:.1f} MB\n"
            f"🔄 **Bot Version:** 0.6b\n"
            f"👨‍💻 **Bot Developer:** moongetsu\n\n"
            f"**Python Version:** {platform.python_version()}\n"
            f"**Nextcord Version:** {discord.__version__}"
        )
        
        embed = discord.Embed(
            title="📊 Ryujin Statistics",
            description=description,
            color=0x2a2a2a,
        )
        embed.set_author(
            name="Ryujin",
            icon_url=self.logo
        )
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Information System",
            icon_url=self.logo
        )
        await self.bot.maybe_send_ad(interaction)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(BotStatsCog(bot)) 