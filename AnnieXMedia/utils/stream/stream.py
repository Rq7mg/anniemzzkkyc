# Authored By Certified Coders © 2025
import os
from typing import Union
from pyrogram.types import InlineKeyboardMarkup
import config
from AnnieXMedia import YouTube, app
from AnnieXMedia.core.call import StreamController
from AnnieXMedia.misc import db
from AnnieXMedia.utils.database import is_active_chat
from AnnieXMedia.utils.exceptions import AssistantErr
from AnnieXMedia.utils.inline import aq_markup, stream_markup
from AnnieXMedia.utils.stream.queue import put_queue
from AnnieXMedia.utils.thumbnails import get_thumb
from AnnieXMedia.utils.errors import capture_internal_err
from AnnieXMedia.utils.stream.api_handler import get_video_from_api

@capture_internal_err
async def stream(
    _, mystic, user_id, result, chat_id, user_name, original_chat_id,
    video: Union[bool, str] = None, streamtype: Union[bool, str] = None,
    spotify: Union[bool, str] = None, forceplay: Union[bool, str] = None,
) -> None:
    if not result: return
    is_video = bool(video)
    if bool(forceplay): await StreamController.force_stop_stream(chat_id)

    if streamtype == "youtube":
        vidid = result["vidid"]
        file_path = await get_video_from_api(vidid)
        if not file_path:
            raise AssistantErr("Görüntü kaynağı yok gardaş! API'ler cevap vermiyor.")

        if await is_active_chat(chat_id):
            await put_queue(chat_id, original_chat_id, file_path, result["title"], result["duration_min"], user_name, vidid, user_id, "video" if is_video else "audio")
            await app.send_message(chat_id=original_chat_id, text=_["queue_4"].format("Sırada", result["title"][:27], result["duration_min"], user_name))
        else:
            db[chat_id] = []
            await StreamController.join_call(chat_id, original_chat_id, file_path, video=is_video, image=result["thumb"])
            await put_queue(chat_id, original_chat_id, file_path, result["title"], result["duration_min"], user_name, vidid, user_id, "video" if is_video else "audio")
            img = await get_thumb(vidid)
            await app.send_photo(original_chat_id, photo=img, caption=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}", result["title"][:23], result["duration_min"], user_name), reply_markup=InlineKeyboardMarkup(stream_markup(_, chat_id)))
