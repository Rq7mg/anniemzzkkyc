# Authored By Certified Coders © 2025
import os
import aiohttp
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
from AnnieXMedia.utils.stream.api_handler import get_video_from_api

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

        file_path = await get_video_from_api(vidid)
        if not file_path:
            raise AssistantErr("Görüntü kaynağı yok gardaş! API'ler cevap vermiyor. Bi daha oynat de hele.")

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
    # Playlist ve diğerleri get_video_from_api üzerinden çalışacak şekilde devam eder...
