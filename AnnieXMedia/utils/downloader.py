# Authored By Certified Coders © 2025
import asyncio
import os
import re
from typing import Dict, Optional

import aiofiles
import aiohttp
from aiohttp import TCPConnector
from yt_dlp import YoutubeDL

from AnnieXMedia.core.dir import CACHE_DIR, DOWNLOAD_DIR
from AnnieXMedia.utils.cookie_handler import COOKIE_PATH as _COOKIES_FILE
from AnnieXMedia.utils.tuning import CHUNK_SIZE
from config import API_KEY, API_URL
from AnnieXMedia.logging import LOGGER

LOGGER = LOGGER(__name__)

_session: Optional[aiohttp.ClientSession] = None
_session_lock = asyncio.Lock()
YOUTUBE_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{11}$")

def extract_video_id(link: str) -> str:
    if not link: return ""
    s = link.strip()
    if YOUTUBE_ID_RE.match(s): return s
    if "v=" in s: return s.split("v=")[-1].split("&")[0]
    last = s.split("/")[-1].split("?")[0]
    return last if YOUTUBE_ID_RE.match(last) else ""

def get_cookie_file() -> Optional[str]:
    if _COOKIES_FILE and os.path.exists(_COOKIES_FILE) and os.path.getsize(_COOKIES_FILE) > 0:
        return _COOKIES_FILE
    return None

def get_ytdlp_base_opts(is_video: bool = False) -> Dict[str, object]:
    opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "overwrites": True,
        "continuedl": True,
        "socket_timeout": 30,
        "retries": 10,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }
    
    if is_video:
        # Video için en iyi kaliteyi seçer (720p genellikle idealdir)
        opts["format"] = "best[ext=mp4]/best"
    else:
        # Ses için en iyi sesi seçer
        opts["format"] = "bestaudio/best"

    if cookiefile := get_cookie_file():
        opts["cookiefile"] = cookiefile
    return opts

async def yt_dlp_download(link: str, **kwargs) -> Optional[str]:
    """Her şeyi doğrudan indiren ana fonksiyon"""
    loop = asyncio.get_running_loop()
    
    # Gelen isteğin video olup olmadığını kontrol et
    is_video = kwargs.get("type") == "video"
    opts = get_ytdlp_base_opts(is_video=is_video)
    
    def _download():
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(link, download=True)
            return ydl.prepare_filename(info)

    try:
        title = kwargs.get("title", "Parça")
        LOGGER.info(f"{'Video' if is_video else 'Ses'} indiriliyor: {title}")
        return await loop.run_in_executor(None, _download)
    except Exception as e:
        LOGGER.error(f"İndirme hatası: {e}")
        return None

# Eski API fonksiyonlarını hata vermemesi için boş bırakıyoruz
async def api_download_audio(link: str): return None
async def api_download_video(link: str): return None
