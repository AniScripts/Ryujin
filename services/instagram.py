import os
import logging
import asyncio
import requests
import instaloader

log = logging.getLogger(__name__)


def _cleanup_orphans(temp_dir, keep):
    for file in os.listdir(temp_dir):
        fpath = os.path.join(temp_dir, file)
        if fpath not in keep:
            try:
                os.remove(fpath)
            except OSError:
                pass


async def download_instagram_content(url):
    shortcode = url.split("/")[-2]
    temp_dir = "temp/instagramdl"
    os.makedirs(temp_dir, exist_ok=True)

    def _fetch_post():
        L = instaloader.Instaloader(
            dirname_pattern=temp_dir,
            filename_pattern="{shortcode}",
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
        )
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        downloaded_files = []

        if post.typename == "GraphSidecar":
            for i, node in enumerate(post.get_sidecar_nodes()):
                if node.is_video:
                    vp = os.path.join(temp_dir, f"{shortcode}_{i}.mp4")
                    r = requests.get(node.video_url, timeout=30)
                    if r.status_code == 200:
                        with open(vp, 'wb') as f:
                            f.write(r.content)
                        downloaded_files.append(vp)
                else:
                    ip = os.path.join(temp_dir, f"{shortcode}_{i}.jpg")
                    r = requests.get(node.display_url, timeout=30)
                    if r.status_code == 200:
                        with open(ip, 'wb') as f:
                            f.write(r.content)
                        downloaded_files.append(ip)

        elif post.is_video:
            vp = os.path.join(temp_dir, f"{shortcode}.mp4")
            r = requests.get(post.video_url, timeout=30)
            if r.status_code == 200:
                with open(vp, 'wb') as f:
                    f.write(r.content)
                downloaded_files.append(vp)
        else:
            ip = os.path.join(temp_dir, f"{shortcode}.jpg")
            r = requests.get(post.url, timeout=30)
            if r.status_code == 200:
                with open(ip, 'wb') as f:
                    f.write(r.content)
                downloaded_files.append(ip)

        _cleanup_orphans(temp_dir, downloaded_files)
        return downloaded_files

    try:
        result = await asyncio.to_thread(_fetch_post)
    except Exception as e:
        log.error("Instagram download error: %s", e)
        raise RuntimeError(f"Failed to download Instagram content: {e}") from e

    if not result:
        raise RuntimeError("No content was downloaded")

    return result
