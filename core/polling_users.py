from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from core.__main__ import StatelessFirebaseRepository
from core.config import settings

bot = Bot(token=settings.bot.token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    # Call the function to register the user in Firestore database
    register_user(user_id)
    await message.reply("Hello! You are now registered.")


def register_user(user_id):
    # Call the function to register the user in Firestore database
    user_repo = StatelessFirebaseRepository(credentials=settings.firebase.credentials)
    user_repo.register_user(user_id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
