import aiohttp
from pyrogram import filters
from pyrogram.types import Message

from DAXXMUSIC import app
import config

TMDB_API_KEY = getattr(config, "TMDB_API_KEY", None)
TMDB_IMG = "https://image.tmdb.org/t/p/w500"


async def fetch_json(session, url, params):
    async with session.get(url, params=params) as resp:
        return await resp.json()


@app.on_message(filters.command(["movie", "tv"]))
async def movie_tv(_, message: Message):
    if not TMDB_API_KEY:
        return await message.reply_text(
            "❌ sᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ (ᴛᴍᴅʙ ᴋᴇʏ ɴᴏᴛ sᴇᴛ).",
            quote=True,
        )

    if len(message.command) < 2:
        return await message.reply_text(
            "❌ **ɪɴᴠᴀʟɪᴅ ᴜsᴀɢᴇ**\n\n"
            "`/movie <name>` ᴏʀ `/tv <name>`",
            quote=True,
        )

    query = message.text.split(None, 1)[1]
    mode = message.command[0].lower()  # movie or tv

    status = await message.reply_text("🔎 sᴇᴀʀᴄʜɪɴɢ ᴅᴇᴛᴀɪʟs...")

    try:
        async with aiohttp.ClientSession() as session:
            # ---- search ----
            search_url = f"https://api.themoviedb.org/3/search/{mode}"
            search = await fetch_json(
                session,
                search_url,
                {"api_key": TMDB_API_KEY, "query": query},
            )

            if not search.get("results"):
                return await status.edit("❌ ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ.")

            item = search["results"][0]
            item_id = item["id"]

            # ---- details ----
            details_url = f"https://api.themoviedb.org/3/{mode}/{item_id}"
            details = await fetch_json(
                session, details_url, {"api_key": TMDB_API_KEY}
            )

            # ---- credits ----
            credits_url = f"https://api.themoviedb.org/3/{mode}/{item_id}/credits"
            credits = await fetch_json(
                session, credits_url, {"api_key": TMDB_API_KEY}
            )

            # ---- watch providers ----
            providers_url = f"https://api.themoviedb.org/3/{mode}/{item_id}/watch/providers"
            providers = await fetch_json(
                session, providers_url, {"api_key": TMDB_API_KEY}
            )

        actors = ", ".join(
            a["name"] for a in credits.get("cast", [])[:5]
        ) or "ɴ/ᴀ"

        # OTT platforms (India first, fallback any)
        ott = "ɴ/ᴀ"
        results = providers.get("results", {})
        region = results.get("IN") or next(iter(results.values()), {})
        if region and region.get("flatrate"):
            ott = ", ".join(p["provider_name"] for p in region["flatrate"])

        title = details.get("title") or details.get("name")
        release = details.get("release_date") or details.get("first_air_date")
        rating = details.get("vote_average", "ɴ/ᴀ")
        overview = details.get("overview", "ɴ/ᴀ")
        poster = details.get("poster_path")
        imdb_id = details.get("imdb_id")

        caption = (
            f"🎬 **ᴛɪᴛʟᴇ :** {title}\n"
            f"📅 **ʀᴇʟᴇᴀsᴇ :** {release}\n"
            f"⭐ **ʀᴀᴛɪɴɢ :** {rating}\n\n"
            f"📝 **ᴏᴠᴇʀᴠɪᴇᴡ :**\n{overview}\n\n"
            f"🎭 **ᴀᴄᴛᴏʀs :** {actors}\n"
            f"📺 **ᴏᴛᴛ :** {ott}\n"
        )

        if imdb_id:
            caption += f"\n🔗 **ɪᴍᴅʙ :** https://www.imdb.com/title/{imdb_id}/"

        caption += "\n\n✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot"

        await status.delete()

        if poster:
            await message.reply_photo(
                photo=f"{TMDB_IMG}{poster}",
                caption=caption,
            )
        else:
            await message.reply_text(caption)

    except Exception:
        await status.edit("❌ ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴅᴇᴛᴀɪʟs.")


# ================= HELP SYSTEM =================
__mod_name__ = "Mᴏᴠɪᴇs"

__help__ = """
❍ /movie <ɴᴀᴍᴇ> : ᴍᴏᴠɪᴇ ɪɴғᴏ (ᴘᴏsᴛᴇʀ, ɪᴍᴅʙ, ᴏᴛᴛ)
❍ /tv <ɴᴀᴍᴇ> : ᴛᴠ / ᴡᴇʙ sᴇʀɪᴇs ɪɴғᴏ
"""
