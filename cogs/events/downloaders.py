import discord
from discord.ext import commands
import logging
import os
import time
import asyncio

from cogs.utils.constants import CONTENT_URLS
from services.youtube import download_youtube_video, download_youtube_audio
from services.tiktok import download_tiktok_video
from services.instagram import download_instagram_content

log = logging.getLogger(__name__)


class DownloaderListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_channel_config(self, guild_id):
        if not self.bot.connection:
            return {}
        cursor = self.bot.connection.cursor()
        configs = {}
        tables = ["youtubedl", "youtubedlaudio", "tiktokdl", "instagramdl"]
        for table in tables:
            cursor.execute(
                f"SELECT channel_id FROM {table} WHERE server_id = %s",
                (str(guild_id),),
            )
            result = cursor.fetchone()
            if result:
                configs[table] = int(result[0])
        cursor.close()
        return configs

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or not message.guild:
            return

        channel_configs = await self.get_channel_config(message.guild.id)
        if not channel_configs:
            return

        channel_id = message.channel.id
        if channel_id not in channel_configs.values():
            return

        is_chat = not message.attachments and not any(
            url in message.content.lower() for url in CONTENT_URLS
        )
        if is_chat:
            await message.delete()
            warning = await message.channel.send(
                "**This channel is only for downloading content. Please do not chat here!**"
            )
            await asyncio.sleep(5)
            await warning.delete()
            return

        if channel_configs.get("youtubedl") == channel_id:
            await self._handle_youtube_video(message)
        elif channel_configs.get("youtubedlaudio") == channel_id:
            await self._handle_youtube_audio(message)
        elif channel_configs.get("tiktokdl") == channel_id:
            await self._handle_tiktok(message)
        elif channel_configs.get("instagramdl") == channel_id:
            await self._handle_instagram(message)

    async def _handle_youtube_video(self, message):
        content = message.content
        if not content.startswith(("https://www.youtube.com/", "https://youtu.be/", "https://youtube.com/shorts/")):
            return
        await self._download_and_send(
            message,
            download_youtube_video,
            "video",
            content,
            boost_count=message.guild.premium_subscription_count,
        )

    async def _handle_youtube_audio(self, message):
        content = message.content
        if not content.startswith(("https://www.youtube.com/", "https://youtu.be/")):
            return
        await self._download_and_send(message, download_youtube_audio, "audio", content)

    async def _handle_tiktok(self, message):
        content = message.content
        if not content.startswith(("https://www.tiktok.com/", "https://vm.tiktok.com/", "https://vt.tiktok.com/")):
            return
        start = time.time()
        log.info("%s sent '%s' in '%s'", message.author, content, message.guild)
        try:
            files = await download_tiktok_video(content)
            duration = time.time() - start
            discord_files = [discord.File(path) for path in files]
            await message.channel.send(
                f"**Your TikTok video has been downloaded in `{duration:.2f}` seconds.**",
                files=discord_files,
            )
        except Exception as e:
            log.error("TikTok download error: %s", e)
            await message.channel.send(f"**Sorry, can't download that TikTok. Error: `{e}`**")

    async def _handle_instagram(self, message):
        content = message.content
        if not content.startswith(("https://www.instagram.com/", "https://instagram.com/")):
            return
        start = time.time()
        log.info("%s sent '%s' in '%s'", message.author, content, message.guild)
        try:
            files = await download_instagram_content(content)
            duration = time.time() - start
            discord_files = [discord.File(path) for path in files]
            await message.channel.send(
                f"**Your Instagram content has been downloaded in `{duration:.2f}` seconds.**",
                files=discord_files,
            )
        except Exception as e:
            log.error("Instagram download error: %s", e)
            await message.channel.send(f"**Error downloading Instagram content: `{e}`**")

    async def _download_and_send(self, message, service_fn, label, url, **kwargs):
        start = time.time()
        log.info("%s sent '%s' in '%s'", message.author, url, message.guild)
        try:
            file_path = await service_fn(url, **kwargs)
            if file_path is None:
                await message.channel.send("**Content is too long (max 30 minutes).**")
                return
            duration = time.time() - start
            with open(file_path, 'rb') as f:
                await message.channel.send(
                    f"**Your {label} has been downloaded in `{duration:.2f}` seconds.**",
                    file=discord.File(f, filename=os.path.basename(file_path)),
                )
            try:
                os.remove(file_path)
            except OSError:
                pass
        except Exception as e:
            log.error("Download error (%s): %s", label, e)
            await message.channel.send(f"**Sorry, can't download that {label}. Error: `{e}`**")


async def setup(bot):
    await bot.add_cog(DownloaderListeners(bot))
