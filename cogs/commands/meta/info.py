import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.base import RyujinCog

class InfoCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    def create_info_embed(self):
        embed = discord.Embed(
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
    @app_commands.command(name="info", description="Shows information about Ryujin Bot")
    async def info(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if await self.blacklist_guard(interaction):
            return
        embed = self.create_info_embed()
        await self.bot.maybe_send_ad(interaction)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    @app_commands.command(name="bug", description="Report a bug to the Ryujin team")
    async def bug(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if await self.blacklist_guard(interaction):
            return
        embed = discord.Embed(
            title="Report a bug",
            description="Join the support server and report it in the `🐞〢bugs` channel.",
            color=0x2a2a2a
        )
        embed.set_footer(text="© Ryujin Bot (2023-2025) | Information System", icon_url=self.logo)
        embed.set_author(name="Ryujin", icon_url=self.logo)
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/FSjRSaJ4bt", style=discord.ButtonStyle.link))
        await self.bot.maybe_send_ad(interaction)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    @app_commands.command(name="donate", description="Support the development of Ryujin")
    async def donate(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if await self.blacklist_guard(interaction):
            return
        embed = discord.Embed(
            title="Support Ryujin",
            description="Help keep the bot running by donating via the button below.",
            color=0x2a2a2a
        )
        embed.set_footer(text="© Ryujin Bot (2023-2025) | Information System", icon_url=self.logo)
        embed.set_author(name="Ryujin", icon_url=self.logo)
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Donate", url="https://ko-fi.com/ryujinsupport", style=discord.ButtonStyle.link))
        await self.bot.maybe_send_ad(interaction)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(InfoCog(bot))