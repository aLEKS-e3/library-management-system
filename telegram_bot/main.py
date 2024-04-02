import os

import telebot


TOKEN = os.getenv("TELEGRAM_API")

tb = telebot.TeleBot(TOKEN)


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        chatid = m.chat.id
        if m.content_type == 'text':
            text = m.text
            tb.send_message(chatid, text)


tb.set_update_listener(listener)  # register listener
tb.polling(interval=1)

while True:  # Don't let the main Thread end.
    pass
