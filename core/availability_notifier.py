import time
import sys
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed


class TerminBremenScraper:
    TELEGRAM_BOT_TOKEN = ""
    TELEGRAM_CHAT_ID = ""
    URL1 = "https://termin.bremen.de/termine/"
    POLLING_INTERVAL = 60  # Polling interval in seconds

    def __init__(self):
        self.dates_list = self.generate_dates_list()
        self.first_page = ""
        self.second_page = ""
        self.final_page = ""
    def generate_dates_list(self):
        """
        Generate a list containing the dates for the next 3 weeks to check for available time-slots.
        """
        current_date = datetime.now()
        dates_list = []

        for i in range(1, 22):  # 3 weeks * 7 days = 21 days
            future_date = current_date + timedelta(days=i)
            formatted_date = future_date.strftime("%A, %d/%m/%Y")
            dates_list.append(formatted_date)

        return dates_list

    def get_headers(self, cookie):
        """
        Generate the headers for the request.
        """
        return {
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

    def get_available_dates(self, page) -> list:
        """
        Get the available dates and time slots from the website.
        """
        session = requests.Session()
        response = session.get(self.URL1)
        cookie = session.cookies.get_dict()
        headers = self.get_headers(cookie)

        if page == "mitte":
            self.first_page = "https://termin.bremen.de/termine/select2?md=5"
            self.second_page = "https://termin.bremen.de/termine/suggest?mdt=701&select_cnc=1&cnc-8568=0&cnc-8580=0&cnc-8582=0&cnc-8598=0&cnc-8583=0&cnc-8587=0&cnc-8597=0&cnc-8579=0&cnc-8596=0&cnc-8599=0&cnc-8600=0&cnc-8797=0&cnc-8790=1&cnc-8588=0&cnc-8591=0&cnc-8798=0&cnc-8569=0&cnc-8570=0&cnc-8571=0&cnc-8572=0&cnc-8574=0&cnc-8576=0&cnc-8595=0&cnc-8573=0&cnc-8593=0&cnc-8789=0&cnc-8577=0&cnc-8575=0&cnc-8578=0&cnc-8590=0&cnc-8585=0&cnc-8581=0"
        else:
            self.first_page = "https://termin.bremen.de/termine/select2?md=6"
            self.second_page = "https://termin.bremen.de/termine/suggest?mdt=702&select_cnc=1&cnc-8626=0&cnc-8627=0&cnc-8628=0&cnc-8650=0&cnc-8604=0&cnc-8629=0&cnc-8633=0&cnc-8619=0&cnc-8647=0&cnc-8651=0&cnc-8652=0&cnc-8801=0&cnc-8800=0&cnc-8793=1&cnc-8637=0&cnc-8639=0&cnc-8605=0&cnc-8606=0&cnc-8607=0&cnc-8608=0&cnc-8609=0&cnc-8610=0&cnc-8611=0&cnc-8613=0&cnc-8631=0&cnc-8649=0&cnc-8603=0&cnc-8616=0&cnc-8620=0&cnc-8621=0&cnc-8622=0&cnc-8623=0&cnc-8624=0&cnc-8648=0&cnc-8630=0&cnc-8632=0&cnc-8634=0&cnc-8612=0&cnc-8641=0&cnc-8642=0&cnc-8643=0&cnc-8644=0&cnc-8645=0&cnc-8601=0&cnc-8602=0&cnc-8617=0&cnc-8615=0&cnc-8614=0&cnc-8618=0&cnc-8625=0&cnc-8653=0&cnc-8646=0"

        response = session.get(self.first_page)
        cookie = session.cookies.get_dict()
        headers['Cookie'] = f"cookie_accept=1; TVWebSession={cookie['TVWebSession']}"

        response = requests.get(self.second_page, headers=headers)

        if response.status_code == 200:
            self.final_page = response.url
        else:
            print(f"Error: {response.status_code}")
            sys.exit()

        cookie = session.cookies.get_dict()

        headers['Cookie'] = f"cookie_accept=1; TVWebSession={cookie['TVWebSession']}"

        final_page = requests.get(self.final_page, headers=headers)

        return self.parse_dates(final_page.text)

    def parse_dates(self, page_content):
        """
        Parse the available dates and time slots from the HTML content.
        """
        datetime_list = []
        doc = BeautifulSoup(page_content, 'html.parser')

        # Find all h3 elements with the dates
        date_elements = doc.find_all('h3', {'class': 'ui-accordion-header'})

        if not date_elements:
            print("Dates not found")
        else:
            for date_element in date_elements:
                # Get the date text
                date_text = date_element.text.strip()

                # Convert the date text to a datetime object
                date_obj = datetime.strptime(date_text, "%A, %m/%d/%Y")

                # Find the next sibling (the div containing the time table)
                time_table_div = date_element.find_next_sibling('div')

                # Find the table element with the time buttons
                time_table = time_table_div.find('table', {'class': 'sugg_table'})
                time_buttons = time_table.find_all('button', {'class': 'suggest_btn'})

                for btn in time_buttons:
                    # Get the time text
                    time_text = btn.text.strip()

                    # Convert the time text to a datetime object (with today's date)
                    time_obj = datetime.strptime(time_text, "%H:%M")

                    # Combine the date and time into a single datetime object
                    datetime_obj = date_obj.replace(hour=time_obj.hour, minute=time_obj.minute)

                    # Add the datetime object to the list
                    datetime_list.append(datetime_obj)

        return datetime_list

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(30),
           retry_error_callback=lambda _: print("Failed to retrieve dates after 10 trials."))
    def run(self):
        """
        Run the scraper with tenacity retries (10 times every 30 seconds).
        """
        available_dates = self.get_available_dates()
        if not available_dates:
            print("The dates are not available on the website. Trying again in 60 seconds")
            raise Exception("Empty date list")

        print(f"Successfully retrieved dates: {available_dates}")

if __name__ == "__main__":
    scraper = TerminBremenScraper()
    scraper.run(page="mitte")

