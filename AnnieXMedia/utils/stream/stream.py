# Authored By Certified Coders © 2025
import os
from random import randint
from typing import Union
from pyrogram.types import InlineKeyboardMarkup
import config
from AnnieXMedia import Carbon, YouTube, app
from AnnieXMedia.core.call import StreamController
from AnnieXMedia.misc import db
from AnnieXMedia.utils.database import is_active_chat
from AnnieXMedia.utils.exceptions import AssistantErr
from AnnieXMedia.utils.inline import aq_markup, close_markup, stream_markup
from AnnieXMedia.utils.pastebin import ANNIEBIN
from AnnieXMedia.utils.stream.queue import put_queue
from AnnieXMedia.utils.thumbnails import get_thumb
from AnnieXMedia.utils.errors import capture_internal_err

@capture_internal_err
async def stream(
    _, mystic, user_id, result, chat_id, user_name, original_chat_id,
    video: Union[bool, str] = None, streamtype: Union[bool, str] = None,
    spotify: Union[bool, str] = None, forceplay: Union[bool, str] = None,
) -> None:
    if not result:
        return
    is_video = bool(video)
    if bool(forceplay):
        await StreamController.force_stop_stream(chat_id)

    if streamtype == "youtube":
        vidid = result["vidid"]
        title = (result["title"]).title()
        
        # Senin ilk başta verdiğin orijinal indirme sistemi
        try:
            file_path, direct = await YouTube.download(
                vidid, mystic, video=is_video, videoid=vidid
            )
        except Exception:
            raise AssistantErr(_["play_14"])

        if not file_path:
            raise AssistantErr(_["play_14"])

        if await is_active_chat(chat_id):
            await put_queue(chat_id, original_chat_id, file_path if direct else f"vid_{vidid}", title, result["duration_min"], user_name, vidid, user_id, "video" if is_video else "audio")
            position = len(db.get(chat_id)) - 1
            await app.send_message(chat_id=original_chat_id, text=_["queue_4"].format(position, title[:27], result["duration_min"], user_name))
        else:
            if not bool(forceplay):
                db[chat_id] = []
            await StreamController.join_call(chat_id, original_chat_id, file_path, video=is_video, image=result["thumb"])
            await put_queue(chat_id, original_chat_id, file_path if direct else f"vid_{vidid}", title, result["duration_min"], user_name, vidid, user_id, "video" if is_video else "audio")
            img = await get_thumb(vidid)
            run = await app.send_photo(original_chat_id, photo=img, caption=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}", title[:23], result["duration_min"], user_name), reply_markup=InlineKeyboardMarkup(stream_markup(_, chat_id)))
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
