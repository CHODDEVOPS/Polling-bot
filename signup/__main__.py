"""This module is responsible for handling user signup."""

from loguru import logger
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from common.repository.firebase import UserFirebaseRepository, UserRepository
from config import settings

user_repo: UserRepository = UserFirebaseRepository(
    settings.firebase.application_credentials
)


async def send_dates_as_buttons(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if update.message is None:
        logger.warning("Get an update with no message")
        return

    chat_id = update.message.chat_id

    user_repo.create_user(chat_id)


logger.info("Start!")

app = ApplicationBuilder().token(settings.bot.token).build()
app.add_handler(
    CommandHandler("start", send_dates_as_buttons),
)
app.run_polling()
