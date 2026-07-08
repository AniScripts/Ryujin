import discord
from discord.ext import commands
import logging
import asyncio
import aiohttp

from cogs.utils.constants import RYUJIN_LOGO
from services.remove_bg import remove_background


class RemoveBgListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_removebg_channel(self, guild_id):
        if not self.bot.connection:
            return None
        cursor = self.bot.connection.cursor()
        cursor.execute("SELECT channel_id FROM removebg WHERE server_id = %s", (str(guild_id),))
        result = cursor.fetchone()
        cursor.close()
        return int(result[0]) if result else None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or not message.guild:
            return

        channel_id = await self.get_removebg_channel(message.guild.id)
        if not channel_id or message.channel.id != channel_id:
            return

        user_id = message.author.id
        if user_id in self.bot.blacklist:
            embed = discord.Embed(
                title="You are blacklisted!",
                description=f"**You can't use Ryujin's functions anymore because you have been blacklisted for `{self.bot.blacklist[user_id]}`.**",
                color=discord.Color.red()
            )
            embed.set_footer(text="(c) Ryujin Bot (2023-2025) | Info System")
            embed.set_author(name="Ryujin", icon_url=RYUJIN_LOGO)
            blacklist_msg = await message.channel.send(embed=embed)
            await asyncio.sleep(10)
            await blacklist_msg.delete()
            logging.warning("%s is blacklisted. Unable to process Remove Background request.", message.author)
            return

        if not message.attachments:
            await message.delete()
            warning = await message.channel.send("**This channel is only for removing backgrounds from images. Please attach an image!**")
            await asyncio.sleep(5)
            await warning.delete()
            return

        processing_msg = await message.channel.send("**Processing your image...**")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(message.attachments[0].url) as resp:
                    if resp.status != 200:
                        raise RuntimeError("Failed to fetch image")
                    image_data = await resp.read()

            result = await remove_background(image_data)

            await processing_msg.delete()
            await message.channel.send(
                "**Background removed successfully!**",
                file=discord.File(result, "removebg.png"),
            )
            logging.info("Remove Background processed for %s in '%s'.", message.author, message.guild)

        except Exception as e:
            logging.error("Error removing background: %s", e)
            await processing_msg.delete()
            error_msg = await message.channel.send(
                "**Failed to remove background. The image might be too complex or in an unsupported format. Please try with a different image.**"
            )
            await asyncio.sleep(10)
            await error_msg.delete()
            await message.delete()


async def setup(bot):
    await bot.add_cog(RemoveBgListener(bot))
