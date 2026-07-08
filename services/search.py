import logging
import urllib.parse
import aiohttp
import os
import uuid
import asyncio
import yt_dlp
import subprocess
from tiktok_downloader import snaptik
from shazamio import Shazam

from cogs.utils.helpers import extract_video_id_from_url

log = logging.getLogger(__name__)


async def anime_search(image_url):
    encoded_url = urllib.parse.quote_plus(image_url)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.trace.moe/search?anilistInfo&url={encoded_url}") as resp:
            if resp.status != 200:
                raise RuntimeError(f"trace.moe API returned status {resp.status}")
            return await resp.json()


async def font_search(image_data_bytes):
    api_key = os.getenv("WHATFONTIS_API_KEY", "")
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field("file", image_data_bytes, filename="image.jpg", content_type="image/jpeg")
        headers = {"Authorization": f"Bearer {api_key}"}
        async with session.post("https://api.whatfontis.com/v2/fonts", headers=headers, data=form) as resp:
            if resp.status != 200:
                raise RuntimeError(f"WhatFontIs API returned status {resp.status}")
            return await resp.json()


async def _download_audio_for_search(url):
    if url.startswith(("https://www.youtube.com/", "https://youtu.be/", "https://youtube.com/shorts/")):
        clean_url = extract_video_id_from_url(url)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'temp/%(title)s.%(ext)s',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            'noplaylist': True,
            'extract_flat': False,
        }
        def _dl():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(clean_url, download=True)
                return ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
        return await asyncio.to_thread(_dl)

    elif url.startswith(("https://www.tiktok.com/", "https://vm.tiktok.com/", "https://vt.tiktok.com/")):
        video_objects = await asyncio.to_thread(snaptik, url)
        if not video_objects:
            raise RuntimeError("Could not download TikTok audio")
        unique_id = str(uuid.uuid4())[:8]
        file_path = f"temp/tiktok_{unique_id}.mp3"
        temp_video = f"temp/tiktok_{unique_id}.mp4"
        def _dl():
            video_objects[0].download(temp_video)
            subprocess.run(['ffmpeg', '-i', temp_video, '-q:a', '0', '-map', 'a', file_path], capture_output=True)
            os.remove(temp_video)
            return file_path
        return await asyncio.to_thread(_dl)

    return None


async def song_search(source):
    file_path = None
    if source.startswith(("http://", "https://")):
        file_path = await _download_audio_for_search(source)
        if not file_path:
            raise RuntimeError("Failed to download audio for identification")
    elif os.path.isfile(source):
        file_path = source
    else:
        raise ValueError("source must be a URL or file path")

    try:
        shazam = Shazam()
        result = await shazam.recognize(file_path)
        return result
    finally:
        if file_path and file_path.startswith("temp/") and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass
