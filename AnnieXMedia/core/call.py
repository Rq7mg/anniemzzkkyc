# Authored By Certified Coders © 2025
import asyncio
import os
from datetime import datetime, timedelta
from typing import Union

from ntgcalls import TelegramServerError, ConnectionNotFound
from pyrogram import Client
from pyrogram.errors import FloodWait, ChatAdminRequired
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls
from pytgcalls.exceptions import NoActiveGroupCall, NoAudioSourceFound, NoVideoSourceFound
from pytgcalls.types import AudioQuality, ChatUpdate, MediaStream, StreamEnded, Update, VideoQuality

import config
from strings import get_string
from AnnieXMedia import LOGGER, YouTube, app
from AnnieXMedia.misc import db
from AnnieXMedia.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_lang,
    get_loop,
    group_assistant,
    is_autoend,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from AnnieXMedia.utils.exceptions import AssistantErr
from AnnieXMedia.utils.formatters import check_duration, seconds_to_min, speed_converter
from AnnieXMedia.utils.inline.play import stream_markup
from AnnieXMedia.utils.stream.autoclear import auto_clean
from AnnieXMedia.utils.thumbnails import get_thumb
from AnnieXMedia.utils.errors import capture_internal_err

# --- KIYICI GÜNCELLEME: API SİSTEMİNİ BURAYA DA EKLEDİK ---
from AnnieXMedia.utils.stream.stream import get_video_from_api

def dynamic_media_stream(path: str, video: bool = False, ffmpeg_params: str = None) -> MediaStream:
    # YouTube engellerini aşmak için FFmpeg'e özel kimlik (User-Agent) ekliyoruz
    extra_params = f"-user_agent 'Mozilla/5.0' {ffmpeg_params if ffmpeg_params else ''}"
    
    if video:
        return MediaStream(
            media_path=path,
            audio_parameters=AudioQuality.HIGH,
            video_parameters=VideoQuality.SD_480p,
            audio_flags=MediaStream.Flags.REQUIRED,
            video_flags=MediaStream.Flags.REQUIRED,
            ffmpeg_parameters=extra_params,
        )
    else:
        return MediaStream(
            media_path=path,
            audio_parameters=AudioQuality.HIGH,
            audio_flags=MediaStream.Flags.REQUIRED,
            video_flags=MediaStream.Flags.IGNORE,
            ffmpeg_parameters=extra_params,
        )

async def _clear_(chat_id: int) -> None:
    popped = db.pop(chat_id, None)
    if popped:
        await auto_clean(popped)
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

    @capture_internal_err
    async def join_call(self, chat_id: int, original_chat_id: int, link: str, video: Union[bool, str] = None, image: Union[bool, str] = None) -> None:
        assistant = await group_assistant(self, chat_id)
        lang = await get_lang(chat_id)
        _ = get_string(lang)
        stream = dynamic_media_stream(path=link, video=bool(video))
        try:
            await assistant.play(chat_id, stream)
        except Exception as e:
            raise AssistantErr(f"Gardaş yayın başlamıyor. Hata: {e}")
        self.active_calls.add(chat_id)
        await add_active_chat(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)

    @capture_internal_err
    async def play(self, client, chat_id: int) -> None:
        check = db.get(chat_id)
        if not check:
            return await self.stop_stream(chat_id)
        
        popped = None
        loop = await get_loop(chat_id)
        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                loop = loop - 1
                await set_loop(chat_id, loop)
            await auto_clean(popped)
        except:
            return

        if not check:
            await _clear_(chat_id)
            return await client.leave_call(chat_id)

        # SIRADAKİ PARÇA İÇİN API KONTROLÜ
        videoid = check[0]["vidid"]
        title = check[0]["title"]
        user = check[0]["by"]
        original_chat_id = check[0]["chat_id"]
        is_video = True if str(check[0]["streamtype"]) == "video" else False

        # --- YOUTUBE LİNKİ ÇEKME (Go Botundaki gibi güvenli) ---
        if check[0]["file"].startswith("vid_") or check[0]["file"].startswith("live_"):
            # Önce API'den taze link almayı dene
            file_path = await get_video_from_api(videoid)
            if not file_path:
                return await app.send_message(original_chat_id, text="Sıradaki parça açılamadı, YouTube banı devam ediyor.")
        else:
            file_path = check[0]["file"]

        stream = dynamic_media_stream(path=file_path, video=is_video)
        try:
            await client.play(chat_id, stream)
        except Exception:
            return await app.send_message(original_chat_id, text="Yayında bir kesinti oldu gardaş.")

        img = await get_thumb(videoid)
        button = stream_markup(get_string(await get_lang(chat_id)), chat_id)
        await app.send_photo(
            chat_id=original_chat_id,
            photo=img,
            caption=f"**Sıradaki Parça Oynatılıyor**\n\n**Başlık:** {title[:30]}\n**İsteyen:** {user}",
            reply_markup=InlineKeyboardMarkup(button),
        )

    # ... Diğer pause, resume, ping fonksiyonlarını kodun kalanından kopyalayabilirsin ...
    # (Yer darlığından sadece değişen kritik kısımları verdim ama yapı bu)
