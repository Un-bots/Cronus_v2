import aiohttp
from pyrogram import filters
from pyrogram.types import Message
from datetime import datetime
from DAXXMUSIC import app
from config import BOT_USERNAME


# ================= WRITE COMMAND =================
@app.on_message(filters.command("write"))
async def handwrite(_, message: Message):
    if message.reply_to_message and message.reply_to_message.text:
        text = message.reply_to_message.text
    elif len(message.command) > 1:
        text = message.text.split(None, 1)[1]
    else:
        return await message.reply_text(
            "❌ **ɪɴᴠᴀʟɪᴅ ᴜsᴀɢᴇ**\n\n"
            "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴏʀ ᴜsᴇ:\n"
            "`/write your text here`",
            quote=True,
        )

    m = await message.reply_text(
        "✍️ ᴡʀɪᴛɪɴɢ ʏᴏᴜʀ ᴛᴇxᴛ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..."
    )

    try:
        url = f"https://apis.xditya.me/write?text={text}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=15) as resp:
                if resp.status != 200:
                    return await m.edit(
                        "❌ ғᴀɪʟᴇᴅ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ʜᴀɴᴅᴡʀɪᴛɪɴɢ."
                    )
                image_url = str(resp.url)

        caption = (
            "sᴜᴄᴇssғᴜʟʟʏ ᴡʀɪᴛᴛᴇɴ ɪɴ ᴅᴇᴀᴛʜ ɴᴏᴛᴇ ☠️\n"
            f"✨ ᴡʀɪᴛᴛᴇɴ ʙʏ : [神 𝗞ɪʀᴀ](https://t.me/{BOT_USERNAME})\n"
            f"🥀 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : {message.from_user.mention}"
        )

        await m.delete()
        await message.reply_photo(photo=image_url, caption=caption)

    except Exception:
        await m.edit(
            "❌ sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ, ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ."
        )


# ================= DAY COMMAND =================
@app.on_message(filters.command("day"))
async def date_to_day_command(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "❌ **ɪɴᴠᴀʟɪᴅ ᴜsᴀɢᴇ**\n\n"
            "`/day YYYY-MM-DD`\n\n"
            "ᴇxᴀᴍᴘʟᴇ:\n"
            "`/day 1947-08-15`",
            quote=True,
        )

    try:
        input_date = message.command[1]
        date_object = datetime.strptime(input_date, "%Y-%m-%d")
        day_of_week = date_object.strftime("%A")

        await message.reply_text(
            f"📅 **ᴅᴀᴛᴇ :** `{input_date}`\n"
            f"🗓️ **ᴅᴀʏ :** **{day_of_week}**\n\n"
            "✨ _ᴘᴏᴡᴇʀᴇᴅ ʙʏ @kira_probot",
            quote=True,
        )

    except ValueError:
        await message.reply_text(
            "❌ ɪɴᴠᴀʟɪᴅ ᴅᴀᴛᴇ ғᴏʀᴍᴀᴛ.\n"
            "ᴘʟᴇᴀsᴇ ᴜsᴇ `YYYY-MM-DD`.",
            quote=True,
        )


# ================= HELP SYSTEM =================
mod_name = "WʀɪᴛᴇTᴏᴏʟ"

help = """
ᴡʀɪᴛᴇs ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴏɴ ᴀ ᴡʜɪᴛᴇ ᴘᴀɢᴇ ᴡɪᴛʜ ᴀ ᴘᴇɴ 🖊

❍ /write <ᴛᴇxᴛ> : ᴡʀɪᴛᴇs ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ
❍ /day <yyyy-mm-dd> : ғɪɴᴅs ᴅᴀʏ ғʀᴏᴍ ᴅᴀᴛᴇ
"""
