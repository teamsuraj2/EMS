# Copyright (c) 2025 Rajputshivsingh65. All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
# Written by Rajputshivsingh65 <choudharydilip256@gmail.com>, January 2025.

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def send_start_message(bot, message):
    """Sends the start message with inline buttons and an image."""
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
    start_text = (
    f"Hello {full_name} 👋, I'm your 𝗘𝗱𝗶𝘁 𝗚𝘂𝗮𝗿𝗱𝗶𝗮𝗻 𝗕𝗼𝘁, here to maintain a secure environment for our discussions.\n\n"
    "🚫 𝗘𝗱𝗶𝘁𝗲𝗱 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗗𝗲𝗹𝗲𝘁𝗶𝗼𝗻: 𝗜'𝗹𝗹 𝗿𝗲𝗺𝗼𝘃𝗲 𝗲𝗱𝗶𝘁𝗲𝗱 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀 𝘁𝗼 𝗺𝗮𝗶𝗻𝘁𝗮𝗶𝗻 𝘁𝗿𝗮𝗻𝘀𝗽𝗮𝗿𝗲𝗻𝗰𝘆.\n\n"
    "• Auto-removes all types of media — photos, gifs, stickers..\n\n"
    "Offers flexible admin controls like authentication and deletion delay:\n"
    "1. Add me to your group.\n"
    "2. I'll start protecting instantly.\n\n"
    "⚙️ **👇Commands to know more!:**\n"
    "• /set_delay <minutes> — Change the auto-delete time for media, sticker, gift.\n"
    "• /get_delay — Default media deletion time is 60 minute..\n\n"
    "➡️ Click on 𝗔𝗱𝗱 𝗚𝗿𝗼𝘂𝗽 to add me and keep our group safe!"
)


    markup = InlineKeyboardMarkup(row_width=2)  
    markup.add(
        InlineKeyboardButton("𝖴𝗉𝖽𝖺𝗍𝖾 🚀", url="https://t.me/Team_Dns_Network"),
        InlineKeyboardButton("𝖲𝗎𝗉𝗉𝗈𝗋𝗍 💬", url="https://t.me/dns_support_group")
    )
    markup.add(InlineKeyboardButton("✨ 𝖠𝖽𝖽 𝖦𝗋𝗈𝗎𝗉", url="https://t.me/EditGuardiansBot?startgroup=s&admin=delete_messages+invite_users"))

    # Send the photo along with the message
    bot.send_photo(message.chat.id, photo="https://files.catbox.moe/h7d6wk.jpg", caption=start_text, reply_markup=markup)
