import asyncio
import os
import time

from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from yt_dlp import YoutubeDL

from DAXXMUSIC import app
import config

# ================= SETTINGS =================
COOLDOWN_TIME = 3          # seconds
AUTO_DELETE_TIME = 3600    # 1 hour

user_cooldown = {}


def is_privileged(user_id: int) -> bool:
    return user_id in config.SUDO_USERS or user_id == config.OWNER_ID


ADD_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ",
                url="https://t.me/kira_probot?startgroup=true",
            )
        ]
    ]
)


@app.on_message(filters.command(["yt", "video"]))
async def yt_video_download(_, message: Message):
    user_id = message.from_user.id

    # ---------- COOLDOWN CHECK ----------
    if not is_privileged(user_id):
        last_time = user_cooldown.get(user_id, 0)
        now = time.time()
        remaining = COOLDOWN_TIME - (now - last_time)

        if remaining > 0:
            warn = await message.reply_text(
                f"⏳ **Please wait...**\n\n"
                f"You can use this command again in **{remaining:.1f} seconds**.\n\n"
                "💡 To avoid cooldown, add the bot to your group.",
                reply_markup=ADD_BUTTON,
                quote=True,
            )
            await asyncio.sleep(5)
            return await warn.delete()

        user_cooldown[user_id] = now

    # ---------- INPUT CHECK ----------
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ **Invalid Usage**\n\n"
            "`/video <song name or youtube link>`",
            quote=True,
        )

    query = message.text.split(None, 1)[1]

    status = await message.reply_text(
        "🔎 sᴇᴀʀᴄʜɪɴɢ ʏᴏᴜᴛᴜʙᴇ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..."
    )

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "quiet": True,
        "nocheckcertificate": True,
        "geo_bypass": True,
        "outtmpl": "downloads/%(id)s.%(ext)s",
    }

    try:
        loop = asyncio.get_running_loop()

        def download():
            with YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(query, download=True)

        info = await loop.run_in_executor(None, download)

    except Exception as e:
        return await status.edit(
            f"❌ **Failed to download video**\n\n`{str(e)}`"
        )

    file_path = f"downloads/{info['id']}.{info['ext']}"

    caption = (
        f"🎬 **ᴛɪᴛʟᴇ :** [{info.get('title')}]({info.get('webpage_url')})\n"
        f"📺 **ᴄʜᴀɴɴᴇʟ :** {info.get('uploader', 'N/A')}\n"
        f"⏱ **ᴅᴜʀᴀᴛɪᴏɴ :** {int(info.get('duration', 0) // 60)} min\n"
        f"🥀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {message.from_user.mention}\n\n"
        "⚠️ **Note:** This media will be **automatically deleted after 1 hour**.\n"
        "📥 Please forward or save it if needed.\n\n"
        "✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot"
    )

    await status.delete()

    sent = await message.reply_video(
        video=file_path,
        caption=caption,
        supports_streaming=True,
        reply_markup=ADD_BUTTON,
    )

    # ---------- AUTO DELETE MEDIA ----------
    async def auto_delete(msg, path):
        await asyncio.sleep(AUTO_DELETE_TIME)
        try:
            await msg.delete()
        except:
            pass
        if os.path.exists(path):
            os.remove(path)

    asyncio.create_task(auto_delete(sent, file_path))


# ================= HELP SYSTEM =================
__mod_name__ = "Vɪᴅᴇᴏ"

__help__ = """
❍ /video <ɴᴀᴍᴇ / ʟɪɴᴋ> : ᴅᴏᴡɴʟᴏᴀᴅs ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ
❍ /yt <ɴᴀᴍᴇ / ʟɪɴᴋ> : sᴀᴍᴇ ᴀs /video
"""
