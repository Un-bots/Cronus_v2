import os
from pyrogram import filters
from DAXXMUSIC import app
import config

# ========= SETTINGS =========
# Feature toggle (future ke liye)
REMOVE_BG_ENABLED = False


@app.on_message(filters.command("rmbg"))
async def rmbg(bot, message):
    user_id = message.from_user.id if message.from_user else 0

    # ---- SUDO CHECK ----
    if user_id not in config.SUDO_USERS:
        return await message.reply_text(
            "❌ **Service Unavailable**\n\n"
            "Sorry, this feature is currently not available.\n"
            "Please check back later.",
            quote=True,
        )

    # ---- FEATURE DISABLED ----
    if not REMOVE_BG_ENABLED:
        return await message.reply_text(
            "⚠️ **Temporarily Disabled**\n\n"
            "The background removal service is currently offline "
            "due to maintenance and API limitations.\n\n"
            "We’ll notify you once it’s available again.",
            quote=True,
        )

    # ---- FUTURE IMPLEMENTATION PLACEHOLDER ----
    await message.reply_text(
        "ℹ️ This feature is reserved for future use.",
        quote=True,
    )
