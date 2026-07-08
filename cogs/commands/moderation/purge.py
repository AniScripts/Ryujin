import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from cogs.utils.base import RyujinCog

class PurgeCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="purge",
        description="Delete a certain number of messages from a channel."
    )
    async def purge(
        self,
        interaction: nextcord.Interaction,
        messages: int = SlashOption(
            name="messages",
            description="The number of messages to delete (max 100).",
            required=True
        )
    ):
        if await self.blacklist_guard(interaction):
            return

        await interaction.response.defer(ephemeral=True)

        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.send("❌ You don't have permission to use this command.", ephemeral=True)

        if messages < 1 or messages > 100:
            return await interaction.send("❌ You must specify between 1 and 100 messages.", ephemeral=True)

        try:
            deleted = await interaction.channel.purge(limit=messages)
            embed = nextcord.Embed(
                title="🧹 Messages Purged",
                description=f"Successfully deleted `{len(deleted)}` messages from {interaction.channel.mention}.",
                color=nextcord.Color.red()
            )
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Moderation System", icon_url=self.logo)

            if interaction.guild.icon:
                embed.set_author(
                    name=interaction.guild.name, 
                    icon_url=interaction.guild.icon.url
                )
            else:
                embed.set_author(
                    name="Ryujin", 
                    icon_url=self.logo
            )

            await self.bot.maybe_send_ad(interaction)
            await interaction.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.send(f"❌ Failed to purge messages: `{e}`", ephemeral=True)

def setup(bot):
    bot.add_cog(PurgeCog(bot))
