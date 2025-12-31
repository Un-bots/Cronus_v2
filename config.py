import re
from os import getenv
# ------------------------------------
# ------------------------------------
from dotenv import load_dotenv
from pyrogram import filters
# ------------------------------------
# ------------------------------------
load_dotenv()
# ------------------------------------
# -----------------------------------------------------

# ================= CORE REQUIRED =================

API_ID = int(getenv("API_ID", 0))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

# 🔒 CRASH EARLY (2027 SAFE)
if not API_ID or not API_HASH or not BOT_TOKEN:
    raise RuntimeError(
        "❌ Missing required ENV vars: API_ID / API_HASH / BOT_TOKEN"
    )

# ------------------------------------------------------

EVAL = list(map(int, getenv("EVAL", "6253265083 6253265083").split()))
# ------------------------------------------------------
OWNER_USERNAME = getenv("OWNER_USERNAME","harsh_un")
# --------------------------------------------------------
BOT_USERNAME = getenv("BOT_USERNAME" , "KIRA_PROBOT")
# --------------------------------------------------------
BOT_NAME = getenv("BOT_NAME" , "神 𝗞ɪʀᴀ")
# ---------------------------------------------------------
ASSUSERNAME = getenv("ASSUSERNAME" , "UNB")
# ---------------------------------------------------------

# ================= DATABASE =================

MONGO_DB_URI = getenv("MONGO_DB_URI", None)

# ================= LIMITS =================

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))

# ================= LOGGING =================

LOGGER_ID = int(getenv("LOGGER_ID", -1002040932096))

# ================= OWNERS =================

OWNER_ID = int(getenv("OWNER_ID", 6253265083))
DEV_ID = int(getenv("DEV_ID", 6253265083))

# ================= LEGACY (KEPT AS-IS) =================
# ❌ Not used in Railway but kept for compatibility

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ================= TMDB (MOVIES / TV) =================
TMDB_API_KEY = getenv("TMDB_API_KEY", None)

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/un-bots/cronus",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "Master")
GIT_TOKEN = getenv("GIT_TOKEN", None)

# ================= SUPPORT =================

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/kira_update")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/unb_support")

# ================= ASSISTANT SETTINGS =================

AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "True")
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "900"))

SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))

# ================= SPOTIFY =================
# ⚠️ Values kept as-is (you filled them)

SPOTIFY_CLIENT_ID = getenv(
    "SPOTIFY_CLIENT_ID",
    "1c21247d714244ddbb09925dac565aed"
)
SPOTIFY_CLIENT_SECRET = getenv(
    "SPOTIFY_CLIENT_SECRET",
    "709e1a2969664491b58200860623ef19"
)

# ================= PLAYLIST =================

PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))

# ================= TELEGRAM LIMITS =================

TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))

# ================= STRING SESSIONS =================

STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)
STRING6 = getenv("STRING_SESSION6", None)
STRING7 = getenv("STRING_SESSION7", None)

# ================= RUNTIME DATA =================

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# ================= IMAGES =================

START_IMG_URL = getenv(
    "START_IMG_URL", "https://telegra.ph/file/0fb5799f17005b83a8d14.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://telegra.ph/file/0fb5799f17005b83a8d14.jpg"
)
PLAYLIST_IMG_URL = "https://telegra.ph/file/0fb5799f17005b83a8d14.jpg"
STATS_IMG_URL = "https://telegra.ph/file/0fb5799f17005b83a8d14.jpg"
TELEGRAM_AUDIO_URL = "https://telegra.ph/file/0fb5799f17005b83a8d14.jpg"
TELEGRAM_VIDEO_URL = "https://telegra.ph/file/0fb5799f17005b83a8d14.jpg"
STREAM_IMG_URL = "https://telegra.ph/file/0fb5799f17005b83a8d14.jpg"
SOUNCLOUD_IMG_URL = "https://telegra.ph/file/d723f4c80da157fca1678.jpg"
YOUTUBE_IMG_URL = "https://telegra.ph/file/4dc854f961cd3ce46899b.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://telegra.ph/file/d723f4c80da157fca1678.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://telegra.ph/file/6c741a6bc1e1663ac96fc.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://telegra.ph/file/6c741a6bc1e1663ac96fc.jpg"

# ================= HELPERS =================

def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60**i
        for i, x in enumerate(reversed(stringt.split(":")))
    )

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

# ================= URL VALIDATION =================

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - SUPPORT_CHANNEL url must start with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - SUPPORT_CHAT url must start with https://"
)# ---------------------------------------------------------------------------------------



# ------------------------------------
# ------------------------------------
# ------------------------------------
# ------------------------------------
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)
STRING6 = getenv("STRING_SESSION6", None)
STRING7 = getenv("STRING_SESSION7", None)
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# ------------------------------------
# ------------------------------------
# ------------------------------------
# ------------------------------------

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
START_IMG_URL = getenv(
    "START_IMG_URL", "https://telegra.ph/file/0fb5799f17005b83a8d14.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://telegra.ph/file/0fb5799f17005b83a8d14.jpg"
)
PLAYLIST_IMG_URL = "https://telegra.ph/file/0fb5799f17005b83a8d14.jpg"
STATS_IMG_URL = "https://telegra.ph/file/0fb5799f17005b83a8d14.jpg"
TELEGRAM_AUDIO_URL = "https://telegra.ph/file/0fb5799f17005b83a8d14.jpg"
TELEGRAM_VIDEO_URL = "https://telegra.ph/file/0fb5799f17005b83a8d14.jpg"
STREAM_IMG_URL = "https://telegra.ph/file/0fb5799f17005b83a8d14.jpg"
SOUNCLOUD_IMG_URL = "https://telegra.ph/file/d723f4c80da157fca1678.jpg"
YOUTUBE_IMG_URL = "https://telegra.ph/file/4dc854f961cd3ce46899b.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://telegra.ph/file/d723f4c80da157fca1678.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://telegra.ph/file/6c741a6bc1e1663ac96fc.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://telegra.ph/file/6c741a6bc1e1663ac96fc.jpg"

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# ------------------------------------------------------------------------------
if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
# ---------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
