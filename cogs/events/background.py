import nextcord
from nextcord.ext import commands
import logging
import asyncio
from datetime import datetime

from cogs.utils.constants import RYUJIN_LOGO
from cogs.utils.embeds import create_info_embed, create_servers_embed
from cogs.utils.config import load_messages_config, save_messages_config
from cogs.utils.helpers import handle_pagination


class BackgroundTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.change_status())
        self.bot.loop.create_task(self.update_info_message())
        self.bot.loop.create_task(self.update_servers_message())

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_channel(int(self.bot.welcome_leave_channel))
        if not channel:
            return
        embed = nextcord.Embed(
            title="Ryujin has been added to a new server!",
            description=f"**{guild.name}** has added Ryujin to their server!\n\n**Server Information:**\n- Members: {guild.member_count}\n- Created: <t:{int(guild.created_at.timestamp())}:R>",
            color=0x2a2a2a
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else RYUJIN_LOGO)
        embed.set_author(name="Ryujin Bot", icon_url=RYUJIN_LOGO)
        embed.set_footer(text="(c) Ryujin Bot (2023-2025) | Bot Events", icon_url=RYUJIN_LOGO)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_channel(int(self.bot.welcome_leave_channel))
        if not channel:
            return
        embed = nextcord.Embed(
            title="Ryujin has been removed from a server!",
            description=f"**{guild.name}** has removed Ryujin from their server.\nWas Added: <t:{int(guild.me.joined_at.timestamp())}:R>",
            color=0xff0000
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else RYUJIN_LOGO)
        embed.set_author(name="Ryujin Bot", icon_url=RYUJIN_LOGO)
        embed.set_footer(text="(c) Ryujin Bot (2023-2025) | Bot Events", icon_url=RYUJIN_LOGO)
        await channel.send(embed=embed)

    async def change_status(self):
        while True:
            statuses = [
                nextcord.Activity(name="Editing tools at your service", type=nextcord.ActivityType.playing),
                nextcord.Activity(name="AMV community growing", type=nextcord.ActivityType.watching),
                nextcord.Activity(name="suggestions in support server", type=nextcord.ActivityType.listening),
                nextcord.Activity(name="Ryujin v0.7b", type=nextcord.ActivityType.playing),
            ]
            for status in statuses:
                await self.bot.change_presence(status=nextcord.Status.dnd, activity=status)
                await asyncio.sleep(10)

    async def update_info_message(self):
        message_config = load_messages_config()
        while True:
            try:
                info_channel = self.bot.get_channel(int(message_config["Info"]["channel_id"]))
                if not info_channel:
                    await asyncio.sleep(60)
                    continue
                info_embed = create_info_embed(self.bot)
                if not message_config["Info"]["message_id"]:
                    message = await info_channel.send(embed=info_embed)
                    message_config["Info"]["message_id"] = str(message.id)
                    save_messages_config(message_config)
                else:
                    try:
                        message = await info_channel.fetch_message(int(message_config["Info"]["message_id"]))
                        await message.edit(embed=info_embed)
                    except (nextcord.NotFound, nextcord.HTTPException):
                        message = await info_channel.send(embed=info_embed)
                        message_config["Info"]["message_id"] = str(message.id)
                        save_messages_config(message_config)
                await asyncio.sleep(60)
            except Exception as e:
                logging.error(f"Info message update error: {e}")
                await asyncio.sleep(60)

    async def update_servers_message(self):
        message_config = load_messages_config()
        while True:
            try:
                servers_channel = self.bot.get_channel(int(message_config["Servers"]["channel_id"]))
                if not servers_channel:
                    await asyncio.sleep(300)
                    continue
                sorted_guilds = sorted(self.bot.guilds, key=lambda g: g.member_count, reverse=True)
                pages = []
                for i in range(0, len(sorted_guilds), 50):
                    page_guilds = sorted_guilds[i:i+50]
                    embed = create_servers_embed(page_guilds, i//50, -(-len(sorted_guilds)//50))
                    pages.append(embed)
                if not message_config["Servers"]["message_id"]:
                    message = await servers_channel.send(embed=pages[0])
                    message_config["Servers"]["message_id"] = str(message.id)
                    save_messages_config(message_config)
                else:
                    try:
                        message = await servers_channel.fetch_message(int(message_config["Servers"]["message_id"]))
                        await message.edit(embed=pages[0])
                    except (nextcord.NotFound, nextcord.HTTPException):
                        message = await servers_channel.send(embed=pages[0])
                        message_config["Servers"]["message_id"] = str(message.id)
                        save_messages_config(message_config)
                if len(pages) > 1:
                    await handle_pagination(message, pages, self.bot)
                await asyncio.sleep(300)
            except Exception as e:
                logging.error(f"Servers message update error: {e}")
                await asyncio.sleep(60)


def setup(bot):
    bot.add_cog(BackgroundTasks(bot))
