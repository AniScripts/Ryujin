import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.base import RyujinCog

class LockCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="lock",
        description="Locks a channel for @everyone.",
        default_member_permissions=discord.Permissions(manage_channels=True)
    )
    async def lock(
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
        guild = interaction.guild
        everyone_role = guild.default_role

        try:
            overwrite = target_channel.overwrites_for(everyone_role)
            overwrite.send_messages = False
            await target_channel.set_permissions(everyone_role, overwrite=overwrite)

            embed = discord.Embed(
                title="🔒 Channel Locked",
                description=f"{target_channel.mention} has been locked for `@everyone`.",
                color=discord.Color.red()
            )
            embed.set_footer(text="© Ryujin Bot (2023-2025) | Moderation System", icon_url=self.logo)

            if guild.icon:
                embed.set_author(name=guild.name, icon_url=guild.icon.url)
            else:
                embed.set_author(name="Ryujin", icon_url=self.logo)

            await self.bot.maybe_send_ad(interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to lock the channel: `{e}`", ephemeral=True)
    @app_commands.command(
        name="unlock",
        description="Unlocks a channel for @everyone.",
        default_member_permissions=discord.Permissions(manage_channels=True)
    )
    async def unlock(
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
        guild = interaction.guild
        everyone_role = guild.default_role

        try:
            overwrite = target_channel.overwrites_for(everyone_role)
            overwrite.send_messages = True
            await target_channel.set_permissions(everyone_role, overwrite=overwrite)

            embed = discord.Embed(
                title="🔓 Channel Unlocked",
                description=f"{target_channel.mention} has been unlocked for `@everyone`.",
                color=discord.Color.green()
            )
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Moderation System", 
                icon_url=self.logo
            )

            if guild.icon:
                embed.set_author(
                    name=guild.name, 
                    icon_url=guild.icon.url
                )
            else:
                embed.set_author(
                    name="Ryujin", 
                    icon_url=self.logo
                )

            await self.bot.maybe_send_ad(interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to unlock the channel: `{e}`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(LockCog(bot))