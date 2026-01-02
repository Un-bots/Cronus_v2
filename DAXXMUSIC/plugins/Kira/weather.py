from pyrogram import Client, filters
from pyrogram.types import Message
from DAXXMUSIC import app


@app.on_message(filters.command("weather"))
def weather(client: Client, message: Message):
    if len(message.command) < 2:
        return message.reply_text(
            "❌ **Usage:**\n`/weather <city name>`\n\n"
            "Example: `/weather new york`",
            quote=True,
        )

    location = " ".join(message.command[1:]).strip()
    weather_url = f"https://wttr.in/{location}.png"

    message.reply_photo(
        photo=weather_url,
        caption=(
            f"🌦 **ᴡᴇᴀᴛʜᴇʀ ᴜᴘᴅᴀᴛᴇ**\n"
            f"📍 {location.title()}\n\n"
            "✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot"
        ),
    )
