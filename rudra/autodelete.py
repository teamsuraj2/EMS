import time
import threading
from telebot import TeleBot
import rudra.user as user


bot: TeleBot = None


def set_bot(bot_instance: TeleBot):
    global bot
    bot = bot_instance


def schedule_delete(chat_id: int, message_id: int, delay: int):
    delete_at = int(time.time()) + delay
    user.pending_deletes.insert_one({
        "chat_id": chat_id,
        "message_id": message_id,
        "delete_at": delete_at
    })


def delete_worker():
    while True:
        now = int(time.time())
        tasks = list(user.pending_deletes.find({"delete_at": {"$lte": now}}))
        for task in tasks:
            try:
                bot.delete_message(task["chat_id"], task["message_id"])
            except Exception as e:
                print(f"Delete failed: {e}")
            user.pending_deletes.delete_one({"_id": task["_id"]})
        time.sleep(5)  # Check every 5 seconds


def register_handlers(bot_instance: TeleBot):
    set_bot(bot_instance)

    @bot.message_handler(content_types=["photo", "video", "sticker", "animation"])
    def handle_media(message):
        chat_id = message.chat.id
        delay = user.get_group_delay(chat_id)
        schedule_delete(chat_id, message.message_id, delay)

    @bot.message_handler(commands=["set_delay"])
    def handle_set_delay(message):
        chat_id = message.chat.id

        if message.chat.type not in ["group", "supergroup"]:
            bot.reply_to(message, "❌ This command can only be used in groups.")
            return

        try:
            member = bot.get_chat_member(chat_id, message.from_user.id)
            if member.status not in ["administrator", "creator"]:
                bot.reply_to(message, "❌ Only admins can run this command.")
                return
        except Exception:
            bot.reply_to(message, "❌ Admin check failed.")
            return

        try:
            parts = message.text.split()
            if len(parts) < 2:
                bot.reply_to(message, "Usage: /set_delay <minutes>")
                return
            minutes = int(parts[1])
            delay_seconds = minutes * 60
            user.set_group_delay(chat_id, delay_seconds)
            bot.reply_to(message, f"✅ Delete delay has been set to {minutes} minutes.")
        except ValueError:
            bot.reply_to(message, "❌ Please enter a valid number.")

    @bot.message_handler(commands=["get_delay"])
    def handle_get_delay(message):
        chat_id = message.chat.id
        delay = user.get_group_delay(chat_id) // 60
        bot.reply_to(message, f"🕒 Current delete delay for this group is: {delay} minutes.")
