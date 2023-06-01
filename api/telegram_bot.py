from http.server import BaseHTTPRequestHandler
from availability_notifier import TerminBremenScraper

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        # Call your bot function here
        # Call the parse_dates function and get the date_time_dict
        parser = TerminBremenScraper()
        date_time_dict = parser.run(page="polizei")

        # format the response
        self.wfile.write(str(date_time_dict).encode())
        return
