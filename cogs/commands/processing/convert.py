import nextcord
from nextcord.ext import commands
import os
import re

from services.media import convert_media
from cogs.utils.base import RyujinCog


class ConvertCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    def sanitize_filename(self, filename):
        return re.sub(r'[<>:"/\\|?*]', '', filename)

    @nextcord.slash_command(name="convert", description="Convert a file from one format to another.")
    async def convert(
        self,
        interaction: nextcord.Interaction,
        from_format: str = nextcord.SlashOption(
            choices=["MP4", "MKV", "MOV", "AVI", "MP3", "WAV", "M4A", "PNG", "JPG", "JPEG", "SVG", "WEBP", "ICO"],
            description="Source format",
        ),
        to_format: str = nextcord.SlashOption(
            choices=["MP4", "MKV", "MOV", "AVI", "MP3", "WAV", "M4A", "PNG", "JPG", "JPEG", "SVG", "WEBP", "ICO"],
            description="Target format",
        ),
        file: nextcord.Attachment = nextcord.SlashOption(description="File to convert", required=True),
    ):
        if await self.blacklist_guard(interaction):
            return

        await interaction.response.defer(ephemeral=True)

        input_path = f"temp/{file.filename}"
        base_name = os.path.splitext(file.filename)[0]
        output_path = f"temp/{self.sanitize_filename(base_name)}.{to_format.lower()}"
        try:
            os.makedirs('temp', exist_ok=True)
            await file.save(input_path)

            await convert_media(input_path, output_path, from_format, to_format)

            await interaction.followup.send(file=nextcord.File(output_path), ephemeral=True)
            await self.bot.maybe_send_ad(interaction)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)
        finally:
            for p in (input_path, output_path):
                try:
                    if os.path.exists(p):
                        os.remove(p)
                except OSError:
                    pass


def setup(bot):
    bot.add_cog(ConvertCog(bot))
