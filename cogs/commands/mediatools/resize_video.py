import discord
from discord.ext import commands
from discord import app_commands
import os

from services.media import resize_video
from cogs.utils.base import RyujinCog


class ResizeVideoCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="resize_video", description="Resize a video to a specific resolution while maintaining aspect ratio")
    @app_commands.describe(width="Target width in pixels", height="Target height in pixels")
    async def resize_video(
        self,
        interaction: discord.Interaction,
        video: discord.Attachment,
        width: int,
        height: int,
    ):
        if await self.blacklist_guard(interaction):
            return

        if not video.filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            await interaction.response.send_message("Please provide a valid video file.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        input_path = f"temp/resize_in_{video.filename}"
        output_path = f"temp/resize_out_{video.filename}"
        try:
            os.makedirs('temp', exist_ok=True)
            await video.save(input_path)

            await resize_video(input_path, output_path, width, height)

            original_size = os.path.getsize(input_path)
            resized_size = os.path.getsize(output_path)

            await interaction.followup.send(
                f"Video resized successfully!\n"
                f"Original: {original_size/1024/1024:.2f} MB\n"
                f"Resized: {resized_size/1024/1024:.2f} MB\n"
                f"Resolution: {width}x{height}",
                file=discord.File(output_path),
                ephemeral=True,
            )
            await self.bot.maybe_send_ad(interaction)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)
        finally:
            for p in (input_path, output_path):
                try:
                    if os.path.exists(p):
                        os.remove(p)
                except OSError:
                    pass


async def setup(bot):
    await bot.add_cog(ResizeVideoCog(bot))
