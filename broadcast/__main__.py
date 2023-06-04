import asyncio

import requests
from loguru import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from broadcast.availability_notifier import TerminBremenScraper
from common.repository.firebase import UserFirebaseRepository
from config import settings


async def broadcast_dates() -> None:
    user_repo = UserFirebaseRepository(credentials=settings.firebase.credentials)
    logger.info("Fetching user list...")

    user_list = user_repo.get_list_of_users()

    logger.info("Initialized scraper")

    # Call the parse_dates function and get the date_time_dict
    parser = TerminBremenScraper()
    date_time_dict = parser.run(page="polizei")

    message = """
    """

    for date in date_time_dict.keys():
        slots = date_time_dict[date]
        message += f'{date.strftime("%A, %B %d")}\n'
        message += "Time slots:\n"
        message += "–" + "\n–".join(slots) + "\n\n"

    date_keyboard = [
        [
            InlineKeyboardButton(
                "Go to Termine",
                url="https://termin.bremen.de/termine/",
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(date_keyboard)

    bot_token = settings.bot.token
    for chat_id in user_list:
        requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={
                "chat_id": chat_id,
                "text": message,
                "reply_markup": reply_markup.to_json(),
            },
        )
    logger.info("Broadcasted dates to all users!")


asyncio.run(broadcast_dates())
