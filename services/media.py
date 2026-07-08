import os
import uuid
import subprocess
import asyncio
import logging
from PIL import Image

log = logging.getLogger(__name__)

AUDIO_EXTS = {'.mp3', '.wav', '.m4a', '.ogg'}
VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.ico', '.svg'}
VIDEO_FORMATS = {'MP4', 'MKV', 'MOV', 'AVI'}
AUDIO_FORMATS = {'MP3', 'WAV', 'M4A'}
IMAGE_FORMATS = {'PNG', 'JPG', 'JPEG', 'WEBP', 'ICO', 'SVG'}


async def pitch_shift(input_path, output_path, semitones):
    import nightcore as nc
    def _process():
        nc_audio = input_path @ nc.Tones(semitones)
        nc_audio.export(output_path, format="mp3")
    await asyncio.to_thread(_process)


async def cut_audio(input_path, output_path, start_seconds, end_seconds):
    os.makedirs("temp", exist_ok=True)
    cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-ss', str(start_seconds), '-to', str(end_seconds),
        '-acodec', 'copy', output_path,
    ]
    def _run():
        subprocess.run(cmd, check=True, capture_output=True)
    await asyncio.to_thread(_run)
    return {
        "original_size": os.path.getsize(input_path),
        "cut_size": os.path.getsize(output_path),
        "duration": end_seconds - start_seconds,
    }


async def convert_media(input_path, output_path, from_fmt, to_fmt):
    os.makedirs("temp", exist_ok=True)
    to_ext = to_fmt.lower()

    if from_fmt in VIDEO_FORMATS:
        if to_fmt in AUDIO_FORMATS:
            await _video_to_audio(input_path, output_path, to_ext)
        elif to_fmt in VIDEO_FORMATS:
            await _video_to_video(input_path, output_path, to_ext)
        else:
            raise ValueError(f"Cannot convert video to {to_fmt}")

    elif from_fmt in AUDIO_FORMATS:
        if to_fmt in AUDIO_FORMATS:
            await _audio_to_audio(input_path, output_path, to_ext)
        else:
            raise ValueError(f"Cannot convert audio to {to_fmt}")

    elif from_fmt in IMAGE_FORMATS:
        if to_fmt in IMAGE_FORMATS:
            await _image_to_image(input_path, output_path, to_ext)
        else:
            raise ValueError(f"Cannot convert image to {to_fmt}")
    else:
        raise ValueError(f"Unsupported source format: {from_fmt}")


async def _video_to_audio(input_path, output_path, to_ext):
    codecs = {'mp3': 'libmp3lame', 'wav': 'pcm_s16le', 'm4a': 'aac'}
    codec = codecs.get(to_ext, 'libmp3lame')
    ext = 'm4a' if to_ext == 'm4a' else to_ext
    cmd = ['ffmpeg', '-y', '-i', input_path, '-vn', '-acodec', codec, output_path]
    def _run():
        subprocess.run(cmd, check=True, capture_output=True)
    await asyncio.to_thread(_run)


async def _video_to_video(input_path, output_path, to_ext):
    cmd = ['ffmpeg', '-y', '-i', input_path, '-c:v', 'libx264', '-c:a', 'aac', output_path]
    def _run():
        subprocess.run(cmd, check=True, capture_output=True)
    await asyncio.to_thread(_run)


async def _audio_to_audio(input_path, output_path, to_ext):
    codecs = {'mp3': 'libmp3lame', 'wav': 'pcm_s16le', 'm4a': 'aac'}
    codec = codecs.get(to_ext, 'libmp3lame')
    cmd = ['ffmpeg', '-y', '-i', input_path, '-acodec', codec, output_path]
    def _run():
        subprocess.run(cmd, check=True, capture_output=True)
    await asyncio.to_thread(_run)


async def _image_to_image(input_path, output_path, to_ext):
    pil_format = to_ext.upper()
    if pil_format == 'JPG':
        pil_format = 'JPEG'
    def _run():
        with Image.open(input_path) as img:
            if img.mode in ('RGBA', 'P') and pil_format == 'JPEG':
                img = img.convert('RGB')
            img.save(output_path, pil_format)
    await asyncio.to_thread(_run)


async def compress_video(input_path, output_path):
    cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-c:v', 'libx264', '-crf', '23', '-preset', 'medium',
        '-c:a', 'aac', '-b:a', '128k', output_path,
    ]
    def _run():
        subprocess.run(cmd, check=True, capture_output=True)
    await asyncio.to_thread(_run)


async def compress_audio(input_path, output_path):
    cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-c:a', 'libmp3lame', '-b:a', '192k', output_path,
    ]
    def _run():
        subprocess.run(cmd, check=True, capture_output=True)
    await asyncio.to_thread(_run)


async def compress_image(input_path, output_path, ext):
    def _run():
        with Image.open(input_path) as img:
            if ext in ('.jpg', '.jpeg'):
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                img.save(output_path, 'JPEG', quality=85, optimize=True)
            elif ext == '.png':
                img.save(output_path, 'PNG', optimize=True)
            elif ext == '.webp':
                img.save(output_path, 'WEBP', quality=85)
    await asyncio.to_thread(_run)


async def compress_pdf(input_path, output_path):
    cmd = [
        'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
        '-dPDFSETTINGS=/ebook', '-dNOPAUSE', '-dQUIET', '-dBATCH',
        f'-sOutputFile={output_path}', input_path,
    ]
    def _run():
        subprocess.run(cmd, check=True, capture_output=True)
    await asyncio.to_thread(_run)


async def compress_archive(input_path, output_path):
    cmd = ['7z', 'a', '-mx=9', output_path, input_path]
    def _run():
        subprocess.run(cmd, check=True, capture_output=True)
    await asyncio.to_thread(_run)


async def resize_video(input_path, output_path, width, height):
    vf = f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2'
    cmd = ['ffmpeg', '-y', '-i', input_path, '-vf', vf, '-c:a', 'copy', output_path]
    def _run():
        subprocess.run(cmd, check=True, capture_output=True)
    await asyncio.to_thread(_run)
