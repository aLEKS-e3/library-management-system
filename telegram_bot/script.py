import os
from datetime import datetime

from celery import shared_task
from dotenv import load_dotenv

import telebot

from borrowings.models import Borrowing

load_dotenv()

TOKEN = os.getenv("TELEGRAM_API", "6979456698:AAFS3oW6nJuf6Os2JBp9IbUOppeJH9NJc6Q")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

tb = telebot.TeleBot(TOKEN)


def send_borrowing_info(message: str) -> None:
    if message:
        tb.send_message(chat_id, message)


@shared_task
def send_overdue_notification() -> None:
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lt=datetime.today(),
        actual_return_date__isnull=True
    )

    if overdue_borrowings:
        text = "Information regarding overdue borrowings:\n\n"
        for borrowing in overdue_borrowings:
            text += (
                f"{borrowing.user} had to return {borrowing.book.title} "
                f"on {borrowing.expected_return_date}\n"
            )
        tb.send_message(chat_id, text)
    else:
        tb.send_message(chat_id, "No borrowings overdue today!")
