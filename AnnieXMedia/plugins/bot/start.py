# Authored By Certified Coders © 2025
# Mekanın Sahibi: Mustafa Araz (@officialkiyici)
import asyncio
import random
import time
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.aio import VideosSearch

import config
from AnnieXMedia import app
from AnnieXMedia.misc import _boot_
from AnnieXMedia.plugins.sudo.sudoers import sudoers_list
from AnnieXMedia.utils import bot_sys_stats
from AnnieXMedia.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    get_served_chats,
    get_served_users,
    is_banned_user,
    is_on_off,
)
from AnnieXMedia.utils.decorators.language import LanguageStart
from AnnieXMedia.utils.formatters import get_readable_time
from AnnieXMedia.utils.inline.start import private_panel, start_panel
from AnnieXMedia.utils.inline.help import first_page
from config import BANNED_USERS, AYUV, HELP_IMG_URL, START_VIDS, STICKERS
from strings import get_string


async def delete_sticker_after_delay(message: Message, delay: int) -> None:
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    try:
        await add_served_user(message.from_user.id)
    except Exception:
        pass

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name.startswith("help"):
            keyboard = first_page(_)
            return await message.reply_text(
                text=f"**𝐋𝐚 𝐠𝐚𝐫𝐝𝐚𝐬̧, 𝐲𝐚𝐫𝐝𝐢𝐦 𝐦𝐢 𝐥𝐚𝐳𝐢𝐦? 𝐀𝐥 𝐛𝐚𝐤 𝐛𝐮𝐧𝐥𝐚𝐫𝐚 𝐢𝐬̧𝐭𝐞:**\n\n{_['help_1'].format(config.SUPPORT_CHAT)}",
                reply_markup=keyboard,
            )

        if name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            return

        if name.startswith("inf"):
            m = await message.reply_text("🔎 **𝐌𝐞𝐯𝐳𝐮𝐲𝐮 𝐚𝐫𝐚𝐬̧𝐭𝐢𝐫𝐢𝐲𝐨𝐫𝐮𝐦...**")
            try:
                vid_id = str(name).replace("info_", "", 1)
                query = f"https://www.youtube.com/watch?v={vid_id}"
                results = VideosSearch(query, limit=1)
                data = await results.next()
                result = (data.get("result") or [None])[0]
                if not result:
                    await m.edit_text("𝐁𝐨𝐬̧𝐚 𝐚𝐫𝐚𝐦𝐚 𝐠𝐚𝐫𝐝𝐚𝐬̧, 𝐛𝐮𝐥𝐚𝐦𝐚𝐝𝐢𝐦.")
                    return

                title = result.get("title") or "İsimsiz Mevzu"
                duration = result.get("duration") or "Belli Değil"
                views = (result.get("viewCount") or {}).get("short") or "0"
                thumbnail = ((result.get("thumbnails") or [{}])[0].get("url") or "").split("?")[0]
                
                searched_text = f"⁍ **𝐌𝐞𝐯𝐳𝐮:** {title}\n⁍ **𝐕𝐚𝐤𝐢𝐭:** {duration}\n⁍ **𝐓𝐢𝐤𝐥𝐚𝐧𝐦𝐚:** {views}\n\n**𝐀𝐜̧𝐚𝐥𝐢𝐦 𝐦𝐢 𝐛𝐮𝐧𝐮 𝐠𝐚𝐫𝐝𝐚𝐬̧?**"
                key = InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="𝐌𝐞𝐯𝐳𝐮𝐲𝐚 𝐆𝐢𝐭", url=result.get("link")),
                      InlineKeyboardButton(text="𝐃𝐞𝐬𝐭𝐞𝐤", url=config.SUPPORT_CHAT)]]
                )

                await m.delete()
                await message.reply_photo(photo=thumbnail, caption=searched_text, reply_markup=key)
            except Exception as e:
                await m.edit_text(f"𝐌𝐞𝐯𝐳𝐮 𝐩𝐚𝐭𝐥𝐚𝐝𝐢: {e}")
            return

    # Özel Mesaj Karşılama - Sticker Raconu
    sticker_message = await message.reply_sticker(sticker=random.choice(STICKERS))
    asyncio.create_task(delete_sticker_after_delay(sticker_message, 2))

    # --- MUSTAFA ARAZ (KIYICI BOSS) ÖZEL PANEL ---
    # İstediğin fontlar ve sert dil birebir işlendi gardaş
    START_TEXT = f"""
𝐕𝐚𝐲 𝐠𝐚𝐫𝐝𝐚𝐬‌𝐢𝐦 {message.from_user.mention} 𝐡𝐨𝐬‌ 𝐠𝐞𝐥𝐝𝐢𝐧! 𝐌𝐞𝐤𝐚𝐧𝐢𝐧 𝐬𝐚𝐡𝐢𝐛𝐢 𝐠𝐞𝐥𝐝𝐢, 𝐝𝐚𝐠‌𝐢𝐥𝐢𝐧 𝐥𝐚! 👊

𝐁𝐞𝐧 **𝐊𝐈𝐘𝐈𝐂𝐈** 𝐌𝐮‌𝐳𝐢𝐤 𝐁𝐨𝐭𝐮, 𝐞𝐦𝐫𝐢𝐧𝐝𝐞𝐲𝐢𝐦 𝐠𝐚𝐫𝐝𝐚𝐬‌. 𝐇𝐚𝐲𝐢𝐫𝐝𝐢𝐫 𝐛𝐢' 𝐦𝐞𝐯𝐳𝐮 𝐦𝐮 𝐯𝐚𝐫 𝐲𝐨𝐤𝐬𝐚 𝐤𝐮𝐥𝐚𝐠‌𝐢𝐧𝐢𝐧 𝐩𝐚𝐬𝐢𝐧𝐢 𝐦𝐢 𝐬𝐢𝐥𝐞𝐥𝐢𝐦? 🔪

𝐒𝐞𝐧 𝐢𝐬𝐭𝐞 𝐲𝐞𝐭𝐞𝐫 𝐤𝐢, 𝐦𝐚𝐡𝐚𝐥𝐥𝐞𝐲𝐢 𝐢𝐧𝐥𝐞𝐭𝐦𝐞𝐲𝐞 𝐡𝐚𝐳𝐢𝐫𝐢𝐳. 𝐀𝐬‌𝐚𝐠‌𝐢𝐝𝐚𝐤𝐢 𝐛𝐮𝐭𝐨𝐧𝐥𝐚𝐫𝐝𝐚𝐧 𝐦𝐞𝐯𝐳𝐮𝐲𝐚 𝐚𝐤𝐚𝐛𝐢𝐥𝐢𝐫𝐬𝐢𝐧. 𝐃𝐢𝐤𝐤𝐚𝐭 𝐞𝐭, 𝐬𝐢𝐬𝐭𝐞𝐦𝐢𝐧 𝐜𝐚𝐧𝐢𝐧𝐢 𝐬𝐢𝐤𝐦𝐚! 👇
"""

    buttons = [
        [
            InlineKeyboardButton(
                text="🤘 𝐌𝐞𝐯𝐳𝐮𝐲𝐚 𝐀𝐤𝐚𝐥𝐢𝐦",
                url=f"https://t.me/{app.username}?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton(text="❄️ 𝐁𝐢𝐳𝐞 𝐊𝐚𝐭𝐢𝐥", url=config.SUPPORT_CHAT),
            InlineKeyboardButton(text="❓ 𝐑𝐚𝐜𝐨𝐧 & 𝐃𝐮𝐲𝐮𝐫𝐮𝐥𝐚𝐫", url="https://t.me/kiyiciupdate")
        ],
        [
            InlineKeyboardButton(text="👑 𝐌𝐞𝐤𝐚𝐧𝐢𝐧 𝐒𝐚𝐡𝐢𝐛𝐢", url="https://t.me/officialkiyici")
        ]
    ]

    await message.reply_text(
        text=START_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    uptime = int(time.time() - _boot_)
    try:
        await message.reply_text(
            text=f"**𝐇𝐚𝐲𝐢𝐫𝐥𝐢 𝐢𝐬̧𝐥𝐞𝐫 𝐠𝐚𝐫𝐝𝐚𝐬̧𝐥𝐚𝐫!**\n\n"
                 f"**𝐁𝐨𝐭𝐮𝐦𝐮𝐳 {get_readable_time(uptime)} 𝐬𝐮̈𝐫𝐞𝐝𝐢𝐫 𝐦𝐞𝐯𝐳𝐮𝐧𝐮𝐧 𝐛𝐚𝐬̧𝐢𝐧𝐝𝐚.**\n"
                 f"**𝐌𝐮̈𝐳𝐢𝐤 𝐚𝐜̧𝐦𝐚𝐤 𝐢𝐬𝐭𝐞𝐲𝐞𝐧 `/oynat` 𝐲𝐚𝐳𝐬𝐢𝐧.**",
            reply_markup=InlineKeyboardMarkup(start_panel(_)),
        )
    except:
        pass
    return await add_served_chat(message.chat.id)

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                    return await message.reply_text("**𝐋𝐚 𝐠𝐚𝐫𝐝𝐚𝐬̧ 𝐛𝐮 𝐛𝐞𝐛𝐞 𝐬𝐚𝐛𝐢𝐤𝐚𝐥𝐢, 𝐚𝐭𝐭𝐢𝐦 𝐠𝐢𝐭𝐭𝐢!**")
                except Exception:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text("**𝐁𝐚ᴋ 𝐠𝐚𝐫𝐝𝐚𝐬̧, 𝐛𝐞𝐧𝐢 𝐬𝐮̈𝐩𝐞𝐫 𝐠𝐫𝐮𝐩 𝐲𝐚𝐩𝐦𝐚𝐳𝐬𝐚𝐧 𝐜̧𝐚𝐥𝐢𝐬̧𝐦𝐚𝐦!**")
                    return await app.leave_chat(message.chat.id)

                await message.reply_text(
                    text=f"**𝐒𝐞𝐥𝐚𝐦𝐮𝐧 𝐀𝐥𝐞𝐲𝐤𝐮̈𝐦 𝐠𝐫ᴜᴘ 𝐚𝐡𝐚𝐥𝐢𝐬𝐢!**\n\n"
                         f"**{message.from_user.mention} 𝐠𝐚𝐫𝐝𝐚𝐬̧𝐢𝐦 𝐛𝐞𝐧𝐢 𝐛𝐮𝐫𝐚𝐲𝐚 𝐠𝐞𝐭𝐢𝐫𝐝𝐢.**\n"
                         f"**𝐇𝐚𝐝𝐢 𝐛𝐚𝐤𝐚𝐥𝐢𝐦, 𝐦𝐞𝐯𝐳𝐮𝐲𝐚 𝐛𝐚𝐬̧𝐥𝐚𝐭𝐚𝐥𝐢𝐦!**",
                    reply_markup=InlineKeyboardMarkup(start_panel(_)),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as ex:
            print(ex)
