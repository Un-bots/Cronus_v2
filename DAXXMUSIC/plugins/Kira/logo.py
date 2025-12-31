import aiohttp
from pyrogram import filters
from pyrogram.types import Message
from DAXXMUSIC import app


@app.on_message(filters.command("logo"))
async def logo(_, msg: Message):
    if len(msg.command) == 1:
        return await msg.reply_text(
            "❌ **Invalid Usage**\n\n`/logo your text`",
            quote=True,
        )

    text = msg.text.split(None, 1)[1]
    url = f"https://api.sdbots.tech/logohq?text={text}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            image_url = str(resp.url)

    await msg.reply_photo(photo=image_url)


@app.on_message(filters.command("animelogo"))
async def animelogo(_, msg: Message):
    if len(msg.command) == 1:
        return await msg.reply_text(
            "❌ **Invalid Usage**\n\n`/animelogo your text`",
            quote=True,
        )

    text = msg.text.split(None, 1)[1]
    url = f"https://api.sdbots.tech/anime-logo?name={text}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            image_url = str(resp.url)

    await msg.reply_photo(photo=image_url)


# ================= HELP SYSTEM =================
__mod_name__ = "Fᴜɴ"

__help__ = """
❍ /gay : ғᴜɴ ɢᴀʏ ᴍᴇᴛᴇʀ (ʀᴀɴᴅᴏᴍ)

❍ /logo <ᴛᴇxᴛ> : ɢᴇɴᴇʀᴀᴛᴇs ʟᴏɢᴏ
❍ /animelogo <ᴛᴇxᴛ> : ᴀɴɪᴍᴇ sᴛʏʟᴇ ʟᴏɢᴏ
"""
