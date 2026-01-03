import os
import subprocess
from pyrogram import filters
from pyrogram.types import Message

from DAXXMUSIC import app
from DAXXMUSIC.misc import SUDOERS

TMP_DIR = "downloads"
os.makedirs(TMP_DIR, exist_ok=True)

# =====================================================
# REMOVE AUDIO / VIDEO (SUDO ONLY)
# =====================================================

@app.on_message(filters.command("remove") & filters.reply & SUDOERS)
async def remove_media(_, message: Message):
    replied = message.reply_to_message

    if not replied.video:
        return await message.reply_text("❌ Reply to a video file.")

    if len(message.command) < 2:
        return await message.reply_text(
            "❌ **Usage:**\n`/remove audio`\n`/remove video`"
        )

    mode = message.command[1].lower()
    status = await message.reply_text("⚙ Processing...")

    input_video = await replied.download(
        file_name=f"{TMP_DIR}/input.mp4"
    )

    try:
        if mode == "audio":
            out = f"{TMP_DIR}/output.mp3"
            subprocess.run(
                ["ffmpeg", "-y", "-i", input_video, out],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            await message.reply_audio(
                out,
                caption="🎧 ᴀᴜᴅɪᴏ ᴇxᴛʀᴀᴄᴛᴇᴅ\n✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot",
            )

        elif mode == "video":
            out = f"{TMP_DIR}/output.mp4"
            subprocess.run(
                ["ffmpeg", "-y", "-i", input_video, "-an", out],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            await message.reply_video(
                out,
                caption="🎬 ᴠɪᴅᴇᴏ (ᴀᴜᴅɪᴏ ʀᴇᴍᴏᴠᴇᴅ)\n✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot",
            )

        else:
            await status.edit("❌ Use only `/remove audio` or `/remove video`")
            return

        await status.delete()

    except Exception as e:
        await status.edit(f"❌ Error: `{e}`")

    finally:
        for f in os.listdir(TMP_DIR):
            path = os.path.join(TMP_DIR, f)
            if os.path.exists(path):
                os.remove(path)
