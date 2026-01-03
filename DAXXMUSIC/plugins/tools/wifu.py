import asyncio
import requests
from pyrogram import filters
from DAXXMUSIC import app

# ================= CONFIG =================

AUTO_DELETE_TIME = 1800  # 30 minutes
BOT_USERNAME = "kira_probot"

WAIFU_API_URL = "https://api.waifu.im/search"


def get_waifu_data(tags):
    params = {
        "included_tags": tags,
        "height": ">=2000"
    }
    try:
        r = requests.get(WAIFU_API_URL, params=params, timeout=20)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None


@app.on_message(filters.command("waifu"))
async def waifu_command(_, message):
    try:
        data = get_waifu_data(["maid"])
        if not data or "images" not in data:
            return await message.reply_text("❌ No waifu found.")

        img_url = data["images"][0]["url"]

        caption = (
            "💫 ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot\n\n"
            "⚠️ ᴘʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ᴏʀ sᴀᴠᴇ ᴛʜɪs ᴍᴇᴅɪᴀ.\n"
            "⏳ ɪᴛ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ɪɴ 30 ᴍɪɴᴜᴛᴇs."
        )

        waifu_msg = await message.reply_photo(
            photo=img_url,
            caption=caption
        )

        # Auto delete after 30 minutes
        await asyncio.sleep(AUTO_DELETE_TIME)
        await waifu_msg.delete()

    except Exception:
        await message.reply_text("⚠️ Waifu service is temporarily unavailable.")
