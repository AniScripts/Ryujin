import discord
from discord.ext import commands
from discord import app_commands
import os
import re

from services.media import convert_media
from cogs.utils.base import RyujinCog


class ConvertCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    def sanitize_filename(self, filename):
        return re.sub(r'[<>:"/\\|?*]', '', filename)

    @app_commands.command(name="convert", description="Convert a file from one format to another.")
    @app_commands.describe(from_format="Source format", to_format="Target format")
    async def convert(
        self,
        interaction: discord.Interaction,
        from_format: str,
        to_format: str,
        file: discord.Attachment ,
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

            await interaction.followup.send(file=discord.File(output_path), ephemeral=True)
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


async def setup(bot):
    await bot.add_cog(ConvertCog(bot))
