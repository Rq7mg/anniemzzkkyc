# Authored By Certified Coders © 2025
import time
from pyrogram.types import InlineKeyboardButton
from AnnieXMedia.utils.formatters import time_to_seconds

LAST_UPDATE_TIME = {}

# -------------------------------
# 🎵 DARK KIYICI THEME FONKSİYONLARI
# -------------------------------

def build_dark_caption(user, title, duration, chat_title, count):
    return f"""
🖤─── KIYICI FM ───🖤
💥 Şu An Çalıyor 💥

🎶 Parça: {title}
⏱ Süre: {duration}
👤 İsteyen: {user}
🏠 Grup: {chat_title}
👥 Üye Sayısı: {count}

▰▰▰▰▰▰▱▱ 0:00 / {duration}
"""

def generate_dark_bar(played_sec, duration_sec):
    if duration_sec == 0:
        percentage = 0
    else:
        percentage = min((played_sec / duration_sec) * 100, 100)

    bar_length = 10
    filled = int(round(bar_length * percentage / 100))
    return "▰" * filled + "▱" * (bar_length - filled)

def dark_control_buttons(_, chat_id):
    # Butonları 2 ayrı satıra böldük, böylece sıkışmayacaklar.
    return [
        [
            InlineKeyboardButton("⏸ Duraklat", callback_data=f"stream_admin Pause|{chat_id}"),
            InlineKeyboardButton("🎧 Oynat", callback_data=f"stream_admin Resume|{chat_id}")
        ],
        [
            InlineKeyboardButton("↻ Tekrar", callback_data=f"stream_admin Replay|{chat_id}"),
            InlineKeyboardButton("⏭ Geç", callback_data=f"stream_admin Skip|{chat_id}"),
            InlineKeyboardButton("🛑 Durdur", callback_data=f"stream_admin Stop|{chat_id}")
        ]
    ]

# -------------------------------
# ESKİ FONKSİYONLAR / BUTTONLAR
# -------------------------------

def track_markup(_, videoid, user_id, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}"
            )
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}"
            )
        ]
    ]

def should_update_progress(chat_id):
    now = time.time()
    last = LAST_UPDATE_TIME.get(chat_id, 0)
    if now - last >= 6:
        LAST_UPDATE_TIME[chat_id] = now
        return True
    return False

def stream_markup_timer(_, chat_id, played, dur):
    if not should_update_progress(chat_id):
        return None

    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    bar = generate_dark_bar(played_sec, duration_sec)
    progress_line = f"{played} {bar} {dur}"

    # Butonları satır satır ekliyoruz
    buttons = [
        # 1. Satır: İlerleme Çubuğu (Tek başına, uzun)
        [InlineKeyboardButton(text=progress_line, callback_data="GetTimer")]
    ]
    
    # 2. ve 3. Satır: Kontrol Butonları (Oynat, Duraklat vb.)
    buttons.extend(dark_control_buttons(_, chat_id))
    
    # 4. Satır: Kapat Butonu
    buttons.append(
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]
    )

    return buttons

def stream_markup(_, chat_id):
    # Timersız görünümde de önce kontroller, en alta kapat butonu
    buttons = dark_control_buttons(_, chat_id)
    buttons.append(
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]
    )
    return buttons

def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"AnniePlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}"
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"AnniePlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}"
            )
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}"
            )
        ]
    ]

def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}"
            )
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}"
            )
        ]
    ]

def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    short_query = query[:20]
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}"
            )
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{short_query}|{user_id}|{channel}|{fplay}"
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {short_query}|{user_id}"
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{short_query}|{user_id}|{channel}|{fplay}"
            )
        ]
    ]
