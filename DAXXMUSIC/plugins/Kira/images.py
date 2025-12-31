import httpx
import random
from bs4 import BeautifulSoup
from pyrogram import filters
from pyrogram.types import Message, InputMediaPhoto


@filters.command("img")
async def image_search(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("🖼️ Usage: /img Pm modi")

    query = message.text.split(None, 1)[1]
    search_url = f"https://duckduckgo.com/?q={query}&iax=images&ia=images"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(search_url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    images = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and src.startswith("http"):
            images.append(src)

    if len(images) < 6:
        return await message.reply_text("❌ I did not find the image")

    selected = random.sample(images, 6)

    media = [InputMediaPhoto(photo=url) for url in selected]

    await message.reply_media_group(media)
