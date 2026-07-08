import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.base import RyujinCog

class ShowGuildsCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="show_guilds",
        description="Shows all the guilds that Ryujin is in!",
    )
    async def show_guilds(self, interaction: discord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        if interaction.user.id == 977190163736322088:
            guilds = list(self.bot.guilds)
            guilds.sort(key=lambda guild: guild.member_count, reverse=True)

            chunked_guilds = [guilds[i:i + 25] for i in range(0, len(guilds), 25)]

            for index, guild_chunk in enumerate(chunked_guilds):
                fields = []
                
                for guild in guild_chunk:
                    truncated_name = guild.name[:25]
                    if len(guild.name) > 25:
                        truncated_name += "..."
                    
                    fields.append((truncated_name, f"{guild.member_count} members\nOwner: **{guild.owner}**"))
                
                embed = discord.Embed(
                    title=f"Info about the guilds that Ryujin is in (Part {index + 1})",
                    description=f"<@1060316037997936751> is in **{len(guilds)}** guilds."
                )
                embed.set_author(name="Ryujin", icon_url=self.logo)
                embed.set_footer(
                    text="© Ryujin Bot (2023-2025) | Development System",
                    icon_url=self.logo
                )
                
                for name, value in fields:
                    embed.add_field(name=name, value=value)
                
                await self.bot.maybe_send_ad(interaction)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("This command is working only for `moongetsu`.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ShowGuildsCog(bot)) 