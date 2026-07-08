import os
import uuid
import logging
import asyncio
import yt_dlp
from tiktok_downloader import snaptik

log = logging.getLogger(__name__)


async def download_tiktok_video(url):
    video_objects = await asyncio.to_thread(snaptik, url)
    if not video_objects:
        raise RuntimeError("Failed to get video from TikTok")

    unique_id = str(uuid.uuid4())[:8]
    os.makedirs("temp", exist_ok=True)

    video_path = os.path.join("temp", f"video_{unique_id}.mp4")

    def _merge_parts():
        with open(video_path, 'wb') as output_file:
            for i, video_object in enumerate(video_objects):
                part_path = os.path.join("temp", f"video_{unique_id}_{i}.mp4")
                video_object.download(part_path)
                with open(part_path, 'rb') as input_file:
                    output_file.write(input_file.read())
                os.remove(part_path)

    await asyncio.to_thread(_merge_parts)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'temp/audio_{unique_id}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    def _extract_audio():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"

    try:
        audio_path = await asyncio.to_thread(_extract_audio)
    except Exception as e:
        log.warning("Failed to extract TikTok audio: %s", e)
        audio_path = None

    files = []
    if os.path.exists(video_path):
        files.append(video_path)
    if audio_path and os.path.exists(audio_path):
        files.append(audio_path)

    if not files:
        raise RuntimeError("No files were downloaded")

    return files
