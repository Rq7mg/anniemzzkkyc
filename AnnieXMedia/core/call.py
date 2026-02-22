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
from AnnieXMedia.utils.exceptions import AssistantErr
from AnnieXMedia.utils.inline.play import stream_markup
from AnnieXMedia.utils.stream.api_handler import get_video_from_api
from AnnieXMedia.utils.errors import capture_internal_err

# --- KRİTİK DEĞİŞKENLER ---
autoend = {}
counter = {}

def dynamic_media_stream(path: str, video: bool = False) -> MediaStream:
    extra_params = "-user_agent 'Mozilla/5.0'"
    return MediaStream(
        media_path=path,
        audio_parameters=AudioQuality.HIGH,
        video_parameters=VideoQuality.SD_480p if video else None,
        ffmpeg_parameters=extra_params,
    )

async def _clear_(chat_id: int) -> None:
    popped = db.pop(chat_id, None)
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)
    await set_loop(chat_id, 0)

class Call:
    def __init__(self):
        self.userbot1 = Client("AnnieXAssis1", config.API_ID, config.API_HASH, session_string=config.STRING1) if config.STRING1 else None
        self.one = PyTgCalls(self.userbot1) if self.userbot1 else None
        self.userbot2 = Client("AnnieXAssis2", config.API_ID, config.API_HASH, session_string=config.STRING2) if config.STRING2 else None
        self.two = PyTgCalls(self.userbot2) if self.userbot2 else None
        self.userbot3 = Client("AnnieXAssis3", config.API_ID, config.API_HASH, session_string=config.STRING3) if config.STRING3 else None
        self.three = PyTgCalls(self.userbot3) if self.userbot3 else None
        self.userbot4 = Client("AnnieXAssis4", config.API_ID, config.API_HASH, session_string=config.STRING4) if config.STRING4 else None
        self.four = PyTgCalls(self.userbot4) if self.userbot4 else None
        self.userbot5 = Client("AnnieXAssis5", config.API_ID, config.API_HASH, session_string=config.STRING5) if config.STRING5 else None
        self.five = PyTgCalls(self.userbot5) if self.userbot5 else None
        self.active_calls: set[int] = set()

    # --- BOT BAŞLATMA FONKSİYONU ---
    async def start(self) -> None:
        LOGGER(__name__).info("Asistanlar devreye alınıyor...")
        if config.STRING1: await self.one.start()
        if config.STRING2: await self.two.start()
        if config.STRING3: await self.three.start()
        if config.STRING4: await self.four.start()
        if config.STRING5: await self.five.start()

    # --- HATA VEREN DECORATORS FONKSİYONU ---
    @capture_internal_err
    async def decorators(self) -> None:
        assistants = list(filter(None, [self.one, self.two, self.three, self.four, self.five]))
        
        CRITICAL = (
            ChatUpdate.Status.KICKED
            | ChatUpdate.Status.LEFT_GROUP
            | ChatUpdate.Status.CLOSED_VOICE_CHAT
        )

        async def unified_update_handler(client, update: Update) -> None:
            if isinstance(update, StreamEnded):
                await self.play(client, update.chat_id)
            elif isinstance(update, ChatUpdate):
                status = update.status
                if (status & ChatUpdate.Status.LEFT_CALL) or (status & CRITICAL):
                    await self.stop_stream(update.chat_id)

        for assistant in assistants:
            assistant.on_update()(unified_update_handler)

    @capture_internal_err
    async def join_call(self, chat_id, original_chat_id, link, video=None, image=None):
        assistant = await group_assistant(self, chat_id)
        stream = dynamic_media_stream(path=link, video=bool(video))
        try:
            await assistant.play(chat_id, stream)
        except Exception as e:
            raise AssistantErr(f"Yayın başlatılamadı: {e}")
        self.active_calls.add(chat_id)
        await add_active_chat(chat_id)
        await music_on(chat_id)
        if video: await add_active_video_chat(chat_id)
        if await is_autoend():
            counter[chat_id] = {}
            users = len(await assistant.get_participants(chat_id))
            if users == 1: autoend[chat_id] = datetime.now() + timedelta(minutes=1)

    @capture_internal_err
    async def play(self, client, chat_id: int) -> None:
        check = db.get(chat_id)
        if not check: return
        try:
            popped = check.pop(0)
            if not check:
                await _clear_(chat_id)
                return await client.leave_call(chat_id)
        except: return

        videoid = check[0]["vidid"]
        file_path = await get_video_from_api(videoid) if check[0]["file"].startswith("vid_") else check[0]["file"]
        if not file_path: return

        stream = dynamic_media_stream(path=file_path, video=True if str(check[0]["streamtype"]) == "video" else False)
        await client.play(chat_id, stream)

    @capture_internal_err
    async def stop_stream(self, chat_id: int) -> None:
        assistant = await group_assistant(self, chat_id)
        await _clear_(chat_id)
        try: await assistant.leave_call(chat_id)
        except: pass
        self.active_calls.discard(chat_id)

    @capture_internal_err
    async def force_stop_stream(self, chat_id: int) -> None:
        await self.stop_stream(chat_id)

    @capture_internal_err
    async def ping(self) -> str:
        pings = []
        if config.STRING1: pings.append(self.one.ping)
        return str(round(sum(pings) / len(pings), 3)) if pings else "0.0"

StreamController = Call()
