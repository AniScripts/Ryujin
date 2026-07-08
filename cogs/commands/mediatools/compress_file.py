import nextcord
from nextcord.ext import commands
import os

from services.media import compress_video, compress_audio, compress_image, compress_pdf, compress_archive
from cogs.utils.base import RyujinCog


class CompressFileCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    @nextcord.slash_command(name="compress_file", description="Compress a file to reduce its size while maintaining quality")
    async def compress_file(self, interaction: nextcord.Interaction, file: nextcord.Attachment):
        if await self.blacklist_guard(interaction):
            return

        await interaction.response.defer(ephemeral=True)

        input_path = f"temp/{file.filename}"
        output_path = f"temp/compressed_{file.filename}"
        file_ext = os.path.splitext(file.filename)[1].lower()
        try:
            os.makedirs('temp', exist_ok=True)
            await file.save(input_path)

            if file_ext in ('.mp4', '.mov', '.avi', '.mkv', '.webm'):
                await compress_video(input_path, output_path)
            elif file_ext in ('.jpg', '.jpeg', '.png', '.webp'):
                await compress_image(input_path, output_path, file_ext)
            elif file_ext in ('.mp3', '.wav', '.m4a', '.ogg'):
                await compress_audio(input_path, output_path)
            elif file_ext == '.pdf':
                await compress_pdf(input_path, output_path)
            elif file_ext in ('.zip', '.rar', '.7z'):
                await compress_archive(input_path, output_path)
            else:
                await interaction.followup.send("Unsupported file format. Supported: video, image, audio, PDF, archives.", ephemeral=True)
                return

            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            reduction = ((original_size - compressed_size) / original_size) * 100

            await interaction.followup.send(
                f"File compressed successfully!\n"
                f"Original: {original_size/1024/1024:.2f} MB\n"
                f"Compressed: {compressed_size/1024/1024:.2f} MB\n"
                f"Reduction: {reduction:.1f}%",
                file=nextcord.File(output_path),
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


def setup(bot):
    bot.add_cog(CompressFileCog(bot))
