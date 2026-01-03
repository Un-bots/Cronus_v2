from pyrogram import Client, filters
from pyrogram.types import Message
import random

from DAXXMUSIC import app


def get_random_message(love_percentage: int) -> str:
    if love_percentage <= 30:
        return random.choice([
            "💔 ʟᴏᴠᴇ ɪs ɪɴ ᴛʜᴇ ᴀɪʀ, ʙᴜᴛ ɪᴛ ɴᴇᴇᴅs ᴀ ʟɪᴛᴛʟᴇ sᴘᴀʀᴋ.",
            "🙂 ᴀ ɢᴏᴏᴅ sᴛᴀʀᴛ, ʙᴜᴛ ᴛʜᴇʀᴇ’s ʀᴏᴏᴍ ᴛᴏ ɢʀᴏᴡ.",
            "🌱 ɪᴛ’s ᴊᴜsᴛ ᴛʜᴇ ʙᴇɢɪɴɴɪɴɢ ᴏғ sᴏᴍᴇᴛʜɪɴɢ."
        ])
    elif love_percentage <= 70:
        return random.choice([
            "❤️ ᴀ sᴛʀᴏɴɢ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ɪs ᴛʜᴇʀᴇ. ᴋᴇᴇᴘ ɴᴜʀᴛᴜʀɪɴɢ ɪᴛ.",
            "✨ ʏᴏᴜ’ᴠᴇ ɢᴏᴛ ᴀ ɢᴏᴏᴅ ᴄʜᴀɴᴄᴇ. ᴡᴏʀᴋ ᴏɴ ɪᴛ.",
            "🌸 ʟᴏᴠᴇ ɪs ʙʟᴏssᴏᴍɪɴɢ, ᴋᴇᴇᴘ ɢᴏɪɴɢ."
        ])
    else:
        return random.choice([
            "💖 ᴡᴏᴡ! ɪᴛ’s ᴀ ᴍᴀᴛᴄʜ ᴍᴀᴅᴇ ɪɴ ʜᴇᴀᴠᴇɴ!",
            "💞 ᴘᴇʀғᴇᴄᴛ ᴍᴀᴛᴄʜ! ᴄʜᴇʀɪsʜ ᴛʜɪs ʙᴏɴᴅ.",
            "💍 ᴅᴇsᴛɪɴᴇᴅ ᴛᴏ ʙᴇ ᴛᴏɢᴇᴛʜᴇʀ. ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs!"
        ])


@app.on_message(filters.command("love"))
async def love_command(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.reply_text(
            "❌ **ᴜsᴀɢᴇ:**\n`/love name1 name2`\n\n"
            "💡 Example: `/love harsh anshi`",
            quote=True,
        )

    name1 = message.command[1].strip()
    name2 = message.command[2].strip()

    love_percentage = random.randint(10, 100)
    love_message = get_random_message(love_percentage)

    response = (
        f"💘 **ʟᴏᴠᴇ ᴄᴀʟᴄᴜʟᴀᴛᴏʀ** 💘\n\n"
        f"👤 {name1} ❤️ {name2}\n"
        f"📊 **ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ:** `{love_percentage}%`\n\n"
        f"{love_message}\n\n"
        f"✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot"
    )

    await message.reply_text(response)
