# Authored By Certified Coders © 2025
import asyncio
import random
import string

from pyrogram import filters
from pyrogram.errors import FloodWait, RandomIdDuplicate
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import AYU, BANNED_USERS, lyrical
from AnnieXMedia import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from AnnieXMedia.core.call import StreamController
from AnnieXMedia.utils import seconds_to_min, time_to_seconds
from AnnieXMedia.utils.channelplay import get_channeplayCB
from AnnieXMedia.utils.decorators.language import languageCB
from AnnieXMedia.utils.decorators.play import PlayWrapper
from AnnieXMedia.utils.errors import capture_err, capture_callback_err
from AnnieXMedia.utils.formatters import formats
from AnnieXMedia.utils.inline import (
    botplaylist_markup,
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from AnnieXMedia.utils.logger import play_logs
from AnnieXMedia.utils.stream.stream import stream


@app.on_message(
    filters.command(
        [
            "play",
            "vplay",
            "cplay",
            "cvplay",
            "playforce",
            "vplayforce",
            "cplayforce",
            "cvplayforce",
            "oynat", # Ankara usulü oynat komutu
            "cal",
        ]
    )
    & filters.group
    & ~BANNED_USERS
)
@PlayWrapper
@capture_err
async def play_command(
    client,
    message: Message,
    _,
    chat_id,
    video,
    channel,
    playmode,
    url,
    fplay,
):
    try:
        # Karşılama mesajlarını sertleştirdik
        mystic = await message.reply_text("𝐁𝐞𝐤𝐥𝐞 𝐥𝐚 𝐠𝐚𝐫𝐝𝐚𝐬̧, 𝐦𝐞𝐯𝐳𝐮𝐲𝐮 𝐜̧𝐨̈𝐳𝐮̈𝐩 𝐠𝐞𝐥𝐢𝐲𝐨𝐫𝐮𝐦...")
    except FloodWait as e:
        await asyncio.sleep(e.value)
        mystic = await message.reply_text("𝐋𝐚 𝐛𝐢 𝐝𝐮𝐫, 𝐬𝐢𝐫𝐚𝐲𝐚 𝐠𝐢𝐫! 𝐁𝐢𝐫𝐚𝐳𝐝𝐚𝐧 𝐡𝐚𝐥𝐥𝐞𝐝𝐞𝐜𝐞𝐦.")
    except Exception:
        mystic = await app.send_message(message.chat.id, "𝐌𝐞𝐯𝐳𝐮 𝐝𝐞𝐫𝐢𝐧, 𝐛𝐢 𝐬𝐚𝐧𝐢𝐲𝐞 𝐛𝐞𝐤𝐥𝐞...")

    plist_id, plist_type, spotify, slider = None, None, None, None
    internal_type, log_label = None, None
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # Telgraf dosyaları için sert uyarılar
    audio_telegram = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )

    if audio_telegram:
        if audio_telegram.file_size > config.TG_AUDIO_FILESIZE_LIMIT:
            return await mystic.edit_text("𝐋𝐚 𝐛𝐮 𝐧𝐞! 𝐂̧𝐨𝐤 𝐛𝐮̈𝐲𝐮̈𝐤 𝐛𝐮 𝐝𝐨𝐬𝐲𝐚, 𝐛𝐢𝐳𝐢 𝐦𝐢 𝐲𝐨𝐫𝐚𝐜𝐚𝐧?")

        if audio_telegram.duration > config.DURATION_LIMIT:
            return await mystic.edit_text("𝐁𝐮 𝐤𝐚𝐝𝐚𝐫 𝐮𝐳𝐮𝐧 𝐩𝐚𝐫𝐜̧𝐚 𝐦𝐢 𝐨𝐥𝐮𝐫? 𝐊𝐚𝐩𝐚𝐭 𝐬𝐮𝐧𝐮!")

        file_path = await Telegram.get_filepath(audio=audio_telegram)
        downloaded = await Telegram.download(_, message, mystic, file_path)
        if downloaded:
            # ... (diğer kodlar aynı kalacak şekilde devam ediyor)
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(audio_telegram, audio=True)
            dur = await Telegram.get_duration(audio_telegram, file_path)
            details = {"title": file_name, "link": message_link, "path": file_path, "dur": dur}
            try:
                internal_type = "telegram"
                await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, streamtype=internal_type, forceplay=bool(fplay))
            except Exception as e:
                return await mystic.edit_text(f"𝐇𝐚𝐭𝐚 𝐜̧𝐢𝐤𝐭𝐢 𝐠𝐚𝐫𝐝𝐚𝐬̧: {e}")
            await play_logs(message, streamtype="Telegram [Ses]")
            return await mystic.delete()

    # Spotify Mevzusu
    if url:
        if await Spotify.valid(url):
            spotify = True
            if not config.SPOTIFY_CLIENT_ID or not config.SPOTIFY_CLIENT_SECRET:
                return await mystic.edit_text("𝐒𝐩𝐨𝐭𝐢𝐟𝐲 𝐝𝐚𝐡𝐚 𝐛𝐢𝐳𝐝𝐞 𝐲𝐨𝐤 𝐠𝐚𝐫𝐝𝐚𝐬̧, 𝐛𝐨𝐬̧𝐚 𝐮𝐠̆𝐫𝐚𝐬̧𝐦𝐚!")

    # Arama Mevzusu
    else:
        if len(message.command) < 2:
            return await mystic.edit_text("𝐋𝐚 𝐧𝐞 𝐜̧𝐚𝐥𝐚𝐜𝐚𝐦? 𝐁𝐢 𝐬̧𝐞𝐲 𝐲𝐚𝐳 𝐝𝐚 𝐨𝐲𝐧𝐚𝐭𝐚𝐥𝐢𝐦!")

        slider = True
        query = message.text.split(None, 1)[1]
        
        # Youtube arama başlasın
        try:
            details, track_id = await YouTube.track(query)
        except Exception:
            return await mystic.edit_text("𝐀𝐫𝐚𝐝𝐢𝐠̆𝐢𝐧 𝐦𝐞𝐯𝐳𝐮𝐲𝐮 𝐛𝐮𝐥𝐚𝐦𝐚𝐝𝐢𝐦 𝐠𝐚𝐫𝐝𝐚𝐬̧, 𝐛𝐚𝐬̧𝐤𝐚 𝐛𝐢𝐬̧𝐞𝐲 𝐝𝐞.")

        internal_type = "youtube"
        
    # Mevzuyu Başlatma (Stream)
    try:
        if str(playmode) == "Direct":
            await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, video=bool(video), streamtype=internal_type, spotify=spotify, forceplay=bool(fplay))
            await mystic.delete()
        else:
            # Butonlu kısım
            if slider:
                buttons = slider_markup(_, track_id, user_id, query, 0, "c" if channel else "g", "f" if fplay else "d")
                await mystic.delete()
                await message.reply_photo(photo=details["thumb"], caption=f"⁍ **𝐏𝐚𝐫𝐜̧𝐚:** {details['title']}\n⁍ **𝐒𝐮̈𝐫𝐞:** {details['duration_min']}\n\n**𝐌𝐞𝐯𝐳𝐮𝐲𝐮 𝐛𝐚𝐬̧𝐥𝐚𝐭𝐢𝐲𝐨𝐫𝐮𝐦, 𝐤𝐮𝐥𝐚𝐠̆𝐢𝐧𝐢𝐳𝐢 𝐚𝐜̧𝐢𝐧!**", reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        await mystic.edit_text(f"𝐌𝐞𝐯𝐳𝐮 𝐩𝐚𝐭𝐥𝐚𝐝𝐢 𝐠𝐚𝐫𝐝𝐚𝐬̧: {e}")

# ... Kodun geri kalanı aynı mantıkla devam eder ...
