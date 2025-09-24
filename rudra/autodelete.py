import threading
import time
from telebot import TeleBot
from rudra.user import get_group_delay

scheduled_messages = {}
lock = threading.Lock()

def schedule_auto_delete(bot: TeleBot, message):
    chat_id = message.chat.id
    delay = get_group_delay(chat_id)
    delete_time = time.time() + delay
    with lock:
        if chat_id not in scheduled_messages:
            scheduled_messages[chat_id] = []
        scheduled_messages[chat_id].append((message.message_id, delete_time))

def auto_delete_worker(bot: TeleBot):
    while True:
        now = time.time()
        with lock:
            for chat_id in list(scheduled_messages.keys()):
                new_list = []
                for msg_id, delete_time in scheduled_messages[chat_id]:
                    if now >= delete_time:
                        try:
                            bot.delete_message(chat_id, msg_id)
                        except:
                            pass
                    else:
                        new_list.append((msg_id, delete_time))
                scheduled_messages[chat_id] = new_list
        time.sleep(10)
