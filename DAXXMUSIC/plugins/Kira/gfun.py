import random
from pyrogram import filters
from pyrogram.types import Message
from DAXXMUSIC import app


def calculate_gay_percentage():
    return random.randint(1, 100)


def generate_gay_response(percent: int) -> str:
    if percent < 30:
        return "ʏᴏᴜ'ʀᴇ sᴛʀᴀɪɢʜᴛ ᴀs ᴀɴ ᴀʀʀᴏᴡ. 🏹"
    elif percent < 70:
        return "ʏᴏᴜ ᴍɪɢʜᴛ ʜᴀᴠᴇ ᴀ ʙɪᴛ ᴏғ ᴀ ʀᴀɪɴʙᴏᴡ ɪɴ ʏᴏᴜ. 🌈"
    else:
        return "ʏᴏᴜ'ʀᴇ sʜɪɴɪɴɢ ᴡɪᴛʜ ʀᴀɪɴʙᴏᴡ ᴄᴏʟᴏʀs! 🌟🏳️‍🌈"


@app.on_message(filters.command("gay"))
async def gay_meter(_, message: Message):
    percent = calculate_gay_percentage()
    response = generate_gay_response(percent)

    await message.reply_text(
        f"🏳️‍🌈 **ɢᴀʏ ᴍᴇᴛᴇʀ**\n\n"
        f"**ᴘᴇʀᴄᴇɴᴛᴀɢᴇ :** `{percent}%`\n"
        f"{response}\n\n"
        "✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot",
        quote=True,
    )
