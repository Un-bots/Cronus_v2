from DAXXMUSIC import app
from pyrogram import filters
import feedparser


@app.on_message(filters.command("news"))
async def news_handler(client, message):
    feed_url = "https://news.google.com/rss"

    try:
        feed = feedparser.parse(feed_url)
        if not feed.entries:
            return await message.reply_text("📰 **ɴᴏ ɴᴇᴡs ғᴏᴜɴᴅ.**")

        text = "📰 **ʟᴀᴛᴇsᴛ ɴᴇᴡs**\n\n"
        for i, entry in enumerate(feed.entries[:7], start=1):
            text += f"**{i}. {entry.title}**\n{entry.link}\n\n"

        text += "✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot"

        await message.reply_text(
            text,
            disable_web_page_preview=True,
        )

    except Exception:
        await message.reply_text(
            "❌ **ᴇʀʀᴏʀ ғᴇᴛᴄʜɪɴɢ ɴᴇᴡs.**"
        )

  __help__ = """
❍ /websearch <query> *:* sᴇᴀʀᴄʜ ᴛʜᴇ ᴡᴇʙ.
❍ /news *:* ɢᴇᴛ ʟᴀᴛᴇsᴛ ɴᴇᴡs.
"""

__mod_name__ = "Sᴇᴀʀᴄʜ & Nᴇᴡs"
