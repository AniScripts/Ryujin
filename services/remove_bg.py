import logging
import urllib.parse
import aiohttp
from io import BytesIO

log = logging.getLogger(__name__)


async def remove_background(image_data_bytes):
    import os
    api_url = os.getenv("REMOVEBG_API_URL", "http://191.96.94.248:5080/remove-bg")

    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field("image", image_data_bytes, filename="image.png", content_type="image/png")
        async with session.post(api_url, data=form) as resp:
            if resp.status != 200:
                try:
                    err = await resp.json()
                    msg = err.get("error", f"API returned status {resp.status}")
                except Exception:
                    msg = f"API returned status {resp.status}"
                raise RuntimeError(msg)
            return await resp.read()
