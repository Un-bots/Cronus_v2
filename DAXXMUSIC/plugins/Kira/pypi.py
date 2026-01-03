from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from DAXXMUSIC import app


def get_pypi_info(package_name: str):
    api_url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        r = requests.get(api_url, timeout=10)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


@app.on_message(filters.command("pypi"))
def pypi_info_command(client: Client, message: Message):
    if len(message.command) < 2:
        return message.reply_text(
            "❌ **ᴜsᴀɢᴇ:**\n`/pypi <package_name>`\n\n"
            "📦 Example: `/pypi pyrogram`",
            quote=True,
        )

    package_name = message.command[1].strip()
    pypi_info = get_pypi_info(package_name)

    if not pypi_info:
        return message.reply_text(
            "❌ **ᴘᴀᴄᴋᴀɢᴇ ɴᴏᴛ ғᴏᴜɴᴅ**\n"
            "Please check the package name.",
            quote=True,
        )

    info = pypi_info.get("info", {})

    name = info.get("name", "N/A")
    version = info.get("version", "N/A")
    summary = info.get("summary", "No description available.")
    homepage = (
        info.get("project_urls", {}).get("Homepage")
        or info.get("home_page")
        or "N/A"
    )

    text = (
        f"📦 **ᴘʏᴘɪ ᴘᴀᴄᴋᴀɢᴇ ɪɴғᴏ**\n\n"
        f"• **ɴᴀᴍᴇ:** `{name}`\n"
        f"• **ʟᴀᴛᴇsᴛ ᴠᴇʀsɪᴏɴ:** `{version}`\n"
        f"• **ᴅᴇsᴄʀɪᴘᴛɪᴏɴ:** {summary}\n"
        f"• **ʜᴏᴍᴇᴘᴀɢᴇ:** {homepage}\n\n"
        f"✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot"
    )

    message.reply_text(text, disable_web_page_preview=True)
