import asyncio
import firebase_admin
from firebase_admin import credentials, firestore
from loguru import logger

# from telegram.utils.request import Request
from requests import Request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from core.availability_notifier import TerminBremenScraper
from core.config import settings
from core.repository.firebase import UserFirebaseRepository


class StatelessFirebaseRepository:
    def __init__(self, credentials_path: str) -> None:
        cred = credentials.Certificate(credentials_path)
        self.app = firebase_admin.initialize_app(cred)
        self.client = firestore.client()

    def get_list_of_users(self) -> list[int]:
        users_ref = self.client.collection("burger-users")
        docs = users_ref.stream()
        return [doc.to_dict() for doc in docs]


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

    print("here")

    date_keyboard = [
        [
            InlineKeyboardButton(
                "Go to Termine",
                url="https://termin.bremen.de/termine/",
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(date_keyboard)

    request = Request()
    bot_token = settings.bot.token
    for chat_id in user_list:
        request.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={
                "chat_id": chat_id,
                "text": message,
                "reply_markup": reply_markup.to_json(),
            },
        )
    logger.info("Broadcasted dates to all users!")


asyncio.run(broadcast_dates())