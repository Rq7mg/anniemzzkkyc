# Authored By Certified Coders © 2025
import asyncio
import random

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, Message

import config
from config import AYU, BANNED_USERS
from AnnieXMedia import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from AnnieXMedia.utils.decorators.play import PlayWrapper
from AnnieXMedia.utils.errors import capture_err
from AnnieXMedia.utils.inline import slider_markup
from AnnieXMedia.utils.stream.stream import stream


@app.on_message(
    filters.command(
        [
            "oynat",          # Sesli oynat
            "voynat",         # Videolu oynat
            "atla",           # Şarkı geç
            "play", 
            "vplay",
            "cplay",
            "cvplay",
            "playforce",
            "vplayforce",
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
        mystic = await message.reply_text("𝐁𝐞𝐤𝐥𝐞 𝐥𝐚 𝐠𝐚𝐫𝐝𝐚𝐬̧, 𝐦𝐞𝐯𝐳𝐮𝐲𝐮 𝐜̧𝐨̈𝐳𝐮̈𝐩 𝐠𝐞𝐥𝐢𝐲𝐨𝐫𝐮𝐦...")
    except FloodWait as e:
        await asyncio.sleep(e.value)
        mystic = await message.reply_text("𝐋𝐚 𝐛𝐢 𝐝𝐮𝐫, 𝐬𝐢𝐫𝐚𝐲ᴀ 𝐠𝐢𝐫! 𝐁𝐢𝐫𝐚𝐳𝐝𝐚𝐧 𝐡𝐚𝐥𝐥𝐞𝐝𝐞𝐜𝐞𝐦.")
    except Exception:
        mystic = await app.send_message(message.chat.id, "𝐌𝐞𝐯𝐳𝐮 𝐝𝐞𝐫𝐢𝐧, 𝐛𝐢 𝐬𝐚𝐧𝐢𝐲𝐞 𝐛𝐞𝐤𝐥𝐞...")

    details = None
    track_id = None
    spotify = None
    slider = None
    internal_type = None
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # --- TELEGRAM DOSYALARI (SES / VİDEO / BELGE) ---
    reply = message.reply_to_message if message.reply_to_message else None
    
    # Video Yanıtlama Kontrolü (Düzeltildi)
    video_telegram = (reply.video or reply.document) if reply and video else None
    # Ses Yanıtlama Kontrolü
    audio_telegram = (reply.audio or reply.voice) if reply else None

    # Eğer bir video dosyasına yanıt verilmişse
    if video_telegram:
        if video_telegram.file_size > config.TG_VIDEO_FILESIZE_LIMIT:
            return await mystic.edit_text("𝐋𝐚 𝐛𝐮 𝐯𝐢𝐝𝐞𝐨 𝐧𝐞! 𝐂̧𝐨𝐤 𝐚𝐠̆𝐢𝐫, 𝐬𝐮𝐧𝐮𝐜𝐮𝐲𝐮 𝐦𝐮 𝐩𝐚𝐭𝐥𝐚𝐭𝐚𝐜𝐚𝐧?")
        
        file_path = await Telegram.get_filepath(video=video_telegram)
        downloaded = await Telegram.download(_, message, mystic, file_path)
        if downloaded:
            message_link = await Telegram.get_link(message)
            file_name = "Telegram Video"
            dur = await Telegram.get_duration(video_telegram, file_path)
            details = {"title": file_name, "link": message_link, "path": file_path, "dur": dur}
            try:
                await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, video=True, streamtype="telegram", forceplay=bool(fplay))
            except Exception as e:
                return await mystic.edit_text(f"𝐇𝐚𝐭𝐚 𝐜̧𝐢𝐤𝐭𝐢 𝐠𝐚ʀ𝐝𝐚𝐬̧: {e}")
            return await mystic.delete()

    # Eğer bir ses dosyasına yanıt verilmişse
    if audio_telegram:
        if audio_telegram.file_size > config.TG_AUDIO_FILESIZE_LIMIT:
            return await mystic.edit_text("𝐋𝐚 𝐛𝐮 𝐧𝐞! 𝐂̧𝐨𝐤 𝐛𝐮̈𝐲𝐮̈𝐤 𝐛𝐮 𝐝𝐨𝐬𝐲𝐚, 𝐛𝐢𝐳𝐢 𝐦𝐢 𝐲𝐨𝐫𝐚𝐜𝐚𝐧?")
        if audio_telegram.duration > config.DURATION_LIMIT:
            return await mystic.edit_text("𝐁𝐮 𝐤𝐚𝐝𝐚𝐫 𝐮𝐳𝐮𝐧 𝐩𝐚𝐫𝐜̧𝐚 𝐦𝐢 𝐨𝐥𝐮𝐫? 𝐊𝐚𝐩𝐚𝐭 𝐬𝐮𝐧𝐮!")

        file_path = await Telegram.get_filepath(audio=audio_telegram)
        downloaded = await Telegram.download(_, message, mystic, file_path)
        if downloaded:
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(audio_telegram, audio=True)
            dur = await Telegram.get_duration(audio_telegram, file_path)
            details = {"title": file_name, "link": message_link, "path": file_path, "dur": dur}
            try:
                await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, streamtype="telegram", forceplay=bool(fplay))
            except Exception as e:
                return await mystic.edit_text(f"𝐇𝐚𝐭𝐚 𝐜̧𝐢𝐤𝐭𝐢 𝐠𝐚ʀ𝐝𝐚𝐬̧: {e}")
            return await mystic.delete()

    # --- LİNK MEVZUSU (YOUTUBE / SPOTIFY) ---
    if url:
        if await Spotify.valid(url):
            spotify = True
            if not config.SPOTIFY_CLIENT_ID or not config.SPOTIFY_CLIENT_SECRET:
                return await mystic.edit_text("𝐒𝐩𝐨𝐭𝐢𝐟𝐲 𝐝𝐚𝐡𝐚 𝐛𝐢𝐳𝐝𝐞 𝐲𝐨𝐤 𝐠𝐚𝐫𝐝𝐚𝐬̧, 𝐛𝐨𝐬̧𝐚 𝐮𝐠̆𝐫𝐚𝐬̧𝐦𝐚!")
        
        try:
            details, track_id = await YouTube.track(url)
            internal_type = "youtube"
        except Exception as e:
            return await mystic.edit_text(f"𝐋𝐚 𝐛𝐮 𝐥𝐢𝐧𝐤𝐭𝐞 𝐛𝐢 𝐜̧𝐚𝐩𝐚𝐧𝐨𝐠̆𝐥𝐮 𝐯𝐚𝐫, 𝐚𝐜̧𝐢𝐥𝐦𝐢𝐲𝐨!\n𝐇𝐚𝐭𝐚: {e}")

    # --- ARAMA MEVZUSU ---
    else:
        # Eğer ne link var ne de yanıtlanan bir dosya varsa hata ver
        if not details and len(message.command) < 2:
            return await mystic.edit_text("𝐋𝐚 𝐧𝐞 𝐜̧𝐚𝐥𝐚𝐜𝐚𝐦? 𝐁𝐢 𝐬̧𝐞𝐲 𝐲𝐚𝐳 𝐝𝐚 𝐨𝐲𝐧𝐚𝐭𝐚𝐥𝐢𝐦!")

        if not details: # Sadece arama yapılacaksa
            slider = True
            query = message.text.split(None, 1)[1]
            
            try:
                details, track_id = await YouTube.track(query)
                internal_type = "youtube"
            except Exception as e:
                return await mystic.edit_text(f"𝐀𝐫𝐚𝐝𝐢𝐠̆𝐢𝐧 𝐦𝐞𝐯𝐳𝐮𝐲𝐮 𝐛𝐮𝐥𝐚𝐦𝐚𝐝𝐢𝐦 𝐠𝐚𝐫𝐝𝐚𝐬̧!\n𝐒𝐞𝐛𝐞𝐩: {e}")

    # --- MEVZUYU BAŞLATMA (STREAM) ---
    if not details:
        return await mystic.edit_text("𝐃𝐞𝐭𝐚𝐲𝐥𝐚𝐫 𝐚𝐥𝐢𝐧𝐚𝐦𝐚𝐝𝐢, 𝐛𝐢 𝐝𝐚𝐡𝐚 𝐝𝐞𝐧𝐞 𝐡𝐞𝐥𝐞.")

    try:
        if str(playmode) == "Direct":
            await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, video=bool(video), streamtype=internal_type, spotify=spotify, forceplay=bool(fplay))
            await mystic.delete()
        else:
            if slider:
                buttons = slider_markup(_, track_id, user_id, query, 0, "c" if channel else "g", "f" if fplay else "d")
                await mystic.delete()
                await message.reply_photo(
                    photo=details["thumb"], 
                    caption=f"⁍ **𝐏𝐚𝐫𝐜̧𝐚:** {details['title']}\n⁍ **𝐒𝐮̈𝐫𝐞:** {details['duration_min']}\n\n**𝐌𝐞𝐯𝐳𝐮𝐲𝐮 𝐛𝐚𝐬̧𝐥𝐚𝐭𝐢𝐲𝐨𝐫𝐮𝐦, 𝐤𝐮𝐥𝐚𝐠̆𝐢𝐧𝐢𝐳𝐢 𝐚𝐜̧𝐢𝐧!**", 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            else:
                await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, video=bool(video), streamtype=internal_type, spotify=spotify, forceplay=bool(fplay))
                await mystic.delete()
    except Exception as e:
        await mystic.edit_text(f"𝐌𝐞𝐯𝐳𝐮 𝐩𝐚𝐭𝐥𝐚𝐝𝐢 𝐠𝐚𝐫𝐝𝐚𝐬̧: {e}")
