import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.base import RyujinCog

class PurgeCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="purge",
        description="Bulk delete messages from a channel",
    )
    async def purge(
        self,
        interaction: discord.Interaction,
        messages: int,
    ):
        if await self.blacklist_guard(interaction):
            return

        await interaction.response.defer(ephemeral=True)

        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)

        if messages < 1 or messages > 100:
            return await interaction.response.send_message("❌ You must specify between 1 and 100 messages.", ephemeral=True)

        try:
            deleted = await interaction.channel.purge(limit=messages)
            embed = discord.Embed(
                title="🧹 Messages Purged",
                description=f"Successfully deleted `{len(deleted)}` messages from {interaction.channel.mention}.",
                color=discord.Color.red()
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
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to purge messages: `{e}`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(PurgeCog(bot))
