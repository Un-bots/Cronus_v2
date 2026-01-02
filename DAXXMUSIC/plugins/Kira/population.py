from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from DAXXMUSIC import app


@app.on_message(filters.command("population"))
def country_command_handler(client: Client, message: Message):
    # Check input
    if len(message.command) < 2:
        return message.reply_text(
            "❌ **Usage:**\n`/population <country code>`\n\n"
            "Example: `/population in`",
            quote=True,
        )

    country_code = message.command[1].strip()

    api_url = f"https://restcountries.com/v3.1/alpha/{country_code}"

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()

        country_info = response.json()
        if not country_info:
            return message.reply_text("❌ ɴᴏ ᴅᴀᴛᴀ ғᴏᴜɴᴅ.")

        data = country_info[0]

        country_name = data.get("name", {}).get("common", "ɴ/ᴀ")
        capital = data.get("capital", ["ɴ/ᴀ"])[0]
        population = data.get("population", "ɴ/ᴀ")

        text = (
            "🌍 **ᴄᴏᴜɴᴛʀʏ ɪɴғᴏʀᴍᴀᴛɪᴏɴ**\n\n"
            f"• **ɴᴀᴍᴇ :** {country_name}\n"
            f"• **ᴄᴀᴘɪᴛᴀʟ :** {capital}\n"
            f"• **ᴘᴏᴘᴜʟᴀᴛɪᴏɴ :** {population}\n\n"
            "✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot"
        )

    except requests.exceptions.HTTPError:
        text = "❌ **ɪɴᴠᴀʟɪᴅ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ.**\nExample: `in`, `us`, `gb`"
    except Exception:
        text = "❌ **sᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ. ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.**"

    message.reply_text(text, quote=True)
