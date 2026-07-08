import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from cogs.utils.base import RyujinCog

class HelpCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="help",
        description="Shows all Ryujin's commands!",
    )
    async def help(self, interaction: discord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        commands_dict = {
            "Meta": [
                ("info", "Shows information about the bot"),
                ("help", "Shows all Ryujin's commands"),
                ("ping", "Check bot latency and response time"),
                ("pong", "Respond with ping"),
                ("latency", "Get detailed latency information"),
                ("resources", "Shows all the available editing resources"),
                ("bug", "Sends the server support link to report a bug"),
                ("donate", "Support the development of Ryujin"),
                ("bot_stats", "Display detailed statistics about the bot")
            ],
            "Resources": [
                ("overlay", "Sends a random overlay"),
                ("edit_audio <style>", "Sends a random edit audio for each style"),
                ("audios_categories", "Shows all the available audio categories"),
                ("random_edit", "Sends a random edit"),
                ("compress_file <file>", "Compress a file"),
                ("resize_video <video> <width> <height>", "Resize a video"),
                ("sfx <category>", "Sends a random SFX from a category"),
                ("sfx_categories", "See the SFX categories")
            ],
            "After Effects": [
                ("preset <type>", "Sends a random preset from a category"),
                ("presets_categories", "Sends all preset categories"),
                ("projects_list", "Shows all project files"),
                ("project_file <name>", "Get a project file with preview"),
                ("scripts_list", "Shows all scripts"),
                ("script <number>", "Sends a script"),
                ("extensions_list", "Shows all extensions"),
                ("extension <number>", "Sends an extension")
            ],
            "Media Processing": [
                ("nightcore <song>", "Convert audio to Nightcore"),
                ("spedup <song>", "Convert audio to Sped Up"),
                ("slowed <song>", "Convert audio to Slowed"),
                ("convert <from> <to> <file>", "Convert file format"),
                ("cut_audio <audio> <start> <end>", "Cut audio to duration")
            ],
            "Social": [
                ("trending", "See what's trending in AMV Community"),
                ("generatetags", "Generate hashtags for posting"),
                ("afk", "Set AFK status"),
                ("afk_list", "Show all AFK users")
            ],
            "Moderation": [
                ("managesystem", "Setup system channels"),
                ("disableads", "Disable promotional messages"),
                ("slowmode", "Enable slowmode in a channel"),
                ("remove_slowmode", "Disable slowmode in a channel"),
                ("lock", "Restrict messages in a channel"),
                ("unlock", "Allow messages in a channel"),
                ("purge", "Bulk delete messages"),
                ("timeout", "Temporarily mute a user"),
                ("remove_timeout", "Remove timeout from a user"),
                ("kick", "Kick a user with DM notification"),
                ("ban", "Ban a user with DM notification"),
                ("unban", "Unban a user"),
                ("softban", "Softban (ban + unban)"),
                ("warn", "Warn a user"),
                ("warns", "View warnings for a user"),
                ("remove_warn", "Remove a warning")
            ],
            "Admin": [
                ("blacklist", "Manage user blacklist (Owner)"),
                ("apikey", "Manage remove.bg API keys"),
                ("add_trending_anime", "Add trending anime"),
                ("add_trending_song", "Add trending song"),
                ("remove_trending", "Remove from trending"),
                ("show_guilds", "List all bot guilds (Owner)")
            ]
        }

        embed = discord.Embed(
            title="Ryujin Command Guide",
            description="Here's everything I can help you with:",
            color=0x2a2a2a
        )

        for category, cmds in commands_dict.items():
            formatted_commands = "\n".join(f"`/{cmd}` • {desc}" for cmd, desc in cmds)
            embed.add_field(
                name=f"━━ {category} ━━",
                value=formatted_commands,
                inline=False
            )

        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Information System",
            icon_url=self.logo
        )
        embed.set_author(
            name="Ryujin",
            icon_url=self.logo
        )
        await self.bot.maybe_send_ad(interaction)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))