# Authored By Certified Coders © 2025
import asyncio
import os
from datetime import datetime, timedelta
from typing import Union
from ntgcalls import TelegramServerError, ConnectionNotFound
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls
from pytgcalls.exceptions import NoActiveGroupCall, NoAudioSourceFound, NoVideoSourceFound
from pytgcalls.types import AudioQuality, MediaStream, StreamEnded, Update, VideoQuality
import config
from strings import get_string
from AnnieXMedia import LOGGER, YouTube, app
from AnnieXMedia.misc import db
from AnnieXMedia.utils.database import (
    add_active_chat, add_active_video_chat, get_lang, get_loop,
    group_assistant, is_autoend, music_on, remove_active_chat,
    remove_active_video_chat, set_loop,
)
from AnnieXMedia.utils.exceptions import AssistantErr
from AnnieXMedia.utils.inline.play import stream_markup
from AnnieXMedia.utils.stream.api_handler import get_video_from_api
from AnnieXMedia.utils.errors import capture_internal_err

def dynamic_media_stream(path: str, video: bool = False) -> MediaStream:
    extra_params = "-user_agent 'Mozilla/5.0'"
    return MediaStream(
        media_path=path,
        audio_parameters=AudioQuality.HIGH,
        video_parameters=VideoQuality.SD_480p if video else None,
        ffmpeg_parameters=extra_params,
    )

class Call:
    def __init__(self):
        self.userbot1 = Client("AnnieXAssis1", config.API_ID, config.API_HASH, session_string=config.STRING1) if config.STRING1 else None
        self.one = PyTgCalls(self.userbot1) if self.userbot1 else None
        # Diğer asistanlar da buraya eklenebilir...
        self.active_calls: set[int] = set()

    @capture_internal_err
    async def join_call(self, chat_id, original_chat_id, link, video=None, image=None):
        assistant = await group_assistant(self, chat_id)
        stream = dynamic_media_stream(path=link, video=bool(video))
        await assistant.play(chat_id, stream)
        self.active_calls.add(chat_id)
        await add_active_chat(chat_id)
        await music_on(chat_id)

    @capture_internal_err
    async def play(self, client, chat_id: int) -> None:
        check = db.get(chat_id)
        if not check: return
        popped = check.pop(0)
        if not check:
            await client.leave_call(chat_id)
            return

        videoid = check[0]["vidid"]
        file_path = await get_video_from_api(videoid) if check[0]["file"].startswith("vid_") else check[0]["file"]
        if not file_path: return

        stream = dynamic_media_stream(path=file_path, video=True if str(check[0]["streamtype"]) == "video" else False)
        await client.play(chat_id, stream)
        # Kapak fotoğrafı ve bildirim mesajı buraya eklenebilir...

    @capture_internal_err
    async def stop_stream(self, chat_id: int) -> None:
        assistant = await group_assistant(self, chat_id)
        try: await assistant.leave_call(chat_id)
        except: pass
        self.active_calls.discard(chat_id)

    @capture_internal_err
    async def force_stop_stream(self, chat_id: int) -> None:
        await self.stop_stream(chat_id)

StreamController = Call()
