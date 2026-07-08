import discord
from discord.ext import commands
from discord import app_commands
from mysql.connector import Error
from cogs.utils.db import add_to_blacklist, remove_from_blacklist, get_blacklist
from cogs.utils.base import RyujinCog

class BlacklistCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(
        name="blacklist",
        description="Manage user blacklist (Development only)",
        guild_ids=[1060144274722787328]
    )
    async def blacklist(
        self,
        interaction: discord.Interaction,
        action: str,
        user: discord.Member ,
        reason: str):
        if interaction.user.id != 977190163736322088:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don't have permission to use this command. Only the bot owner can manage the blacklist.",
                color=0xff0000
            )
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Development System",
                icon_url=self.logo
            )
            embed.set_author(
                name="Ryujin",
                icon_url=self.logo
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            if action == "add":
                if not user:
                    embed = discord.Embed(
                        title="❌ Error",
                        description="Please specify a user to blacklist.",
                        color=0xff0000
                    )
                    embed.set_footer(
                        text="© Ryujin Bot (2023-2025) | Development System",
                        icon_url=self.logo
                    )
                    embed.set_author(
                        name="Ryujin",
                        icon_url=self.logo
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

                if not reason:
                    reason = "No reason provided"

                await add_to_blacklist(self.bot.connection, user.id, reason)
                
                self.bot.blacklist = get_blacklist(self.bot.connection)
                
                embed = discord.Embed(
                    title="✅ User Blacklisted",
                    description=f"**{user.mention}** has been added to the blacklist.\n\n**Reason:** {reason}",
                    color=0xff0000
                )
                embed.set_thumbnail(url=user.display_avatar.url)
                embed.set_footer(
                    text="© Ryujin Bot (2023-2025) | Development System",
                    icon_url=self.logo
                )
                embed.set_author(
                    name="Ryujin",
                    icon_url=self.logo
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

            elif action == "remove":
                if not user:
                    embed = discord.Embed(
                        title="❌ Error",
                        description="Please specify a user to remove from blacklist.",
                        color=0xff0000
                    )
                    embed.set_footer(
                        text="© Ryujin Bot (2023-2025) | Development System",
                        icon_url=self.logo
                    )
                    embed.set_author(
                        name="Ryujin",
                        icon_url=self.logo
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

                removed = await remove_from_blacklist(self.bot.connection, user.id)
                
                if removed:
                    self.bot.blacklist = get_blacklist(self.bot.connection)
                    
                    embed = discord.Embed(
                        title="✅ User Removed from Blacklist",
                        description=f"**{user.mention}** has been removed from the blacklist.",
                        color=0x00ff00
                    )
                    embed.set_thumbnail(url=user.display_avatar.url)
                    embed.set_footer(
                        text="© Ryujin Bot (2023-2025) | Development System",
                        icon_url=self.logo
                    )
                    embed.set_author(
                        name="Ryujin",
                        icon_url=self.logo
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(
                        title="❌ User Not Found",
                        description=f"**{user.mention}** is not in the blacklist.",
                        color=0xff0000
                    )
                    embed.set_footer(
                        text="© Ryujin Bot (2023-2025) | Development System",
                        icon_url=self.logo
                    )
                    embed.set_author(
                        name="Ryujin",
                        icon_url=self.logo
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)

            elif action == "list":
                blacklist = get_blacklist(self.bot.connection)
                
                if not blacklist:
                    embed = discord.Embed(
                        title="📋 Blacklist",
                        description="No users are currently blacklisted.",
                        color=0x2a2a2a
                    )
                    embed.set_footer(
                        text="© Ryujin Bot (2023-2025) | Development System",
                        icon_url=self.logo
                    )
                    embed.set_author(
                        name="Ryujin",
                        icon_url=self.logo
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

                embed = discord.Embed(
                    title="📋 Blacklisted Users",
                    description=f"Total blacklisted users: **{len(blacklist)}**",
                    color=0x2a2a2a
                )

                for i, (user_id, reason) in enumerate(list(blacklist.items())[:25]):
                    try:
                        user_obj = await self.bot.fetch_user(user_id)
                        user_mention = user_obj.mention
                        user_name = user_obj.name
                    except:
                        user_mention = f"<@{user_id}>"
                        user_name = f"Unknown User ({user_id})"

                    embed.add_field(
                        name=f"#{i+1} {user_name}",
                        value=f"**User:** {user_mention}\n**Reason:** {reason}",
                        inline=False
                    )

                if len(blacklist) > 25:
                    embed.add_field(
                        name="Note",
                        value=f"Showing first 25 users. Total: {len(blacklist)}",
                        inline=False
                    )

                embed.set_footer(
                    text="© Ryujin Bot (2023-2025) | Development System",
                    icon_url=self.logo
                )
                embed.set_author(
                    name="Ryujin",
                    icon_url=self.logo
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

            elif action == "check":
                if not user:
                    embed = discord.Embed(
                        title="❌ Error",
                        description="Please specify a user to check.",
                        color=0xff0000
                    )
                    embed.set_footer(
                        text="© Ryujin Bot (2023-2025) | Development System",
                        icon_url=self.logo
                    )
                    embed.set_author(
                        name="Ryujin",
                        icon_url=self.logo
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

                blacklist = get_blacklist(self.bot.connection)
                
                if user.id in blacklist:
                    embed = discord.Embed(
                        title="🔴 User is Blacklisted",
                        description=f"**{user.mention}** is currently blacklisted.\n\n**Reason:** {blacklist[user.id]}",
                        color=0xff0000
                    )
                    embed.set_thumbnail(url=user.display_avatar.url)
                else:
                    embed = discord.Embed(
                        title="🟢 User is Not Blacklisted",
                        description=f"**{user.mention}** is not in the blacklist.",
                        color=0x00ff00
                    )
                    embed.set_thumbnail(url=user.display_avatar.url)

                embed.set_footer(
                    text="© Ryujin Bot (2023-2025) | Development System",
                    icon_url=self.logo
                )
                embed.set_author(
                    name="Ryujin",
                    icon_url=self.logo
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Error as e:
            embed = discord.Embed(
                title="❌ Database Error",
                description=f"An error occurred while accessing the database: {str(e)}",
                color=0xff0000
            )
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Development System",
                icon_url=self.logo
            )
            embed.set_author(
                name="Ryujin",
                icon_url=self.logo
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"An unexpected error occurred: {str(e)}",
                color=0xff0000
            )
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Development System",
                icon_url=self.logo
            )
            embed.set_author(
                name="Ryujin",
                icon_url=self.logo
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(BlacklistCog(bot)) 