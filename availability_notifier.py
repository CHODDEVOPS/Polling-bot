import time
import requests
import datetime as dt
from bs4 import BeautifulSoup
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Global constants
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
URL1 = "https://termin.bremen.de/termine/suggest?mdt=701&select_cnc=1&cnc-8568=0&cnc-8580=0&cnc-8582=0&cnc-8598=0&cnc-8583=0&cnc-8587=0&cnc-8597=0&cnc-8579=0&cnc-8596=0&cnc-8599=0&cnc-8600=0&cnc-8797=0&cnc-8790=1&cnc-8588=0&cnc-8591=0&cnc-8798=0&cnc-8569=0&cnc-8570=0&cnc-8571=0&cnc-8572=0&cnc-8574=0&cnc-8576=0&cnc-8595=0&cnc-8573=0&cnc-8593=0&cnc-8789=0&cnc-8577=0&cnc-8575=0&cnc-8578=0&cnc-8590=0&cnc-8585=0&cnc-8581=0"
URL2 = "https://termin.bremen.de/termine/suggest?mdt=705&select_cnc=1&cnc-8665=0&cnc-8674=0&cnc-8675=0&cnc-8676=0&cnc-8690=0&cnc-8678=0&cnc-8679=0&cnc-8673=0&cnc-8689=0&cnc-8691=0&cnc-8692=0&cnc-8693=0&cnc-8688=0&cnc-8804=0&cnc-8792=1&cnc-8682=0&cnc-8684=0&cnc-8664=0&cnc-8666=0&cnc-8667=0&cnc-8668=0&cnc-8669=0&cnc-8670=0&cnc-8671=0&cnc-8672=0&cnc-8677=0&cnc-8791=0&cnc-8686=0&cnc-8802=0"
POLLING_INTERVAL = 60  # Polling interval in seconds

# Dates to check for available slots
current_date = dt.datetime.now()
dates_list = []  # List containing the dates for the next 3 weeks to check for available time-slots

for i in range(1, 22):  # 3 weeks * 7 days = 21 days
    future_date = current_date + dt.timedelta(days=i)
    formatted_date = future_date.strftime("%A, %d/%m/%Y")
    dates_list.append(formatted_date)


# Polling functions
def check_website(url: str, dates_list: list) -> bool:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    element_list = []
    for date in dates_list:  # Check for dates up to 3 weeks in the future
        search_criteria = {"tag": "h3", "attr": "title", "value": str(date)}
        element_list.append(soup.find(search_criteria["tag"], {search_criteria["attr"]: search_criteria["value"]}))

    # Return if there is at least one true date in the list
    return any(element_list)


def send_notification(text: str):
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    updater.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)


def polling_bot(dates_list: list):
    while True:
        is_available_url1 = check_website(URL1, dates_list)  # Check Bsc-mitte
        is_available_url2 = check_website(URL2, dates_list)  # Check Nord

        if is_available_url1 or is_available_url2:
            if is_available_url1:
                print("Success!")
                # send_notification(f"Hi there, early slots are now available to register your apartment on: {URL1}")
            if is_available_url2:
                print("Success2!")
                # send_notification(f"Hi there, early slots are now available to register your apartment on: {URL2}")
            break
        else:
            print(f"Information not available yet. Checking again in {POLLING_INTERVAL} seconds...")
            time.sleep(POLLING_INTERVAL)


if __name__ == "__main__":
    polling_bot(dates_list)
