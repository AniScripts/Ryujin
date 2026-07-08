import nextcord
from nextcord.ext import commands
import os
import re

from services.media import cut_audio
from cogs.utils.base import RyujinCog


class CutAudioCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
    @nextcord.slash_command(name="cut_audio", description="Cut an audio file to a specific duration")
    async def cut_audio(
        self,
        interaction: nextcord.Interaction,
        audio: nextcord.Attachment,
        start_time: str = nextcord.SlashOption(description="Start time (format: 0:00)", required=True),
        end_time: str = nextcord.SlashOption(description="End time (format: 0:00)", required=True),
    ):
        if await self.blacklist_guard(interaction):
            return

        if not audio.filename.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg')):
            await interaction.response.send_message("Please provide a valid audio file.", ephemeral=True)
            return

        def time_to_seconds(time_str):
            parts = time_str.split(':')
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            raise ValueError

        try:
            start_sec = time_to_seconds(start_time)
            end_sec = time_to_seconds(end_time)
        except ValueError:
            await interaction.response.send_message("Invalid time format. Please use format 0:00", ephemeral=True)
            return

        if start_sec >= end_sec:
            await interaction.response.send_message("Start time must be less than end time.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        input_path = f"temp/cut_in_{audio.filename}"
        output_path = f"temp/cut_out_{audio.filename}"
        try:
            os.makedirs('temp', exist_ok=True)
            await audio.save(input_path)

            result = await cut_audio(input_path, output_path, start_sec, end_sec)

            await interaction.followup.send(
                f"Audio cut successfully!\n"
                f"Duration: {result['duration']} seconds\n"
                f"Original size: {result['original_size']/1024/1024:.2f} MB\n"
                f"Cut size: {result['cut_size']/1024/1024:.2f} MB",
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
    bot.add_cog(CutAudioCog(bot))
