# Authored By Certified Coders © 2025
import os
import aiohttp
import logging
from random import randint
from typing import Union
from pyrogram.types import InlineKeyboardMarkup
import config
from AnnieXMedia import Carbon, YouTube, app
from AnnieXMedia.core.call import StreamController
from AnnieXMedia.misc import db
from AnnieXMedia.utils.database import add_active_video_chat, is_active_chat
from AnnieXMedia.utils.exceptions import AssistantErr
from AnnieXMedia.utils.inline import aq_markup, close_markup, stream_markup
from AnnieXMedia.utils.pastebin import ANNIEBIN
from AnnieXMedia.utils.stream.queue import put_queue, put_queue_index
from AnnieXMedia.utils.thumbnails import get_thumb
from AnnieXMedia.utils.errors import capture_internal_err

# --- SÜPER GÜÇLENDİRİLMİŞ API VE PROXY HAVUZU ---
async def get_video_from_api(youtube_id):
    # Go botundaki çalışan mantığı buraya daha sert bir şekilde kuruyoruz
    apis = [
        f"https://api.youtubify.com/download?url=https://www.youtube.com/watch?v={youtube_id}",
        f"https://fallen-api.vercel.app/api/yt?url=https://www.youtube.com/watch?v={youtube_id}",
        f"https://yukki-api.vercel.app/download?url={youtube_id}",
        f"https://anonx-api.vercel.app/api/yt?url={youtube_id}",
        # Alternatif Google Proxy yolları
        f"https://www.youtube.com/watch?v={youtube_id}",
        f"https://api.youtubify.com/download?url=https://www.youtube.com/watch?v={youtube_id}"
    ]
    
    user_api = getattr(config, "VIDEO_API_URL", None)
    if user_api:
        base_api = user_api.rstrip("/")
        apis.insert(0, f"{base_api}/yt?link=https://www.youtube.com/watch?v={youtube_id}")

    async with aiohttp.ClientSession() as session:
        for api_url in apis:
            try:
                async with session.get(api_url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Diğer botun (Go) kullandığı tüm veri formatlarını tarıyoruz
                        res_url = data.get("url") or data.get("link") or (data.get("data", {}).get("url") if isinstance(data.get("data"), dict) else None)
                        if res_url and "googlevideo.com" not in res_url: # Banlı link gelirse reddet
                            return res_url
            except Exception:
                continue
    return None

@capture_internal_err
async def stream(
    _, mystic, user_id, result, chat_id, user_name, original_chat_id,
    video: Union[bool, str] = None, streamtype: Union[bool, str] = None,
    spotify: Union[bool, str] = None, forceplay: Union[bool, str] = None,
) -> None:
    if not result:
        return

    forceplay = bool(forceplay)
    is_video = bool(video)

    if forceplay:
        await StreamController.force_stop_stream(chat_id)

    if streamtype == "youtube":
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = result["duration_min"]
        thumbnail = result["thumb"]

        # MEVZUYU KÖKTEN ÇÖZEN KISIM
        file_path = await get_video_from_api(vidid)
        
        # EĞER API'LERDEN LİNK GELMEZSE ASLA YOUTUBE'A GİTME (HATA VER Kİ BANLANMA)
        if not file_path:
            raise AssistantErr("Görüntü kaynağı yok gardaş! Tüm API havuzu YouTube engeline takılmış. Bi daha oynat de hele.")

        if await is_active_chat(chat_id):
            await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, vidid, user_id, "video" if is_video else "audio")
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await app.send_message(chat_id=original_chat_id, text=_["queue_4"].format(position, title[:27], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
        else:
            if not forceplay:
                db[chat_id] = []
            await StreamController.join_call(chat_id, original_chat_id, file_path, video=is_video, image=thumbnail)
            await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, vidid, user_id, "video" if is_video else "audio", forceplay=forceplay)
            img = await get_thumb(vidid)
            button = stream_markup(_, chat_id)
            run = await app.send_photo(original_chat_id, photo=img, caption=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}", title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"

    # Diğer Playlist, Telegram vb. kısımları yukarıdaki mantıkla aynı olacak şekilde kalsın...
