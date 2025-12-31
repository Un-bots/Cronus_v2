import os
import asyncio
import time
import re
import yt_dlp

from pyrogram import filters, Client
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio,
    InputMediaVideo,
)
from pyrogram.enums import ChatAction

from DAXXMUSIC import app, YouTube
from config import (
    BANNED_USERS,
    SONG_DOWNLOAD_DURATION,
    SONG_DOWNLOAD_DURATION_LIMIT,
)

from DAXXMUSIC.utils.decorators.language import language, languageCB
from DAXXMUSIC.utils.formatters import convert_bytes
from DAXXMUSIC.utils.inline.song import song_markup


# ================= COMMAND =================

SONG_COMMAND = ["song"]


# ================= GROUP HANDLER =================

@app.on_message(
    filters.command(SONG_COMMAND)
    & filters.group
    & ~BANNED_USERS
)
@language
async def song_commad_group(client, message: Message, _):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["SG_B_1"],
                    url=f"https://t.me/{app.username}?start=song",
                ),
            ]
        ]
    )
    await message.reply_text(_["song_1"], reply_markup=upl)


# ================= PRIVATE HANDLER =================

@app.on_message(
    filters.command(SONG_COMMAND)
    & filters.private
    & ~BANNED_USERS
)
@language
async def song_commad_private(client, message: Message, _):
    await message.delete()
    url = await YouTube.url(message)

    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["song_5"])

        mystic = await message.reply_text(_["play_1"])
        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(url)

        if str(duration_min) == "None":
            return await mystic.edit_text(_["song_3"])

        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_4"].format(SONG_DOWNLOAD_DURATION, duration_min)
            )

        buttons = song_markup(_, vidid)
        await mystic.delete()
        return await message.reply_photo(
            thumbnail,
            caption=_["song_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    if len(message.command) < 2:
        return await message.reply_text(_["song_2"])

    mystic = await message.reply_text(_["play_1"])
    query = message.text.split(None, 1)[1]

    try:
        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(query)
    except:
        return await mystic.edit_text(_["play_3"])

    if str(duration_min) == "None":
        return await mystic.edit_text(_["song_3"])

    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(
            _["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min)
        )

    buttons = song_markup(_, vidid)
    await mystic.delete()
    return await message.reply_photo(
        thumbnail,
        caption=_["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


# ================= CALLBACKS =================

@app.on_callback_query(filters.regex(r"song_back") & ~BANNED_USERS)
@languageCB
async def songs_back_helper(client, CallbackQuery, _):
    stype, vidid = CallbackQuery.data.split(None, 1)[1].split("|")
    buttons = song_markup(_, vidid)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(r"song_helper") & ~BANNED_USERS)
@languageCB
async def song_helper_cb(client, CallbackQuery, _):
    stype, vidid = CallbackQuery.data.split(None, 1)[1].split("|")

    try:
        await CallbackQuery.answer(_["song_6"], show_alert=True)
    except:
        pass

    try:
        formats_available, _ = await YouTube.formats(vidid, True)
    except:
        return await CallbackQuery.edit_message_text(_["song_7"])

    keyboard = []
    done = []

    for x in formats_available:
        if x["filesize"] is None:
            continue

        if stype == "audio" and "audio" in x["format"]:
            form = x["format_note"].title()
            if form in done:
                continue
            done.append(form)

        elif stype == "video":
            allowed = [160, 133, 134, 135, 136, 137, 298, 299, 264, 304, 266]
            if int(x["format_id"]) not in allowed:
                continue
            form = x["format"]

        else:
            continue

        size = convert_bytes(x["filesize"])
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{form} = {size}",
                    callback_data=f"song_download {stype}|{x['format_id']}|{vidid}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(_["BACK_BUTTON"], callback_data=f"song_back {stype}|{vidid}"),
            InlineKeyboardButton(_["CLOSE_BUTTON"], callback_data="close"),
        ]
    )

    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ================= DOWNLOAD =================

@app.on_callback_query(filters.regex(r"song_download") & ~BANNED_USERS)
@languageCB
async def song_download_cb(client, CallbackQuery, _):
    await CallbackQuery.answer("Downloading...")

    stype, format_id, vidid = CallbackQuery.data.split(None, 1)[1].split("|")
    mystic = await CallbackQuery.edit_message_text(_["song_8"])

    yturl = f"https://www.youtube.com/watch?v={vidid}"

    with yt_dlp.YoutubeDL({"quiet": True}) as ytdl:
        info = ytdl.extract_info(yturl, download=False)

    title = re.sub(r"\W+", " ", info["title"]).title()
    duration = info["duration"]
    thumb = await CallbackQuery.message.download()

    if stype == "video":
        file_path = await YouTube.download(
            yturl, mystic, songvideo=True, format_id=format_id, title=title
        )

        media = InputMediaVideo(
            media=file_path,
            duration=duration,
            thumb=thumb,
            caption=title,
            supports_streaming=True,
        )

        await app.send_chat_action(
            CallbackQuery.message.chat.id, ChatAction.UPLOAD_VIDEO
        )
        await CallbackQuery.edit_message_media(media=media)
        os.remove(file_path)

    else:
        file_path = await YouTube.download(
            yturl, mystic, songaudio=True, format_id=format_id, title=title
        )

        media = InputMediaAudio(
            media=file_path,
            caption=title,
            thumb=thumb,
            title=title,
            performer=info.get("uploader"),
        )

        await app.send_chat_action(
            CallbackQuery.message.chat.id, ChatAction.UPLOAD_AUDIO
        )
        await CallbackQuery.edit_message_media(media=media)
        os.remove(file_path)
