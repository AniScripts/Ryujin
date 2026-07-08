import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.base import RyujinCog

class DisableAdsCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="disableads",
        description="Disable promotional messages in this server",
    )
    async def disableads(self, interaction: discord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        if not (interaction.user.id == 977190163736322088 or 
                interaction.user == interaction.guild.owner or 
                interaction.user.guild_permissions.administrator):
            await interaction.response.send_message(
                "Only the server owner or administrators can disable ads.",
                ephemeral=True
            )
            return

        cursor = self.bot.connection.cursor()
        cursor.execute("SELECT server_id FROM disableads_servers WHERE server_id = %s", (interaction.guild.id,))
        result = cursor.fetchone()
        
        if result:
            embed = discord.Embed(
                title="Already Disabled",
                description="Promotional messages are already disabled in this server!",
                color=0x2a2a2a
            )
        else:
            cursor.execute("INSERT INTO disableads_servers (server_id) VALUES (%s)", (interaction.guild.id,))
            self.bot.connection.commit()
            
            embed = discord.Embed(
                title="Ads Disabled", 
                description="Promotional messages have been disabled for this server!",
                color=0x2a2a2a
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

async def setup(bot):
    await bot.add_cog(DisableAdsCog(bot)) 