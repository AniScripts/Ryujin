import os
import logging
import asyncio
import yt_dlp

from cogs.utils.helpers import extract_video_id_from_url

log = logging.getLogger(__name__)


async def download_youtube_video(url, boost_count=0):
    boost_count = boost_count or 0
    if boost_count >= 7:
        size_limit = 50 * 1024 * 1024
        ydl_opts = {
            'format': 'bestvideo[height<=1080][ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best',
            'merge_output_format': 'webm',
            'postprocessor_args': ['-c:v', 'copy', '-c:a', 'copy'],
            'outtmpl': 'temp/1080p_%(title)s.webm',
        }
    else:
        size_limit = 8 * 1024 * 1024
        ydl_opts = {
            'format': 'bestvideo[height<=720][ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best',
            'merge_output_format': 'webm',
            'postprocessor_args': ['-c:v', 'copy', '-c:a', 'copy'],
            'outtmpl': 'temp/720p_%(title)s.webm',
        }

    os.makedirs('temp', exist_ok=True)

    def _download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info.get('duration', 0) > 1800:
                raise ValueError("Video exceeds 30 minute limit")
            ydl.download([url])
            return ydl.prepare_filename(info)

    try:
        video_file = await asyncio.to_thread(_download)
    except ValueError:
        return None

    file_size = os.path.getsize(video_file)
    if file_size > size_limit:
        os.remove(video_file)
        raise ValueError(f"Video too large ({file_size / (1024 * 1024):.0f} MB) for this server")

    return video_file


async def download_youtube_audio(url):
    clean_url = extract_video_id_from_url(url)
    if clean_url != url:
        log.info("Cleaned playlist URL: %s -> %s", url, clean_url)

    ydl_opts = {
        'format': 'bestaudio/best[ext=m4a]/best[ext=mp3]/best',
        'outtmpl': 'temp/%(title)s.%(ext)s',
        'postprocessors': [],
        'socket_timeout': 20,
        'retries': 2,
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'extract_flat': False,
    }

    os.makedirs('temp', exist_ok=True)

    def _download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(clean_url, download=False)
            if info.get('duration', 0) > 1800:
                raise ValueError("Audio exceeds 30 minute limit")
            ydl.download([clean_url])
            path = ydl.prepare_filename(info)
        if not os.path.exists(path):
            raise FileNotFoundError("Could not find downloaded audio file")
        return path

    try:
        download_path = await asyncio.to_thread(_download)
    except (ValueError, FileNotFoundError):
        return None

    if os.path.getsize(download_path) == 0:
        os.remove(download_path)
        raise RuntimeError("Downloaded file is empty")

    return download_path
