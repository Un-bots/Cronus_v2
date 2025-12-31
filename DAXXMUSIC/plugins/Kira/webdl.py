import os
import re
import aiohttp
import asyncio

from pyrogram import filters
from pyrogram.types import Message

from DAXXMUSIC import app
from DAXXMUSIC.misc import SUDOERS


URL_REGEX = re.compile(
    r"^(https?:\/\/)"
    r"([\w\-]+\.)+[\w\-]+"
    r"([\/\w\-.?=&%+]*)?$"
)


async def fetch_source(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120 Safari/537.36"
        )
    }

    timeout = aiohttp.ClientTimeout(total=20)

    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise RuntimeError(f"HTTP {resp.status}")
            return await resp.text()


@app.on_message(filters.command("webdl") & SUDOERS)
async def web_download(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ **Usage:**\n`/webdl https://example.com`",
            quote=True,
        )

    url = message.command[1]

    if not re.match(URL_REGEX, url):
        return await message.reply_text(
            "❌ **Invalid URL format.**\nPlease provide a valid website URL.",
            quote=True,
        )

    status = await message.reply_text("🌐 ғᴇᴛᴄʜɪɴɢ ᴡᴇʙsɪᴛᴇ sᴏᴜʀᴄᴇ...")

    try:
        source = await fetch_source(url)
    except Exception as e:
        return await status.edit(
            f"❌ ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ sᴏᴜʀᴄᴇ.\n\n**ʀᴇᴀsᴏɴ:** `{e}`"
        )

    file_name = "website_source.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(source)

    await status.delete()
    await message.reply_document(
        document=file_name,
        caption=(
            f"📄 **ᴡᴇʙsɪᴛᴇ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ**\n"
            f"🔗 {url}\n\n"
            "✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot"
        ),
    )

    await asyncio.sleep(2)
    os.remove(file_name)


# ================= HELP SYSTEM =================
__mod_name__ = "WᴇʙDL"

__help__ = """
❍ /webdl <ᴜʀʟ> : ᴅᴏᴡɴʟᴏᴀᴅs ᴡᴇʙsɪᴛᴇ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ (sᴜᴅᴏ ᴏɴʟʏ)
"""
