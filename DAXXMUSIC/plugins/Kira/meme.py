from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import asyncio

from DAXXMUSIC import app

AUTO_DELETE_TIME = 60 * 60  # 1 hour (seconds)


@app.on_message(filters.command("meme"))
async def meme_command(client: Client, message: Message):
    api_url = "https://meme-api.com/gimme"

    try:
        r = requests.get(api_url, timeout=10)
        if r.status_code != 200:
            return await message.reply_text(
                "❌ Failed to fetch meme. Try again later."
            )

        data = r.json()
        meme_url = data.get("url")
        title = data.get("title", "Random Meme")

        if not meme_url:
            return await message.reply_text(
                "❌ Meme not available right now."
            )

        caption = (
            f"😂 **{title}**\n\n"
            f"🥀 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : {message.from_user.mention}\n"
            f"⚠️ ᴛʜɪs ᴍᴇᴍᴇ ᴡɪʟʟ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ɪɴ 1 ʜᴏᴜʀ\n"
            f"✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot"
        )

        sent = await message.reply_photo(
            photo=meme_url,
            caption=caption,
        )

        # ⏳ Auto delete after 1 hour
        await asyncio.sleep(AUTO_DELETE_TIME)
        await sent.delete()

    except Exception:
        await message.reply_text(
            "❌ Something went wrong while fetching meme."
        )
