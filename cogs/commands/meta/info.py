import nextcord
from nextcord.ext import commands
from cogs.utils.base import RyujinCog

class InfoCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    def create_info_embed(self):
        embed = nextcord.Embed(
            title="About Ryujin",
            description="Ryujin is a Discord bot designed for the AMV and editing community. It provides media tools, After Effects resources, downloaders, and more.",
            color=0x2a2a2a
        )
        embed.add_field(
            name="Features",
            value="• Media Processing (Nightcore, Sped Up, Slowed)\n• After Effects Resources (Presets, Scripts, Extensions, Projects)\n• Media Downloaders (YouTube, TikTok, Instagram)\n• Song/Anime/Font Search\n• Background Removal\n• Hashtag Generator & Trending\n• Moderation Tools",
            inline=False
        )
        embed.add_field(
            name="Developer",
            value="moongetsu",
            inline=True
        )
        embed.add_field(
            name="Version",
            value="0.7b",
            inline=True
        )
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Information System",
            icon_url=self.logo
        )
        embed.set_author(
            name="Ryujin",
            icon_url=self.logo
        )
        return embed
    @nextcord.slash_command(name="info", description="Shows information about Ryujin Bot")
    async def info(self, interaction: nextcord.Interaction):
        user_id = interaction.user.id
        if await self.blacklist_guard(interaction):
            return
        embed = self.create_info_embed()
        await self.bot.maybe_send_ad(interaction)
        await interaction.send(embed=embed, ephemeral=True)
    @nextcord.slash_command(name="bug", description="Report a bug to the Ryujin team")
    async def bug(self, interaction: nextcord.Interaction):
        user_id = interaction.user.id
        if await self.blacklist_guard(interaction):
            return
        embed = nextcord.Embed(
            title="Report a bug",
            description="Join the support server and report it in the `🐞〢bugs` channel.",
            color=0x2a2a2a
        )
        embed.set_footer(text="© Ryujin Bot (2023-2025) | Information System", icon_url=self.logo)
        embed.set_author(name="Ryujin", icon_url=self.logo)
        view = nextcord.ui.View()
        view.add_item(nextcord.ui.Button(label="Support Server", url="https://discord.gg/FSjRSaJ4bt", style=nextcord.ButtonStyle.link))
        await self.bot.maybe_send_ad(interaction)
        await interaction.send(embed=embed, view=view, ephemeral=True)
    @nextcord.slash_command(name="donate", description="Support the development of Ryujin")
    async def donate(self, interaction: nextcord.Interaction):
        user_id = interaction.user.id
        if await self.blacklist_guard(interaction):
            return
        embed = nextcord.Embed(
            title="Support Ryujin",
            description="Help keep the bot running by donating via the button below.",
            color=0x2a2a2a
        )
        embed.set_footer(text="© Ryujin Bot (2023-2025) | Information System", icon_url=self.logo)
        embed.set_author(name="Ryujin", icon_url=self.logo)
        view = nextcord.ui.View()
        view.add_item(nextcord.ui.Button(label="Donate", url="https://ko-fi.com/ryujinsupport", style=nextcord.ButtonStyle.link))
        await self.bot.maybe_send_ad(interaction)
        await interaction.send(embed=embed, view=view, ephemeral=True)

def setup(bot):
    bot.add_cog(InfoCog(bot))