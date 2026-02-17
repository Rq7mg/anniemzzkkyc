# Authored By Certified Coders © 2025
import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

# Ortam değişkenlerini yükle
load_dotenv()

# ── Ana Bot Ayarları ───────────────────────────────────────────────────────────
API_ID = int(getenv("API_ID", 27798659))
API_HASH = getenv("API_HASH", "26100c77cee02e5e34b2bbee58440f86")
BOT_TOKEN = getenv("BOT_TOKEN")

# Senin Bilgilerin
OWNER_ID = int(getenv("OWNER_ID", 7044783841))
OWNER_USERNAME = getenv("OWNER_USERNAME", "OfficialKiyici") # Senin Kullanıcı Adın
BOT_USERNAME = getenv("BOT_USERNAME", "Kycmuzikbot")        # Botun Kullanıcı Adı
BOT_NAME = getenv("BOT_NAME", "𝐊𝐈𝐘𝐈𝐂𝐈 𝐌𝐔𝐙𝐈𝐊 🇹🇷")
ASSUSERNAME = getenv("ASSUSERNAME", "musicxannie")

# ── Veritabanı ve Log ──────────────────────────────────────────────────────────
MONGO_DB_URI = getenv("MONGO_DB_URI")
LOGGER_ID = int(getenv("LOGGER_ID", -1002014167331))

# ── Sınırlar ───────────────────────────────────────────────────────────────────
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 300))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "1200"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "1800"))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "157286400"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "1288490189"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "30"))

# ── Hosting / Deployment ───────────────────────────────────────────────────────
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ── Destek Bağlantıları ────────────────────────────────────────────────────────
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/CertifiedNetwork")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/CertifiedDiscussion")

# ── Görsel Varlıklar (Videoları Kapattık) ──────────────────────────────────────
# /start verince video çıkmasın diye içini boşalttık, sadece resim linki koyduk.
START_VIDS = [] 
HELP_IMG_URL = "https://files.catbox.moe/yg2vky.jpg"
PING_VID_URL = "https://files.catbox.moe/3ivvgo.mp4"
PLAYLIST_IMG_URL = "https://files.catbox.moe/yhaja5.jpg"
STATS_VID_URL = "https://telegra.ph/file/e2ab6106ace2e95862372.mp4"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/mlztag.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/tiss2b.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/1d3da7.jpg"

# ── Bot Tanıtım Mesajları (Harbi Ankara Şivesi) ────────────────────────────────
AYU = ["🔥", "🍷", "🥂", "🥃"]
AYUV = [
    "Selamın Aleyküm Gardaşım {0}, 🥀\n\nBen {1} !\n\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ◆ Mevzuyu biliyosun, her türlü çalarız.\n┠ ◆ Youtube, Spotify ne varsa getir.\n┗━━━━━━━━━━━━━━━━━⧫\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ➥ Ayaktayız : {2}\n┠ ➥ Depo : {3}\n┠ ➥ Motor Yükü : {4}\n┠ ➥ Hafıza : {5}\n┠ ➥ Bebeler : {6}\n┠ ➥ Gruplar : {7}\n┗━━━━━━━━━━━━━━━━━⧫\n\n🫧 Sahibi ➪ [@OfficialKiyici](https://t.me/OfficialKiyici)",
    "Hayırdır {0}, neye bakmıştın? ~\n\n◆ Ben {1}, Angara'nın en hızlı müzik botuyum.\n\n✨ İCRAATLARIM ⚡️\n◆ Kasmam, donmam, yarı yolda bırakmam.\n◆ Videolu, sesli ne istersen patlatırım.\n◆ Canlı yayın varsa çökerim.\n◆ Reklam falan yapmam, pavyon değil burası.\n\nBotu gruba al, admin yap, sonra arkana yaslan 🎵.\n\n🫧 Sahibi ➪ [@OfficialKiyici](https://t.me/OfficialKiyici)",
]

# ── Diğer Ayarlar ──────────────────────────────────────────────────────────────
BANNED_USERS = filters.user()
adminlist, lyrical, autoclean, confirmer = {}, {}, [], {}

def time_to_seconds(time: str) -> int:
    return sum(int(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))

DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")
