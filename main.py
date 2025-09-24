# Copyright (c) 2025 Rajputshivsingh65. All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
# Written by Rajputshivsingh65 <choudharydilip256@gmail.com>, January 2025.

import telebot
import logging 
from rudra.start import send_start_message
from rudra.delete_media_edits import handle_media_edited_message
from rudra.user import get_group_count, get_user_count, add_group, add_user, set_group_delay
from rudra.warn import warn_user
from rudra.broadcast import send_broadcast_message
from rudra.logging import log_user_activity, log_group_activity, send_thank_you_message 
from config import BOT_TOKEN, OWNER_ID
from rudra.delete_edits import handle_edited_message
from rudra.autodelete import schedule_auto_delete, auto_delete_worker 

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def handle_start(message):
    user_id = message.from_user.id
    add_user(user_id)
    log_user_activity(user_id)  
    send_start_message(bot, message)

@bot.edited_message_handler(func=lambda message: True)
def on_message_edited(message):
    warn_user(bot, message)
    handle_edited_message(bot, message)

@bot.edited_message_handler(content_types=["photo", "video", "audio", "document", "voice"])
def on_media_edited(message):
    warn_user(bot, message)
    handle_media_edited_message(bot, message)

@bot.message_handler(commands=["user"])
def handle_user_count(message):
    if str(message.from_user.id) == OWNER_ID:
        user_count = get_user_count()
        bot.send_message(message.chat.id, f"Total users: {user_count}")
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")

@bot.message_handler(commands=["group"])
def handle_group_count(message):
    if str(message.from_user.id) == OWNER_ID:
        group_count = get_group_count()
        bot.send_message(message.chat.id, f"Total groups: {group_count}")
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")

@bot.message_handler(commands=['broadcast'])
def handle_broadcast(message):
    if str(message.from_user.id) == OWNER_ID:
        message_text = message.text[11:]
        if message_text:
            send_broadcast_message(message_text)
            bot.reply_to(message, "Broadcast message sent to all users and groups!")
        else:
            bot.reply_to(message, "Please provide a message to broadcast.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

@bot.my_chat_member_handler(func=lambda member: member.new_chat_member.status in ["member", "administrator"])
def handle_bot_added_to_group(event):
    try:
        chat = event.chat
        if chat.type in ["group", "supergroup"]:
            group_id = chat.id
            group_name = chat.title
            user = event.from_user
            add_group(group_id)
            log_group_activity(group_id, group_name, "added")
            send_thank_you_message(user, group_name, group_id)
            logging.info(f"Bot added to group: {group_name} (ID: {group_id})")
    except Exception as e:
        logging.error(f"Error handling bot added to group: {e}")   


@bot.message_handler(commands=["set_delay"])
def handle_set_delay(message):
    chat = message.chat
    if chat.type not in ["group", "supergroup"]:
        bot.reply_to(message, "This command can only be used in groups.")
        return
    try:
        member = bot.get_chat_member(chat.id, message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            bot.reply_to(message, "Only group admins can set delay.")
            return
    except:
        bot.reply_to(message, "Error checking admin rights.")
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Usage: /set_delay <minutes>")
            return
        minutes = int(parts[1])
        if minutes < 1:
            bot.reply_to(message, "Delay must be at least 1 minute.")
            return
        delay = set_group_delay(chat.id, minutes)
        bot.reply_to(message, f"Auto-delete delay set to {minutes} minutes for this group.")
    except ValueError:
        bot.reply_to(message, "Please enter a valid number of minutes.")

if __name__ == "__main__":
    bot.infinity_polling()
