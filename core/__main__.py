from datetime import datetime, timedelta

from loguru import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from core.config import settings


async def send_dates_as_buttons(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if update.message is None:
        logger.warning("Get an update with no message")
        return

    chat_id = update.message.chat_id
    date_list = [datetime.today() + timedelta(days=x) for x in range(7)]
    date_keyboard = [
        [
            InlineKeyboardButton(
                date.strftime("%A, %B %d"),
                url="http://example.com/" + date.strftime("%Y-%m-%d"),
            )
        ]
        for date in date_list
    ]
    reply_markup = InlineKeyboardMarkup(date_keyboard)
    await context.bot.send_message(
        chat_id=chat_id, text="Here are the next 7 dates:", reply_markup=reply_markup
    )


app = ApplicationBuilder().token(settings.bot.token).build()
app.add_handler(
    CommandHandler("dates", send_dates_as_buttons),
)
app.run_polling()
