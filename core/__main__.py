from loguru import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from core.availability_notifier import TerminBremenScraper
from core.config import settings


async def send_dates_as_buttons(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if update.message is None:
        logger.warning("Get an update with no message")
        return

    chat_id = update.message.chat_id

    # Call the parse_dates function and get the date_time_dict
    parser = TerminBremenScraper()
    logger.info("Initialized scraper")

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
    await context.bot.send_message(
        chat_id=chat_id,
        text=message,
        reply_markup=reply_markup,
    )


logger.info("Start!")

app = ApplicationBuilder().token(settings.bot.token).build()
app.add_handler(
    CommandHandler("dates", send_dates_as_buttons),
)
app.run_polling()
