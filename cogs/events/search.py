import nextcord
from nextcord.ext import commands
import logging
import asyncio
import aiohttp

from cogs.utils.constants import RYUJIN_LOGO


class SearchListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_search_channels(self, guild_id):
        if not self.bot.connection:
            return {}
        cursor = self.bot.connection.cursor()
        configs = {}
        for table in ["animesearch", "songsearch", "fontsearch"]:
            cursor.execute(f"SELECT channel_id FROM {table} WHERE server_id = %s", (str(guild_id),))
            result = cursor.fetchone()
            if result:
                configs[table] = int(result[0])
        cursor.close()
        return configs

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or not message.guild:
            return

        channel_configs = await self.get_search_channels(message.guild.id)
        if not channel_configs:
            return

        channel_id = message.channel.id

        if channel_configs.get("animesearch") == channel_id:
            await self._handle_anime_search(message)
        elif channel_configs.get("songsearch") == channel_id:
            await self._handle_song_search(message)
        elif channel_configs.get("fontsearch") == channel_id:
            await self._handle_font_search(message)

    async def _handle_anime_search(self, message):
        from services.search import anime_search

        if not message.attachments:
            return
        attachment = message.attachments[0]
        if not any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
            return

        try:
            result = await anime_search(attachment.url)
            if not result.get('result') or len(result['result']) == 0:
                embed = nextcord.Embed(title="No Match Found", description="Sorry, I couldn't find any matching anime for this image.", color=0xed4245)
                await message.channel.send(embed=embed)
                return

            best_match = result['result'][0]
            anilist = best_match['anilist']

            embed = nextcord.Embed(title="Anime Found!", description="Here's what I found:", color=0x2a2a2a)
            titles = f"English: {anilist['title']['english']}\nRomaji: {anilist['title']['romaji']}\nNative: {anilist['title']['native']}"
            embed.add_field(name="Anime Title", value=f"```{titles}```", inline=False)
            embed.add_field(name="Episode", value=f"```{best_match.get('episode', 'Unknown')}```", inline=True)
            embed.add_field(name="Match Accuracy", value=f"```{best_match['similarity'] * 100:.2f}%```", inline=True)

            if 'from' in best_match and 'to' in best_match:
                fm, fs = int(best_match['from'] // 60), int(best_match['from'] % 60)
                tm, ts = int(best_match['to'] // 60), int(best_match['to'] % 60)
                embed.add_field(name="Timestamp", value=f"```{fm:02d}:{fs:02d} - {tm:02d}:{ts:02d}```", inline=True)

            embed.set_image(url=attachment.url)
            embed.set_footer(text="(c) Ryujin Bot (2023-2025) | Anime Search (Powered by trace.moe & AniList)", icon_url=RYUJIN_LOGO)
            embed.set_author(name="Ryujin", icon_url=RYUJIN_LOGO)
            await message.reply(embed=embed)

        except Exception as e:
            logging.error("Anime search error: %s", e)
            embed = nextcord.Embed(title="Error", description="Sorry, there was an error processing your request.", color=0xff0000)
            embed.set_footer(text="(c) Ryujin Bot (2023-2025) | Anime Search System", icon_url=RYUJIN_LOGO)
            await message.channel.send(embed=embed)

    async def _handle_song_search(self, message):
        from services.search import song_search

        try:
            source = None
            if message.content.startswith(("https://www.youtube.com/", "https://youtu.be/", "https://youtube.com/shorts/",
                                           "https://www.tiktok.com/", "https://vm.tiktok.com/", "https://vt.tiktok.com/")):
                source = message.content
            elif message.attachments:
                for attachment in message.attachments:
                    if attachment.filename.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg', '.mp4', '.webm')):
                        file_path = f"temp/{attachment.filename}"
                        await attachment.save(file_path)
                        source = file_path
                        break
                if not source:
                    await message.delete()
                    warning = await message.channel.send("**This channel is only for identifying songs. Please upload an audio file or share a video link!**")
                    await asyncio.sleep(5)
                    await warning.delete()
                    return
            else:
                await message.delete()
                warning = await message.channel.send("**Please upload an audio file or share a supported video link!**")
                await asyncio.sleep(5)
                await warning.delete()
                return

            result = await song_search(source)

            if not result or 'track' not in result:
                embed = nextcord.Embed(title="No Match Found", description="Sorry, I couldn't identify any song.", color=0xed4245)
                embed.set_footer(text="(c) Ryujin Bot (2023-2025) | Song Finder System", icon_url=RYUJIN_LOGO)
                embed.set_author(name="Ryujin", icon_url=RYUJIN_LOGO)
                await message.channel.send(embed=embed)
                return

            track = result['track']
            embed = nextcord.Embed(title="Song Found!", description="Here's what I found:", color=0x2a2a2a)
            embed.add_field(name="Title", value=f"```{track.get('title', 'Unknown')}```", inline=True)
            embed.add_field(name="Artist", value=f"```{track.get('subtitle', 'Unknown Artist')}```", inline=True)

            if 'genres' in track:
                embed.add_field(name="Genre", value=f"```{track['genres'].get('primary', 'Unknown')}```", inline=True)

            links = []
            if 'share' in track:
                if 'spotify' in track['share']:
                    links.append(f"[Spotify]({track['share']['spotify']})")
                if 'apple_music' in track['share']:
                    links.append(f"[Apple Music]({track['share']['apple_music']})")
                if 'youtube' in track['share']:
                    links.append(f"[YouTube]({track['share']['youtube']})")
            if links:
                embed.add_field(name="Listen On", value=" | ".join(links), inline=False)

            if 'images' in track and 'coverart' in track['images']:
                embed.set_image(url=track['images']['coverart'])

            embed.set_footer(text="(c) Ryujin Bot (2023-2025) | Song Finder System", icon_url=RYUJIN_LOGO)
            embed.set_author(name="Ryujin", icon_url=RYUJIN_LOGO)
            await message.channel.send(embed=embed)

        except Exception as e:
            logging.error("Song search error: %s", e)
            embed = nextcord.Embed(title="Error", description=f"An error occurred: {str(e)}", color=0xff0000)
            embed.set_footer(text="(c) Ryujin Bot (2023-2025) | Song Finder System", icon_url=RYUJIN_LOGO)
            embed.set_author(name="Ryujin", icon_url=RYUJIN_LOGO)
            await message.channel.send(embed=embed)

    async def _handle_font_search(self, message):
        from services.search import font_search

        try:
            if not message.attachments:
                await message.delete()
                warning = await message.channel.send("**This channel is only for identifying fonts. Please upload an image!**")
                await asyncio.sleep(5)
                await warning.delete()
                return

            attachment = message.attachments[0]
            if not attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                await message.delete()
                warning = await message.channel.send("**Please upload a valid image file (PNG, JPG, JPEG)!**")
                await asyncio.sleep(5)
                await warning.delete()
                return

            image_data = await attachment.read()
            data = await font_search(image_data)

            embed = nextcord.Embed(title="Font Search Results", description="Here are the closest matching fonts I found:", color=0x2b2d31)
            for i, font in enumerate(data['fonts'][:5], 1):
                embed.add_field(
                    name=f"Match #{i}: {font['name']}",
                    value=f"Family: {font['family']}\nFoundry: {font['foundry']}\nLicense: {font['license']}",
                    inline=False,
                )
            embed.set_image(url=attachment.url)
            embed.set_footer(text="(c) Ryujin Bot (2023-2025) | Font Search System", icon_url=RYUJIN_LOGO)
            embed.set_author(name="Ryujin", icon_url=RYUJIN_LOGO)
            await message.reply(embed=embed)

        except Exception as e:
            logging.error("Font search error: %s", e)
            embed = nextcord.Embed(title="Error", description="Sorry, there was an error processing your request.", color=0xff0000)
            embed.set_footer(text="(c) Ryujin Bot (2023-2025) | Font Search System", icon_url=RYUJIN_LOGO)
            await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(SearchListeners(bot))
