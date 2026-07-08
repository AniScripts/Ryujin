import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.base import RyujinCog

class SlowmodeCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="slowmode",
        default_member_permissions=discord.Permissions(manage_channels=True)
    )
    async def slowmode(
        self,
        interaction: discord.Interaction,
        seconds: int,
        channel: discord.TextChannel = None,
    ):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        target_channel = channel or interaction.channel

        if seconds < 0 or seconds > 21600:
            return await interaction.response.send_message("❌ Slowmode must be between 0 and 21600 seconds (6 hours).", ephemeral=True)

        try:
            await target_channel.edit(slowmode_delay=seconds)

            embed = discord.Embed(
                title="🐢 Slowmode Updated",
                description=f"Slowmode in {target_channel.mention} is now set to `{seconds}` seconds.",
                color=discord.Color.blurple()
            )
            embed.set_footer(text="© Ryujin Bot (2023-2025) | Moderation System", icon_url=self.logo)

            if interaction.guild.icon:
                embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
            else:
                embed.set_author(name="Ryujin", icon_url=self.logo)

            await self.bot.maybe_send_ad(interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to update slowmode: `{e}`", ephemeral=True)
    @app_commands.command(
        name="remove_slowmode",
        default_member_permissions=discord.Permissions(manage_channels=True)
    )
    async def remove_slowmode(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel 
    ):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        target_channel = channel or interaction.channel

        try:
            await target_channel.edit(slowmode_delay=0)

            embed = discord.Embed(
                title="🧯 Slowmode Removed",
                description=f"Slowmode has been disabled in {target_channel.mention}.",
                color=discord.Color.green()
            )
            embed.set_footer(text="© Ryujin Bot (2023-2025) | Moderation System", icon_url=self.logo)

            if interaction.guild.icon:
                embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
            else:
                embed.set_author(name="Ryujin", icon_url=self.logo)

            await self.bot.maybe_send_ad(interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to remove slowmode: `{e}`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SlowmodeCog(bot))
