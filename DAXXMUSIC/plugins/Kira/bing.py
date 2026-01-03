from DAXXMUSIC import app
import requests as r
from pyrogram import filters

API_URL = "https://sugoi-api.vercel.app/search"


@app.on_message(filters.command("bingsearch"))
async def bing_search(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ **ᴜsᴀɢᴇ:**\n`/bingsearch <ǫᴜᴇʀʏ>`\n\n"
            "Example:\n`/bingsearch bill gates`",
            quote=True,
        )

    keyword = " ".join(message.command[1:]).strip()

    try:
        response = r.get(API_URL, params={"keyword": keyword}, timeout=15)

        if response.status_code != 200:
            return await message.reply_text(
                "⚠️ **sᴇᴀʀᴄʜ sᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ.**\nᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ."
            )

        results = response.json()
        if not results:
            return await message.reply_text(
                "🔍 **ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ.**"
            )

        text = f"🔎 **ʙɪɴɢ sᴇᴀʀᴄʜ ʀᴇsᴜʟᴛs**\n\n"
        for i, result in enumerate(results[:7], start=1):
            title = result.get("title", "No title")
            link = result.get("link", "")
            text += f"**{i}. {title}**\n{link}\n\n"

        text += "✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot"

        await message.reply_text(
            text,
            disable_web_page_preview=True,
        )

    except Exception as e:
        await message.reply_text(
            "❌ **ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ.**\n"
            "ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ."
        )
