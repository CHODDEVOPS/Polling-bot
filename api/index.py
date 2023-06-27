from http.server import BaseHTTPRequestHandler

from signup.__main__ import run_polling


class handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        run_polling()
        return
