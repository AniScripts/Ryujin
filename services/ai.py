import asyncio
import logging
from groq import Groq
import os

from cogs.utils.constants import AI_SYSTEM_PROMPT

log = logging.getLogger(__name__)

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))
    return _client


async def chat_completion(user_message, system_prompt=None, model="llama-3.3-70b-versatile"):
    if system_prompt is None:
        system_prompt = AI_SYSTEM_PROMPT

    def _call():
        client = _get_client()
        return client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            model=model,
        )

    response = await asyncio.to_thread(_call)
    return response.choices[0].message.content
