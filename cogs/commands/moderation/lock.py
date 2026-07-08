import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from cogs.utils.base import RyujinCog

class LockCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="lock",
        description="Locks a channel for @everyone.",
        default_member_permissions=nextcord.Permissions(manage_channels=True)
    )
    async def lock(
        self,
        interaction: nextcord.Interaction,
        channel: nextcord.TextChannel = SlashOption(
            name="channel",
            description="The channel to lock. If not provided, the current channel will be used.",
            required=False
        )
    ):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.send("❌ You don't have permission to use this command.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        target_channel = channel or interaction.channel
        guild = interaction.guild
        everyone_role = guild.default_role

        try:
            overwrite = target_channel.overwrites_for(everyone_role)
            overwrite.send_messages = False
            await target_channel.set_permissions(everyone_role, overwrite=overwrite)

            embed = nextcord.Embed(
                title="🔒 Channel Locked",
                description=f"{target_channel.mention} has been locked for `@everyone`.",
                color=nextcord.Color.red()
            )
            embed.set_footer(text="© Ryujin Bot (2023-2025) | Moderation System", icon_url=self.logo)

            if guild.icon:
                embed.set_author(name=guild.name, icon_url=guild.icon.url)
            else:
                embed.set_author(name="Ryujin", icon_url=self.logo)

            await self.bot.maybe_send_ad(interaction)
            await interaction.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.send(f"❌ Failed to lock the channel: `{e}`", ephemeral=True)
    @nextcord.slash_command(
        name="unlock",
        description="Unlocks a channel for @everyone.",
        default_member_permissions=nextcord.Permissions(manage_channels=True)
    )
    async def unlock(
        self,
        interaction: nextcord.Interaction,
        channel: nextcord.TextChannel = SlashOption(
            name="channel",
            description="The channel to unlock. If not provided, the current channel will be used.",
            required=False
        )
    ):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.send("❌ You don't have permission to use this command.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        target_channel = channel or interaction.channel
        guild = interaction.guild
        everyone_role = guild.default_role

        try:
            overwrite = target_channel.overwrites_for(everyone_role)
            overwrite.send_messages = True
            await target_channel.set_permissions(everyone_role, overwrite=overwrite)

            embed = nextcord.Embed(
                title="🔓 Channel Unlocked",
                description=f"{target_channel.mention} has been unlocked for `@everyone`.",
                color=nextcord.Color.green()
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
            await interaction.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.send(f"❌ Failed to unlock the channel: `{e}`", ephemeral=True)

def setup(bot):
    bot.add_cog(LockCog(bot))