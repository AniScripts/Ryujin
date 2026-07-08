import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from cogs.utils.base import RyujinCog

class SlowmodeCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="slowmode",
        description="Set slowmode for a channel.",
        default_member_permissions=nextcord.Permissions(manage_channels=True)
    )
    async def slowmode(
        self,
        interaction: nextcord.Interaction,
        seconds: int = SlashOption(
            name="seconds",
            description="The slowmode duration in seconds (0 to disable).",
            required=True
        ),
        channel: nextcord.TextChannel = SlashOption(
            name="channel",
            description="The channel to apply slowmode. Defaults to current channel.",
            required=False
        )
    ):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.send("❌ You don't have permission to use this command.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        target_channel = channel or interaction.channel

        if seconds < 0 or seconds > 21600:
            return await interaction.send("❌ Slowmode must be between 0 and 21600 seconds (6 hours).", ephemeral=True)

        try:
            await target_channel.edit(slowmode_delay=seconds)

            embed = nextcord.Embed(
                title="🐢 Slowmode Updated",
                description=f"Slowmode in {target_channel.mention} is now set to `{seconds}` seconds.",
                color=nextcord.Color.blurple()
            )
            embed.set_footer(text="© Ryujin Bot (2023-2025) | Moderation System", icon_url=self.logo)

            if interaction.guild.icon:
                embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
            else:
                embed.set_author(name="Ryujin", icon_url=self.logo)

            await self.bot.maybe_send_ad(interaction)
            await interaction.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.send(f"❌ Failed to update slowmode: `{e}`", ephemeral=True)
    @nextcord.slash_command(
        name="remove_slowmode",
        description="Remove slowmode from a channel.",
        default_member_permissions=nextcord.Permissions(manage_channels=True)
    )
    async def remove_slowmode(
        self,
        interaction: nextcord.Interaction,
        channel: nextcord.TextChannel = SlashOption(
            name="channel",
            description="The channel to remove slowmode. Defaults to current channel.",
            required=False
        )
    ):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.send("❌ You don't have permission to use this command.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        target_channel = channel or interaction.channel

        try:
            await target_channel.edit(slowmode_delay=0)

            embed = nextcord.Embed(
                title="🧯 Slowmode Removed",
                description=f"Slowmode has been disabled in {target_channel.mention}.",
                color=nextcord.Color.green()
            )
            embed.set_footer(text="© Ryujin Bot (2023-2025) | Moderation System", icon_url=self.logo)

            if interaction.guild.icon:
                embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
            else:
                embed.set_author(name="Ryujin", icon_url=self.logo)

            await self.bot.maybe_send_ad(interaction)
            await interaction.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.send(f"❌ Failed to remove slowmode: `{e}`", ephemeral=True)

def setup(bot):
    bot.add_cog(SlowmodeCog(bot))
