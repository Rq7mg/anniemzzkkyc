# Authored By Certified Coders © 2025
import asyncio
import os
from datetime import datetime, timedelta
from typing import Union
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioQuality, ChatUpdate, MediaStream, StreamEnded, Update, VideoQuality
import config
from strings import get_string
from AnnieXMedia import LOGGER, YouTube, app
from AnnieXMedia.misc import db
from AnnieXMedia.utils.database import (
    add_active_chat, add_active_video_chat, get_lang, get_loop,
    group_assistant, is_autoend, music_on, remove_active_chat,
    remove_active_video_chat, set_loop,
)
from AnnieXMedia.utils.inline.play import stream_markup
from AnnieXMedia.utils.thumbnails import get_thumb
from AnnieXMedia.utils.errors import capture_internal_err

autoend = {}
counter = {}

class Call:
    def __init__(self):
        self.userbot1 = Client("AnnieXAssis1", config.API_ID, config.API_HASH, session_string=config.STRING1) if config.STRING1 else None
        self.one = PyTgCalls(self.userbot1) if self.userbot1 else None
        self.active_calls: set[int] = set()

    async def start(self) -> None:
        if config.STRING1: await self.one.start()

    @capture_internal_err
    async def decorators(self) -> None:
        async def handler(client, update: Update) -> None:
            if isinstance(update, StreamEnded):
                await self.play(client, update.chat_id)
        if self.one: self.one.on_update()(handler)

    @capture_internal_err
    async def join_call(self, chat_id, original_chat_id, link, video=None, image=None):
        assistant = await group_assistant(self, chat_id)
        stream = MediaStream(link, audio_parameters=AudioQuality.HIGH, video_parameters=VideoQuality.SD_480p if video else None)
        await assistant.play(chat_id, stream)
        self.active_calls.add(chat_id)
        await add_active_chat(chat_id)
        await music_on(chat_id)

    @capture_internal_err
    async def play(self, client, chat_id: int) -> None:
        check = db.get(chat_id)
        if not check: return
        try:
            check.pop(0)
            if not check:
                await client.leave_call(chat_id)
                return
        except: return
        
        # Orijinal sıradaki parçayı oynatma mantığı
        queued = check[0]["file"]
        videoid = check[0]["vidid"]
        stream = MediaStream(queued, audio_parameters=AudioQuality.HIGH, video_parameters=VideoQuality.SD_480p if str(check[0]["streamtype"]) == "video" else None)
        await client.play(chat_id, stream)

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
