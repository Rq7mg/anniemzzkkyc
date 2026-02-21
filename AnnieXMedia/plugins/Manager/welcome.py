# Authored By Certified Coders © 2025
# WELCOME SİSTEMİ TAMAMEN DEVRE DIŞI BIRAKILMIŞTIR

import os
import asyncio
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters, enums
from pyrogram.types import Message, ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import TopicClosed, PeerIdInvalid, ChannelPrivate, SlowmodeWait
from AnnieXMedia import app
from AnnieXMedia.mongo.welcomedb import is_on, set_state, bump, cool, auto_on


# -------------------------------------------------
# 🚫 WELCOME KOMUTU DEVRE DIŞI
# -------------------------------------------------

@app.on_message(filters.command("welcome") & filters.group)
async def toggle(client, m: Message):
    return


# -------------------------------------------------
# 🚫 YENİ ÜYE EVENTİ TAMAMEN KAPATILDI
# -------------------------------------------------

@app.on_chat_member_updated(filters.group & filters.create(lambda _, __, ___: False), group=-3)
async def welcome(client, update: ChatMemberUpdated):
    return
