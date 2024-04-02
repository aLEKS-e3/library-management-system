import os
from dotenv import load_dotenv

import telebot


load_dotenv()

TOKEN = os.getenv("TELEGRAM_API")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

tb = telebot.TeleBot(TOKEN)


def send_borrowing_info(message: str) -> None:
    tb.send_message(chat_id, message)
