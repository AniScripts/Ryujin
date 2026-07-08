import discord
from discord.ext import commands
import logging
import asyncio

from cogs.utils.constants import RYUJIN_LOGO
from cogs.utils.helpers import split_long_text
from services.ai import chat_completion

log = logging.getLogger(__name__)


class RyujinAIListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_ai_channel(self, guild_id):
        if not self.bot.connection:
            return None
        cursor = self.bot.connection.cursor()
        cursor.execute("SELECT channel_id FROM ryujinai WHERE server_id = %s", (str(guild_id),))
        result = cursor.fetchone()
        cursor.close()
        return int(result[0]) if result else None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or not message.guild:
            return

        channel_id = await self.get_ai_channel(message.guild.id)
        if not channel_id or message.channel.id != channel_id:
            return

        user_id = message.author.id
        if user_id in self.bot.blacklist:
            embed = discord.Embed(
                title="You are blacklisted!",
                description=f"**You can't use Ryujin's functions anymore because you have been blacklisted for `{self.bot.blacklist[user_id]}`.**",
                color=discord.Color.red()
            )
            embed.set_footer(text="(c) Ryujin Bot (2023-2025) | Blacklist System")
            embed.set_author(name="Ryujin", icon_url=RYUJIN_LOGO)
            blacklist_msg = await message.channel.send(embed=embed)
            await asyncio.sleep(10)
            await blacklist_msg.delete()
            log.warning("%s is blacklisted. Unable to process AI request.", message.author)
            return

        if not message.content.strip():
            return

        async with message.channel.typing():
            try:
                response = await chat_completion(message.content)
                if len(response) <= 2000:
                    await message.reply(response)
                else:
                    chunks = split_long_text(response)
                    first = chunks[0][:4096]
                    embed = discord.Embed(title="Ryujin AI Response", description=first, color=0x2a2a2a)
                    embed.set_footer(text=f"(c) Ryujin Bot (2023-2025) | AI System | Page 1/{len(chunks)}", icon_url=RYUJIN_LOGO)
                    embed.set_author(name="Ryujin AI", icon_url=RYUJIN_LOGO)
                    embed.add_field(name="Asked by", value=f"{message.author.mention} ({message.author.name})", inline=False)
                    await message.reply(embed=embed)
                    for i, chunk in enumerate(chunks[1:], 1):
                        embed = discord.Embed(
                            title="Ryujin AI Response (Continued)",
                            description=chunk[:4096],
                            color=0x2a2a2a,
                        )
                        embed.set_footer(text=f"(c) Ryujin Bot (2023-2025) | AI System | Page {i+1}/{len(chunks)}", icon_url=RYUJIN_LOGO)
                        embed.set_author(name="Ryujin AI", icon_url=RYUJIN_LOGO)
                        await message.channel.send(embed=embed)

                log.info("AI response sent to %s in '%s'", message.author, message.guild)

            except Exception as e:
                error_embed = discord.Embed(
                    title="AI Error",
                    description=f"Sorry, I encountered an error: `{str(e)}`\n\nPlease try again in a moment!",
                    color=0xff0000,
                )
                error_embed.set_footer(text="(c) Ryujin Bot (2023-2025) | AI System", icon_url=RYUJIN_LOGO)
                error_embed.set_author(name="Ryujin AI", icon_url=RYUJIN_LOGO)
                await message.channel.send(embed=error_embed)
                log.error("AI error for %s: %s", message.author, e)


async def setup(bot):
    await bot.add_cog(RyujinAIListener(bot))
