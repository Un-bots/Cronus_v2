from DAXXMUSIC import app
from pyrogram import filters
import requests

API_URL = "https://sugoi-api.vercel.app/search"


@app.on_message(filters.command("websearch"))
async def web_search(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ **ᴜsᴀɢᴇ:**\n`/websearch <ǫᴜᴇʀʏ>`\n\n"
            "Example:\n`/websearch ai news`",
            quote=True,
        )

    query = " ".join(message.command[1:]).strip()

    try:
        r = requests.get(API_URL, params={"keyword": query}, timeout=15)
        if r.status_code != 200:
            return await message.reply_text(
                "⚠️ **sᴇᴀʀᴄʜ sᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ.**"
            )

        results = r.json()
        if not results:
            return await message.reply_text("🔍 **ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ.**")

        text = "🌐 **ᴡᴇʙ sᴇᴀʀᴄʜ ʀᴇsᴜʟᴛs**\n\n"
        for i, item in enumerate(results[:7], start=1):
            title = item.get("title", "No title")
            link = item.get("link", "")
            text += f"**{i}. {title}**\n{link}\n\n"

        text += "✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot"

        await message.reply_text(
            text,
            disable_web_page_preview=True,
        )

    except Exception:
        await message.reply_text(
            "❌ **ᴇʀʀᴏʀ ғᴇᴛᴄʜɪɴɢ sᴇᴀʀᴄʜ ʀᴇsᴜʟᴛs.**"
        )
