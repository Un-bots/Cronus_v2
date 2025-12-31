import re
import time
import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from DAXXMUSIC import app
import config

# ================= REGEX =================
INSTAGRAM = r"(https?://(www\.)?instagram\.com/[^\s]+)"
TWITTER = r"(https?://(www\.)?(x\.com|twitter\.com)/[^\s]+)"
YT_SHORTS = r"(https?://(www\.)?youtube\.com/shorts/[^\s]+)"

# ================= SETTINGS =================
USER_COOLDOWN = {}
GROUP_SETTINGS = {}

COOLDOWN_TIME = 3
COOLDOWN_MSG_DELETE = 5
AUTO_DELETE_TIME = 3600  # 1 hour

# ================= BUTTON =================
ADD_BOT_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "➕ Add KIRA to Your Group",
                url=f"https://t.me/{config.BOT_USERNAME}?startgroup=true",
            )
        ]
    ]
)


# ================= HELPERS =================
async def auto_delete(msg: Message, delay: int):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except:
        pass


async def is_admin_or_owner(client, message: Message) -> bool:
    try:
        member = await client.get_chat_member(
            message.chat.id, message.from_user.id
        )
        return member.status in (
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
        )
    except:
        return False


# ================= GROUP COMMAND =================
@app.on_message(filters.command("autodownload") & filters.group)
async def autodownload_toggle(client, message: Message):
    if not await is_admin_or_owner(client, message):
        return await message.reply_text(
            "❌ Only **group admins** can change auto-download settings."
        )

    if len(message.command) < 2:
        status = GROUP_SETTINGS.get(message.chat.id, True)
        return await message.reply_text(
            f"📥 Auto download is currently **{'ON' if status else 'OFF'}**."
        )

    arg = message.command[1].lower()
    if arg == "on":
        GROUP_SETTINGS[message.chat.id] = True
        await message.reply_text("✅ Auto download has been **ENABLED** for this group.")
    elif arg == "off":
        GROUP_SETTINGS[message.chat.id] = False
        await message.reply_text("❌ Auto download has been **DISABLED** for this group.")


# ================= AUTO DOWNLOADER =================
@app.on_message(filters.text & ~filters.edited)
async def auto_downloader(client, message: Message):
    if not message.text or not message.from_user:
        return

    # Group ON/OFF check
    if message.chat.type != "private":
        if not GROUP_SETTINGS.get(message.chat.id, True):
            return

    # Cooldown (admins bypass)
    if not await is_admin_or_owner(client, message):
        now = time.time()
        last = USER_COOLDOWN.get(message.from_user.id, 0)
        remaining = COOLDOWN_TIME - (now - last)

        if remaining > 0:
            warn = await message.reply_text(
                f"⏳ Please wait **{remaining:.1f} seconds** before sending another link.\n"
                "Cooldown is still active.",
                quote=True,
            )
            asyncio.create_task(auto_delete(warn, COOLDOWN_MSG_DELETE))
            return

        USER_COOLDOWN[message.from_user.id] = now

    text = message.text.strip()

    try:
        # ===== INSTAGRAM =====
        if re.search(INSTAGRAM, text):
            url = re.search(INSTAGRAM, text).group(1)
            dl = url.replace("instagram.com", "ddinstagram.com")

            media = await message.reply_video(
                dl,
                caption="📥 Instagram Downloaded\n✨ via @kira_probot",
                reply_markup=ADD_BOT_BUTTON,
            )

        # ===== TWITTER / X =====
        elif re.search(TWITTER, text):
            url = re.search(TWITTER, text).group(1)
            dl = (
                url.replace("twitter.com", "vxtwitter.com")
                   .replace("x.com", "vxtwitter.com")
            )

            media = await message.reply_video(
                dl,
                caption="📥 X / Twitter Downloaded\n✨ via @kira_probot",
                reply_markup=ADD_BOT_BUTTON,
            )

        # ===== YOUTUBE SHORTS =====
        elif re.search(YT_SHORTS, text):
            msg = await message.reply_text("⬇️ Downloading YouTube Shorts…")
            video = await app.download_media(text)
            await msg.delete()

            media = await message.reply_video(
                video,
                caption="📥 YouTube Shorts Downloaded\n✨ via @kira_probot",
                reply_markup=ADD_BOT_BUTTON,
            )

        else:
            return

        notice = await message.reply_text(
            "⚠️ **Important Notice**\n\n"
            "Please **save or forward this media**.\n"
            "This content will be **automatically deleted after 1 hour** "
            "for copyright safety.",
            quote=True,
        )

        asyncio.create_task(auto_delete(media, AUTO_DELETE_TIME))
        asyncio.create_task(auto_delete(notice, AUTO_DELETE_TIME))

    except Exception:
        pass
