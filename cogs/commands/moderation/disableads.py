import nextcord
from nextcord.ext import commands
from cogs.utils.base import RyujinCog

class DisableAdsCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="disableads",
        description="Disable promotional messages in this server",
    )
    async def disableads(self, interaction: nextcord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        if not (interaction.user.id == 977190163736322088 or 
                interaction.user == interaction.guild.owner or 
                interaction.user.guild_permissions.administrator):
            await interaction.send(
                "Only the server owner or administrators can disable ads.",
                ephemeral=True
            )
            return

        cursor = self.bot.connection.cursor()
        cursor.execute("SELECT server_id FROM disableads_servers WHERE server_id = %s", (interaction.guild.id,))
        result = cursor.fetchone()
        
        if result:
            embed = nextcord.Embed(
                title="Already Disabled",
                description="Promotional messages are already disabled in this server!",
                color=0x2a2a2a
            )
        else:
            cursor.execute("INSERT INTO disableads_servers (server_id) VALUES (%s)", (interaction.guild.id,))
            self.bot.connection.commit()
            
            embed = nextcord.Embed(
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
        await interaction.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(DisableAdsCog(bot)) 