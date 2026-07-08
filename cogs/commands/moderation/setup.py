import discord
from discord.ext import commands
from discord import app_commands
import asyncio

from cogs.utils.constants import RYUJIN_LOGO
from cogs.utils.base import RyujinCog

SYSTEM_CONFIG = {
    "youtubedl": {
        "title": "YouTube Downloader",
        "description": "Send a YouTube video link here and the bot will download it.",
        "image_url": "https://media.discordapp.net/attachments/977518313217347604/1190938143935967242/image.png",
        "label": "YouTube Video DL",
        "emoji": "\ud83c\udfa5",
    },
    "youtubedlaudio": {
        "title": "YouTube Audio Downloader",
        "description": "Send a YouTube link here and the bot will extract the audio.",
        "image_url": "https://media.discordapp.net/attachments/1060154095161319585/1206256287415935026/image.png",
        "label": "YouTube Audio DL",
        "emoji": "\ud83c\udfb5",
    },
    "tiktokdl": {
        "title": "TikTok Downloader",
        "description": "Send a TikTok link here and the bot will download the video.",
        "image_url": "https://media.discordapp.net/attachments/977518313217347604/1230776377427365950/image.png",
        "label": "TikTok DL",
        "emoji": "\ud83c\udfa4",
    },
    "instagramdl": {
        "title": "Instagram Downloader",
        "description": "Send an Instagram post link here and the bot will download it.",
        "image_url": "https://cdn.moongetsu.ro/Ryujin/InstagramDL/embed-image.png",
        "label": "Instagram DL",
        "emoji": "\ud83d\udcf7",
    },
    "removebg": {
        "title": "Remove Background",
        "description": "Send an image here and the bot will remove its background.",
        "image_url": "https://media.discordapp.net/attachments/1060170039078178856/1157948324947697746/image.png",
        "label": "Remove Background",
        "emoji": "\ud83d\uddbc\ufe0f",
    },
    "animesearch": {
        "title": "Anime Search",
        "description": "Send an anime screenshot here and the bot will find the source.",
        "image_url": "https://cdn.moongetsu.ro/Ryujin/AnimeSearch/embed-image.png",
        "label": "Anime Search",
        "emoji": "\ud83d\udd0d",
    },
    "songsearch": {
        "title": "Song Search",
        "description": "Send audio or a YouTube/TikTok link here to identify the song.",
        "image_url": "https://cdn.moongetsu.ro/Ryujin/SongSearch/embed-image.png",
        "label": "Song Search",
        "emoji": "\ud83c\udfb6",
    },
    "fontsearch": {
        "title": "Font Search",
        "description": "Send a font screenshot here and the bot will identify it.",
        "image_url": "https://cdn.moongetsu.ro/Ryujin/FontSearch/embed-image.png",
        "label": "Font Search",
        "emoji": "\ud83d\udd24",
    },
    "ryujinai": {
        "title": "Ryujin AI",
        "description": "Chat with Ryujin AI for editing advice, creative ideas, and help.",
        "image_url": "https://cdn.moongetsu.ro/Ryujin/RyujinAI/embed-image.png",
        "label": "Ryujin AI",
        "emoji": "\ud83e\udd16",
    },
}


