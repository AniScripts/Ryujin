import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from cogs.utils.base import RyujinCog

class KickCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="kick",
        description="Kick a member from the server.",
        default_member_permissions=nextcord.Permissions(kick_members=True)
    )
    async def kick(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(description="The user to kick"),
        reason: str = SlashOption(description="The reason for the kick")
    ):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.kick_members:
            return await interaction.send("❌ You don't have permission to use this command.", ephemeral=True)

        if member == interaction.user:
            return await interaction.send("❌ You can't kick yourself.", ephemeral=True)

        if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            return await interaction.send("❌ You can't kick someone with equal or higher role than yours.", ephemeral=True)

        try:
            try:
                dm_embed = nextcord.Embed(
                    title="You have been kicked",
                    description=f"You have been kicked from **{interaction.guild.name}**.\nReason: {reason}",
                    color=nextcord.Color.red()
                )
                dm_embed.set_footer(
                    text="© Ryujin Bot (2023-2025) | Moderation System",
                    icon_url=self.logo
                )
                await member.send(embed=dm_embed)
            except nextcord.Forbidden:
                pass

            await member.kick(reason=reason)

            embed = nextcord.Embed(
                title="👢 Member Kicked",
                description=f"**{member.mention}** has been kicked.\nReason: {reason}",
                color=nextcord.Color.red()
            )
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Moderation System",
                icon_url=self.logo
            )
            await self.bot.maybe_send_ad(interaction)
            await interaction.send(embed=embed)

        except Exception as e:
            await interaction.send(f"❌ Failed to kick user: {e}", ephemeral=True)

def setup(bot):
    bot.add_cog(KickCog(bot))
