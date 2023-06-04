from http.server import BaseHTTPRequestHandler

import signup


class handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        signup.run_polling()
        return