class SetupSelect(discord.ui.Select):
    def __init__(self, bot):
        options = []
        for table, cfg in SYSTEM_CONFIG.items():
            options.append(
                discord.SelectOption(
                    label=cfg["label"],
                    description=cfg["description"][:100],
                    emoji=cfg["emoji"],
                    value=table,
                )
            )
        super().__init__(
            placeholder="Select features to set up...",
            min_values=1,
            max_values=len(options),
            options=options,
        )
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild
        if not guild:
            await interaction.followup.send("This command can only be used in a server.", ephemeral=True)
            return

        if not guild.me.guild_permissions.manage_channels:
            await interaction.followup.send(
                "I need the **Manage Channels** permission to create channels. Please grant it and try again.",
                ephemeral=True,
            )
            return

        selected = self.values
        cursor = self.bot.connection.cursor()

        category = await self._get_or_create_category(guild)

        created = []
        skipped = []
        failed = []

        for table in selected:
            cfg = SYSTEM_CONFIG[table]
            channel_name = cfg["label"].lower().replace(" ", "-")

            cursor.execute(f"SELECT channel_id FROM {table} WHERE server_id = %s", (str(guild.id),))
            existing = cursor.fetchone()
            if existing:
                skipped.append(cfg["label"])
                continue

            try:
                overwrites = self._build_overwrites(guild)
                channel = await category.create_text_channel(
                    name=channel_name,
                    overwrites=overwrites,
                    reason=f"Ryujin setup by {interaction.user}",
                )

                cursor.execute(
                    f"INSERT INTO {table} (server_id, channel_id) VALUES (%s, %s)",
                    (str(guild.id), str(channel.id)),
                )
                self.bot.connection.commit()

                embed = discord.Embed(
                    title=cfg["title"],
                    description=cfg["description"],
                    color=0x2a2a2a,
                )
                embed.set_image(url=cfg["image_url"])
                embed.set_footer(
                    text=f"(c) Ryujin Bot (2023-2025) | {cfg['title']}",
                    icon_url=RYUJIN_LOGO,
                )
                embed.set_author(name="Ryujin", icon_url=RYUJIN_LOGO)
                info_msg = await channel.send(embed=embed)
                await info_msg.pin()
                created.append(cfg["label"])

            except Exception as e:
                failed.append(f"{cfg['label']} ({e})")

        cursor.close()

        embed = discord.Embed(
            title="Ryujin Setup Complete",
            color=0x2a2a2a,
        )
        if created:
            embed.add_field(name=f"Created ({len(created)})", value="\n".join(f"{cfg['emoji']} {name}" for cfg in SYSTEM_CONFIG.values() if cfg['label'] in created) or "None", inline=False)
        if skipped:
            embed.add_field(name=f"Skipped - already set ({len(skipped)})", value="\n".join(f"- {name}" for name in skipped), inline=False)
        if failed:
            embed.add_field(name=f"Failed ({len(failed)})", value="\n".join(f"- {name}" for name in failed), inline=False)

        embed.set_footer(text="(c) Ryujin Bot (2023-2025) | Setup System", icon_url=RYUJIN_LOGO)
        embed.set_author(name="Ryujin", icon_url=RYUJIN_LOGO)
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def _get_or_create_category(self, guild):
        category_name = "Ryujin"
        existing = discord.utils.get(guild.categories, name=category_name)
        if existing:
            return existing
        return await guild.create_category(
            name=category_name,
            reason="Ryujin system channels",
        )

    def _build_overwrites(self, guild):
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                attach_files=True,
            ),
            guild.me: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                manage_messages=True,
                manage_channels=True,
                attach_files=True,
            ),
        }
        return overwrites


class SetupView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.add_item(SetupSelect(bot))


class SetupCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup", description="Quick setup: auto-create Ryujin system channels")
    async def setup(self, interaction: discord.Interaction):
        if not (interaction.user.id == 977190163736322088 or
                interaction.user == interaction.guild.owner or
                interaction.user.guild_permissions.administrator):
            await interaction.response.send_message("Only the server owner or administrators can use this command.", ephemeral=True)
            return

        if not self.bot.connection:
            await interaction.response.send_message("Database connection is not available. Setup cannot proceed.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Ryujin Setup",
            description="Select which features you want to set up. Channels will be auto-created in a **Ryujin** category.\n\nFeatures already configured will be skipped.",
            color=0x2a2a2a,
        )
        embed.set_footer(text="(c) Ryujin Bot (2023-2025) | Setup System", icon_url=RYUJIN_LOGO)
        embed.set_author(name="Ryujin", icon_url=RYUJIN_LOGO)

        view = SetupView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(SetupCog(bot))
