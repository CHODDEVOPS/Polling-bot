import time
import requests
import datetime as dt
from bs4 import BeautifulSoup
# from telegram import Update, ForceReply
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Global constants
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
URL1 = "https://termin.bremen.de/termine/"
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
    # updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    # updater.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
    pass


def polling_bot(dates_list: list):
    # while True:
    #     is_available_url1 = check_website(URL1, dates_list)  # Check Bsc-mitte
    #
    #     if is_available_url1:
    #             print("Success!")
    #             send_notification(f"Hi there, early slots are now available to register your apartment on: {URL1}")
    #     else:
    #         print(f"Information not available yet. Checking again in {POLLING_INTERVAL} seconds...")
    #         time.sleep(POLLING_INTERVAL)

    # Get cookie
    session = requests.Session()
    response = session.get(URL1)
    cookie = session.cookies.get_dict()

    # Get the available dates
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': f"cookie_accept=1; TVWebSession={cookie['TVWebSession']}",
        'If-Modified-Since': 'Thu, 20 Apr 2023 18:47:29 GMT',
        'Referer': 'https://termin.bremen.de/termine/select2?md=5',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }

    response = requests.get(URL1, headers=headers)

    if response.status_code == 200:
        data = response.content
        print(data)
    else:
        print(f"Error: {response.status_code}")


    # List of available dates

    valid_date_list = []



if __name__ == "__main__":
    polling_bot(dates_list)
