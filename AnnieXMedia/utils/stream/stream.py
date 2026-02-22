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

# --- MECBURİ API ÇEKİCİ SİSTEMİ ---
async def get_video_from_api(youtube_id):
    """
    YouTube engelini aşmak için SADECE API'leri kullanır.
    """
    user_api = getattr(config, "VIDEO_API_URL", None)
    
    apis = []
    if user_api:
        base_api = user_api.rstrip("/")
        # Botun her zaman temiz link alması için 3 farklı format deniyoruz
        apis.append(f"{base_api}/yt?link=https://www.youtube.com/watch?v={youtube_id}")
        apis.append(f"{base_api}/download?url=https://www.youtube.com/watch?v={youtube_id}")
    
    # Yedek Genel API'ler
    apis.extend([
        f"https://api.youtubify.com/download?url=https://www.youtube.com/watch?v={youtube_id}",
        f"https://fallen-api.vercel.app/api/yt?url=https://www.youtube.com/watch?v={youtube_id}"
    ])
    
    async with aiohttp.ClientSession() as session:
        for api_url in apis:
            try:
                async with session.get(api_url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        res_url = data.get("url") or data.get("link") or data.get("data", {}).get("url")
                        if res_url:
                            return res_url
            except Exception:
                continue
    return None

@capture_internal_err
async def stream(
    _,
    mystic,
    user_id,
    result,
    chat_id,
    user_name,
    original_chat_id,
    video: Union[bool, str] = None,
    streamtype: Union[bool, str] = None,
    spotify: Union[bool, str] = None,
    forceplay: Union[bool, str] = None,
) -> None:
    if not result:
        return

    forceplay = bool(forceplay)
    is_video = bool(video)

    if forceplay:
        await StreamController.force_stop_stream(chat_id)

    if streamtype == "playlist":
        msg = f"{_['play_19']}\n\n"
        count = 0
        for search in result:
            if int(count) == config.PLAYLIST_FETCH_LIMIT:
                continue
            try:
                title, duration_min, _, thumbnail, vidid = await YouTube.details(search, videoid=search)
            except Exception:
                continue

            # Playlist için mecburi API kontrolü
            file_path = await get_video_from_api(vidid)
            direct = True
            
            if not file_path:
                # API yoksa playlistte bu şarkıyı atla, botu çökertme
                continue

            if await is_active_chat(chat_id):
                await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, vidid, user_id, "video" if is_video else "audio")
                count += 1
                msg += f"{count}. {title[:70]}\n"
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
                count += 1

        if count == 0:
            return
        link = await ANNIEBIN(msg)
        return await app.send_photo(original_chat_id, photo=config.PLAYLIST_IMG_URL, caption=_["play_21"].format(count, link), reply_markup=close_markup(_))

    elif streamtype == "youtube":
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = result["duration_min"]
        thumbnail = result["thumb"]

        # --- MECBURİ API KONTROLÜ ---
        file_path = await get_video_from_api(vidid)
        direct = True
        
        if not file_path:
            # API başarısız olursa botun yasaklı YouTube linkine gitmesini KESİNLİKLE ENGELLİYORUZ
            raise AssistantErr("Görüntü kaynağı yok gardaş! API'ler cevap vermiyor, YouTube IP'mizi engellemiş olabilir. Bi daha oynat de hele.")
        # ----------------------------

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

    # SoundCloud, Telegram, Live ve Index kısımları aynı kalıyor...
    elif streamtype == "soundcloud":
        file_path = result["filepath"]
        title = result["title"]
        duration_min = result["duration_min"]
        if not file_path:
            raise AssistantErr(_["play_14"])

        if await is_active_chat(chat_id):
            await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, streamtype, user_id, "audio")
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await app.send_message(chat_id=original_chat_id, text=_["queue_4"].format(position, title[:27], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
        else:
            if not forceplay:
                db[chat_id] = []
            await StreamController.join_call(chat_id, original_chat_id, file_path, video=False)
            await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, streamtype, user_id, "audio", forceplay=forceplay)
            button = stream_markup(_, chat_id)
            run = await app.send_photo(original_chat_id, photo=config.SOUNCLOUD_IMG_URL, caption=_["stream_1"].format(config.SUPPORT_CHAT, title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"

    elif streamtype == "telegram":
        file_path = result["path"]
        link = result["link"]
        title = (result["title"]).title()
        duration_min = result["dur"]
        if not file_path:
            raise AssistantErr(_["play_14"])

        if await is_active_chat(chat_id):
            await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, streamtype, user_id, "video" if is_video else "audio")
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await app.send_message(chat_id=original_chat_id, text=_["queue_4"].format(position, title[:27], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
        else:
            if not forceplay:
                db[chat_id] = []
            await StreamController.join_call(chat_id, original_chat_id, file_path, video=is_video)
            await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, streamtype, user_id, "video" if is_video else "audio", forceplay=forceplay)
            if is_video:
                await add_active_video_chat(chat_id)
            button = stream_markup(_, chat_id)
            run = await app.send_photo(original_chat_id, photo=config.TELEGRAM_VIDEO_URL if is_video else config.TELEGRAM_AUDIO_URL, caption=_["stream_1"].format(link, title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"

    elif streamtype == "live":
        vidid = result["vidid"]
        title = (result["title"]).title()
        thumbnail = result["thumb"]
        duration_min = "BiTMEYEN YAYIN"

        file_path = await get_video_from_api(vidid)
        if not file_path:
            raise AssistantErr("Canlı yayın kaynağı API tarafından sağlanamadı!")

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
            db[chat_id][0]["markup"] = "tg"

    elif streamtype == "index":
        link = result
        title = "ʟɪɴᴋᴛᴇɴ ᴄᴀʟıʏᴏʀᴜᴢ ɢᴀʀᴅᴀs"
        duration_min = "00:00"

        if await is_active_chat(chat_id):
            await put_queue_index(chat_id, original_chat_id, "index_url", title, duration_min, user_name, link, "video" if is_video else "audio")
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await mystic.edit_text(text=_["queue_4"].format(position, title[:27], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
        else:
            if not forceplay:
                db[chat_id] = []
            await StreamController.join_call(chat_id, original_chat_id, link, video=is_video)
            await put_queue_index(chat_id, original_chat_id, "index_url", title, duration_min, user_name, link, "video" if is_video else "audio", forceplay=forceplay)
            button = stream_markup(_, chat_id)
            run = await app.send_photo(original_chat_id, photo=config.STREAM_IMG_URL, caption=_["stream_2"].format(user_name), reply_markup=InlineKeyboardMarkup(button))
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await mystic.delete()
