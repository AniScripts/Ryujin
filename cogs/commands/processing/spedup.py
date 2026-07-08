import discord
from discord.ext import commands
from discord import app_commands
import os

from services.media import pitch_shift
from cogs.utils.base import RyujinCog


class SpedupCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="spedup", description="Converts an uploaded audio file into a Sped Up version.")
    async def spedup_command(self, interaction: discord.Interaction, song: discord.Attachment):
        user_id = interaction.user.id
        if await self.blacklist_guard(interaction):
            return

        await interaction.response.defer(ephemeral=True)

        audio_path = f"temp/{song.filename}"
        output_path = f"temp/spedup_{song.filename}"
        try:
            os.makedirs('temp', exist_ok=True)
            await song.save(audio_path)

            if not audio_path.lower().endswith(('.mp3', '.wav')):
                await interaction.followup.send("Please upload a valid audio file (MP3, WAV).", ephemeral=True)
                return

            await pitch_shift(audio_path, output_path, 1)
            await self.bot.maybe_send_ad(interaction)
            await interaction.followup.send(file=discord.File(output_path), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)
        finally:
            for p in (audio_path, output_path):
                try:
                    if os.path.exists(p):
                        os.remove(p)
                except OSError:
                    pass


async def setup(bot):
    await bot.add_cog(SpedupCog(bot))
