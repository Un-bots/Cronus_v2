from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from DAXXMUSIC import app, YouTube
from motor.motor_asyncio import AsyncIOMotorClient
import config
import random
import json

# ---------------- DATABASE ---------------- #

mongo = AsyncIOMotorClient(config.MONGO_DB_URI)
db = mongo.playlists
collection = db.user_playlists

PLAYLIST_LIMIT = 30

# ---------------- HELPERS ---------------- #

async def get_playlist(user_id):
    data = await collection.find_one({"user_id": user_id})
    return data["songs"] if data else []


async def save_playlist(user_id, songs):
    await collection.update_one(
        {"user_id": user_id},
        {"$set": {"songs": songs}},
        upsert=True,
    )


# ---------------- ADD SONG ---------------- #

@app.on_message(filters.command("pladd") & filters.private)
async def add_playlist(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("ᴜsᴀɢᴇ: /pladd <song name or link>")

    query = message.text.split(None, 1)[1]
    songs = await get_playlist(message.from_user.id)

    if len(songs) >= PLAYLIST_LIMIT:
        return await message.reply("🚫 ʟɪᴍɪᴛ 30 sᴏɴɢs ʀᴇᴀᴄʜᴇᴅ.")

    try:
        title, _, _, _, vidid = await YouTube.details(query)
    except:
        return await message.reply("❌ ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ sᴏɴɢ.")

    songs.append({"title": title, "vidid": vidid})
    await save_playlist(message.from_user.id, songs)

    await message.reply(f"✅ {title} ᴀᴅᴅᴇᴅ.")


# ---------------- VIEW + INLINE ---------------- #

@app.on_message(filters.command("playlist") & filters.private)
async def view_playlist(_, message: Message):
    songs = await get_playlist(message.from_user.id)

    if not songs:
        return await message.reply("🎵 ᴘʟᴀʏʟɪsᴛ ᴇᴍᴘᴛʏ.")

    text = "🎶 ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ:\n\n"

    for i, song in enumerate(songs, 1):
        text += f"{i}. {song['title']}\n"

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔀 Shuffle", callback_data="pl_shuffle"),
            InlineKeyboardButton("📤 Export", callback_data="pl_export"),
        ],
        [
            InlineKeyboardButton("📥 Import", callback_data="pl_import"),
        ]
    ])

    await message.reply(text, reply_markup=buttons)


# ---------------- SHUFFLE ---------------- #

@app.on_callback_query(filters.regex("pl_shuffle"))
async def shuffle_playlist(_, query):
    songs = await get_playlist(query.from_user.id)

    if not songs:
        return await query.answer("Playlist empty", show_alert=True)

    random.shuffle(songs)
    await save_playlist(query.from_user.id, songs)

    await query.answer("🔀 Shuffled Successfully", show_alert=True)


# ---------------- EXPORT ---------------- #

@app.on_callback_query(filters.regex("pl_export"))
async def export_playlist(_, query):
    songs = await get_playlist(query.from_user.id)

    if not songs:
        return await query.answer("Playlist empty", show_alert=True)

    data = json.dumps(songs)

    await query.message.reply_document(
        document=data.encode(),
        file_name="playlist.json",
        caption="📤 ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ ᴇxᴘᴏʀᴛ"
    )

    await query.answer()


# ---------------- IMPORT ---------------- #

@app.on_message(filters.document & filters.private)
async def import_playlist(_, message: Message):
    if message.document.file_name != "playlist.json":
        return

    file_path = await message.download()

    with open(file_path, "r") as f:
        songs = json.load(f)

    if len(songs) > PLAYLIST_LIMIT:
        songs = songs[:PLAYLIST_LIMIT]

    await save_playlist(message.from_user.id, songs)

    await message.reply("📥 ᴘʟᴀʏʟɪsᴛ ɪᴍᴘᴏʀᴛᴇᴅ.")


# ---------------- PLAY IN GROUP ---------------- #

@app.on_message(filters.command("playplaylist") & filters.group)
async def play_playlist(_, message: Message):
    songs = await get_playlist(message.from_user.id)

    if not songs:
        return await message.reply("🎵 ᴘʟᴀʏʟɪsᴛ ᴇᴍᴘᴛʏ.")

    await message.reply("▶️ ᴀᴅᴅɪɴɢ ᴛᴏ ǫᴜᴇᴜᴇ...")

    for song in songs:
        # integrate with your existing play system
        await app.send_message(
            message.chat.id,
            f"🎵 {song['title']} ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ."
  )
