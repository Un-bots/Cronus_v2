from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from DAXXMUSIC import app, YouTube
from motor.motor_asyncio import AsyncIOMotorClient
import config
import random
import uuid

# ================= DATABASE ================= #

mongo = AsyncIOMotorClient(config.MONGO_DB_URI)
db = mongo.playlists

user_collection = db.user_playlists
shared_collection = db.shared_playlists

PLAYLIST_LIMIT = 30

# ================= HELPERS ================= #

async def get_playlist(user_id):
    data = await user_collection.find_one({"user_id": user_id})
    return data["songs"] if data else []

async def save_playlist(user_id, songs):
    await user_collection.update_one(
        {"user_id": user_id},
        {"$set": {"songs": songs}},
        upsert=True,
    )

# ================= ADD SONG (DM ONLY) ================= #

@app.on_message(filters.command("pladd") & filters.private)
async def add_playlist(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /pladd <song name or link>")

    query = message.text.split(None, 1)[1]
    songs = await get_playlist(message.from_user.id)

    if len(songs) >= PLAYLIST_LIMIT:
        return await message.reply("🚫 Playlist limit (30 songs) reached.")

    try:
        title, _, _, _, vidid = await YouTube.details(query)
    except:
        return await message.reply("❌ Failed to fetch song.")

    songs.append({"title": title, "vidid": vidid})
    await save_playlist(message.from_user.id, songs)

    await message.reply(f"✅ {title} added to playlist.")

# ================= REMOVE SONG ================= #

@app.on_message(filters.command("plremove") & filters.private)
async def remove_song(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /plremove <song number>")

    songs = await get_playlist(message.from_user.id)

    if not songs:
        return await message.reply("Playlist empty.")

    try:
        index = int(message.command[1]) - 1
        removed = songs.pop(index)
    except:
        return await message.reply("Invalid number.")

    await save_playlist(message.from_user.id, songs)

    await message.reply(f"🗑 Removed: {removed['title']}")

# ================= VIEW PLAYLIST ================= #

@app.on_message(filters.command("playlist") & filters.private)
async def view_playlist(_, message: Message):
    songs = await get_playlist(message.from_user.id)

    if not songs:
        return await message.reply("🎵 Playlist empty.")

    text = "🎶 Your Playlist:\n\n"

    for i, song in enumerate(songs, 1):
        text += f"{i}. {song['title']}\n"

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔀 Shuffle", callback_data="pl_shuffle"),
            InlineKeyboardButton("📤 Share", callback_data="pl_share"),
        ]
    ])

    await message.reply(text, reply_markup=buttons)

# ================= SHUFFLE ================= #

@app.on_callback_query(filters.regex("pl_shuffle"))
async def shuffle_playlist(_, query):
    songs = await get_playlist(query.from_user.id)

    if not songs:
        return await query.answer("Playlist empty", show_alert=True)

    random.shuffle(songs)
    await save_playlist(query.from_user.id, songs)

    await query.answer("🔀 Playlist Shuffled", show_alert=True)

# ================= SHARE PLAYLIST ================= #

@app.on_callback_query(filters.regex("pl_share"))
async def share_playlist(_, query):
    songs = await get_playlist(query.from_user.id)

    if not songs:
        return await query.answer("Playlist empty", show_alert=True)

    playlist_id = str(uuid.uuid4())[:8]

    await shared_collection.insert_one({
        "playlist_id": playlist_id,
        "owner_id": query.from_user.id,
        "songs": songs
    })

    share_link = f"https://t.me/{config.BOT_USERNAME}?start=pl_{playlist_id}"

    await query.message.reply(
        f"📤 Share this link:\n\n{share_link}"
    )

    await query.answer()

# ================= LOAD SHARED PLAYLIST ================= #

@app.on_message(filters.private & filters.regex("^/start pl_"))
async def load_shared_playlist(_, message: Message):
    playlist_id = message.text.split("pl_")[1]

    data = await shared_collection.find_one({"playlist_id": playlist_id})

    if not data:
        return await message.reply("❌ Playlist not found.")

    songs = data["songs"]

    text = "🎶 Shared Playlist:\n\n"

    for i, song in enumerate(songs, 1):
        text += f"{i}. {song['title']}\n"

    await message.reply(text)

# ================= IMPORT FROM LINK ================= #

@app.on_message(filters.command("import") & filters.private)
async def import_from_link(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /import <playlist link>")

    link = message.command[1]

    if "pl_" not in link:
        return await message.reply("Invalid link.")

    playlist_id = link.split("pl_")[1]

    data = await shared_collection.find_one({"playlist_id": playlist_id})

    if not data:
        return await message.reply("Playlist not found.")

    songs = data["songs"][:PLAYLIST_LIMIT]

    await save_playlist(message.from_user.id, songs)

    await message.reply("📥 Playlist imported successfully.")

# ================= PLAY SHARED PLAYLIST IN GROUP ================= #

@app.on_message(filters.command("play") & filters.group)
async def play_shared_playlist(_, message: Message):

    if len(message.command) < 2:
        return

    arg = message.command[1]

    if "pl_" not in arg:
        return

    playlist_id = arg.split("pl_")[1]

    data = await shared_collection.find_one({"playlist_id": playlist_id})

    if not data:
        return await message.reply("Playlist not found.")

    songs = data["songs"]

    await message.reply("▶️ Playing shared playlist...")

    for song in songs:
        await app.send_message(
            message.chat.id,
            f"/play https://youtube.com/watch?v={song['vidid']}"
    )
