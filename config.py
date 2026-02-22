import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# ── 1. GİRİŞ VE API AYARLARI ──────────────────────────────────────────────────
API_ID = int(getenv("API_ID", 27798659))
API_HASH = getenv("API_HASH", "26100c77cee02e5e34b2bbee58440f86")
BOT_TOKEN = getenv("BOT_TOKEN")

# ── 2. SENİN BİLGİLERİN ───────────────────────────────────────────────────────
OWNER_ID = int(getenv("OWNER_ID", 6563936773))
OWNER_USERNAME = getenv("OWNER_USERNAME", "OfficialKiyici")
BOT_USERNAME = getenv("BOT_USERNAME", "Kycmuzikbot")
BOT_NAME = getenv("BOT_NAME", "𝐊𝐈𝐘𝐈𝐂𝐈 𝐌𝐔𝐙𝐈𝐊 🇹🇷")
ASSUSERNAME = getenv("ASSUSERNAME", "musicxannie")

# ── 3. GÜNCELLEME VE REPO ─────────────────────────────────────────────────────
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/Rq7mg/anniemzzkkyc")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "Master")
GIT_TOKEN = getenv("GIT_TOKEN", None)

# ── 4. VERİTABANI VE HEROKU ───────────────────────────────────────────────────
MONGO_DB_URI = getenv("MONGO_DB_URI")
LOGGER_ID = int(getenv("LOGGER_ID", -1002014167331))
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ── 5. HATA AYIKLAMA ──────────────────────────────────────────────────────────
DEBUG_IGNORE_LOG = getenv("DEBUG_IGNORE_LOG", True)

# ── 6. MEDYA VE GÖRSELLER ─────────────────────────────────────────────────────
START_VIDS = []
STICKERS = [
    "CAACAgQAAxkBAAEQi55plWMpsTieNpfxgftt1vHzMcFg_gACCwsAAjo-OVHsAAGFGBKRAtk6BA", 
]

HELP_IMG_URL = "https://i.postimg.cc/76cKmJYN/IMG-20251205-113622-026.jpg"
PING_VID_URL = "https://i.postimg.cc/76cKmJYN/IMG-20251205-113622-026.jpg"
PLAYLIST_IMG_URL = "https://i.postimg.cc/76cKmJYN/IMG-20251205-113622-026.jpg"
STATS_VID_URL = "https://i.postimg.cc/76cKmJYN/IMG-20251205-113622-026.jpg"
TELEGRAM_AUDIO_URL = "https://i.postimg.cc/76cKmJYN/IMG-20251205-113622-026.jpg"
TELEGRAM_VIDEO_URL = "https://i.postimg.cc/76cKmJYN/IMG-20251205-113622-026.jpg"
STREAM_IMG_URL = "https://i.postimg.cc/76cKmJYN/IMG-20251205-113622-026.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/zhymxl.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/veykzq.jpg"
SPOTIFY_ARTIST_IMG_URL = SPOTIFY_ALBUM_IMG_URL = SPOTIFY_PLAYLIST_IMG_URL = YOUTUBE_IMG_URL

# ── 7. ANKARA ŞİVESİ MESAJLAR ────────────────────────────────────────────────
AYU = ["🔥", "🍷", "🥂", "🥃"]

AYUV = [
    "Selamın Aleyküm Gardaşım {0}, 🥀\n\nBen {1} !\n\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ◆ Mevzuyu biliyosun, her türlü çalarız.\n┠ ◆ Youtube, Spotify ne varsa getir.\n┗━━━━━━━━━━━━━━━━━⧫\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ➥ Ayaktayız: {2}\n┠ ➥ Depo: {3}\n┠ ➥ Motor Yükü: {4}\n┠ ➥ Hafıza: {5}\n┠ ➥ Bebeler: {6}\n┠ ➥ Gruplar: {7}\n┗━━━━━━━━━━━━━━━━━⧫\n\n🫧 Sahibi ➪ [@OfficialKiyici](https://t.me/OfficialKiyici)",
    "Hayırdır {0}, neye bakmıştın? ~\n\n◆ Ben {1}, Angara'nın en hızlı müzik botuyum.\n\n✨ İCRAATLARIM ⚡️\n◆ Kasmam, donmam, yarı yolda bırakmam.\n◆ Videolu, sesli ne istersen patlatırım.\n◆ Canlı yayın varsa çökerim.\n◆ Reklam falan yapmam, pavyon değil burası.\n\nBotu gruba al, admin yap, sonra arkana yaslan 🎵.\n\n🫧 Sahibi ➪ [@OfficialKiyici](https://t.me/OfficialKiyici)",
]

# ── 8. LİMİTLER VE ASİSTAN AYARLARI ──────────────────────────────────────────
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/Kiyiciupdate")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/KiyiciZeminChat")

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 1440))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "18000"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "36000"))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "2147483648"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "4294967296"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "500"))


SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6563936773").split()))
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "True")
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("AUTO_LEAVE_ASSISTANT_TIME", "3600"))

# -- GÖRÜNTÜ SORUNU İÇİN EKLENEN KRİTİK AYARLAR --
COOKIE_URL = getenv("COOKIE_URL")
# Görüntü akışını zorlamak için default parametreler
VIDEO_STREAM_LIMIT = 3
SERVER_PLAYLIST_LIMIT = 30
# FFmpeg yolu tanımlaması (Heroku Buildpack için)
FFMPEG_PATH = getenv("FFMPEG_PATH", "ffmpeg") 

API_URL = getenv("API_URL")
VIDEO_API_URL = getenv("VIDEO_API_URL")
API_KEY = getenv("API_KEY")
DEEP_API = getenv("DEEP_API")

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "22b6125bfe224587b722d6815002db2b")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "c9c63c6fbf2f467c8bc68624851e9773")

STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")

BANNED_USERS = filters.user()
adminlist, lyrical, autoclean, confirmer = {}, {}, [], {}

if SUPPORT_CHANNEL and not re.match(r"^https?://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHANNEL URL. Must start with https://")

if SUPPORT_CHAT and not re.match(r"^https?://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHAT URL. Must start with https://")

def time_to_seconds(time: str) -> int:
    return sum(int(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))

DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")
